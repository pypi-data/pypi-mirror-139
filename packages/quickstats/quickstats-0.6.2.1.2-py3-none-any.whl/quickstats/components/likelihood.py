import os
import math
import time
import json
from itertools import repeat
from typing import Optional, Dict, List, Union

import numpy as np
import ROOT
from quickstats.components import ExtendedModel, ExtendedMinimizer
from quickstats.maths.numerics import approx_n_digit, str_encode_value, str_decode_value, pretty_value
from quickstats.utils import common_utils

def load_cache(fname:str):
    if (fname is not None) and os.path.exists(fname):
        with open(fname, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

from quickstats.components import AnalysisObject
from quickstats.utils.common_utils import parse_config

class Likelihood(AnalysisObject):
    
    def __init__(self, filename:str, poi_name:Optional[Union[str, List[str]]]=None,
                 data_name:str='combData', 
                 config:Optional[Dict]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        config = parse_config(config)
        config['filename']  = filename
        config['poi_name']  = poi_name
        config['data_name'] = data_name
        config['verbosity'] = verbosity
        self._inherit_init(super().__init__, **config)
    
    @staticmethod
    def _parse_poi_val(pois:"ROOT.RooArgSet", poi_val:Optional[Union[Dict[str, float], float]]=None):
        if poi_val is None:
            poi_val = {}
            for poi in pois:
                poi_val[poi.GetName()] = poi.getVal()
        elif not isinstance(poi_val, dict):
            poi_val_tmp = poi_val
            poi_val = {}
            for poi in pois:
                poi_val[poi.GetName()] = poi_val_tmp
        else:
            # fill in missing values
            for poi in pois:
                poi_name = poi.GetName()
                if poi_name not in poi_val:
                    poi_val[poi_name] = poi.getVal()
        return poi_val
        
    def nll_fit(self, poi_val:Optional[Union[Dict[str, float], float]]=None,
                mode:int=2, snapshot_name:Optional[str]="currentSnapshot",
                do_minos:bool=False):
        if not isinstance(self.poi, ROOT.RooArgSet):
            pois = ROOT.RooArgSet(self.poi)
        else:
            pois = self.poi
        
        poi_val = self._parse_poi_val(pois, poi_val)

        if snapshot_name is None:
            self.save_snapshot("tmpSnapshot")
            snapshot_name = "tmpSnapshot"
        
        nll_uncond = None
        nll_cond   = None
        muhat      = None
        
        tmp_do_minos = self.minimizer.config['minos']
        
        self.minimizer.config['minos'] = do_minos
        if do_minos:
            self.minimizer.minos_set = pois
        
        start_time = time.time()
        muhat = {}
        muhat_errlo = {}
        muhat_errhi = {}
        # unconditional nll
        if mode in [0, 1]:
            # restore initial parameter values after each fit
            self.load_snapshot(snapshot_name)
            # fix other pois if they are not studied
            for poi in self.model.pois:
                poi.setConstant(1)
            for poi in pois:
                poi.setConstant(0)
                val = poi_val[poi.GetName()]
                poi.setVal(val)
            fit_status_uncond = self.minimizer.minimize()
            self.save_snapshot("uncondFit")
            nll_uncond = self.minimizer.nll.getVal()
            for poi in pois:
                poi_name = poi.GetName()
                muhat[poi_name]       = poi.getVal()
                muhat_errlo[poi_name] = poi.getErrorLo()
                muhat_errhi[poi_name] = poi.getErrorHi()
        fit_time_uncond = time.time() - start_time
        # conditional nll
        if mode in [0, 2]:
            # restore initial parameter values after each fit
            self.load_snapshot(snapshot_name)
            # fix other pois if they are not studied
            for poi in self.model.pois:
                poi.setConstant(1)
            for poi in pois:
                poi.setConstant(1)
                val = poi_val.get(poi.GetName(), poi.getVal())
                poi.setVal(val)
            fit_status_cond = self.minimizer.minimize()
            self.save_snapshot("condFit")
            nll_cond = self.minimizer.nll.getVal()
        fit_time_cond = time.time() - fit_time_uncond - start_time
        
        fit_result = {}
        self.stdout.info("INFO: NLL evaluation completed with")
        if mode in [0, 1]:
            if len(pois) == 1:
                poi_name = pois.first().GetName()
                muhat = muhat[poi_name]
                muhat_errlo = muhat_errlo[poi_name]
                muhat_errhi = muhat_errhi[poi_name]
                self.stdout.info(f"\tmu hat = {muhat:.5f}")
            else:
                best_fit_str = ", ".join([f"{name}={value:.5f}" for name, value in muhat.items()])
                self.stdout.info("\tbest fit: {}".format(best_fit_str))
            self.stdout.info(f"\tuncond NLL = {nll_uncond:.5f}")
            fit_result['uncond_fit'] = {
                'muhat': muhat,
                'muhat_errlo': muhat_errlo,
                'muhat_errhi': muhat_errhi,
                'nll': nll_uncond,
                'status': fit_status_uncond,
                'time': fit_time_uncond
            }
        if mode in [0, 2]:
            if len(pois) == 1:
                poi_name = pois.first().GetName()
                mu = pretty_value(poi_val[poi_name])
                self.stdout.info("\tmu = {:.5f}".format(mu))
            else:
                mu = poi_val
                mu_str = ", ".join([f"{name}={pretty_value(value)}" for name, value in poi_val.items()])
                self.stdout.info("\tmu: {}".format(mu_str))
            self.stdout.info("\tcond NLL = {:.5f}".format(nll_cond))
            fit_result['cond_fit'] = {
                'mu': mu,
                'nll': nll_cond,
                'status': fit_status_cond,
                'time': fit_time_cond
            }
        if mode == 0:
            pnll = nll_cond - nll_uncond
            qmu  = 2*pnll
            self.stdout.info("\tPNLL = {:.5f}".format(nll_cond - nll_uncond))
            fit_result['pnll'] = pnll
            fit_result['qmu']  = qmu
            
            if (qmu >= 0):
                ndof = len(pois)
                if ndof == 1:
                    # ndof = 1 case
                    poi_name = pois.first().GetName()
                    x0 = poi_val[poi_name]
                    significance = math.sqrt(qmu)
                    pvalue = 1 - ROOT.Math.normal_cdf(significance, 1, x0)
                else:
                    x0 = list(set(poi_val.values()))
                    if len(x0) > 1:
                        fit_result['significance'] = None
                        fit_result['pvalue'] = None
                    else:
                        pvalue = ROOT.Math.chisquared_cdf_c(qmu, ndof, x0[0])
                        significance = ROOT.RooStats.PValueToSignificance(pvalue)
                fit_result['significance'] = significance
                fit_result['pvalue'] = pvalue
            else:
                fit_result['significance'] = None
                fit_result['pvalue'] = None
                
        self.stdout.info("\ttime (uncond_fit, cond_fit) = {:.3f}, {:.3f}".format(fit_time_uncond, fit_time_cond))
        fit_result['total_time'] = fit_time_uncond + fit_time_cond
        
        # finallizing
        self.minimizer.config['minos'] = tmp_do_minos
        self.minimizer.minos_set = ROOT.RooArgSet()
        
        return fit_result
        
    def evaluate_nll(self, poi_val:Optional[Union[Dict[str, float], float]]=None,
                     mode:int=2, snapshot_name:Optional[str]="currentSnapshot"):
        """Evalute post-fit NLL value
        
        Arguments:
            poi_val: (Optional) float
                Value of parameter of interest during fit. If not specified, the original value is used.
            mode: int
                Evaluation mode. Choose from:
                    0: Evaluate nll_mu - nll_muhat
                    1: Evaluate unconditional NLL (nll_muhat)
                    2: Evaluate conditional NLL (nll_mu)
            snapshot_name: (Optional) str
                Name of snapshot to load before fitting.
        """
        fit_result = self.nll_fit(poi_val=poi_val, mode=mode, snapshot_name=snapshot_name)
        
        if mode == 0:
            return fit_result['pnll']
        if mode == 1:
            return fit_result['uncond_fit']['nll']
        if mode == 2:
            return fit_result['cond_fit']['nll']
    
def evaluate_nll(filename:str, poi_val:Optional[float]=None, poi_name:str=None, mode:int=1,
                 ws_name:Optional[str]=None, mc_name:Optional[str]=None, data_name:str='combData', 
                 snapshot_name:str=None, profile_param:str="", fix_param:str="", 
                 constrain_nuis:bool=True, minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', 
                 num_cpu:int=1, binned_likelihood:bool=True, eps:float=1.0, strategy:int=1, 
                 optimize:int=2, offset:bool=True, fix_cache:bool=True, fix_multi:bool=True, 
                 max_calls:int=-1, max_iters:int=-1, print_level:int=-1, verbosity:int="WARNING",  
                 outname:str=None, cache:bool=False, detailed_output:bool=False, save_log:bool=False):
    if cache:
        cached_result = load_cache(outname)
        if cached_result is not None:
            poi_name, nll = cached_result['poi'], cached_result['nll']
            if not save_log:
                print('INFO: Found NLL cache from "{}"'.format(outname))
                if poi_val is None:
                    print('INFO: Cached unconditional NLL for POI "{}": {}'.format(poi_name, nll))
                else:
                    print('INFO: Cached NLL for POI "{}" at {:.2f}: {}'.format(poi_name, poi_val, nll))
            return nll
    
    config = {
        'ws_name' : ws_name,
        'mc_name' : mc_name,
        'snapshot_name': snapshot_name,
        'profile_param': profile_param,
        'fix_param': fix_param,
        'constrain_nuis': constrain_nuis,
        'minimizer_type': minimizer_type,
        'minimizer_algo': minimizer_algo,
        'num_cpu': num_cpu,
        'binned_likelihood': binned_likelihood,
        'eps': eps,
        'strategy': strategy,
        'optimize': optimize,
        'offset': offset,
        'fix_cache': fix_cache,
        'fix_multi': fix_multi,
        'max_calls': max_calls,
        'max_iters': max_iters,
        'print_level': print_level,
        'verbosity': verbosity,
    }
    if save_log and (outname is not None):
        log_path = os.path.splitext(outname)[0] + ".log"
    else:
        log_path = None

    from quickstats.concurrent.logging import standard_log
    with standard_log(log_path) as logger:
        if poi_val is None:
            print(f'INFO: Evaluating unconditional NLL for POI "{poi_name}"')
        else:
            print(f'INFO: Evaluating conditional NLL for POI "{poi_name}" at mu = {poi_val}')
        start = time.time()
        likelihood = Likelihood(filename=filename, poi_name=poi_name, data_name=data_name, config=config,
                                verbosity=verbosity)
        poi_name = likelihood.poi.GetName()
        nll = likelihood.evaluate_nll(poi_val, mode=mode)
        end = time.time()
        results = {
            'nll': nll,
            'poi': poi_name,
            'offset': int(offset),
            'constrain_nuis': int(constrain_nuis),
            'poi_value': poi_val
        }
        if poi_val is None:
            poi_val = likelihood.poi.getVal()
            results['poi_bestfit'] = poi_val
        results['time'] = end-start

        # save results
        if outname is not None:
            with open(outname, 'w') as outfile:
                json.dump(results, outfile)
            print('INFO: Saved NLL result to {}'.format(outname))

    if detailed_output:
        return results
    return nll

def scan_nll(filename:str, poi_min:float, poi_max:float, poi_step:float, poi_name:Optional[str]=None, 
             cache:bool=True, outname:str="{poi_name}.json", outdir:str='output', ws_name:Optional[str]=None, 
             mc_name:Optional[str]=None, data_name:str='combData', snapshot_name:str=None, 
             profile_param:str="", fix_param:str="", constrain_nuis:bool=True, minimizer_type:str='Minuit2',
             minimizer_algo:str='Migrad', num_cpu:int=1, binned_likelihood:bool=True, eps:float=1.0, 
             strategy:int=0, fix_cache:bool=True, fix_multi:bool=True, verbosity:int="WARNING", 
             print_level:int=-1, max_calls:int=-1, max_iters:int=-1, optimize:int=2, offset:bool=True, 
             parallel:int=-1, save_log:bool=True, **kwargs):
    start_time = time.time()
    points     = np.arange(poi_min, poi_max+poi_step, poi_step)
    points     = np.concatenate(([None], points))
    modes      = [1] + [2]*(len(points)-1)
    # try to get the number of significant digits of poi_step
    sd = approx_n_digit(poi_step)
    if poi_name is None:
        poi_name = ExtendedModel.get_poi_names(filename, ws_name, mc_name)[0]
        print('INFO: POI not given, default as "{}".'.format(poi_name))
    outname_noext = os.path.splitext(outname)[0]
    # save cache file as outdir/cache/outname_{str_encoded_poi_value}.json
    outnames = ["{}_{}.json".format(outname_noext.format(poi_name=poi_name), "uncond" if point is None \
                else str_encode_value(point, sd)) for point in points]
    cachedir = os.path.join(outdir, "cache")
    outnames = [os.path.join(cachedir, name) for name in outnames]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    arguments = (repeat(filename), points, repeat(poi_name), modes, repeat(ws_name),repeat(mc_name), 
                 repeat(data_name), repeat(snapshot_name), repeat(profile_param), repeat(fix_param), 
                 repeat(constrain_nuis), repeat(minimizer_type), repeat(minimizer_algo), repeat(num_cpu),
                 repeat(binned_likelihood), repeat(eps), repeat(strategy), repeat(optimize), repeat(offset),
                 repeat(fix_cache), repeat(fix_multi), repeat(max_calls), repeat(max_iters), 
                 repeat(print_level), repeat(verbosity), outnames, repeat(cache), repeat(False),
                 repeat(save_log))
    
    results = common_utils.execute_multi_tasks(evaluate_nll, *arguments, parallel=parallel)

    uncond_nll = results[0]
    data = {'mu': [], 'nll':[], 'qmu':[]}
    for mu, nll in zip(points, results):
        data['mu'].append(mu)
        data['nll'].append(nll)
        data['qmu'].append(2*(nll-uncond_nll))
    final_outname = os.path.join(outdir, outname.format(poi_name=poi_name))
    with open(final_outname, 'w') as outfile:
        json.dump(data, outfile, indent=3)
    end_time = time.time()
    print('INFO: All jobs have finished. Total time taken: {:.3f} s'.format(end_time-start_time))  