import re
import itertools
import os
import sys
import pandas as pd
import subprocess
from subprocess import PIPE
import io
import math
import concurrent.futures
import csv

        
def isint(s):  # 正規表現を使って判定を行う
    p = '[-+]?\d+'
    return True if re.fullmatch(p, s) else False

def isfloat(s):  # 正規表現を使って判定を行う
    p = '[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?'
    return True if re.fullmatch(p, s) else False

def digit(s):  # 正規表現を使って小数点以下の桁数
    if re.search("\.",s)!= None:
        return len(re.split("\.",s)[1])
    else:
        return 0

def variables_to_dataframe(var_list : list) -> pd.DataFrame:
    # 変数辞書->変数リスト変換
    vlist = []
    for v in var_list:
        vlist.append({'char':v['char'],'value':mkNumList(v['start'],v['stop'],v['step'],v['digit'])})
    # 変数リスト変換->変数Dataframe
    colum = [d.get('char') for d in vlist]
    contents = [list(tup) for tup in itertools.product(*[d.get('value') for d in vlist])]
    df = pd.DataFrame(contents,columns=colum)
    print("======== variable value dataframe ========")
    print(df)
    return df


def get_variables(input : str) -> list:

    # 変数の前につける先頭文字(正規表現)
    lead_str = '\*v\*'

    var = []

    for l in input.splitlines():
        if re.search(lead_str,l) != None:
            subdata = re.sub('#|\(|\)|\s|'+lead_str,'',l)
            # print(subdata)
            spldata = re.split("=|;",subdata)
            if len(spldata) == 5:
                di = digit(spldata[4])
                for i in range(1,5):
                    if isint(spldata[i]):
                        # print("int")
                        spldata[i] = int(spldata[i])
                    elif isfloat(spldata[i]):
                        # print("float")
                        spldata[i] = float(spldata[i])
                    else:
                        print("数値変換ができません。")
                        print(l)
                        sys.exit()
                vv = {"char":spldata[0], "default":spldata[1], "start":spldata[2], "stop":spldata[3], "step":spldata[4], "digit":di}
                var.append(vv)
            else:
                print("\033[31m変数の書き方が間違っています。\033[0m")
                print(lead_str+"<変数>=(<default>;<start>;<stop>;<step>)")
                sys.exit()
    # 取得結果の表示
    print("\033[34mvariable data\033[0m")
    print(var)
    print("\n")
    return var

def get_judge_spuid(input : str) -> list:
    squids = []
    # 改行が一回だけ、すなわち連続されて記述されている(.print phase <要素>)の部分を取得
    for m in re.finditer('\.print\s+phase.+\n.*\.print\s+phase\s+.+',input):
        rawdata = m.group()
        subdata = re.sub('[\t\f\v ]|\.print\s+phase','',rawdata)
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
    print("\n")
    return squids


def mkNumList(start,stop,step,digit) -> list:
    res = []
    value = start
    while(value<stop+step):
        res.append(str(round(value,digit)))
        value = value + step
    return res

def cut_josim_data(raw : str) -> str:
    first_split = raw.split('100% Formatting Output')

    if len(first_split) == 2:
        return first_split[1]
    else:
        print("\033[31m[ERROR] シュミレーションされませんでした。\033[0m")
        print(raw)
        sys.exit()



def judge(data : pd.DataFrame, judge_squid : list) -> pd.DataFrame:

    p = math.pi *2

    newDataframe = pd.DataFrame()
    for di in judge_squid:
        newDataframe[di['1']+di['2']] = data[di['1']]+data[di['2']]
    # print(newDataframe)

    resultframe = pd.DataFrame(columns=['time', 'element', 'phase'])
    for column_name, srs in newDataframe.iteritems():
        flag = 0
        for i in range(len(srs)-1):
            if (srs.iat[i] - (flag+1)*p) * (srs.iat[i+1] - (flag+1)*p) < 0:
                flag = flag + 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)

            elif (srs.iat[i] - (flag-1)*p) * (srs.iat[i+1] - (flag-1)*p) < 0:
                flag = flag - 1
                resultframe = resultframe.append({'time':srs.index[i], 'element':column_name, 'phase':flag},ignore_index=True)


    resultframe.sort_values('time',inplace=True)
    resultframe.reset_index(drop=True,inplace=True)
    return resultframe
    

