from typing import List
import matplotlib
from numpy import False_
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd


def main(args : List):
    curdir = os.path.dirname(os.path.abspath(__file__))

    if len(args) == 2:
        filepath = curdir+"/"+args[1]
        if os.path.exists(filepath):
            df = pd.read_csv(filepath,index_col=0)

            judge_frame(df)

        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
    else:
        print("引数が足りません。\n入力された引数:"+str(len(args)))



def judge_frame(df : pd.DataFrame):
    df_diff = df.diff()
    df_diff.where(df_diff >= 0, other = 0, inplace = True)
    # df.where(df == 0, other = 1, inplace = True)
    # print(df)
    # print(len(df.columns))
    """
    for colum in df_diff.columns:
        for value in df_diff[colum]:
            print(value)
    """

    for indexs,items in df_diff.iteritems():
        length = len(items)

        # ---------------#
        # 値の連続状態
        # 開始index
        # 合計
        # ---------------#

        keep = False
        start_i = 0   
        sum = 0        

        for i in range(length):

            if keep:
                if items.iat[i] == 0:
                    for j in range(start_i,i-1):
                        items.iat[j] = sum

                    sum = 0
                    keep = False
                
                else:
                    sum += items.iat[i]
            
            else:
                if items.iat[i] != 0:
                    keep = True
                    start_i = i
                    sum += items.iat[i]
                

        """
        for item in items:
            print(item)
            print(type(item))
        """
    
    df.plot()
    plt.show()

if __name__ == '__main__':
    main(sys.argv)