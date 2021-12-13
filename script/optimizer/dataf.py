import pandas as pd
import math

df1 = pd.read_csv('/workspaces/docker-josim/test_netlist_file/df1.txt',index_col=0,header=0, sep='\s+')

print(df1)

df2 = pd.read_csv('/workspaces/docker-josim/test_netlist_file/df2.txt',index_col=0,header=0, sep='\s+')

print(df2)

res = df1.drop('time', axis=1).equals(df2.drop('time', axis=1))

print(res)

print((df1['time'] - df2['time']).abs())