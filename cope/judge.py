import pandas as pd

def judge_frame(df : pd.DataFrame) -> pd.DataFrame:
    df_diff = df.diff()
    df_diff.where(df_diff >= 0, other = 0, inplace = True)

    for indexs,items in df_diff.iteritems():
        length = len(items)

        # ---------------#
        # 値の連続状態
        # 開始index
        # 合計
        # ---------------#

        keep = False
        start_i = 0   
        sum = 0        

        for i in range(length):

            if keep:
                if items.iat[i] == 0:
                    max_tmp = 0
                    max_index = 0
                    for j in range(start_i,i-1):
                        if sum >2:

                            
                            if max_tmp < items.iat[j]:
                                items.iat[max_index] = 0

                                max_index = j
                                max_tmp = items.iat[j]
                                
                                items.iat[j] = sum
                                
                            else:
                                items.iat[j] = 0
                        else:
                            items.iat[j] = 0
                        
                    sum = 0
                    keep = False
                
                else:
                    sum += items.iat[i]
            
            else:
                if items.iat[i] != 0:
                    keep = True
                    start_i = i
                    sum += items.iat[i]
    return df_diff