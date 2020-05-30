x = 0
x_m = 0
x_m1 = 0

fin = open("apagar - Copia.infx", "r+")
data = fin.read()

for x in  range(30):
    x_n = x + 2
    y = str(x)
    y_n = str(x_n)

    if x<10: 
        ind = 'index='
        asp = '"'

        a = '<channel ' + ind + asp + y + asp
        b = ind +' '+ y_n

        # fin = open("apagar - Copia.infx", "rt")
        # data = fin.read()
        data = data.replace(a, b)
        fin.close() 


        fin = open("apagar - Copia.infx", "wt")
        fin.write(data)
        fin.close()

    elif x >= 10 and x < 20:
        x_n = x_m + 2
        y_n = str(x_n)

        a = '<channel ' + ind + asp + y + asp
        b = ind +' '+ y_n

        # fin = open("apagar - Copia.infx", "rt")
        # data = fin.read()
        data = data.replace(a, b)
        fin.close() 


        fin = open("apagar - Copia.infx", "wt")
        fin.write(data)
        fin.close()

        x_m = x_m + 1

    elif x >= 20:
        x_n = x_m1 + 2
        y_n = str(x_n)

        a = '<channel ' + ind + asp + y + asp
        b = ind +' '+ y_n

        #fin = open("apagar - Copia.infx", "rt")
        #data = fin.read()
        data = data.replace(a, b)
        fin.close() 


        fin = open("apagar - Copia.infx", "wt")
        fin.write(data)
        fin.close()

        x_m1 = x_m1 + 1    

    