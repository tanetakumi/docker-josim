import subprocess
import pandas as pd
import io

result = subprocess.check_output( ["josim-cli", "si_inp/si10ps.inp","-V", "1"] )

res_string = result.decode().split('100% Formatting Output')
# print(res_string[1])

"""
if len(res_string) == 2:
    print(res_string[1])
"""

df = pd.read_csv(io.StringIO(res_string[1]),index_col=0,header=0)

print(df.columns)



# print("Hello")

"""


for l in result.decode().split('\n'):
    if '100% Formatting Output' in l:
        print(l)


f = open('myfile.txt','w')
f.writelines(result.decode())
# print(type(f.read()))
f.close()
"""