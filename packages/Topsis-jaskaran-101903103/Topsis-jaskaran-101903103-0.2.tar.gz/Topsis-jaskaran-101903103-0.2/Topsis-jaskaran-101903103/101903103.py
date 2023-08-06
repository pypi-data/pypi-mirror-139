import pandas as pd
import numpy as np
from sklearn import preprocessing
from importlib import resources
import io
import sys

class WrongNumberOfParameters(Exception):
    pass
class NumberOfColumnError(Exception):
    pass
class UnequalWeightandImpacts(Exception):
    pass
class IncorrectImpact(Exception):
    pass
#exception handling
try:
    if len(sys.argv)>4:
        raise WrongNumberOfParameters(" Number of Parameters are wrong")
    dataf=pd.read_csv(sys.argv[1])
    if len(dataf.columns)<3:
        raise NumberOfColumnError("Input dataset has less than 3 columns,retry")
    dfl=dataf
    dataf=dataf.iloc[:,1:]
    sz=len(dataf)
    impacts=sys.argv[3]
    weights=sys.argv[2]
    if len(impacts.split(sep=","))!=len(weights.split(sep=",")):
        raise UnequalWeightandImpacts("Weight and impact size different")
    if len(impacts.split(sep=","))!=len(dataf.columns):
        raise UnequalWeightandImpacts("Dataset and impact size different")
    if len(weights.split(sep=","))!=len(dataf.columns):
        raise UnequalWeightandImpacts("Dataset and weight size different")
    
    best=[]
    worst=[]
    #normalization of table
    for i in dataf.columns:
        arr=dataf.loc[:,i]
        newarr=preprocessing.normalize(np.reshape(np.array(arr),(1,sz)))
        dataf.loc[:,i]=np.reshape(newarr,(sz,1))

        
    wlist=weights.split(sep=",")
    for i in range(len(dataf.columns)):
        dataf.iloc[:,i]*=float(wlist[i])
    ilist=impacts.split(sep=",")
    for point in ilist:
        if point not in ["+","-"]:
            raise IncorrectImpact("ERROR : Impact values are incorrect...")
            
    for i in range(len(dataf.columns)):
        if ilist[i]=="+":
            best=np.append(best,dataf.iloc[:,i].max())
            worst=np.append(worst,dataf.iloc[:,i].min())
        elif ilist[i]=="-":
            best=np.append(best,dataf.iloc[:,i].min())
            worst=np.append(worst,dataf.iloc[:,i].max())
    dataf=dataf.append(pd.Series(best,index=dataf.columns),ignore_index=True)
    dataf=dataf.append(pd.Series(worst,index=dataf.columns),ignore_index=True)

    dist_ib=[]
    dist_iw=[]
    for i in range(sz):
        sumplus=0
        summinus=0
        for j in dataf.columns:
            temp=dataf.loc[i,j]-dataf.loc[sz,j]
            sumplus+=np.power(temp,2)
            temp=dataf.loc[i,j]-dataf.loc[sz+1,j]
            summinus+=np.power(temp,2)
        dist_ib.append(np.sqrt(sumplus))
        dist_iw.append(np.sqrt(summinus))
    topsis=[]
    for i in range(len(dist_iw)):
        topsis.append(dist_iw[i]/(dist_iw[i]+dist_ib[i]))
    dfl["Topsis Score"]=topsis
    dict_rank={}
    #rank determination
    topsis.sort(reverse=True)
    dict_rank[topsis[0]]=1
    rank=2
    for i in range(1,len(topsis)):
        dict_rank[topsis[i]]=rank
        rank+=1
    rank_topsis=[]
    for i in dfl["Topsis Score"]:
        rank_topsis.append(dict_rank[i])
    dfl["Rank"]=rank_topsis
    dfl.to_csv("101903103-result-1.csv",index=False)
except WrongNumberOfParameters as wnop:
    print(wnop)
except ValueError:
    print("Incorrect value present")
except FileNotFoundError:
    print("Input value not found")
except NumberOfColumnError as nce:
    print(nce)
except UnequalWeightandImpacts as uwi:
    print(uwi)
except IncorrectImpact as ii:
    print(ii)
