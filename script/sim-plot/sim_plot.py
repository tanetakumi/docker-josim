import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import re
from . import simulation


def remove_opt_symbol(sim_data : str) -> str:
    # optimize の記述の削除したものの取得
    sim_data = re.sub('\*+\s*optimize\s*\*+[\s\S]+$','', sim_data)

    for s in re.findall('#.+\(.+\)',sim_data):
        value = re.sub('#.+\(|\)','',s)
        sim_data = sim_data.replace(s,value)
    
    return sim_data

def main():
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                raw = f.read()
            
            # print(re.findall('#.+\(.+\)',raw))
            df = simulation(raw)
            print(df)
            df.plot()
            plt.show()
        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv))) 

def sim_plot(filepath : str):
    if os.path.exists(filepath):
        # 読み込み
        with open(filepath, 'r') as f:
            raw = f.read()
        sim_data = remove_opt_symbol(raw)
        df = simulation.simulation(sim_data)
        df.plot()
        plt.show()
    else:
        print("ファイルが存在しません。\n指定されたパス:"+filepath)

def main():
    import sys
    if len(sys.argv) == 2:
        sim_plot(sys.argv[1])
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv))) 

if __name__ == '__main__':
    sim_plot('/workspaces/docker-josim/files/hfqdff_lisan.inp')
    