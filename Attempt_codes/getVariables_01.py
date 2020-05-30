###########################################################################
# Libraries and packages
###########################################################################
import os
import re 
import csv
import math
import pandas as pd
import numpy as np

###########################################################################
# Definition of class
###########################################################################

class GetVariables3(object):
    def __init__(self, INF_path,**kwargs):

        # Default definitions of arguments:
        # It WILL CREATE a CSV file
        # It WILL NOT erase the CSV file after running

        try:
            kwargs['writecsv']
        except KeyError:
            kwargs['writecsv'] = True

        try:
            kwargs['deletecsv']
        except KeyError:
            kwargs['deletecsv'] = False


        # To avoid problems including backslashs, include 'r' before the path

        with open(INF_path) as myfile:   # Open all the lines in the inf path
            lines = myfile.readlines()


        ############################################################################
        # Take the header of the values
        ############################################################################
        n_col = 11                                 # Number of columns that the txt has
        n_var = len(lines)                         # Number of PSCAD Variables
        n_files = int(math.ceil(n_var/10.0))       # Number of .out Files exported (the floating is important)
        n_var_tot = n_var + n_files                # Number of variables including additional time column
        n_var_last = n_var_tot -(n_files-1)*n_col  # Number of variables in the last file
        # print n_files


        pattern = "Desc=\"(.*?)\""  # Patter that holds the variable name
        self.header = [0]*(n_var_tot)    # create a LIST of zeros that will be filled with the variables names later


        b = 0  # to "freeze" the time when storing the "TIME"
        c = 1  # used in the index: from 1 to 11

        # "For" Logic: each file can take 11 variables, and the first one is TIME
        # so this for writes time if it is the time column, or takes the header from
        # the array "header"

        for a in range(0, n_var_tot):

            if (a==0) or (a % n_col == 0):
                self.header[a] = 'self.time'
                b = b - 1
                if a != 0:
                    c = 1
            else:     
                self.header[a] = 'self.'+ re.search(pattern, lines[b]).group(1)   # gets the name of the variable from the line
                self.header[a] =  self.header[a].replace(" ","_")                      # If the header has spaces, it will be replaced
        
            # print a,c, self.header[a]     # USE "a+1" for range 1 to numb_variables, "c" for range 1 to 11
            b = b + 1
            c = c + 1
    

       ############################################################################
        # Take all the paths of the .out files
        ############################################################################

        # Create the path of each file so you can open it and read the values
        # it takes off the ending .inf and replace it with "_0NUMBER".out
        
        OUT_name  = [0] * n_files
        OUT_path  = [0] * n_files
        CSV_name  = [0] * n_files
        CSV_path  = [0] * n_files

        for ii in range(0, n_files):
            OUT_name[ii] = "_0" + str(ii + 1) + ".out"             # Create ending "_0ii".out
            OUT_path[ii] = INF_path.replace(".inf", OUT_name[ii])  # replace in INF_path the.inf for the new end

            CSV_name[ii] = "_0" + str(ii + 1) + ".csv"              # Create ending "_0ii".csv
            CSV_path[ii] = INF_path.replace(".inf", CSV_name[ii])   # replace in INF_path the.inf for the new end

            # print CSV_path[ii]

        ############################################################################
        # SAVE header and Variables in different .CSV files
        ############################################################################

        check = True

        for  ii in range(0,n_files):               # Check if the CSV Files exist, if at least one don't exist
            if os.path.exists(CSV_path[ii]):       # them all are gona be created
                pass
            else: 
                check = False
            
         # If the user wants to create the CSV files or 
         # # if it doesn't exist, it has to be created, and read

        if (kwargs['writecsv'] == True) or (check == False): 
            a = 0

            for ii in range(0,n_files):

                
                
                # df = pd.read_fwf(OUT_path[ii])                                         # Read the .OUT file and
                df = pd.read_csv(OUT_path[ii],delim_whitespace=True, header=None)
                
                # df.to_csv(CSV_path[ii],header=self.header[a:(a+n_col)],index=False)  # Create the .CSV with my header and without index as first row
                df.to_csv(CSV_path[ii],header=None, index=False)
                print 'creating file {}'.format(CSV_name[ii])
                a = a + n_col


        ############################################################################
        # READ all the variables and save it in a object
        ############################################################################

        with open(CSV_path[n_files-1],'r') as csv_file:     # from the last read csv file: gets the number of lines
            # len_csv = len(csv_file.readlines())-1         # that each variables has and take of the header
            len_csv = len(csv_file.readlines())             # once theres no header anymore

        storage = [[] for x in range(n_var_tot)]

        last_row = [0]*n_files

        for ii in range(0,n_files):     # gets the number of columns of every file which will be

            if ii != n_files-1:         # all of them 11, but the last, which value can vary
                b = n_col
            else:
                b = n_var_last

            last_row[ii] = b


        column  = [0]*(len_csv+1)
        

        kk = 0
        nn = 0

        for jj in range(0,n_files):                                  # FOR the number of CSV Files
            print 'storing variables from file {}'.format(jj+1)

            for ii in range(0,last_row[jj]):                         # FOR the number of COLUMNS of each csv
                # print ('column {} from file {}'.format(ii,jj+1))
                # print 'column {}'.format(ii)  
                with open(CSV_path[jj],'r') as csv_file:
                    csv_reader = csv.reader(csv_file)

                    next(csv_reader)                          # Skips the header

                    for line in csv_reader:
                        column = line[ii]                     # By default csv reads strings
                        storage[ii+kk].append(column)       
                        # print column
                        # print line[ii]
                # print storage[ii+kk] 
                exec("%s = %s" % (self.header[nn],storage[ii+kk]))    # Storage a LIST in the variable from header
                # exec('{}=np.array({})'.format(self.header[nn],storage[ii+kk]))
                # exec('{}={}'.format(self.header[nn],np.array(storage[ii+kk]))) # erro pq tenho que entrar com uma lista, e nao um array numpy
                
                 
                nn = nn + 1

            kk =  kk + n_col   

        aaa = 0

        if (kwargs['deletecsv'] == True) and (check == True):

            for ii in range(0,n_files):
                os.remove(CSV_path[ii])
            print "files deleted"
