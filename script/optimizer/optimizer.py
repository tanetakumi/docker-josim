import re
import os
import sys
import pandas as pd
import math
import concurrent.futures
import util
import simulation
import judge
    


def get_optimize_data(data : str) -> tuple:
    assign = lambda x: None if x is None else x.group()
    optimize_data = assign(re.search('\*+\s*optimize\s*\*+[\s\S]+$', data))
    if optimize_data is None:
        print("初期化されていません。")
        sys.exit()
    time1 = get_value(optimize_data, "EndTimeOfBiasRise")
    time2 = get_value(optimize_data, "StartTimeOfPulseInput")
    sim_data = re.sub('\*+\s*optimize\s*\*+[\s\S]+$','', data)
    return (time1, time2, sim_data)

def get_judge_spuid(data : str) -> list:
    squids = []
    # 改行が一回だけ、すなわち連続されて記述されている(.print phase <要素>)の部分を取得
    for m in re.finditer('\.print\s+phase.+\n.*\.print\s+phase\s+.+',data, flags=re.IGNORECASE):
        rawdata = m.group()
        subdata = re.sub('[\t\f\v ]|\.print\s+phase','',rawdata, flags=re.IGNORECASE)
        spldata = re.split("\n",subdata)
        if len(spldata) == 2:
            squids.append({"1" : "P("+spldata[0]+")", "2" : "P("+spldata[1]+")"})
        else:
            print("ERROR")
            print(rawdata)
            print(subdata)
            sys.exit()
    # 取得結果の表示
    print("\033[34mjudge squid data\033[0m")
    print(squids)
    return squids

    
def get_value(data : str, key : str) -> str:
    line = next(filter(lambda x: re.search(key, x), data.splitlines()),None)
    if line is None:
        print(key + " の値が取得できません", file=sys.stderr)
        sys.exit(1)
    else:
        r = re.split('=',line)
        if len(r) == 2:
            return r[1]
        else:
            print(key + " の値が取得できません", file=sys.stderr)
            sys.exit(1)

def get_variable(data : str) -> str:
    line = next(filter(lambda x: re.search('#\(.+\)', x), data.splitlines()),None)
    print(line)

def optimize(filepath : str):
    if os.path.exists(filepath):
        # 読み込み
        with open(filepath, 'r') as f:
            raw = f.read()
        # get end time of bias raise and start time of first pulse
        time1, time2, sim_data = get_optimize_data(raw)

        # get squids data
        squids = get_judge_spuid(raw)

        # 

        # simulation
        print(judge.judge(simulation.simulation(sim_data), squids, (100e-12, 300e-12)))
    else:
        print("ファイルが存在しません。\n指定されたパス:"+filepath)

def main():
    import sys
    if len(sys.argv) == 2:
        optimize(sys.argv[1])
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv))) 


if __name__ == '__main__':
    with open('/workspaces/docker-josim/test_netlist_file/backup.txt','r') as f:
        raw = f.read()
    get_variable(raw)
    # optimize("/workspaces/docker-josim/test_netlist_file/piJTL.inp")