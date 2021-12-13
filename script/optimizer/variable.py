import re
import util


# 先頭の文字列、Line
def get_variable(text : str) -> list:
    line_list = filter(lambda x: re.search('#\(.+\)', x), text.splitlines())
    return_list = []
    for l in line_list:
        first_char = re.search('^[^\s]+',l).group()
        def_val = re.sub('#|\(|\)', '', re.search('#\(.+\)', l).group())
        return_list.append((l,first_char,util.stringToNum(def_val)))
    return return_list


# 先頭の文字列、Line
def get_v(text : str) -> list:
    vlist = []
    for l in re.findall('#.+\(.+\)', text):
        a = re.split('\(', re.sub('#|\)','',l) )
        vlist.append({'char': a[0], 'text': l, 'def': util.stringToNum(a[1])})
    print(vlist[0]['char'])    
    return vlist
        
    
if __name__ == "__main__":
    with open("/workspaces/docker-josim/test_netlist_file/piJTL.inp",'r') as f:
        raw = f.read()
    # get_v(raw)
    print(str(50/7))