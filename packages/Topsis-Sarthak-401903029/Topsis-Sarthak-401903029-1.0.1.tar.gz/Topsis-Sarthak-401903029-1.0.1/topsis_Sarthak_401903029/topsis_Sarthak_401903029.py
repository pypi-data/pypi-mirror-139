import pandas as pd
import sys as sys

def main():
    if(len(sys.argv)!=4):
        print("Number of input arguments are not correct!!! ")
        exit(0)
    
    df=pd.read_csv(sys.argv[1], index_col=0)
    weights = sys.argv[2]
    weights = weights.split(',')
    weights = [int(num) for num in weights]
    impacts = sys.argv[3]
    impacts = impacts.split(',')
    
    if len(df.columns)!=len(weights) or len(df.columns)!=len(impacts):
        print("Input file must contain equal number of weights, number of impacts and number of columns (from 2nd to last columns)!!!")
        exit(0)
    
    allowedVals = ['+', '-']
    for imp in impacts:
        if imp not in allowedVals:
            print("Impacts must be either +ve or -ve!!!")
            exit(0)
    for col in df.columns:
        df.loc[:,col] = pd.to_numeric(df.loc[:,col], errors='coerce')
    newRow = []
    for index, row in df.iterrows():
        include=True
        for col in df.columns:
            if pd.isna(df.loc[index,col])==True:
                include=False
        if include:
            newRow.append(index)
    df=df.loc[newRow,:]
    
    df2=df.copy()
    df2=df2**2
    index=df2.index
    col=df2.columns
    df2.loc['Sqr']=df2.sum(axis=0)**0.5
    df /= df2.loc['Sqr']

    df = df*weights

    x=0
    for col in df:
        if impacts[x]=='+':
            df.loc['vj',col] = df.loc[:,col].min()
            df.loc['vi',col] = df.loc[:,col].max()
        else:
            df.loc['vj',col] = df.loc[:,col].max()
            df.loc['vi',col] = df.loc[:,col].min()
        x+=1

    df2=df.copy()
    col=df2.columns
    for i in index:
        df2.loc[i, 'Si+']=0
        df2.loc[i, 'Si-']=0
        for j in col:
            df2.loc[i,'Si+']+=(df2.loc[i,j]-df2.loc['vi',j])**2
            df2.loc[i,'Si-']+=(df2.loc[i,j]-df2.loc['vj',j])**2
        df2.loc[i, 'Si+']**=0.5
        df2.loc[i, 'Si-']**=0.5
    df2.loc[:,'Pi']=df2.loc[:,'Si-']/(df2.loc[:,'Si-']+df2.loc[:,'Si+'])

    df3=pd.read_csv(sys.argv[1], index_col=0)
    df3.loc[:,'Topsis Score']=round(df2.loc[:,'Pi']*100, 2)
    df3.loc[:,'Rank'] = df2.loc[:,'Pi'].rank(ascending = 0)
    print(df3.fillna('Invalid Data!!!'))

if __name__=="__main__":
    main()