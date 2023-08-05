# Code automatically exported from notebook Meissner.ipynb in directory Notebooks_Algo
# Do not modify
from ... import LinearParallel as lp
from ... import AutomaticDifferentiation as ad
norm_infinity = ad.Optimization.norm_infinity

import numpy as np
from matplotlib import pyplot as plt
import scipy
import scipy.optimize as sciopt
import plotly.graph_objects as go

def LinearConstraint_AD(f):
    """
    Takes a linear constraint f>=0, 
    encoded as an ad.Sparse variable, 
    and turns it into a scipy compatible constraint.
    """
    return sciopt.LinearConstraint(f.tangent_operator(), lb = -f.value, ub=np.inf)

def QuadraticObjective_AD(f):
    """
    Takes a quadratic objective function, 
    encoded as an ad.Sparse2 variable,
    and returns fun, jac and hessian methods.
    """
    val0 = f.value
    grad0 = f.to_first().to_dense().gradient()
    n = len(grad0)
    hess0 = f.hessian_operator(shape=(n,n))
    def fun(x):  return val0+np.dot(grad0,x)+np.dot(x,hess0*x)/2
    def grad(x): return grad0+hess0*x
    def hess(x): return hess0
    return {'fun':fun,'jac':grad,'hess':hess}

def NonlinearObjective(f,fargs):
    """Returns methods computing the value, gradient and hessian 
    of a given objective function f"""
    def fun(x):
        return f(x,*fargs)
    def grad(x): 
        return f(ad.Sparse.identity(constant=x),*fargs).to_dense().gradient()
    def hess(x): 
        return f(ad.Sparse2.identity(constant=x),*fargs).hessian_operator()
    return {'fun':fun,'jac':grad,'hess':hess}

def NonlinearConstraint(f,fargs):
    """
    Represents the constraint : np.bincount(indices,weights) >= 0,
    where (indices, weights) = f(x,*fargs)
    (Indices may be repeated, and the associated values must be summed.)
    """
    def fun(x):
        ind,wei = f(x,*fargs); 
        return np.bincount(ind,wei)
    def grad(x): 
        ind,wei = f(ad.Sparse.identity(constant=x),*fargs)
        triplets = (wei.coef.reshape(-1),(ind.repeat(wei.size_ad),wei.index.reshape(-1)))
        return scipy.sparse.coo_matrix(triplets).tocsr()
    def hess(x,v): # v is a set of weights, provided by the optimizer
        ind,wei = f(ad.Sparse2.identity(constant=x),*fargs)
        return np.sum(v[ind]*wei).hessian_operator()
    return sciopt.NonlinearConstraint(fun,0.,np.inf,jac=grad,hess=hess,keep_feasible=True)

def to_mathematica(Z): return str(Z.T.tolist()).replace("[","{").replace("]","}")

