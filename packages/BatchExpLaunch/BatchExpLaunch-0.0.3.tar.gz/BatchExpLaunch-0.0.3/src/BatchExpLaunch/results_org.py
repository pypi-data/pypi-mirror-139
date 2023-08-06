import glob
import os
import pandas as pd
import json
import matplotlib.pyplot as plt 
from progressbar import progressbar
import numpy as np
from pathlib import Path
import pickle
import logging
def getLogging():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    return logging
def read_json(file_path):
    with open(file_path,"r") as f:
        result=json.load(f)
    return result
def find_max_len(result):
    length=1
    for i in result.keys():
        length=max(length,len(result[i]))
    return length
def append_single(result,max_len):
    for i in result.keys():
        if len(result[i])<max_len:
            result[i]=result[i]+[result[i][-1]]*(max_len-len(result[i]))
def write_back(result,file_path):
    with open(file_path,"w") as f:
        json.dump(result,f)
def get_path_sets(root_path,same_length=False,suffix="jjson"):
    paths=glob.glob(root_path+'/**/*.'+suffix, recursive=True)
    # print(paths)
    path_sets=set()
    for path in paths:
        pp=Path(paths[0])
        # path_root=str(pp.parent.parent)
        path_root=os.path.join(*path.split("/")[:-2])
#         print(path_root,path_root,"path_root")
        if same_length:
            result_cur=read_json(path)
            max_len=find_max_len(result_cur)
            append_single(result_cur,max_len)
            write_back(result_cur,path)
        # print(result_cur)
        # print(path_root)
        path_sets.add(path_root)
    return path_sets
def merge_single_experiment_results(root_path,suffix="jjson"):
    paths=glob.glob(root_path+'/**/*.'+suffix, recursive=True)
    # print(paths,root_path)
    df_result_cur=pd.DataFrame()
    for path in paths:
#         print(path)
        with open(path, "r") as read_file:
        #     print("Converting JSON encoded data into Python dictionary")
            developer = json.load(read_file)
            pd_frame=pd.DataFrame(developer).fillna(np.nan)    
        df_result_cur=df_result_cur.append(pd_frame)
#     print(df_result_cur)
    return df_result_cur

def merge_multiple_experiment_results(root_path,suffix="jjson"):
    path_sets=get_path_sets(root_path)
    for path_set in progressbar(path_sets):
        df_result_cur=merge_single_experiment_results(path_set,suffix=suffix)
        df_result_cur.to_csv(path_set+"/result.ccsv")

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
def get_node(root_path,path):
    # print(root_path,path,"root_path,path")
    all_node=path.split("/")
    start_folder=root_path.split("/")[-1]
    # print(root_path.split("/"),all_node)
    ind=all_node.index(start_folder)
    start_node=all_node[ind+1:]
    # print(start_node)
    return start_node
def set_node_val(node_list,multi_level_dict,val):
    for i in node_list[:-1]:
        multi_level_dict=multi_level_dict[i]
    last_node=node_list[-1]
    multi_level_dict[last_node]=val
def get_result_df(root_path,same_length=False,groupby="iterations",filter_list=[],only_mean=False,rerun=False,suffix="jjson"):
    results_path=os.path.join(root_path,"results.pickle")
    results_path_exist=glob.glob(results_path)
#     print(results_path)
    if results_path_exist and not rerun:
        results_path=results_path_exist[0]
        print("found saved results")
        with open(results_path, 'rb') as handle:
            result,result_mean = pickle.load(handle)
    else:
        path_sets=get_path_sets(root_path,same_length,suffix=suffix)
        # print(path_sets)
        result=AutoVivification()
        result_mean=AutoVivification()
        for path_set in path_sets:
            node=get_node(root_path,path_set)
            result_cur=merge_single_experiment_results(path_set,suffix=suffix)
            set_node_val(node,result,result_cur)
            result_merged_cur=result_cur.groupby(groupby).mean().reset_index()
            set_node_val(node,result_mean,result_merged_cur)
        with open(results_path, 'wb') as handle:
            pickle.dump([result,result_mean], handle, protocol=pickle.HIGHEST_PROTOCOL)
    if not only_mean:
        return result,result_mean
    else:
        return result
def extract_step_metric(result:dict,metric_name,step,data_name):
    result_return=[]
    for key, value in result.items():
        if  isinstance(value, pd.DataFrame) and metric_name in value:
            result_return.append([key,data_name,value[metric_name][step].tolist()])
        else:
            result_return.append([key,data_name,None])
    return result_return 

def latex_two_f(x, y):                      # this is a demo function that takes in two ints and 
    if x>1:
        x="{:#.4G}".format(x)
    else:
        x="{:.3f}".format(x)
    if y>1:
        y="{:#.4G}".format(y)
    else:
        y="{:.3f}".format(y)
    return "&"+str(x) + "\$_{("+str(y)+")}\$"        # concatenate them as str
vec_latex_two_f = np.vectorize(latex_two_f) 
def latex_single_f_latex(x):                      # this is a demo function that takes in two ints and 
    if x>1:
        x="{:#.4G}".format(x)
    else:
        x="{:.3f}".format(x)
    return "&"+str(x)        # concatenate them as str
vec_latex_single_f_latex = np.vectorize(latex_single_f_latex) 
def latex_single_f(x):                      # this is a demo function that takes in two ints and 
    if x>1:
        x="{:.3f}".format(x)
    else:
        x="{:.3f}".format(x)
    return str(x)        # concatenate them as str
vec_latex_single_f = np.vectorize(latex_single_f) 

def to_mean(result_dataframe):
    mean=result_dataframe.applymap(func=np.mean)
    result=pd.DataFrame(vec_latex_single_f(mean),index=mean.index,columns=mean.columns)
    return result

