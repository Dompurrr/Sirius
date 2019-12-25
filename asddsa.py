xman,yman,zman = 'X0','Y0','Z0'
min = 99999999999999
f = open('qwe.txt')
data = f.read().split('\n')
for i in range(len(data)):
    data[i] = data[i].split()
data.sort(key = lambda i: i[0])

for i in range(len(data)):
    if (int(data[i][1][1:]) < int(min)):
        min = data[i][1][1:]
print(min)

for i in range(len(data)):
    xman = data[i][0]
    print(xman,yman,zman)
    zman = data[i][2]
    print(xman,yman,zman)
    yman = data[i][1]
    print(xman,yman,zman)
    yman = 'Y' + str(min)
    print(xman,yman,zman,'\n')

tomato_massive = [[X,Y,Z], ]
gcode = generate_gcode(position, tomato_massive)
