from time import sleep


i = 0

while True:
    pat = 'int : {0:<10} bin : {0:<18b} oct : {0:<10o} hex :{0:<10x}'.format(i)
    print(pat)
    sleep(.1)
    i += 1
