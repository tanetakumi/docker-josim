import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os

import pandas as pd


def main():
    curdir = os.path.dirname(os.path.abspath(__file__))

    df = pd.read_csv(curdir+"/out.csv",index_col=0)

    print(df)
    '''
    x_list=[] # x_listを定義 (空のリストを作成)
    y_list=[] # y_listを定義 
    ##  データを読み込み，x_listとy_listに値を格納する
    for line in f:
        data = line[:-1].split(' ')
        x_list.append(float(data[0]))
        y_list.append(float(data[1]))
    print(x_list)
    print("-------------")
    print(y_list)
    plt.plot(x_list,y_list)
    # plt.plot([1, 3, 3, 4, 5])
    plt.show()
    '''
    df.plot()
    plt.show()

if __name__ == '__main__':
    # cmd = ("jsim si.inp")
    # print(res_cmd_lfeed(cmd))
    main()