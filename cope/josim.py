import subprocess
import pandas as pd
import io
import os
import sys
import matplotlib.pyplot as plt

def simulation(args) -> pd.DataFrame:
    curdir = os.path.dirname(os.path.abspath(__file__))

    if len(args) == 2:
        print(curdir)
        filepath = curdir+"/"+args[1]
        if os.path.exists(filepath):
            # df = pd.read_csv(filepath,index_col=0)
            result = subprocess.check_output( ["josim-cli", filepath,"-V", "1"] )
            res_string = result.decode().split('100% Formatting Output')
            return pd.read_csv(io.StringIO(res_string[1]),index_col=0,header=0)
        else:
            print("ファイルが存在しません。\n指定されたパス:"+filepath)
    else:
        print("引数が足りません。\n入力された引数:"+str(len(args)))


if __name__ == '__main__':
    df = simulation(sys.argv)
    
    df.plot()
    plt.show()
    



