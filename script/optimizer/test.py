import re 


def test(text : str):
    if re.match('.+b',text) is not None:
        print("match")
    else:
        print("not match")



if __name__ == "__main__":
    test("fdfsdfb") 

    test("dfsfsdf")  