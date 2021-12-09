import pandas as pd
import math
import simulation
import matplotlib.pyplot as plt

def judge(data : pd.DataFrame, judge_squid : list, time_tuple : tuple) -> pd.DataFrame:

    p = math.pi
    p2 = math.pi * 2

    newDataframe = pd.DataFrame()
    for di in judge_squid:
        newDataframe[di['1']+di['2']] = data[di['1']]+data[di['2']]

    resultframe = pd.DataFrame(columns=['time', 'element', 'phase'])
    for column_name, srs in newDataframe.iteritems():

        # バイアスをかけた時の状態の位相(初期位相)
        init_phase = srs[( srs.index > time_tuple[0] ) & ( srs.index < time_tuple[1] )].mean()
        # print(column_name," init phase = ",init_phase)
        judge_phase = init_phase + p
        
        # クロックが入ってからのものを抽出
        srs = srs[srs.index > time_tuple[1]]

        # 位相変数
        flag = 0
        for i in range(len(srs)-1):
            if (srs.iat[i] - (flag*p2 + judge_phase)) * (srs.iat[i+1] - (flag*p2 + judge_phase)) < 0:
                flag = flag + 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)
            elif (srs.iat[i] - ((flag-1)*p2 + judge_phase)) * (srs.iat[i+1] - ((flag-1)*p2 + judge_phase)) < 0:
                flag = flag - 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)

    resultframe.sort_values('time',inplace=True)
    resultframe.reset_index(drop=True,inplace=True)
    return resultframe


if __name__ == '__main__':
    with open("/workspaces/docker-josim/test_netlist_file/backup.txt","r") as f:
        raw = f.read()
    
    
    df = simulation.simulation(raw)

    rs = judge(df,[ {'1': 'P(B1|X2)', '2': 'P(B2|X2)'}, {'1': 'P(B1|X3)', '2': 'P(B2|X3)'}],(100e-12, 300e-12))

    print(rs)
