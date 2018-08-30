from functions import * 
import pandas as pd

def process1(indir, outdir, picture_num):
    #data cleanning
    clean_data(indir = indir, outdir = outdir, picture_num = picture_num)
    
    #compute and output distance rate
    for i in range(picture_num):
        print('computing distance: %.0f%%' % ((i+1)/picture_num*100), end='\r')
        data = pd.read_csv('%s/%03d.csv' % (outdir, (i+1)), sep=',')
        dis_rate = distance(data)
        if i == 0:
            dis_rate.iloc[:,2] = 0
        dis_rate.to_csv('%s/AAAt%03d-dis.csv' % (outdir, (i+1)), index=None, header=True)  
    print('----------------------------------------')
    
    #compute total coexistence counts of cell appeared in these pictures
    df_cotimes = coexistence(file_dir = outdir, picture_num = picture_num)
    df_cotimes.to_csv('%s/cotimes.csv' % outdir, index = None, header = True) 
    
####################################################################

def process2(out_dir, picture_num, cut_off):
    #find the near counts (distance rate < cut_off) from each cell pair
    df_cotimes = pd.read_csv('%s/cotimes.csv' % outdir, sep = ',')
    df_near = near_cell(file_dir = out_dir, picture_num = picture_num, df_cotimes = df_cotimes, cut_off = cut_off)
    
    #for each cell pair, computing (near times) / (total times)
    df_corate = df_comtimes.copy()
    df_corate.iloc[:,2] = list(df_near.iloc[:,2] / df_cotimes[:,2])
    df_corate.to_csv('%s/corate.csv' % outdir, index = None, header = True)


def main():
    #call parseArg() to get parameter from command line
    args = parseArg()
    indir= args.indir
    outdir= args.outdir
    picture_num = int(args.num)
    cut_off = float(args.cut)
    
    #P1
    process1(indir, outdir, picture_num)
    #P2
    process2(out_dir, picture_num, cut_off)
    
    
if __name__ == '__main__':
    main()