from function import distance
from function import coexistence
from function import near_cell
import os
import pandas as pd

def main():
#    for i in range(180):
#        #converting format
#        print('converting format: %.0f%%' % ((i+1)/180*100), end='\r')
#        os.system('python clean_data.py -f ./nuclei/t%03d-nuclei -d ./test' % (i+1))
#        #compute and output distance rate
#        data = pd.read_csv('./test/t%03d-nuclei.csv' % (i+1), sep=',', header=None)
#        dis_rate = distance(data)
#        dis_rate.to_csv('./distance_rate/t%03d-dis.csv' % (i+1), index=None, header=None) 
#   
    picture_num = 180
    df_cotimes = coexistence(picture_num)
    df_cotimes.to_csv('./cotimes.csv', index=None, header=None)
    
    df_cotimes = pd.read_csv('./cotimes.csv', sep=',', header=None)
    df_near = near_cell(picture_num=picture_num, df_cotimes=df_cotimes)
    
    #for each cell pair, computing (near times) / (total times)
    df_corate = df_comtimes.copy()
    df_corate.iloc[:,2] = list(df_near.iloc[:,2] / df_cotimes[:,2])
    df_corate.to_csv('./corate.csv', index=None, header=None)

if __name__ == '__main__':
    main()
