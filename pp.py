import os
t=int(input())
cwd = os.getcwd()
d:str = os.path.join(cwd,"mygraph.dot")
with open(d,"w")as p:
    p.write("[[[]]]")

if t ==0:
    print(d)
    os.remove(d)
else:
    print("yeash")