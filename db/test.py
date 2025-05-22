f=open("./db/barangay.txt",'r',encoding="utf8")
for i in f.readlines():
    print(i)
f.close()