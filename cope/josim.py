import subprocess
import pandas as pd
import io
import os
import sys
import matplotlib.pyplot as plt
import judge

def simulation(args) -> pd.DataFrame:
    # カレントディレクトリの取得
    curdir = os.getcwd()
    if len(args) == 2:
        # filepath 
        filepath = curdir+"/"+args[1]
        # if the file exists
        if os.path.exists(filepath):
            # simulate josim and get the result 
            # the result type is buffer
            result = subprocess.check_output( ["josim-cli", filepath,"-V", "1"] )
            # decode the result and split result into progress and simulation result. 
            res_string = result.decode().split('100% Formatting Output')
            # For reading dataframe, result replace ioString.
            return pd.read_csv(io.StringIO(res_string[1]),index_col=0,header=0)

        # if the file doesn't exists
        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
            sys.exit()
    else:
        print("引数が足りません。\n入力された引数:"+str(len(args)))
        sys.exit()


if __name__ == '__main__':
    df = simulation(sys.argv)
    dfj = judge.judge_frame(df)
    df.plot()
    dfj.plot()
    plt.show()
    
    



