###########################################################################
# This version uses the header from .inf and unites it with  the
# other .txt files. Each .txt has it own .csv file 
###########################################################################

import re 
import csv
import math
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt

var = type('test', (), {})()       # create and empty OBJECT that will storage the variables by the endsim
n_col = 11

INF_path = "C:\Users\Luis Arthur\Desktop\Controle_macro\\00_Example 1\Example_1.1.gf42\Channels.inf"
# INF_path = "C:\Users\Luis Arthur\Desktop\Controle_macro\\01 - Inversores\\v_dq_pll.gf42\\noname.inf"

# print INF_path

with open(INF_path) as myfile:   # Open all the lines in the inf path
    lines = myfile.readlines()


############################################################################
# Take the header of the values
############################################################################

n_var = len(lines)                      # Number of PSCAD Variables
n_files = int(math.ceil(n_var/10.0))    # Number of .out Files exported (the floating is important)
n_var_tot = n_var + n_files             # Number of variables including additional time column

# print n_files


pattern = "Desc=\"(.*?)\""  # Patter that holds the variable name
header = [0]*(n_var_tot)    # create a LIST of zeros that will be filled with the variables names later


 
a = 0 # used in the main loop
b = 0 # to "freeze" the time when storing the "TIME'"
c = 1 # used in the index: from 1 to 11

# For Logic: each file can take 11 variables, and the first one is TIME

for a in range(0, n_var_tot):

    if (a==0) or (a % n_col == 0):
        header[a] = 'var.time'
        b = b - 1
        if a != 0:
            c = 1
    else:     
        header[a] = 'var.'+ re.search(pattern, lines[b]).group(1)   # gets the name of the variable from the line
        header[a] =  header[a].replace(" ","_")                   # If the header has spaces, it will be replaced
 
    # print a,c, header[a]     # USE "a+1" for range 1 to numb_variables, "c" for range 1 to 11
    b = b + 1
    c = c + 1




############################################################################
# Take all the paths of the .out files
############################################################################

# Create the path of each file so you can open it and read the values
# it takes off the ending .inf and replace it with "_0NUMBER".out
file_name = [0]*n_files
OUT_path =  [0]*n_files
CSV_path  = [0]*n_files

for ii in range(0, n_files):
    file_name[ii] = "_0" + str(ii+1) +".out"                # Creat ending "_0ii".out
    OUT_path[ii] = INF_path.replace(".inf",file_name[ii])   # replace in INF_path the.inf for the new end

    CSV_path[ii] = "_0" + str(ii+1) +".csv"
    CSV_path[ii] = INF_path.replace(".inf",CSV_path[ii])
    # print CSV_path[ii]



############################################################################
# SAVE header and Variables in different .CSV files
############################################################################

# a = 0

# for ii in range(0,n_files):

#     df = pd.read_fwf(OUT_path[ii])
#     df.to_csv(CSV_path[ii],header=header[a:(a+n_col)],index=False)

#     a = a + n_col


############################################################################
# READ all the variables and save it in a object
############################################################################

with open(CSV_path[n_files-1],'r') as csv_file:     # from the last read csv file: gets the number of lines
    len_csv = len(csv_file.readlines())-1           # that each variables has and take of the header


storage = [[] for x in range(n_var_tot)]

last_row = [0]*n_files
last_row_v = int(round(((n_var_tot/float(n_col)) % 1)*n_col))

for ii in range(0,n_files):     # gets the number of columns of every file which will be

    if ii != n_files-1:         # all of them 11, but the last, which value can vary
        b = n_col
    else:
        b = last_row_v

    last_row[ii] = b


column  = [0]*(len_csv+1)


kk = 0
nn = 0

for jj in range(0,n_files):                                  # FOR the number of CSV Files
    print 'storing variables from file {} in the object called var '.format(jj+1)

    for ii in range(0,last_row[jj]):                         # FOR the number of COLUMNS of each csv
        # print ('column {} from file {}'.format(ii,jj+1))
        # print 'column {}'.format(ii)  
        with open(CSV_path[jj],'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            next(csv_reader)                                 # Skips the header

            for line in csv_reader:
                column = line[ii]                             # By default csv reads as strings
                storage[ii+kk].append(float(column))          # Converts to float and storages it
                # print line[ii]
        # print storage[ii+kk] 
        exec("%s = %s" % (header[nn],storage[ii+kk]))
        nn = nn + 1

    kk =  kk + n_col   



############################################################################
# PLOT variables
############################################################################

a = 1


# plt.plot(var.time,var.wrm)
# plt.title("Variable Plot")
# plt.xlabel("time")
# plt.ylabel("wrm")
# plt.show()


plt.plot(var.time,var.T_tur_pu)
plt.title("Variable Plot")
# plt.xlabel("time")
# plt.ylabel("wrm")
plt.show()

# plt.plot(var.time,var.beta,var.time,var.beta_atual,var.time,var.beta_ref)
# plt.show()


aaaa = 1

