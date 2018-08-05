import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, seaborn
import scipy.optimize as optimize

def load_profile(profile_path):
    df = pd.read_csv(profile_path, sep = '\t', header=None)
    df.columns = ['x','y','z']
    df = df*1e6    
    return df
    
def minimize_perp_distance(x, y, z):
    def model(params, xyz):
        a, b, c, d = params
        x, y, z = xyz
        length = np.sqrt(a**2+b**2+c**2)
        return ((np.abs(a*x + b*y + c*z + d))**2).sum()/length
    def unit_length(params):
        a, b, c, d = params
        return a**2 + b**2 + c**2 - 1

    initial_guess = 0.1, 0.3, 0.2, 0.4
    # constrain the vector perpendicular to the plane be of unit length
    cons = ({'type':'eq', 'fun': unit_length})
    sol = optimize.minimize(model, initial_guess, args=[x, y, z], constraints=cons)
    return tuple(sol.x)

def Z(X, Y, params):
    a, b, c, d = params
    return -(a*X + b*Y + d)/c    

def df_plane_distance(df, params):
    z_new = (df*params[:3]).sum(axis = 1)+params[3]
    return z_new

def level_profiles(dfs):
    ldf = []
    for name, df in dfs.items():
        params =  minimize_perp_distance(*np.array(df).T)
        z_new = df_plane_distance(df, params)
        ldf.append(z_new)
    df = pd.concat(ldf, axis =1)
    df.columns = list(dfs.keys())   
    return df

def df_histogram(df, filename = False):
    fig = plt.figure(figsize = (9,5))
    ax = fig.add_axes([.1,.1,.85,.85])
    df.plot.hist(ax=ax, bins = 200, range = [-20,20], alpha = 0.75, density = True)

    legend = [rf"{val}: $\sigma$ = %.2f $\mu m$, max = %.2f $\mu m$, {os.linesep} q(.99) = %.2f $\mu m$, q(.999) = %.2f $\mu m$" 
              % (df[val].std(), df[val].max(), df[val].quantile(.99), df[val].quantile(.999)) for val in df.columns]

    ax.legend(legend)
    ax.set_xlabel(r"height [$\mu m$]")
    if filename != False:
        fig.savefig(filename, dpi =300)
    else:
        return fig

def main():
    profiles = {'P240':'P240.xyz.gz', 'P500': 'P500.xyz.gz'}
    dfs = {name:load_profile(path) for name, path in profiles.items()}

    df = level_profiles(dfs)

    file_out = "/home/fdutka/Dropbox/profilometry.png"
    df_histogram(df, file_out)
