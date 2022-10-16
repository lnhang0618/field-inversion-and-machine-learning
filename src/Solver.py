import numpy as np
'''
Created on Oct 16 2022

@author:lnhang
'''

class Solver(object):
    def __init__(self,num,h,T_inf) :
        self.num=num
        self.h=h
        self.T_inf=T_inf
        '''
        here T_inf is temperature of surroundings and 
        
        the h is Convection coefficient 
        
        num is the number of data 
        
        '''
        
        self.z=np.linspace(0,1,num+1)
        self.dz=1/(num)
    
    def get_T_base(self,norm=1e-3,iter_max=80000):
 
        T=np.zeros(self.num+1)
        
        L2=10
        iter=0
        '''
        vectorization
        
        '''
        while L2>norm and iter<iter_max:
            T_old=T.copy() #二阶差分
            new=0.5*(T[:self.num-1]+T[2:]+\
                self.dz**2*(5e-4)*\
                (self.T_inf**4-T[1:self.num]**4))
        
            T[1:self.num]=0.5*new+0.5*T[1:self.num]
            L2=np.linalg.norm(T-T_old)
            iter+=1
        
        '''
        iterate this process to generate approximate value
        '''
        
        return T[1:-1]
    
    def get_T_beta(self,beta,norm=1e-3,iter_max=80000):
 
        T=np.zeros(self.num+1)
        
        L2=10
        iter=0
        '''
        vectorization
        
        '''
        while L2>norm and iter<iter_max:
            T_old=T.copy() #二阶差分
            new=0.5*(T[:self.num-1]+T[2:]+\
                self.dz**2*(5e-4)*beta*\
                (self.T_inf**4-T[1:self.num]**4))
        
            T[1:self.num]=0.25*new+0.75*T[1:self.num]
            L2=np.linalg.norm(T-T_old)
            iter+=1
        
        '''
        iterate this process to generate approximate value
        '''
        
        return T[1:-1]