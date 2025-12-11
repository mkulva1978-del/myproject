experimentaldata = [1, 2, 3, 4, 5]
danger = []
crit = float(input())
st1 = float(input())
st2 = float(input())
for i in range (len(experimentaldata)):
    if experimentaldata[i] < crit:
        danger[i]=0
    if experimentaldata[i] > crit and experimentaldata[i] < crit + st1:
        danger[i]=1
    if experimentaldata[i] > crit+st1 and experimentaldata[i] < crit + st2:
        danger[i]=2


