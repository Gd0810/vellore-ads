txt = input('enter string :')


res = ''

repeated = []

for i in range(0,len(txt)):
    if txt[i] in res:
        repeated.append(txt[i])
    else:
        res = res + txt[i]


print(set(repeated))



