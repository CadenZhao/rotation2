# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:44 2018

@author: Xiangjie Zhao

These codes define the functions for computing the matrix of 
cell distance rate and cell co-appearring rate
"""

import numpy as np
import pandas as pd
from itertools import combinations


def distance(data):
    """Computing cell-pair distance before converting
    to distance rate
    
    Parameters
    ______________
    data: the dataframe cleaned

    Returns
    ______________
    df_list: list of dataframes containning two objects,
    distance dataframe (n_cell_pairs, 3)
    and distance rate dataframe (2*n_cell_pairs, 3)
    """  
    cell_number = data.shape[0]
    data_values = data.iloc[:,:3]
    
    #compute distance
    df = pd.DataFrame(columns = ['cellA', 'cellB', 'distance'])
    for i in range(cell_number):
        for j in range(i+1, cell_number):
            dis = np.linalg.norm(data_values.iloc[i,:] - data_values.iloc[j,:])
            df_row = pd.DataFrame([[data.iloc[i,3], data.iloc[j,3], dis]],
                                  columns = ['cellA', 'cellB', 'distance'])
            df = df.append(df_row)
            
    #compute  distance rate
    df_rate = pd.DataFrame(columns=['cellA', 'cellB', 'distance_rate'])
    for i in range(cell_number):
        df_rate_ij = pd.DataFrame(columns=['cellA', 'cellB', 'distance_rate'])
        for j in range(cell_number):
            dis = np.linalg.norm(data_values.iloc[i,:] - data_values.iloc[j,:])
            df_rate_row = pd.DataFrame([[data.iloc[i,3], data.iloc[j,3], dis]],
                              columns = ['cellA', 'cellB', 'distance_rate'])
            df_rate_ij = df_rate_ij.append(df_rate_row)   
        dis_ij = df_rate_ij['distance_rate']    
        df_rate_ij['distance_rate'] =  dis_ij / dis_ij.max()     
        df_rate = df_rate.append(df_rate_ij)    
    #remove 0 distance rate
    df_rate = df_rate[df_rate.iloc[:,2] != 0]
    
    df_list = [df, df_rate]
    return df_list 
    

def coexistence(picture_num):
    """Computing coexistence times and rates of two cell 
    
    Parameters
    ______________
    picture_num: the number of the first few pictures
    chosen from all the pictures

    Returns
    ______________
    result_list: a list contain cell-pair coexisting times and rates
    """  
    count_dict = {}
    for n in range(picture_num):
        data = pd.read_csv('./test/t%03d-nuclei.csv' % (n+1), sep=',', header=None)
        cell_combination = list(combinations(data.iloc[:,3],2))
        for comb in cell_combination:
            if comb in count_dict:
                count_dict[comb] = count_dict[comb]+1
            else:
                count_dict[comb] = 1
    pair = np.array(list(count_dict.keys()))
    count = np.array(list(count_dict.values()))
    stack_array = np.vstack([pair.transpose(), count]).transpose()
    df_cotimes = pd.DataFrame(stack_array, columns=['cellA', 'cellB', 'coexist_time'])
    df_corate = df_cotimes.copy()
    df_corate.columns = ['cellA', 'cellB', 'coexist_rate']
    df_corate.iloc[:,2] = pd.to_numeric(df_corate.iloc[:,2]) / picture_num 
    
    result_list = [df_cotimes, df_corate]
    return result_list
    
    