'''
Created on Nov 18

@author:lnhang

'''

import sys
sys.path.append('../src')

#from GPR2d import GPR

import numpy as np
import matplotlib.pyplot as plt
import pickle

from ML import Guassian_Process
from Solver import Solver
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, RBF

# prepared for train

#T_inf_train, T_obs_train, beta_MAP_train, std_lst = pickle.load(open('../data/ML.p','rb'))
T_inf_train, T_obs_train, beta_MAP_train, std_lst = pickle.load(open('../data/ML_const.p','rb'))

T_inf_train = np.vstack(T_inf_train).flatten()
T_obs_train = np.vstack(T_obs_train).flatten()

beta_MAP_train = np.vstack(beta_MAP_train).flatten()

x_train = np.concatenate([T_obs_train[:, np.newaxis], T_inf_train[:, np.newaxis]],
                         axis=1)
y_train=beta_MAP_train

#prepared for test
T_inf_test, T_true_test, beta_true_test = pickle.load(open('../data/MLtest.p','rb'))




T_inf_test = np.vstack(T_inf_test[4]).flatten()
T_true_test = np.vstack(T_true_test[4]).flatten()

beta_true_test = np.vstack(beta_true_test).flatten()

x_test = np.concatenate([T_true_test[:, np.newaxis], T_inf_test[:, np.newaxis]],
                         axis=1)



# generate mu and sigma by GPR
GPR=Guassian_Process(sigma_noise=0.02)
GPR.train(x_train,y_train)
mu,sigma=GPR.predict(x_test)


n=len(T_inf_test)+1
h=0.5
solver=Solver(n,h,T_inf_test)
'''
T_ML : data generated by ML process
T_base : data generated by base equation
T_inf : data about surrounding Temperature
T_ML_std : Standard Deviation about ML data
'''
T_ML=solver.get_T_beta(mu)
T_base=solver.get_T_base()

beta_ML_std=np.sqrt(np.diag(sigma))

# sample to get std for ML
N_samples=1000

sam_lst=[]

T_ML_sam_lst=[]
for i in range(N_samples):
    beta_sam=np.random.multivariate_normal(mu,sigma)
    T_ML_sam=solver.get_T_beta(beta_sam)
    T_ML_sam_lst.append(T_ML_sam)

samp=np.vstack(T_ML_sam_lst)
T_ML_std=np.std(samp,axis=0)
print(T_ML_std)

pickle.dump((T_true_test, T_base, T_ML,T_ML_std), open('../data/figMLdata_const_case5.p','wb'))


















