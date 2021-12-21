import os
import pandas as pd
import concurrent.futures
from simulation import simulation
from margin import margin
from judge import judge
import data
import re
from margin_plot import margin_plot




def sim_default(data : dict) -> pd.DataFrame:
    sim_data = data['input']
    for v in data['variables']:
        print(v['text'])
        sim_data = sim_data.replace(v['text'], '{:.2f}'.format(v['def']))
    return judge(data['time1'], data['time2'], simulation(sim_data), data['squids'])

    
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

        # vlist 
        vlist = main_data['variables']

        pre = None
        for i in range(7):
            margin_list = get_margins(main_data, def_value_dataframe)
            margin_plot(pd.DataFrame(margin_list).set_index('char'), str(i))
            min_margin = 100
            for m in margin_list:
                print(m)
                if abs(m['lower']) < min_margin:
                    min_margin = abs(m['lower'])
                    min_element = m
                if m['upper'] < min_margin:
                    min_margin = abs(m['upper'])
                    min_element = m

            vlist = main_data['variables']
            for i in range(len(vlist)):
                if vlist[i]['char'] == min_element['char']:
                    upper_margin = min_element['upper_value'] if min_element['upper'] < 100 else min_element['def'] * 2
                    vlist[i]['def'] = ( upper_margin + min_element['lower_value'] )/2
            main_data['variables'] = vlist

            print("-----minimum margin:",min_element,"-----")
            
            
            if pre!= None and pre['char'] == min_element['char']:
                break;
            else:
                pre = min_element

    else:
        print("ファイルが存在しません。\n指定されたパス:"+filepath)

def main():
    import sys
    if len(sys.argv) == 2:
        optimize(sys.argv[1])
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv))) 


if __name__ == '__main__':
    optimize("/workspaces/docker-josim/files/dff.inp")