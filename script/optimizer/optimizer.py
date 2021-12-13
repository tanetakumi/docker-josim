import re
import os
import sys
import pandas as pd
import math
import concurrent.futures

from pandas.core.arrays.integer import IntegerArray
import util
from simulation import simulation
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

# 先頭の文字列、Line
def get_variable(text : str) -> list:
    vlist = []
    for l in re.findall('#.+\(.+\)', text):
        a = re.split('\(', re.sub('#|\)','',l) )
        vlist.append({'char': a[0], 'text': l, 'def': util.stringToNum(a[1])})
    return vlist


def sim_default(time_tuple : tuple, sim_data : str, squid : list, vlist : list) -> pd.DataFrame:
    for v in vlist:
        sim_data = sim_data.replace(v['text'], '{:.2f}'.format(v['def']))
    return judge.judge(time_tuple, simulation(sim_data), squid)

def get_margins(time_tuple : tuple, sim_data : str, squid : list, vlist : list, def_frame : pd.DataFrame):
    margins_list = []
    for v in vlist:
        tmp_sim_data = sim_data
        for v2 in vlist:
            if v == v2:
                vtarg = v
            else:
                tmp_sim_data = tmp_sim_data.replace(v2['text'], '{:.2f}'.format(v2['def']))

        # 変数の初期化=====
        pre_b = True
        high_v = vtarg['def']
        low_v = 0
        tmp_v = (high_v + low_v)/2

        for i in range(6):

            tmp_frame = judge.judge(time_tuple, 
                simulation(tmp_sim_data.replace(vtarg['text'], '{:.2f}'.format(tmp_v))), 
                squid)
            pre_b = judge.compareDataframe(tmp_frame, def_frame)
            if pre_b:
                high_v = tmp_v
                tmp_v = (high_v + low_v)/2
            else:
                low_v = tmp_v
                tmp_v = (high_v + low_v)/2
        low_margin = high_v

        # 変数の初期化=====
        pre_b = True
        high_v = 0
        low_v = vtarg['def']
        tmp_v = vtarg['def'] * 2

        for i in range(6):
            tmp_frame = judge.judge(time_tuple, 
                simulation(tmp_sim_data.replace(vtarg['text'], '{:.2f}'.format(tmp_v))), 
                squid)
            pre_b = judge.compareDataframe(tmp_frame, def_frame)
            if pre_b:
                if high_v == 0:
                    low_v = tmp_v
                    tmp_v = tmp_v * 2
                else:  
                    low_v = tmp_v
                    tmp_v = (high_v + low_v)/2
            else:
                high_v = tmp_v
                tmp_v = (high_v + low_v)/2
        high_margin = low_v
        margins_list.append((v['char'], low_margin, high_margin))
    return margins_list


def optimize(filepath : str):
    if os.path.exists(filepath):
        # 読み込み
        with open(filepath, 'r') as f:
            raw = f.read()
        # 1.get end time of bias raise and start time of first pulse
        time1, time2, sim_data = get_optimize_data(raw)
        time_tuple = (100e-12, 300e-12) # time_tuple=(time1, time2)
        # 2.get squids data
        squids = get_judge_spuid(sim_data)

        # 3.get variable data
        vlist = get_variable(sim_data)

        # simualtion default value
        def_frame = sim_default(time_tuple, sim_data, squids, vlist)
        print(def_frame)

        print(get_margins(time_tuple, sim_data, squids, vlist, def_frame))
        # simulation
        # print(judge.judge(simulation.simulation(sim_data), squids, (100e-12, 300e-12)))
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
    
    optimize("/workspaces/docker-josim/test_netlist_file/piJTL.inp")