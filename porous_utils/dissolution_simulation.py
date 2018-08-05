import scipy
from scipy import stats
import numpy as np
import glob, os
import pandas as pd
from itertools import chain

import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from . import dissolution_experiment as dise
from . import fractal_dimension as frac_dim

#==================================================================================================================

class phimage:
    
    def __init__(self, dirname):
        
        filename = os.path.join(dirname, 'init','phi.dat.00')
        with open(filename,'r') as f:
            l1 = f.readline()
        self.nx, self.ny  = np.array(l1.split()[:2]).astype(int)
        self.name = os.path.basename(dirname)
        self.dirname = dirname
        self.nproc = len(glob.glob(os.path.join(self.dirname, 'init','phi.dat.*')))
    
        filename = os.path.join(dirname, 'init','input.dat')
        with open(filename,'r') as f:
            l1 = f.readlines()
        self.dt = float(l1[1].split()[-1])
    
    def phi(self):
        
        lphi = []
        
        for filename in glob.glob(os.path.join(self.dirname,'init','phi.dat.*')):
            with open(filename,'r') as f:
                phi = [row.split() for row in f.readlines()[1:]]
            lphi.append(np.array(list(chain(*phi))).astype(float))
        lphi = np.array(lphi).ravel().reshape(self.nx,self.ny)     
    
        return lphi
    
    def phi2(self, filename2):
        
        lphi = []
        
        for i in range(self.nproc):
            filename = os.path.join(self.dirname, 'data', filename2+'.'+str(i).zfill(2))
            with open(filename,'r') as f:
                phi = [row.split() for row in f.readlines()[1:]]
            lphi.append(np.array(list(chain(*phi))).astype(float))
        lphi = np.array(lphi).ravel().reshape(self.nx,self.ny)     
    
        return lphi
    
    def mean1(self):
        return self.phi().ravel().mean()
    
    def std1(self):
        return self.phi().ravel().std()
    
    def init(self):
        
        filename = os.path.join(self.dirname, 'init','input.dat')
        with open(filename, 'r') as f:
            data = np.array(f.readlines()[1].split()).astype(float)
        return data
    
    def info(self):
        return f"{'-'*30}\n directory: {self.name} \n mean: {self.mean1()} \n std: {self.std1()} \n{'-'*30}"
    
    def hmax(self):
        filename = os.path.join(self.dirname, 'init','parms.h')
        hmax = 0
        if os.path.isfile(filename):
            with open(filename,'r') as f:
                data = f.readlines()
                hmax = float([val for val in data if "Maximum Aperture" in val][0].split()[2])
        return hmax
    
    def time_steps(self):
        l1 = np.unique(np.array([os.path.basename(val).split('.')[1] for val in glob.glob(os.path.join(self.dirname, 'data', 'phi.*'))]))
        l1 = np.sort(l1.astype(int))
        return l1
    
    def BTime(self):
        
        l1 = self.time_steps()
        i = len(l1)-1
        while (self.phi2('phi.'+str(l1[i]).zfill(4))[-1].max() == self.hmax()) and i>0:
            i=i-1
        
        btime = l1[i]+1
        
        return btime
    
    def timeh(self, time_sim, h0):
        """
        Converts simulation time into experimental time in hours
        
        :param time_sim: float, simulation time
        :param h0: float, experimental height h0 in um
        
        :returns: float, time in hours
        """
        tstep = (1-dise.phi)*dise.csol/(dise.k*dise.csat)
        t = time_sim*self.dt*tstep*h0/1000/3600 
        return t

    def im(self, time, tsh = 0.95, title = "", save=False, filename = None):
        """
        Returns simulation screenshot, at a given time 
        :return fig: figure 
        """

        phi = self.phi2('phi.'+str(time).zfill(4))

        fig = plt.figure(figsize = (5,5))
        fig.patch.set_facecolor('white')
        fig.patch.set_alpha(1)

        ax = fig.add_axes([.1,.1,.85,.85])
        ax.imshow((phi>tsh*self.hmax()).astype(int), cmap= 'Reds');
        ax.set_title(title)

        if save:
            fig.savefig(filename, dpi =300)
            plt.close(fig)
        else:
            return fig      

#==================================================================================================================    
    
def fractal_dim(sim, time, tsh = 0.95):
    """
    Calculates fractal dimension of the binarized image by treshold tsh
    :param sim: phimage class object, simulation
    :param time: int, time of the simulation in which calculate fractal dimension
    :param tsh: float, treshold by which image is binarized
    
    :returns fdim: float, fractl dimnesion of the image
    """
    phi = sim.phi2('phi.'+str(time).zfill(4))
    fdim = frac_dim.fractal_dimension(phi, tsh*sim.hmax())      
    return fdim

def fig_fractal_dim(sim, bt = -1, save = False, filename = None):
    """
    Plots figure of fractal dimension ...
    """
    
    tsteps = sim.time_steps()
    
    if bt<0:
         bt = sim.BTime()
            
    tstepsl = tsteps[tsteps<min(1.1*bt, tsteps[-1])]
    lfdim = []
    for time in tqdm(tstepsl):
        lfdim.append(fractal_dim(sim, time))
    
    fig = plt.figure(figsize = (7,5))
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1)
    ax = fig.add_axes([.1,.1,.85,.8])
    ax.plot(tstepsl, lfdim)
    ax.vlines(bt,0.99*np.array(lfdim).min(),1.01*np.array(lfdim).max(), linestyles='--')
    ax.axes.set_xlabel("time step")
    ax.axes.set_ylabel("fractal dimension")
    ax.axes.set_title(sim.name)
    
    if save:
        fig.savefig(filename, dpi =300)
        fig.clf()
        plt.close(fig)
    else:
        return fig    
    
def final_figure(sim, btime, tsh = 0.95, title = "", save=False, filename = None):
    """
    Returns final figure, at the time of breakthrough, of the simulation
    :return fig: figure 
    """
    
    tend = sim.time_steps()[sim.time_steps()<btime][-1]

    phi = sim.phi2('phi.'+str(tend).zfill(4))
    
    fig = plt.figure(figsize = (5,5))
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1)

    ax = fig.add_axes([.1,.1,.85,.85])
    ax.imshow((phi>0.95*sim.hmax()).astype(int), cmap= 'Reds');
    ax.set_title(title)
    
    if save:
        fig.savefig(filename, dpi =300)
        plt.close(fig)
    else:
        return fig  
    
