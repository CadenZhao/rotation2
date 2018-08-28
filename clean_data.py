# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:44 2018

@author: Xiangjie Zhao

These codes are used to convert
nuclei to cellXYZ
"""

import argparse
import pandas as pd


def parseArg():
    """Recieve parameters from commander line
    
    Parameters
    ______________
    None
    
    Returns
    ______________
    arguments: the arguments parsered
    """
    parser = argparse.ArgumentParser(description='Convert nuclei format to cellXYZ.')
    parser.add_argument("-f", "--file", required=True, help="the input file to be converted")
    parser.add_argument("-d", "--dir", required=True, help="the directory storing the output file")
    argments = parser.parse_args()
    return argments 

args = parseArg()
infile = args.file
outdir = args.dir

raw = pd.read_csv(infile, header=None, sep=', ', engine='python')
data = raw.iloc[:,[5,6,7,9]]
data = data[data.iloc[:,3].str.contains('Nuc|\s') == False]
data.to_csv('%s/%s.csv' % (outdir, infile.split('/')[-1]), index=None, header=None)