from function import distance
from function import coexistence 
import os
import pandas as pd

def main():
    for i in range(180):
        print('converting format: %.0f%%' % ((i+1)/180*100), end='\r')
        os.system('python clean_data.py -f ./nuclei/t%03d-nuclei -d ./test' % (i+1))
        
    data = pd.read_csv('./test/t005-nuclei.csv', sep=',', header=None)
    dis_list = distance(data)
    print(dis_list[0])
    print(dis_list[1])
    
    cotimes = coexistence(180)
    print(cotimes[0])
    print(cotimes[1])

if __name__ == '__main__':
    main()