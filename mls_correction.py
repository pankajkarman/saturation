import h5py
import numpy as np
import pandas as pd

class MLSCorrection():
    def __init__(self, filename):
        self.filename  = filename
        self.fieldname = filename.split('-')[2].split('_')[0]
        
    def read(self, dtype='geolocation'):
        field = self.fieldname
        data = h5py.File(self.filename, 'r+')['HDFEOS']['SWATHS'][field]
        if dtype=='geolocation':
            lat = data['Geolocation Fields']['Latitude'][()]
            lon = data['Geolocation Fields']['Longitude'][()]
            lev = data['Geolocation Fields']['Pressure'][()]
            lsa = data['Geolocation Fields']['LineOfSightAngle'][()]
            lst = data['Geolocation Fields']['LocalSolarTime'][()]  
            oga = data['Geolocation Fields']['OrbitGeodeticAngle'][()]
            sza = data['Geolocation Fields']['SolarZenithAngle'][()]
            tim = data['Geolocation Fields']['Time'][()]  
            chn = data['Geolocation Fields']['ChunkNumber'][()]
            return lat, lon, lev, lsa, lst, oga, sza, tim, chn
        
        if dtype=='data':
            con = data['Data Fields']['Convergence'][()]
            prc = data['Data Fields']['L2gpPrecision'][()]
            mol = data['Data Fields']['L2gpValue'][()]
            qua = data['Data Fields']['Quality'][()]
            sta = data['Data Fields']['Status'][()]
            nlev = data['nLevels'][()]
            nlev = len(nlev)
            ntim = data['nTimes'][()]
            ntim = len(ntim)
            return field, con, prc, mol, qua, sta, nlev, ntim 
        
    def correct(self):
        lat, lon, pre, lsa, lst, oga, sza, tim, chn = self.read(dtype='geolocation')
        field, con, prc, mol, qua, sta, nlev, ntim = self.read(dtype='data')
        do = (pre>260) & (pre<262)
        eo = (pre<0.018)
        ll = (pre>314) & (pre<318)
        hl = (pre>=0.0018) & (pre<0.0025)  
        
        if field == 'O3':
            criteria1 = (con<1.03) & (qua>1.0) & (sta%2==0)
            criteria2 = (pre>0.02) & (pre<261)
            for var in [mol, prc]:
                var[~criteria1, :] = np.nan 
                var[:, ~criteria2] = np.nan
                var[:, ll | eo] = np.nan
            
        if field in ['GPH', 'Temperature']:
            criteria1 = (con<1.03) & (qua>0.2) & (sta%2==0)
            criteria2 = (pre>0.001) & (pre<261)
            criteria3 = (pre>=100) 
            criteria4 = (qua>0.9) 
            for var in [mol, prc]:          
                var[~criteria1, :] = np.nan 
                var[:, ~criteria2] = np.nan
                var[:, criteria3][~criteria4, :]  = np.nan
            
        if field == 'H2O':
            criteria1 = (con<2.0) & (qua>1.45) & (sta%2==0) & (sta!=16) & (sta!=32)
            criteria2 = (pre>0.002) & (pre<317)
            for var in [mol, prc]:
                var[~criteria1, :] = np.nan 
                var[:, ~criteria2] = np.nan
                
        if field == 'N2O':
            criteria1 = (con<2.0) & (qua>1.0) & (sta%2==0) & (sta!=16) & (sta!=32)
            criteria2 = (pre>0.46) & (pre<68)
            for var in [mol, prc]:
                var[~criteria1, :] = np.nan 
                var[:, ~criteria2] = np.nan
                
        mol[prc<=0] = np.nan  
        return mol, prc      
