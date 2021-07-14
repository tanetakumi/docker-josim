import imprements
import readjsim
import judge
import matplotlib.pyplot as plt
import pandas as pd
import os
from time import sleep
import csv




if __name__ == '__main__':
    with open('test7.csv','w') as f:
        writer = csv.writer(f)

        for i in range(15, 50, 1):
            mv = i/10
            
            for j in range(30,60,1):

                file_name = "dchfq.inp"

                with open(file_name) as f:
                    data_lines = f.read()

                voltage = '{:.1f}'.format(mv)
                inductance = str(j)
                # 文字列置換
                data_lines = data_lines.replace("#(v)", voltage).replace("#(L)", inductance)
                #print(data_lines)

                with open("test.inp", mode="w") as f:
                    f.write(data_lines)

                raw_data = imprements.simulation('test.inp')
                os.remove('test.inp')
                df = readjsim.jsim_output_text(readjsim.cut_data(raw_data))
                df_new = pd.DataFrame(index=df.index, columns=["X1","X2","X3","X4","X5"])
                df_new["X1"]=(df[1]+df[2])*(-1)
                df_new["X2"]=(df[3]+df[4])
                df_new["X3"]=(df[5]+df[6])
                df_new["X4"]=(df[7]+df[8])
                df_new["X5"]=(df[9]+df[10])
                dfj = judge.judge_frame(df_new)
                df_bool = (dfj > 4) & ( dfj < 8)
                print(df_bool.values.sum())
                # sleep(0.1)
                if df_bool.values.sum() != 35:
                    writer.writerow([str(mv),str(j),'Blue'])
                else:
                    writer.writerow([str(mv),str(j),'Red'])
                

    """
    df_new.plot()
    dfj.plot()
    plt.title('Title',fontsize=15)
    plt.xlabel('X',fontsize=10)
    plt.ylabel('Y',fontsize=10)
    
    """
    # plt.show()