###########################################################################
# Libraries and packages
###########################################################################
import os
import re
import math
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import scipy.io as sio 
import DyMat 


###########################################################################
# Definition of class for OMEDit
###########################################################################

class OMEditVar1(object):
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


        try:                                 # if the kwarg exist, create a variable called x_func
           kwargs['interp']
           self.time = kwargs['interp']
        except KeyError:                     # if it doesn't exist:
            kwargs['interp'] = 0

        d = DyMat.DyMatFile(CSV_path)

        n_var = len(d.names())
        header = [0]*n_var

        vec = []

        for a in range(0,n_var):
            header[a] = "self." + d.names()[a].replace(".","_")
            header[a] = header[a].replace("(","_")
            header[a] = header[a].replace(")","_")
            
            if type(kwargs['interp']) is not int: # Means it is a vector

                f_lin = interp1d(d.abscissa(d.names()[a])[0], d.data(d.names()[a]))
                vec = f_lin(self.time)
                exec('%s = np.array(%s)' % (header[a],'vec'))


            else:    
                exec('%s = np.array(%s)' % (header[a],'d.data(d.names()[a])'))

        a = 1