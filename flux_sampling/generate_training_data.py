from cobra.io import load_model
from scipy.stats import qmc
import pandas as pd
import numpy as np

def run_N_samples(N):
    model = load_model("textbook")
    sampler = qmc.LatinHypercube(d=95)
    sample = sampler.random(n=N)
    l_bounds = [r.lower_bound for r in model.reactions]
    u_bounds = [r.upper_bound for r in model.reactions]
    sample_scaled = qmc.scale(sample, l_bounds, u_bounds)

    sample_data = pd.DataFrame()
    for s_i in range(N):
        with model as m: 
            for r_i in range(len(model.reactions)):
                m.reactions.get_by_id(model.reactions[r_i].id).bounds = (sample_scaled[s_i][r_i], sample_scaled[s_i][r_i])
            solution = m.optimize()
            if solution.status == 'optimal' and solution.objective_value > 0:
                sample_data = pd.concat([sample_data, pd.DataFrame({'sample': [sample_scaled[s_i]], 'feas': [1], 'objective_function': [solution.objective_value]})])
            else:
                sample_data = pd.concat([sample_data, pd.DataFrame({'sample': [sample_scaled[s_i]], 'feas': [0], 'objective_function': [np.nan]})])
        if s_i % 1000 == 0: sample_data.to_csv('sample_data.csv')    
    return sample_data

run_N_samples(2000)