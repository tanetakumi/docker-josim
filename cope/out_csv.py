import subprocess
import pandas as pd
import io
import os
import sys
import matplotlib.pyplot as plt
import judge


def main():
    # For reading dataframe, result replace ioString.
    df = pd.read_table("JTL.csv",index_col=0,sep=' ')
    print(df)
    df.plot()
    plt.show()




if __name__ == '__main__':
    main()
    
    
