import os
import pandas as pd
import concurrent.futures
from simulation import simulation
import judge
import data


def sim_default(data : dict) -> pd.DataFrame:
    sim_data = data['input']
    for v in data['variables']:
        sim_data = sim_data.replace(v['text'], '{:.2f}'.format(v['def']))
    return judge.judge(data['time1'], data['time2'], simulation(sim_data), data['squids'])


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
    


def get_margins(data : dict, def_df : pd.DataFrame):
    futures = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    margins_list = []
    for v in data['variables']:
        future = executor.submit(margin, data, def_df, v)
        futures.append(future)
    
    for future in concurrent.futures.as_completed(futures):
        margins_list.append(future.result())
    executor.shutdown()

    return margins_list


def optimize(filepath : str):
    if os.path.exists(filepath):
        # 読み込み
        with open(filepath, 'r') as f:
            raw = f.read()
        # get main data
        main_data = data.get_main_data(raw)

        # simualtion default value
        def_frame = sim_default(main_data)
        print(def_frame)

        print(get_margins(main_data, def_frame))

    else:
        print("ファイルが存在しません。\n指定されたパス:"+filepath)

def main():
    import sys
    if len(sys.argv) == 2:
        optimize(sys.argv[1])
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv))) 


if __name__ == '__main__':
    optimize("/workspaces/docker-josim/files/hfqdff_lisan.inp")