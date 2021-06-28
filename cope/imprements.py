import subprocess
from subprocess import PIPE
import os
import sys


def simulation(filepath) -> str:
    # simulate josim and get the result 
    # the result type is buffer
    # result = subprocess.check_output(["pjsim_n",filepath])
    # result = subprocess.check_output(["pjsim_n", filepath])
    result = subprocess.run(["pjsim_n", filepath], stdout=PIPE, stderr=PIPE, text=True)
    # print(type(result.stdout))
    return result.stdout
    # result = subprocess.call(["pjsim_n", filepath])
    # result = subprocess.check_output("pjsim_n "+filepath,shell=True)
    # decode the result and split result into progress and simulation result. 
    # print(result.decode())
    # return result.decode()
    # if the file doesn't exists

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        curdir = os.getcwd()
        path = curdir+"/"+args[1]
        # if the file exists
        if os.path.exists(path):
            simulation(path)
        else:
            print("ファイルが存在しません。\n指定されたパス:"+path)
            sys.exit()
    else:
        print("引数が足りません。\n入力された引数:"+str(len(sys.argv)))
        sys.exit()
    
    
    
    

