import subprocess
import pandas as pd
import io
import matplotlib.pyplot as plt
import imprements


def jsim_output_text(data : str) -> pd.DataFrame:
    # For reading dataframe, result replace ioString.
    df = pd.read_table(io.StringIO(data),index_col=0,sep=' ')
    df.plot()
    plt.show()

def cut_data(raw : str) -> str:
    print("Hello")




if __name__ == '__main__':
    imprements.simulation("jtlsfqhfq0515.inp")
    
    
