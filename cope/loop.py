import imprements
import readjsim
import judge
import matplotlib.pyplot as plt
import pandas as pd




if __name__ == '__main__':
    raw_data = imprements.simulation("dchfq.inp")
    df = readjsim.jsim_output_text(readjsim.cut_data(raw_data))
    df[4]=df[1]+df[2]
    # dfj = judge.judge_frame(df)
    df.plot()
    # dfj.plot()
    plt.show()
    
