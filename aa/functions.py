# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:44 2018

@author: Xiangjie Zhao

These codes define the functions for computing 
cell distance and cell co-appearring times
"""
from itertools import combinations
import argparse
import numpy as np
import pandas as pd


def parseArg():
    """Recieve parameters from commander line
    """
    parser = argparse.ArgumentParser(description='Convert nuclei format to cellXYZ.')
    parser.add_argument("-i", "--indir", required=True, help="the input directory containing files to be converted")
    parser.add_argument("-o", "--outdir", required=True, help="the directory to store the output file")
    parser.add_argument("-n", "--num", required = True, help = "number of files to be converted in input directory")
    parser.add_argument("-c", "--cut", required = True, help = "threshold of distance rate")
    argments = parser.parse_args()
    
    return argments 


def clean_data(indir, outdir, picture_num):
    """These codes are used to convert nuclei to cellXYZ
    
    Parameters
    ______________
    indir: input directory, passed from cmd
    outdir: output directory, passed from cmd
    picture_num: number of files to be chosen, passed from cmd
    
    Returns
    ______________
    none
    """
    for i in range(picture_num):
        print('data cleanning: %.0f%%' % ((i+1)/picture_num*100), end='\r')
        raw = pd.read_csv('%s/t%03d-nuclei' % (indir, (i+1)), sep = ',', header = None)
        data = raw.iloc[:,[5,6,7,9]]
        index = (data.iloc[:,3].str.contains('Nuc') | (data.iloc[:,3] == ' ')) == False
        data = data[index]
        data.columns = ['X', 'Y', 'Z', 'cell_name']
        data = data.sort_values(by = 'cell_name')
        data.to_csv('%s/%03d.csv' % (outdir, (i+1)), index = None, header = True)
    print('----------------------------------------')
    
def distance(data):
    """Computing cell-pair distance before converting
    to distance rate
    
    Parameters
    ______________
    data: the dataframe cleaned

    Returns
    ______________
    df_rate: a dataframe containning 3 columns, cellA, cellB
    and the percent distant
    """  
    cell_number = data.shape[0]
    data_values = data.iloc[:,:3]
    
#    #compute distance
#    df = pd.DataFrame(columns = ['cellA', 'cellB', 'distance'])
#    for i in range(cell_number):
#        for j in range(i+1, cell_number):
#            dis = np.linalg.norm(data_values.iloc[i,:] - data_values.iloc[j,:])
#            df_row = pd.DataFrame([[data.iloc[i,3], data.iloc[j,3], dis]],
#                                  columns = ['cellA', 'cellB', 'distance'])
#            df = df.append(df_row)
            
    #compute  distance rate
    df_rate = pd.DataFrame(columns=['cellA', 'cellB', 'distance_rate'])
    for i in range(cell_number):
        df_rate_i = pd.DataFrame(columns=['cellA', 'cellB', 'distance_rate'])
        for j in range(cell_number):
            dis = np.linalg.norm(data_values.iloc[i,:] - data_values.iloc[j,:])
            df_rate_row = pd.DataFrame([[data.iloc[i,3], data.iloc[j,3], dis]],
                              columns = ['cellA', 'cellB', 'distance_rate'])
            df_rate_i = df_rate_i.append(df_rate_row)    
        #remove 0 distance
        df_rate_i = df_rate_i[df_rate_i.iloc[:,2] != 0]
        dis_i = df_rate_i['distance_rate']
        #scale distance to 0
        df_rate_i['distance_rate'] =  (dis_i-dis_i.min()) / (dis_i.max() -dis_i.min())     
        df_rate = df_rate.append(df_rate_i)    
    
    return df_rate
    

def coexistence(file_dir, picture_num):
    """Computing coexistence times of two cell 
    
    Parameters
    ______________
    picture_num: the number of the first few pictures
    chosen from all the pictures

    Returns
    ______________
    result_list: a dataframe containning 3 columns, cellA, cellB
    and their coexisting times 
    """  
    count_dict = {}
    for n in range(picture_num):
        data = pd.read_csv('%s/t%03d.csv' % (file_dir, (n+1)), sep=',', header=True)
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

    return df_cotimes
    

def near_cell(file_dir, picture_num, df_cotimes, cut_off = .1):
    """Computing the counts of near cell pairs
    according to the cutoff denoted by user
    
    Parameters
    ______________
    picture_num: the number of the first few pictures
    chosen from all the pictures
    cut_off: the threshold to choose near cell pairs
    df_cotimes: the dataframe generated by funtion coexistence(),
    storing times of coexistence of cell pairs
    
    Returns
    ______________
    df_near: a dataframe similar to df_cotimes,
    recording the counts of near cell pairs
    """  
    for file_num in range(picture_num):
        print('cutting off: %.0f%%' % ((file_num +1)/picture_num*100), end='\r')
        df_dis = pd.read_csv('%s/AAAt%03d-dis.csv' % (file_dir, (file_num+1)), sep=',', header=True)
        index = df_dis.iloc[:,2] > cut_off
        df_remove = df_dis[index].iloc[:,:-1]
        #drop redoundance
        for i in range(df_remove.shape[0]):
            df_remove.iloc[i,:] = list(df_remove.iloc[i,:].sort_values())
        df_remove = df_remove.drop_duplicates([0,1])
        #drop counts that is larger than cute_off from total coexistence times
        for j in range(df_remove.shape[0]):
            cellA = df_remove.iloc[j,0]
            cellB = df_remove.iloc[j,1]
            index = (df_cotimes.iloc[:,0] == cellA) & (df_cotimes.iloc[:,1] == cellB)
            recount = int(df_cotimes[index].iloc[0,2]) - 1
            df_cotimes[index] = [cellA, cellB, recount]
    df_near = df_cotimes
    print('----------------------------------------')
    
    return df_near