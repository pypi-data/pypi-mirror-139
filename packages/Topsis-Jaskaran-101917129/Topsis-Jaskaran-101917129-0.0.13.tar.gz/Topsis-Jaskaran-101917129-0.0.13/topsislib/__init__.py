import pandas as pd
import numpy as np
    
"""
Created on Wed Feb 23 22:31:21 2022

@author: Jaskaran S. Purewal
"""

def topsis(dff,weights,impacts):
    df=dff
    ncols=df.shape[1]-1
    nrows=df.shape[0]
    columns=list(df.columns)
    column_1=df[columns[0]]
    df.drop(columns[0],axis=1,inplace=True)
    columns=list(df.columns)
    #Numerical values check
    for c in columns:
        if(df[c].dtype not in ['float64','int64']):
            print("Data must be either float or int.")
            return 1
    if(ncols<2):
        print("There should at least be 2 features.")
        return 1
    if(',' not in weights):
        print("Weights must be separated by ','.")
        return 1
    if(',' not in impacts):
        print("Impacts must be separated by ','.")
        return 1
    weights=weights.split(',')
    weights_parse=[]
    for x in weights:
        weights_parse.append(int(x))
    impacts_parse=impacts.split(',')
    #Number of cols,wts and impacts same check
    if(ncols!=len(weights_parse)):
        print('Number of columns and weights entered are different.')
    if(ncols!=len(impacts_parse)):
        print('Number of columns and impacts entered are different.')
    for x in impacts_parse:
        if(x not in ['+','-']):
            print("Impacts must eiher be + or -.")   
    # Also PRINT RIGHT INPUT FORMAT IF ANY EXCEPTION OCCUR
    
    
    #Step 1 Vector Normalization
    
    for c in columns:
        sqr_sum_sq=0
        for r in range(nrows):
            sqr_sum_sq=sqr_sum_sq+(df[c][r])**2
        sqr_sum_sq=np.sqrt(sqr_sum_sq)
        for r in range(nrows):
            df[c][r]=(df[c][r]/sqr_sum_sq)
    
    # We get Normalized performance values
    
    
    
    
    #Step 2 Weight Assignment
    i=0
    for c in columns:
        for r in range(nrows):
            df[c][r]=df[c][r]*weights_parse[i]
        i=i+1
    
    #We get weighted Normalized Decision Matrix
    
    
    
    
    #Step 3 Ideal Best Ideal Worst
    ideal_best=[]
    ideal_worst=[]
    i=0
    for c in columns:
        if(impacts_parse[i]=='+'):
            ideal_best.append(df[c].max())
            ideal_worst.append(df[c].min())
        else:
            ideal_best.append(df[c].min())
            ideal_worst.append(df[c].max())
        i=i+1
    
    
    
    
    #Step 4 Calculate Euclidian Distance
    from_ideal_best=[]
    from_ideal_worst=[]
    i=0
    for r in range(nrows):
        i=0
        sqr_sum_dsq_best=0
        sqr_sum_dsq_worst=0
        for c in columns:
            sqr_sum_dsq_best=sqr_sum_dsq_best+(ideal_best[i]-df[c][r])**2
            sqr_sum_dsq_worst=sqr_sum_dsq_worst+(ideal_worst[i]-df[c][r])**2
            i=i+1
        sqr_sum_dsq_best=np.sqrt(sqr_sum_dsq_best)
        sqr_sum_dsq_worst=np.sqrt(sqr_sum_dsq_worst)
        
        from_ideal_best.append(sqr_sum_dsq_best)
        from_ideal_worst.append(sqr_sum_dsq_worst)
    
    
    
    
    #Step 5 Performance Score
    Pi=[]
    for x in range(nrows):
        Pi.append((from_ideal_worst[x]/(from_ideal_worst[x]+from_ideal_best[x])))
    
    
    
    #Step 6 Rank
    df['Topsis Score']=Pi
    
    df['Rank']=df['Topsis Score'].rank(ascending=False)
    
    df=pd.concat([column_1,df],axis=1)
    return df