def simulation(input : str, data : pd.Series, filepath : str) -> pd.DataFrame:
    new_file = input
    for index, value in data.iteritems():
        new_file = re.sub('#\('+index+'\)',value,new_file)
    
    with open(filepath, mode="w") as f:
        f.write(new_file)

    result = subprocess.run(["josim-cli", filepath, "-V", "1"], stdout=PIPE, stderr=PIPE, text=True)
    # print(result.stdout)
    split_data = cut_josim_data(result.stdout)
    return pd.read_csv(io.StringIO(split_data),index_col=0,header=0)



def thread_simulation(input :str, df : pd.DataFrame, filepath :str, judge_squid : list, default_data : pd.DataFrame, thread_num : int):
    print("thread"+str(thread_num)+":start")
    res_bool = []
    for index, srs in df.iterrows():
        sim_data = simulation(input, srs, filepath)
        shift_data = judge(sim_data, judge_squid)
        res_bool.append(compareDataframe(shift_data,default_data))
    
    df = df.assign(result = res_bool)
    print("thread"+str(thread_num)+":complete")
    os.remove(filepath)
    return df

    
        

def get_default_data(input : str, filepath : str, dic_data : list, judge_squid : list) -> pd.DataFrame:
    print("Simulation of default value")

    srs = pd.Series(index=[ str(d['char']) for d in dic_data ], data=[ str(d['default']) for d in dic_data ])
    result = simulation(input, srs, filepath)
    os.remove(filepath)
    return judge(result,judge_squid)


def compareDataframe(df1 : pd.DataFrame, df2 : pd.DataFrame) -> bool:
    return df1.drop('time', axis=1).equals(df2.drop('time', axis=1))


def split_dataframe(df, k):
    dfs = [df.loc[i:i+k-1, :] for i in range(0, len(df), k)]
    return dfs




# 引数で入力するのは　python optimizer.py simulation_file output_file
if __name__ == '__main__':
    dir = os.getcwd()
    sim_dir = dir + "/hfq-optimizer-sim"

    print('\033[31mcurrent dir:\t\t\033[0m', dir)
    print('\033[31mdir of this py program:\t\033[0m', os.path.dirname(__file__))

    # confirm argument --------------------------
    if len(sys.argv) != 3:
        print("\033[31m[ERROR]\033[0m Wrong number of arguments for the function.")
        sys.exit()

    if os.path.exists(sys.argv[1]):
        print("\033[31msimulation file:\033[0m\t",sys.argv[1])
    else:
        print("\033[31m[ERROR]\033[0m file not exist:\t",sys.argv[1])
        sys.exit()
    output_filepath = sys.argv[2]
    print("\033[31moutput file:\033[0m\t\t",output_filepath)
    if os.path.exists(output_filepath):
        if input('すでにファイルが存在しています。上書きしますか？[y/n]: ') == "y":
            os.remove(output_filepath)
            print("上書きします。")
        else:
            print("他のファイルを入力してください。プログラムを終了します。")
            sys.exit()

    # confirm argument --------------------------
    # フォルダーの作成
    if not os.path.exists(sim_dir):
        os.mkdir(sim_dir)

    # 読み込み
    with open(sys.argv[1],'r') as f:
        raw = f.read()

    
    # 判定するSQUID部分取得
    squids = get_judge_spuid(raw)

    # 変数部分取得
    variables = get_variables(raw)
    # list dataframe 変換
    df = variables_to_dataframe(variables)
    # 変数Dataframeの分割
    dfs = split_dataframe(df,20)

    # default データの取得
    default_data = get_default_data(raw, sim_dir+'/def.inp', variables, squids)

    with open(output_filepath, 'w') as f:
        writer = csv.writer(f)
        header = [vl['char'] for vl in variables]
        header.append('result')
        writer.writerow(header)


    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
    futures = []
    
    for i, dataf in enumerate(dfs):
        future = executor.submit(thread_simulation, raw, dataf, sim_dir+'/tmp'+str(i)+'.inp', squids, default_data, i)
        futures.append(future)

    # 各futureの完了を待ち、結果を取得。
    # as_completed()は、与えられたfuturesの要素を完了順にたどるイテレータを返す。
    # 完了したタスクが無い場合は、ひとつ完了するまでブロックされる。
    for future in concurrent.futures.as_completed(futures):
        result_df = future.result()
        result_df.to_csv(output_filepath, mode='a', header=False, index=False)
    # すべてのタスクの完了を待ち、後始末をする。
    # 完了していないタスクがあればブロックされる。
    # (上でas_completedをすべてイテレートしているので、実際にはこの時点で完了していないタスクは無いはず。)
    executor.shutdown()
    
    # フォルダーの削除
    os.rmdir(sim_dir)