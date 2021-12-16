import os
import pandas as pd
import concurrent.futures
from simulation import simulation
from margin import margin
import judge
import data



def sim_default(data : dict) -> pd.DataFrame:
    sim_data = data['input']
    for v in data['variables']:
        sim_data = sim_data.replace(v['text'], '{:.2f}'.format(v['def']))
    return judge.judge(data['time1'], data['time2'], simulation(sim_data), data['squids'])

    
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
        def_value_dataframe = sim_default(main_data)

        margin_list = get_margins(main_data, def_value_dataframe)

        print(margin_list)

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