###########################################################################
# Libraries and packages
###########################################################################
import os
import re
import math
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import DyMat 


###########################################################################
# Definition of class for OMEDit
###########################################################################

class OMEditVar(object):
    """ Documentation: This class reads the .csv file exported by OMEDit and storages all the variables in it contained
        
        CSV_path:   str, mandatory. 
        It's the path of the .csv file
        
        interp:     nparray, optional. 
        If you want to interpolate the variables with another time array. Otherwise, the original variables will be storaged
        
        replaceDot: bool, optional. 
        If it's true, replaces the '.' with '_' from the variable name. If it's False,
        it removes everything that's before the last dot in it. 

    
        """

    def __init__(self,CSV_path,**kwargs):

        # Default:
        #   It WILL NOT interpolate the data according to another "step"
        #   It WILL replace the . with _ in the variables names

        try:                                 # if the kwarg exist, create a variable called x_func
           kwargs['interp']
           x_func    = kwargs['interp']
           self.time = kwargs['interp']
        except KeyError:                     # if it doesn't exist:
            kwargs['interp'] = 0

        try:                                 
           kwargs['replaceDot']
        except KeyError:                     
            kwargs['replaceDot'] = True


        if ".csv" in CSV_path:                   # User enters with an CSV file
            df = pd.read_csv(CSV_path)           # Read the .OUT file and storage it in a pandas data frame

            header = df.columns                  # Header that will be modified to create object variables
            header_orig = df.columns             # Original header, just like it is in modelica
            n_var = len(df.columns)              # Number of variables

            aa = ""                              # Add "nothing" to the variables' names and
            header = [aa + s for s in header]    # Now it is a list of strings

            count = [0]*n_var                    # Storage the number of . in a variable's name

            for ii in range(0,n_var):
                if kwargs['replaceDot'] == True:      # replaces . with _
                    for jj in header[ii]:
                            if jj == ".":
                                header[ii] = header[ii].replace(".","_")
                            elif jj == ")":
                                header[ii] = header[ii].replace(")","_")
                            elif jj == "(":
                                header[ii] = header[ii].replace("(","_")
                else:
                    for jj in header[ii]:
                        if jj == ".":
                            count[ii] = count[ii] + 1
                        elif jj == ")":
                            header[ii] = header[ii].replace(")","_")
                        elif jj == "(":
                            header[ii] = header[ii].replace("(","_")                        
                    for kk in range(0,count[ii]):            
                        header[ii] = re.sub(r'^.*?\.',"",header[ii])   # Takes everything before the . and replace with nothing


            h_str = "self."                             # Add "nothing" to the variables names and
            header = [h_str + s for s in header]        # now it is a list of strings


            ############################################################################
            # Interpolate OMEDit Variables with the PSCAD Time variable, if its the case
            # and then storage it in a variable with its name
            ############################################################################

            if type(kwargs['interp']) is not int: # Means the kwarg is a vector 
                df1 = pd.DataFrame()    # A X sized DataFrame can't receive a Y sized df, so a new one is created

                for ii in range(0,n_var):
                    if ii == 0:
                        df1[header_orig[ii]] = x_func
                    else:
                        f_lin = interp1d(df[header_orig[0]], df[header_orig[ii]]) # x = OMEdit time, y = the variable
                        df1[header_orig[ii]] = f_lin(x_func)

                    exec('%s = np.array(%s)' % (header[ii],'df1[header_orig[ii]]'))
            else:
                for ii in range(0,n_var):
                    exec('%s = np.array(%s)' % (header[ii],'df[header_orig[ii]]'))

        else:                                 # If user enters with a .MAT file

            d = DyMat.DyMatFile(CSV_path)

            n_var = len(d.names())
            header = [0]*n_var

            vec = []

            header_lst = list(d.names())

            for a in range(0,n_var):
                header[a] = "self." + header_lst[a].replace(".","_")
                header[a] = header[a].replace("(","_")
                header[a] = header[a].replace(")","_")
                
                if type(kwargs['interp']) is not int:           # Means it is an interpolation vector

                    f_lin = interp1d(d.abscissa(header_lst[a])[0], d.data(header_lst[a]))
                    vec = f_lin(self.time)
                    exec('%s = np.array(%s)' % (header[a],'vec'))


                else:    
                    exec('%s = np.array(%s)' % (header[a],'d.data(header_lst[a])'))
        



############################################################################
############################################################################
############################################################################
##
##                        PSCAD Class ahead
##
############################################################################
############################################################################
############################################################################

            


###########################################################################
# Definition of class
###########################################################################

