import judge
from simulation import simulation
import pandas as pd


def margin(data : dict, def_df : pd.DataFrame, target : dict):

    # シュミレーションデータの作成
    sim_data = data['input']
    for vdict in data['variables']:
        if vdict != target:
            sim_data = sim_data.replace(vdict['text'], '{:.2f}'.format(vdict['def']))

    # lower
    high_v = target['def']
    low_v = 0
    tmp_v = (high_v + low_v)/2

    for i in range(6):
        tmp_df = judge.judge(data['time1'], data['time2'], 
            simulation(sim_data.replace(target['text'], '{:.2f}'.format(tmp_v))), 
            data['squids'])
        if judge.compareDataframe(tmp_df, def_df):
            high_v = tmp_v
            tmp_v = (high_v + low_v)/2
        else:
            low_v = tmp_v
            tmp_v = (high_v + low_v)/2

    lower_margin = high_v

    # upper
    high_v = 0
    low_v = target['def']
    tmp_v = target['def'] * 2

    for i in range(6):
        tmp_df = judge.judge(data['time1'], data['time2'], 
            simulation(sim_data.replace(target['text'], '{:.2f}'.format(tmp_v))), 
            data['squids'])
        if judge.compareDataframe(tmp_df, def_df):
            if high_v == 0:
                low_v = tmp_v
                tmp_v = tmp_v * 2
            else:  
                low_v = tmp_v
                tmp_v = (high_v + low_v)/2
        else:
            high_v = tmp_v
            tmp_v = (high_v + low_v)/2
    upper_margin = low_v
    
    return {'char' : target['char'], 'lower': lower_margin, 'upper' : upper_margin}   