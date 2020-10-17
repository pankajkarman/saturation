
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from mls import *
from utility import *
from scipy import interp
from facets import facets
from astropy.time import Time
from pysagereader.sage_iii_reader import SAGEIIILoaderV400
from pysagereader.sage_ii_reader import SAGEIILoaderV700


# In[2]:


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker 

# matplotlib parameters
mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams["xtick.major.size"]=8
mpl.rcParams["ytick.major.size"]=8
mpl.rcParams["ytick.minor.size"]=5
mpl.rcParams["xtick.minor.size"]=5
mpl.rcParams["xtick.labelsize"]=20
mpl.rcParams["ytick.labelsize"]=20
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'


# In[3]:


data_folder='/home/pankaj/phd/saturation/data/raw/sage/sage2'
floc='/home/pankaj/phd/saturation/plot/oct/'
gama=2.0/7.0
k=1.38E-19


# In[4]:


#select month
mon_no=10
months=['January','February','March','April','May','June','July','August','September','October','November','December']
mon_name=months[mon_no-1]


# In[5]:


#load the data
sage = SAGEIILoaderV700()
sage.data_folder = data_folder
data = sage.load_data('1984-10-19','2005-12-31',-90,-65)
#get rid of bad data
data['O3'][data['O3'] == data['FillVal']] = np.nan
data['O3'][data['O3_Err']>10000]= np.nan
ozo=data['O3']
tem=data['NMC_Temp']
pre=data['NMC_Pres']
pot=tem*(1013.0/pre)**gama
mjds=data['mjd']
vmr=k*ozo*tem/pre
vmr[vmr<0]=np.nan

#setup the time bins
time_res = 1
date = np.arange(np.min(data['mjd']), np.max(data['mjd']), time_res)

alt_pt = np.arange(375,576,25)
oz=np.zeros((len(mjds), len(alt_pt)))
for i in range(len(data['mjd'])):
    oz[i,:]=interp(alt_pt,pot[i,:],vmr[i,:]/1e-6)
o3=np.zeros((len(date), len(alt_pt)))
for idx, mjd in enumerate(date):
    good = (data['mjd'] > mjd) & (data['mjd'] < mjd + time_res)
    o3[idx,:] = np.nanmean(oz[good, :], axis=0)
#date=Time(date, format='mjd')
date=Time(mjds, format='mjd')
date=pd.to_datetime(date.isot)


# In[6]:


fig, axes = facets(3, 3, width=20.0, aspect=0.5, internal_pad=0.0, top_pad=0.1, bottom_pad=0.7, left_pad=1.1, right_pad=0.1)
for num,(pt,ax) in enumerate(zip(alt_pt,axes)):
    ax.plot(date.year[date.month==mon_no], oz[date.month==mon_no,num],'.', color='black')
    ax.axhline(0.1, color='black', linestyle='--', linewidth=0.8,zorder=1)
    ax.set_title(str(pt)+' K',y=.85,x=0.11,fontsize=21)
axes[3].set_yscale('log')
axes[3].set_ylim([0.005,9])
axes[3].yaxis.set_major_formatter(ticker.FuncFormatter(logformat))
axes[3].set_ylabel('Ozone/ppmv',fontsize=25)
axes[7].set_xlabel('Year',fontsize=25)
fig.suptitle(mon_name,y=0.975,x=0.31,fontsize=21)
plt.minorticks_on()
fig.savefig(floc+'sage_antarctic.pdf')
plt.show()

