import pandas as pd
import numpy as np
import cvxpy as cp

def EqualWeighting(drr_data):  
    num_assets = len(drr_data.columns)  
    weights = [1 / num_assets] * num_assets  
    return weights
    
def SimpleStdReverse(drr_data):
    risk_contrbutions = np.std(drr_data,axis = 0)
    weights = 1 / risk_contrbutions
    asset_ratio = list((weights / np.sum(weights)))

    return asset_ratio

def RiskParityModel(drr_data,non_neg = True):
    assets_number = len(drr_data.columns)
    cov_matrix  = pd.DataFrame(drr_data).cov()
    weights = cp.Variable(assets_number)

    constraints = [cp.sum(weights) == 1]
    if non_neg:
        constraints.extend([weights >= 0])
    
    objective = cp.Minimize(cp.quad_form(weights, cov_matrix))  
    prob = cp.Problem(objective, constraints)  
    result = prob.solve()  
    
    optimal_weights = list(weights.value)
    return optimal_weights
    