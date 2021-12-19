from subprocess import PIPE
import subprocess
import pandas as pd
import io
import re
import sys

def check_lastline(data : str) -> str:
    return re.sub('\n*$','\n.end',data) if re.search('\.end\s*$', data) is None else data


def simulation(simulation_data : str) -> pd.DataFrame:
    simulation_data = check_lastline(simulation_data)
    result = subprocess.run(["josim-cli", "-i"], input=simulation_data, stdout=PIPE, stderr=PIPE, text=True)

    first_split = re.split('100%\s*Formatting\s*Output',result.stdout)
    if len(first_split) == 2:
        split_data = first_split[1]
    else:
        print("--- standard error ---")
        print("\033[31m" + result.stderr + "\033[0m")
        sys.exit()

    return pd.read_csv(io.StringIO(split_data),index_col=0,header=0, sep='\s+') if split_data is not None else None


if __name__ == "__main__":
    with open("/workspaces/docker-josim/test_netlist_file/backup.txt",'r') as f:
        raw = f.read()
    print(raw)
    print(simulation(raw))