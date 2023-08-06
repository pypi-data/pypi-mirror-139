
from .Topsis-102097012 import main
# import sys
# import os.path
# import pandas as pd
# import topsispy as tp
# import numpy as np
# from pandas.api.types import is_string_dtype
# from pandas.api.types import is_numeric_dtype

# data = sys.argv[1]
# weight = sys.argv[2]
# impact = sys.argv[3]
# output = sys.argv[4]

# ##########
# if(os.path.exists(data)==False):
#     exit(1)
# ##########


# ##########
# if len(sys.argv)!=5:
#     exit(1)
# ##########



# i=pd.read_csv(data)


# ##########
# if len(i.columns)<3:
#     exit(1)
# ##########
# for j in range(1,len(i.columns)):
#     if(is_numeric_dtype(i.iloc[:,j])==False):
#         exit(1)
# ##########


# # output="102097012-result.csv"
# # i = pd.read_csv("C:/Users/neeru/Documents/chavvi_study/anaconda/102097012-data.csv")
# # weight = '1,1,1,2,1'
# # impact = '+,+,-,+,+'
# weight = weight.split(',')
# weight = [int(i) for i in weight]
# impact = impact.split(',')
# ##########
# for j in range(len(impact)):
#     if impact[j]=="+" or impact[j]=="-":
#         continue
#     else:
#         exit(1)
# ##########
# impact = list(map(lambda x:x.replace('+','1'),impact))
# impact = list(map(lambda x:x.replace('-','-1'),impact))
# impact = [int(i) for i in impact]

# ##########
# if((len(weight)==len(impact) and len(weight)==len(i.columns)-1)==False):
#     exit(1)
# ##########

# table=i.drop(columns=['Fund Name'])
# arr = table.to_numpy()
# topsis = tp.topsis(arr, weight, impact)
# table = pd.DataFrame(arr)
# table.insert(0,"Fund Name",i["Fund Name"])
# table = table.rename(columns={0:"P1",1:'P2',2:'P3',3:'P4',4:'P5'})
# table['Topsis Score'] = topsis[1]
# j = 1
# t = topsis[1]
# t = list(t)
# rank={}
# while len(t)!=0:
#     rank[max(t)] = j
#     t.remove(max(t))
#     j = j + 1

# table['Rank'] = table["Topsis Score"].map(rank)
# table.to_csv(output)
