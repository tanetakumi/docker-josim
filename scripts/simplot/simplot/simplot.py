import matplotlib.pyplot as plt
import os
import re
from .simulation import simulation
import sys

def remove_opt_symbol(sim_data : str) -> str:
    # optimize の記述の削除したものの取得
    sim_data = re.sub('\*+\s*optimize\s*\*+[\s\S]+$','', sim_data)

    for s in re.findall('#.+\(.+\)',sim_data):
        value = re.sub('#.+\(|\)','',s)
        sim_data = sim_data.replace(s,value)
    
    return sim_data

def simulation_plot(filepath : str, savepath : str = None):
    if os.path.exists(filepath):
        # 読み込み
        with open(filepath, 'r') as f:
            raw = f.read()
        sim_data = remove_opt_symbol(raw)
        df = simulation(sim_data)
        df.plot()
        if filepath == None:
            plt.show()
        else:
            plt.savefig(savepath)
    else:
        print("ファイルが存在しません。\n指定されたパス:"+filepath,file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) == 2:
        simulation_plot(sys.argv[1])
    elif len(sys.argv) == 3:
        simulation_plot(sys.argv[1],sys.argv[2])
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv)),file=sys.stderr) 
        sys.exit(1)

if __name__ == '__main__':
    simulation_plot('/workspaces/docker-josim/files/hfqdff_lisan.inp')
    