class PSCADVar(object):
    """ Documentation: 
        This class reads the .out files and returns all of the variables in it contained, as well as the header of the variables, time step and number of variables imported.

        INF_path: str, mandatory. 
        It's the path of the .inf file

        writecsv: bool, optional. 
        Creates a new .CSV file with the .OUT variables
        
        delout:   bool, optional. 
        Deletes the .OUT files once they were already read
        
       """

    def __init__(self, INF_path, **kwargs):
        
        # Default definitions of arguments:
        # It WILL create a CSV file
        # It WILL NOT delete the .OUT files

        try:
            kwargs['writecsv']
        except KeyError:
            kwargs['writecsv'] = True

        try:
            kwargs['delout']
        except KeyError:
            kwargs['delout'] = False
   

        with open(INF_path) as myfile:  # Open all the lines in the inf path
            lines = myfile.readlines()


        ############################################################################
        # Take the header of the values
        ############################################################################

        n_col = 11                                 # Number of columns that the txt has
        n_var = len(lines)                         # Number of PSCAD Variables
        n_files = int(math.ceil(n_var / 10.0))     # Number of .out Files exported (the floating is important)
        n_var_tot = n_var + n_files                # Number of variables INCLUDING additional time column FOR EACH .OUT
        n_var_last = n_var_tot -(n_files-1)*n_col  # Number of variables in the last file
        n_var_exp = n_var + 1                      # Number of variables that will be exported 

        self.number_var = n_var_exp                

        # This "for" gets the number of columns of every file which will be all 11,
        # but the last, which value can vary

        last_col = [0]*n_files

        for ii in range(0,n_files):     

            if ii != n_files-1:         
                b = n_col
            else:
                b = n_var_last

            last_col[ii] = b

        # last_col = [11, 11, 11, 1]

        pattern = "Desc=\"(.*?)\""  # Patter that holds the variable name
        header1 = [0] * (n_var_exp)  # create a LIST of zeros that will be filled with the variables names later
        self.header  = [0] * (n_var_exp)  

        b = 0  # to "freeze" the time when storing the "TIME"
        c = 1  # used in the index: from 1 to 11

        # "For" Logic: each file can take 11 variables, and the first one is TIME
        # so this for writes time if it is the time column, or takes the header from
        # the array "header"

        for a in range(0, n_var_exp):

            if  a == 0 :                    # if it is the first value of all files, storage the time name
                header1[a] = 'self.time'    # 1 header has the 'self.' in order to create variables to send
                self.header[a] = 'time'     # to the object outside
                b = b - 1
                if a != 0:
                    c = 1
            else:
                header1[a] = 'self.' + re.search(pattern, lines[b]).group(1)  # gets the name of the variable from the line
                header1[a] = header1[a].replace(" ", "_")                     # If the header has spaces, it will be replaced
                self.header[a] = re.search(pattern, lines[b]).group(1)  
                self.header[a] = self.header[a].replace(" ", "_")  
            # print a, self.header[a]     # USE "a+1" for range 1 to numb_variables, "c" for range 1 to 11

            
            b = b + 1
            c = c + 1

        ############################################################################
        # Take all the paths of the .out files
        ############################################################################

        # Create the path of each file so you can open it and read the values
        # The "for" takes off the ending .inf and replace it with "_0NUMBER".out
        
        OUT_name  = [0] * n_files
        OUT_path  = [0] * n_files

        for ii in range(0, n_files):
            if ii < 9:
                OUT_name[ii] = "_0" + str(ii + 1) + ".out"             # Create ending "_0ii".out
                OUT_path[ii] = INF_path.replace(".inf", OUT_name[ii])  # replace in INF_path the.inf for the new end
            else:
                
                OUT_name[ii] = "_" + str(ii + 1) + ".out"             # Create ending "_0ii".out
                OUT_path[ii] = INF_path.replace(".inf", OUT_name[ii])  # replace in INF_path the.inf for the new end


            # print CSV_path[ii]

        # Creates the path of the .CSV that's gonna be writen
        CSV_path = INF_path.replace(".inf", ".csv") # Replaces the ending .inf with .csv

        ############################################################################
        # SAVE header and Variables in one .CSV file
        ############################################################################

        df_csv = pd.DataFrame()    # Create an empty pandas dataframe that will storage all the data from the .outs

        c  = 0    # freezes the header if you skip time
        jj = 0

        for ii in range(0,n_files):  # For each file, read it and storage its columns in the .CSV file

            df = pd.read_csv(OUT_path[ii], delim_whitespace=True, header=None)    # Read the .OUT file and storage it in a pandas data frame
            
            if (jj == 0) or (jj % 11 == 0):                # if it is a multiple of 11, means that it's another file
                jj = 0                                     # so you reset the counter 

            while jj < last_col[ii]:                       # While you are inside the file, save values

                if (jj == 0) and (ii == 0):                # It is the first column of the first file: storage time
                    df_csv[self.header[c]] = df[jj]
                elif (jj == 0) and (ii != 0):              # It is the first column of some other file: don't storage time
                    jj = jj + 1
                    df_csv[self.header[c]] = df[jj]
                    # print 'just skipped time'
                else:
                    df_csv[self.header[c]] = df[jj]        # It is other column: storage column
                
                exec('%s = np.array(%s)' % (header1[c],'df[jj]'))
                # print df_csv.head()
                
                # print c
                c = c + 1
                jj = jj + 1


            if kwargs['delout'] == True:                 # If user wants to delete the .OUT files:
                os.remove(OUT_path[ii])

        ############################################################################
        # Gets the step of simulation - PSCAD
        ############################################################################

        self.step = self.time[1] - self.time[0]

              
        ############################################################################
        # Storage data in a.CSV file with all the variables
        ############################################################################
      
        if (kwargs['writecsv'] == True): 
            
            df_csv.to_csv(CSV_path,index=False)          # Storage all the dataframe into one csv file with header




