import os

file_name = "dchfq.inp"

with open(file_name) as f:
    data_lines = f.read()

print(type(data_lines))

# 文字列置換
data_lines = data_lines.replace("#(v)", "4.3").replace("#(L)", "40")
print(data_lines)

# 同じファイル名で保存
with open("test.inp", mode="w") as f:
    f.write(data_lines)

os.remove('test.inp')