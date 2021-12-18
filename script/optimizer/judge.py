from numpy import float64
import pandas as pd
import math
import simulation
import matplotlib.pyplot as plt

def judge(time1 : float, time2 : float, data : pd.DataFrame, judge_squid : list) -> pd.DataFrame:

    p = math.pi
    p2 = math.pi * 2

    newDataframe = pd.DataFrame()
    for di in judge_squid:
        newDataframe[di['1']+di['2']] = data[di['1']]+data[di['2']]

    resultframe = pd.DataFrame(columns=['time', 'element', 'phase'])
    for column_name, srs in newDataframe.iteritems():

        # バイアスをかけた時の状態の位相(初期位相)
        init_phase = srs[( srs.index > time1 ) & ( srs.index < time2 )].mean()
        # print(column_name," init phase = ",init_phase)
        judge_phase = init_phase + p
        
        # クロックが入ってからのものを抽出
        srs = srs[srs.index > time2]

        # 位相変数
        flag = 0
        for i in range(len(srs)-1):
            if (srs.iat[i] - (flag*p2 + judge_phase)) * (srs.iat[i+1] - (flag*p2 + judge_phase)) < 0:
                flag = flag + 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)
            elif (srs.iat[i] - ((flag-1)*p2 + judge_phase)) * (srs.iat[i+1] - ((flag-1)*p2 + judge_phase)) < 0:
                flag = flag - 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)

    # resultframe.sort_values('time',inplace=True)
    # resultframe.reset_index(drop=True,inplace=True)
    return resultframe


def compareDataframe(df1 : pd.DataFrame, df2 : pd.DataFrame) -> bool:
    return df1.sort_values(['phase', 'time']).drop('time', axis=1).reset_index(drop=True)\
        .equals(df2.sort_values(['phase', 'time']).drop('time', axis=1).reset_index(drop=True))

def squidPlot(time1 : float, time2 : float, data : pd.DataFrame, judge_squid : list) -> pd.DataFrame:

    p = math.pi
    p2 = math.pi * 2

    newDataframe = pd.DataFrame()
    for di in judge_squid:
        newDataframe[di['1']+di['2']] = data[di['1']]+data[di['2']]

    newDataframe.plot()
    plt.show()


if __name__ == '__main__':
    with open("/workspaces/docker-josim/test_netlist_file/backup.txt","r") as f:
        raw = f.read()
    
    
    df = simulation.simulation(raw)

    squidPlot(100e-12, 300e-12, df, [ {'1': 'P(B1|X2)', '2': 'P(B2|X2)'}, {'1': 'P(B1|X3)', '2': 'P(B2|X3)'}])


