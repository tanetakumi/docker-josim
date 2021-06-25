import subprocess
import pandas as pd
import io
import sys
import matplotlib.pyplot as plt
import imprements


def jsim_output_text(data : str) -> pd.DataFrame:
    # For reading dataframe, result replace ioString.
    df = pd.read_table(io.StringIO(data),index_col=0,header=None,sep=' ')
    df.drop(len(df.columns) ,axis=1, inplace=True)
    return df
    # df.plot()
    # plt.show()

def cut_data(raw : str) -> str:
    first_split = raw.split('.END')

    if len(first_split) > 1:
        # print(first_split[len(first_split)-1])
        second_split = first_split[len(first_split)-1].split('loop count')

        if len(second_split) >1:
            return second_split[0]
        else:
            print("ERROR1")
            sys.exit
    else:
        print("ERROR2")
        sys.exit



if __name__ == '__main__':
    raw_data = imprements.simulation("jtlsfqhfq0515.inp")
    # print(raw_data)
    jsim_output_text(cut_data(raw_data))
    
    
