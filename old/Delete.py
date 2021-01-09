max=9


files = open('.\\test.txt','r+')
l4 = files.readlines()

l4[9]=''
if(9==max):
    l4[9-1]=l4[9-1][0:-1]

files.close()
files = open('.\\test.txt','w+')
l4 = files.writelines(l4)

files.close()