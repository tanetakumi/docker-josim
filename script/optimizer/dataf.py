import pandas as pd
import math


def compareDataframe(df1 : pd.DataFrame, df2 : pd.DataFrame) -> bool:
    return df1.sort_values(['phase', 'time']).drop('time', axis=1).reset_index(drop=True)\
        .equals(df2.sort_values(['phase', 'time']).drop('time', axis=1).reset_index(drop=True))


if __name__ == "__main__":
    df1 = pd.read_csv('/workspaces/docker-josim/test_netlist_file/df1.txt',index_col=0,header=0, sep='\s+')
    print(df1)
    df2 = pd.read_csv('/workspaces/docker-josim/test_netlist_file/df2.txt',index_col=0,header=0, sep='\s+')
    print(df2)
    # print(compareDataframe(df1, df2))
    print(df2.sort_values(['phase', 'time']).drop('time', axis=1).reset_index(drop=True))