def to_latex(result_dataframe):
    std=result_dataframe.applymap(func=np.std)
    mean=result_dataframe.applymap(func=np.mean)
    result=pd.DataFrame(vec_latex_single_f_latex(mean),index=mean.index,columns=mean.columns)
    result_std=pd.DataFrame(vec_latex_two_f(mean, std),index=mean.index,columns=mean.columns) 
    return result,result_std
def get_freq_singe(x):
    if not isinstance(x, list):
        if pd.isnull(x):
            return 0
        else:
            return 1
    else:
        return len(x)
def get_round_value(x):
    if not isinstance(x, list):
        return 1
    else:
        return [round(i, 2) for i in x]
def to_round(result_dataframe):
    frequency=result_dataframe.applymap(func=get_round_value)
    return frequency
def to_freq(result_dataframe):
    frequency=result_dataframe.applymap(func=get_freq_singe)
    return frequency

import itertools

def plot_metrics(name_results_pair:dict,plots_y_partition:str="metrics_NDCG",errbar=True,
plots_x_partition:str="iterations",groupby="iterations",ax=None,graph_param={})->None:
    
    '''    
        name_results_pair:{method_name:result_dataframe}
        plots_partition: key name in each result_dataframe which need to be plotted
    '''
    
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors_list = prop_cycle.by_key()['color']
    colors=itertools.cycle(colors_list)
    marker = itertools.cycle((',', '+', '.', 'o', '*')) 
    if ax:
        plot=ax
    else:
        plot=plt
    for algo_name in name_results_pair:
            algo_result=name_results_pair[algo_name]
            print(type(algo_result))
            mean=algo_result.groupby(groupby).mean().reset_index()
            std=algo_result.groupby(groupby).std().reset_index()
            if plots_x_partition not in mean.keys() or plots_y_partition not in mean.keys() :
                continue
#             assert plots_y_partition in algo_result, algo_name+" doesn't contain the partition "+plots_y_partition
            ndata=len(mean[plots_x_partition])
            if not errbar:
                plot.plot(mean[plots_x_partition],mean[plots_y_partition], marker = next(marker),color=next(colors), label=algo_name, markevery=ndata//3)
            else:
                plot.errorbar(mean[plots_x_partition],mean[plots_y_partition], yerr=std[plots_y_partition], marker = next(marker),color=next(colors), label=algo_name, markevery=ndata//3)
    if ax is None:
        gca=plot.gca()
        gca.set(**graph_param)
        plot.legend()
    
def paramIterationPlot(result:dict,metrics_name,step,ax=None,xlim=None,savepath=None):
    """
    This function plot the performance along different parameters.
    """
    if ax:
        plot=ax
    else:
        plot=plt
    marker = itertools.cycle(('v', '^', "<",">","p",'x',"X","D", 'o', '*')) 
    for key, value in result.items():
        result_list=extractResultWithParam(value,[metrics_name],step)
        print(key)
        param,result_metric=result_list[0],result_list[1]
        
        if len(result_metric)>1:
#                 print(result_metric[i])
            mean=np.array([np.mean(i)for i in result_metric])
            std=np.array([np.std(i)for i in result_metric])
            ind=np.arange(mean.shape[0])
            if xlim:
                ind=param<=xlim
#                     print(ind)
            ndata=len(ind)
            plot.errorbar(param[ind],mean[ind],yerr=std[ind],marker = next(marker),label=key, markevery=ndata//3)
        else:
            plot.plot(param,result_metric,marker = next(marker),label=key)
def TradeoffPlot(result:dict,metrics_pair,step,ax=None,xlim=None,savepath=None):
    """
    This function plot the tradeoff performance.
    """
    if ax:
        plot=ax
    else:
        plot=plt
    marker = itertools.cycle(('v', '^', "<",">","p",'x',"X","D", 'o', '*')) 
    for key, value in result.items():
        result_list=extractResultWithParam(value,metrics_pair,step)
        xResult=np.array([np.mean(i)for i in result_list[1]])
        yResult=np.array([np.mean(i)for i in result_list[2]])
        ndata=len(xResult)
        plot.plot(xResult,yResult,marker = next(marker),label=key, markevery=ndata//3)
def extractResultWithParam(cur_res_split,res_names=[],step=0):
    tradeoff_params=cur_res_split.keys()
    tradeoff_nums=[]
    tradeoff_params_filtered=[]
    for i in tradeoff_params:
        cur_num=i.split("_")[-1]
        if cur_num.lstrip('-').replace('.','',1).isdigit():
             tradeoff_nums.append(float(cur_num))
             tradeoff_params_filtered.append(i)
    tradeoff_params=tradeoff_params_filtered
    tradeoff_nums=np.array(tradeoff_nums)
    argsort=np.argsort(tradeoff_nums)
    tradeoff_nums=tradeoff_nums[argsort]
    result=[tradeoff_nums]
    for res_name in res_names:
        res_cur_name=[cur_res_split[tradeoff_param][res_name][step].tolist() for tradeoff_param in tradeoff_params ]
        res_cur_name=np.array(res_cur_name)[argsort]
        result.append(res_cur_name)
    return result

def getGrandchildNode(InputDict,GrandchildNode):
    """
    This function get the grandchild node.
    """
    resDict={}
    for keyL1, valueL1 in InputDict.items():
            resDict[keyL1]=valueL1[GrandchildNode]
    return resDict

def filteroutNone(result_list):
    """
    This function filter out results list after we use function extract_step_metric
    """   
    result_list_new=[]
    for result_list_cur in result_list:
        if result_list_cur[2] is not None:
            result_list_new.append(result_list_cur)
    return result_list_new