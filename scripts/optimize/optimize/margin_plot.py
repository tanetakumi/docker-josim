import matplotlib.pyplot as plt
import pandas as pd

def diclist_to_dataframe(margins : list, filename = None):
    df = pd.DataFrame(margins)
    df.set_index('char', inplace=True)
    print(df)
    # margin_plot(df,filename)
        

def margin_plot(df : pd.DataFrame, filename = None):
    df.sort_index(inplace=True)
    plt.rcParams["font.size"] = 15

    plot_color = '#01b8aa'
    index = df.index
    column0 = df['lower']
    column1 = df['upper']

    fig, axes = plt.subplots(figsize=(10,5), facecolor="White", ncols=2, sharey=True)
    fig.tight_layout()
    
    axes[0].barh(index, column0, align='center', color=plot_color)
    axes[0].set_xlim(-100, 0)
    axes[1].barh(index, column1, align='center', color=plot_color)
    axes[1].set_xlim(0, 100)
    axes[1].tick_params(axis='y', colors=plot_color)

    plt.subplots_adjust(wspace=0, top=0.85, bottom=0.1, left=0.18, right=0.95)
    # 
    if filename == None:
        plt.show()
    else:
        fig.savefig(filename)
    

if __name__ == "__main__":
    class_list = ['test1','test2','test3','test4','test5','test6','test7']
    average_length = [-13,-52,-36,-42,-25,-16,-7]
    num_entries = [11,23,243,16,5,131,8]
    data = pd.DataFrame(data=zip(class_list,average_length,num_entries),columns=['index','lower','upper'])
    data.set_index('index', inplace=True)
    data[data > 100] = 100
    print(data)
    # margin_plot(data)