import imprements
import readjsim
import judge
import matplotlib.pyplot as plt
import pandas as pd
import os
from time import sleep
import csv




if __name__ == '__main__':

    raw_data = imprements.simulation('dchfq_test3.inp')
    df = readjsim.jsim_output_text(readjsim.cut_data(raw_data))

    dfj = judge.judge_frame(df)

    df.plot()
    dfj.plot()
    
    
    plt.show()