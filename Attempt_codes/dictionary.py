###########################################################################
# Libraries and packages
###########################################################################
import os
import re
import csv
import math
import pandas as pd
import numpy as np
from collections import defaultdict  


###########################################################################
# Definition of class
###########################################################################

class GetVariables2(object):
    def __init__(self, INF_path, **kwargs):

        # Default definitions of arguments:
        # It WILL NOT CREATE a CSV file

        try:
            kwargs['writecsv']
        except KeyError:
            kwargs['writecsv'] = False


        # To avoid problems including backslashs, include 'r' before the path

        with open(INF_path) as myfile:  # Open all the lines in the inf path
            lines = myfile.readlines()

        ############################################################################
        # Take the header of the values
        ############################################################################
        n_col = 11                                 # Number of columns that the txt has
        n_var = len(lines)                         # Number of PSCAD Variables
        n_files = int(math.ceil(n_var / 10.0))     # Number of .out Files exported (the floating is important)
        n_var_tot = n_var + n_files                # Number of variables including additional time column
        n_var_last = n_var_tot -(n_files-1)*n_col  # Number of variables in the last file
        # print n_files

        pattern = "Desc=\"(.*?)\""  # Patter that holds the variable name
        header1 = [0] * (n_var_tot)  # create a LIST of zeros that will be filled with the variables names later
        self.header  = [0] * (n_var_tot)  

        b = 0  # to "freeze" the time when storing the "TIME"
        c = 1  # used in the index: from 1 to 11

        # "For" Logic: each file can take 11 variables, and the first one is TIME
        # so this for writes time if it is the time column, or takes the header from
        # the array "header"

        for a in range(0, n_var_tot):

            if (a == 0) or (a % n_col == 0):
                header1[a] = 'self.time'         # 1 header has the 'self.' in order to create variables to send
                self.header[a] = 'time'          # to the object outside
                b = b - 1
                if a != 0:
                    c = 1
            else:
                header1[a] = 'self.' + re.search(pattern, lines[b]).group(1)  # gets the name of the variable from the line
                header1[a] = header1[a].replace(" ", "_")  # If the header has spaces, it will be replaced
                self.header[a] = re.search(pattern, lines[b]).group(1)  
                self.header[a] = self.header[a].replace(" ", "_")  

            # exec("{} = np.array({})".format(header1[a],[]))

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



        if (kwargs['writecsv'] == True):  # if the user wants to save, save the .CSV file

            a = 0

            for ii in range(0,n_files):

                df = pd.read_fwf(OUT_path[ii])                                         # Read the .OUT file and
                # df.to_csv(CSV_path[ii],header=self.header[a:(a+n_col)],index=False)  # Create the .CSV with my header and without index as first row
                df.to_csv(CSV_path[ii],header=None, index=False,float_format=)
                print 'creating file {}'.format(CSV_name[ii])
                a = a + n_col
        

        ############################################################################
        # READ variables from .txt 
        # SAVE those variables in the self.(header)
        ############################################################################

        aaa = 1

        # Gets the number of columns of every file which will be
        # all of them 11, but the last, which value can vary

        last_row = [0]*n_files

        for ii in range(0,n_files):     

            if ii != n_files-1:         
                b = n_col
            else:
                b = n_var_last

            last_row[ii] = b

        nn = 0           # for iterating every column of the data_file
        data_file = []   # storage the data from the CSV files
        self.dic = dict()


        for ii in range(0,n_files):

            with open(CSV_path[ii]) as out_file:
                data_file = np.loadtxt(out_file, delimiter=',')


            for jj in range(0,last_row[ii]):
                self.dic.update({self.header[jj+nn]:data_file[:,jj]})
                
                
        
            nn = nn + 11
            



        aaa = 1