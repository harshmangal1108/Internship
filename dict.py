dt = {
    'dd':"1",
    "rccb" : "1"
}
print(dt['dd'])
del dt['dd']
print(dt)
##3 d.items()
d = {'a': 10, 'b': 20, 'c': 30}
list(d.items())
list(d.items())[1][0]
list(d.items())[1][1]
for j in d.values():
    print(j)

z={**dt,**d}
print(z)
