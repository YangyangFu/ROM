# -*- coding: utf-8 -*-
"""
Solving the dynamic linear equations: Ax=b.
Descriptions: this solver can be used to solve linear equations in the general format Ax=b.
where A keeps constant during each time step, b varies in each time step.

Authour: Yangyang Fu
Email: yangyang.fu@pnnl.gov 
"""
class solveLinearEquation(object):
    """
    Solve linear equations
    """
    def __init__(self, A,b):
        """
        A: n-by-n array;
        b: n-by-1 array;
        """
        self.A = A
        self.b = b
        self.x = None
        self._ill_condition_ = False
        
    def _check(self):
        """A must be a full-ranked matrix in order to have a uniqe solution for the equation set. Therefore,
        before solving the equations, we need to check if A is singularity.
        """
        from numpy import linalg
        import sys
        
        # if the matrix A is not ill-conditioned
        if linalg.cond(self.A) >= 1/sys.float_info.epsilon:
            self._ill_condition_ = True
            print ('Matrix A is ill-conditioned. Try LU-factorization or Singluar Value Decomposition to handle the ill-conditioness.') 
        else:
            self._ill_condition_ = False
            print ('Matrix A is well-conditioned, and can be solved using exact method')
            
    def _method(self):
         """
         The equation Ax=b is solved based on the conditioness of A. If A is well conditioned, then use exact method. Otherwise use Singular Value Decomposition.
         
         """
         import numpy as np
         
         if self._ill_condition_:
             u,s,vh = np.linalg.svd(self.A)
             self.x = np.dot(np.dot(vh.transpose()*(1/s),u.transpose()),self.b)
         else:
             self.x = np.linalg.solve(self.A, self.b)
             
    def solve(self):
        
        self._check()
        self._method()
        
        
class solveDynamic:
    """solve linear equations Ax=b in a dynamic time period. Note that b is dynamic and independent of previous time step.
    Therefore, a function to calculate b in terms of previous x should be built independently outside this solve based on 
    the solutions in self.xsol.
    
    """
    
    def __init__(self, A,b,tStart,tEnd,dt,x0):
        """
        A: n-by-n array;
        b: n-by-1 array;
        x0: n-by-1 array;
        """
        self.A = A
        self.b = b
        self.x = None
        self._ill_condition_ = False  
        self.tStart = tStart
        self.tEnd = tEnd
        self.dt = dt 
        self.x0 = x0               
    
    def solve(self):
        import numpy as np
        
        ts = np.arange(self.tStart,self.tEnd+self.dt,self.dt)
        
        # initialize the x before simulation starts
        self.xsol = np.zeros([len(self.x0),len(ts)]) 
        
        for i in range(len(ts)):
            eq = solveLinearEquation(self.A,self.b)
            eq.solve()            
            self.xsol[:,i] = eq.x.reshape(1,-1)
            
            
            
        
     
         
        