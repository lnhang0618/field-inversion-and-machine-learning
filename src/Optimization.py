'''
Created on Nov 1 2022 

@author:lnhang
'''

import numpy as np
import scipy.optimize as optimize
import copy

class Optimization:
    """
    Optimization and post-processing of field inversion.
    Args:
        model: Approximate model 
        prior: Prior distribution
        data: Observations of the physical process
        objfn: Objective function
        beta0: Initial corrective term
        optimizer: Optimization algorithm
    Returns:
        Optimized corrective term.
    """
    
    def __init__(self,Solver,prior,data,Objfn,beta0,optimizer):
        self.Solver=Solver
        self.prior=prior
        self.data=data
        self.Objfn=Objfn
        
        self.solve_inverse_problem(self.Objfn,beta0,optimizer)
    
    def J(self,beta):
        tmp=self.Objfn.compute_J(beta)
        
        self.convI+=[tmp]
        return tmp
    
    def solve_inverse_problem(self,Objfn,beta0,optimizer):
        beta=copy.deepcopy(beta0)
        
        self.convI=[]
        
        res=optimize.minimize(self.J,beta,method=optimizer,jac=Objfn.compute_gradient_adjoint,
                              options={"disp":True,"maxiter":1000})
        
        self.beta_MAP=res.x
        self.conv=np.array(self.convI)
    
    def compute_MAP_properties(self):
        self.T_MAP=self.Solver.get_T_beta(self.beta_MAP)
        
        self.beta_r_MAP=self.Solver.get_beta_r_true(self.T_MAP)
        self.beta_c_MAP=self.Solver.get_beta_c_true(self.T_MAP)
    
    def compute_true_properties(self):
        self.T_true =self.data.get_T_true()
        self.beta_true=self.Solver.get_beta_true(self.T_true,with_rand=False)
        self.J_limit=self.Objfn.compute_J(self.beta_true)
    
    def compute_base_properties(self):
        self.T_base=self.Solver.get_T_base()
        
    def sample_posterior(self,N_samples):
        H=self.Objfn.compute_Hessian_adjoint_direct(self.beta_MAP)
        C_MAP=np.linalg.inv(H)
        R=np.linalg.cholesky(C_MAP)
        
        sam_lst=[]
        for i in range(N_samples):
            s=np.random.randn(self.Solver.num-1)
            sam_lst.append(self.beta_MAP+R.dot(s))
        
        samp=np.vstack(sam_lst)
        self.std=np.std(samp,axis=0)