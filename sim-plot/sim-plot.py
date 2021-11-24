# from typing import List
# matplotlib.use('TkAgg')
from typing import List
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import subprocess
from subprocess import PIPE
import io



def main(args : List):
    if len(args) == 2:
        filepath = args[1]
        if os.path.exists(filepath):
            df = pd.read_csv(filepath,index_col=0)
            print(df)
            df.plot()
            plt.show()
        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
    else:
        print("引数が足りません。\n入力された引数:"+str(len(args)))

def cut_josim_data(raw : str) -> str:
    first_split = raw.split('100% Formatting Output')

    if len(first_split) == 2:
        return first_split[1]
    else:
        print("\033[31m[ERROR] シュミレーションされませんでした。\033[0m")
        sys.exit()

def simulation(filepath : str) -> pd.DataFrame:

    result = subprocess.run(["josim-cli", filepath, "-V", "1"], stdout=PIPE, stderr=PIPE, text=True)
    print(result.stderr)
    split_data = cut_josim_data(result.stdout)
    return pd.read_csv(io.StringIO(split_data),index_col=0,header=0)

    
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        if os.path.exists(filepath):
            df = simulation(filepath)
            print(df)
            df.plot()
            plt.show()
        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv)))