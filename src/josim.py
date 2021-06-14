import subprocess

result = subprocess.check_output( ["josim-cli", "si_inp/si10ps.inp","-V", "1"] )

print(type(result))

f = open('myfile.txt', 'w')
f.writelines(result.decode())
f.close()