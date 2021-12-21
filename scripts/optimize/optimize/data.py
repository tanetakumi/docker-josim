import sys
import re
import util


# 先頭の文字列、Line
def get_variable(text : str) -> list:
    vlist = []
    for l in re.findall('#.+\([\d\.]+\)', text):
        a = re.split('\(', re.sub('#|\)','',l) )
        vlist.append({'char': a[0], 'text': l, 'def': util.stringToNum(a[1])})
    vlist_result = []
    for v in vlist:
        if v not in vlist_result:
            vlist_result.append(v)
    return vlist_result

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


def get_main_data(data : str) -> tuple:
    # 確認
    assign = lambda x: None if x is None else x.group()
    optimize_data = assign(re.search('\*+\s*optimize\s*\*+[\s\S]+$', data))
    if optimize_data is None:
        print("初期化されていません。", file=sys.stderr)
        sys.exit(1)

    # time1, time2 の取得
    time1 = float(get_value(optimize_data, "EndTimeOfBiasRise"))
    time2 = float(get_value(optimize_data, "StartTimeOfPulseInput"))
    
    # optimize の記述の削除したものの取得
    sim_data = re.sub('\*+\s*optimize\s*\*+[\s\S]+$','', data)

    # squids_list の取得
    squids_list = get_judge_spuid(data)

    # 変数リストの取得
    variable_list = get_variable(data)

    return {'time1': time1, 'time2': time2, 'input': sim_data, 'squids': squids_list, 'variables': variable_list}

if __name__ == "__main__":
    with open("/workspaces/docker-josim/files/hfqdff_lisan.inp",'r') as f:
        raw = f.read()
    get_variable(raw)