'''
Created on Nov 5 2022

@author:lnhang

'''


import sys

sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np
from Generate_Data import Generate_Data
from Solver import Solver

from Objfn import Objfn
from Optimization import Optimization
from Prior import Prior

C_m_type = "scalar"