import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd
import cartopy.crs as ccrs
#import datetime
import seaborn as sns
#from matplotlib.colors import DivergingNorm
from scipy import signal
from scipy.signal import find_peaks
import sys
from netCDF4 import Dataset

## Load data

tas_NH = xr.open_dataset('slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_167_NH_ymean.nc')
tas_NH_nv = xr.open_dataset('novolc/slo0043_echam6_BOT_mm_1001-8850_167_NH_ymean.nc')
aod = xr.open_dataset('forcing/eva_holo2.2_aod_550nm_echam_T63_sw_1001_8850_ym.nc')

# Detrend tas data
poly_grid = tas_NH['var167'].polyfit('time', deg=2)
poly_trend = xr.polyval(tas_NH['time'],poly_grid['polyfit_coefficients'])

polygrid_nv = tas_NH_nv['var167'].polyfit('time', deg=2)
polytrend_nv = xr.polyval(tas_NH_nv['time'],polygrid_nv['polyfit_coefficients'])

tas_NH_detr = tas_NH['var167'][:,:,:] - poly_trend[:,:,:]
tas_NH_nv_detr = tas_NH_nv['var167'][:,:,:] - polytrend_nv[:,:,:]

## Calculate eruption years

def get_wghts(lat):

	latr = np.deg2rad(lat) # convert to radians

	weights = np.cos(latr) # calc weights

	return weights
	
lat = aod['lat'][:48]
wgts = get_wghts(lat)

aod_awa = np.average(aod['aod550'][:,:48], axis=1, weights=wgts)

peaks = find_peaks(aod_awa,0.08)

np.diff(peaks[0])

cluster_int = np.array([np.where(np.diff(peaks[0])<10)]).flatten()

cluster = np.unique(sorted(np.concatenate((cluster_int, cluster_int +1))))

single_eruptions = np.delete(peaks[0], cluster)

print(np.shape(single_eruptions))

## Split tropical / extratropical eruptions

lats = []
for i in single_eruptions:
    a = np.where(aod['aod550'][i,:] == np.nanmax(aod['aod550'][i,:]))
    lats = np.append(lats, aod['lat'][a])
    
tropical = single_eruptions[np.where((lats<40)&(lats>-40))]
extratropical = single_eruptions[np.where((lats>40))]


## Calculate accumulated AOD for 10 years after all large eruptions >0.08

aod_acc_10yr_all = []
aod_acc_10yr_se = []
aod_acc_10yr_tr = []
aod_acc_10yr_extr = []
aod_acc_10yr_db = []

aod_lat_acc_10yr_all = []
aod_lat_acc_10yr_se = []
aod_lat_acc_10yr_tr = []
aod_lat_acc_10yr_extr = []
aod_lat_acc_10yr_db = []


for i in single_eruptions:
    aod_acc_10yr_se.append(np.cumsum(aod_awa[i:i+10]))
    aod_lat_acc_10yr_se.append(np.cumsum(aod['aod550'][i:i+10,:], axis=0))
    
for i in peaks[0]:
    aod_acc_10yr_all.append(np.cumsum(aod_awa[i:i+10]))
    aod_lat_acc_10yr_all.append(np.cumsum(aod['aod550'][i:i+10,:], axis=0))
        
for i in extratropical:
    aod_acc_10yr_extr.append(np.cumsum(aod_awa[i:i+10]))
    aod_lat_acc_10yr_extr.append(np.cumsum(aod['aod550'][i:i+10,:], axis=0))
    
for i in tropical:
    aod_acc_10yr_tr.append(np.cumsum(aod_awa[i:i+10]))
    aod_lat_acc_10yr_tr.append(np.cumsum(aod['aod550'][i:i+10,:], axis=0))
    
for i in peaks[0][cluster]:
    aod_acc_10yr_db.append(np.cumsum(aod_awa[i:i+10]))
    aod_lat_acc_10yr_db.append(np.cumsum(aod['aod550'][i:i+10,:], axis=0))
    
## Find max value

max_aod_acc_10yr_all = []
max_aod_acc_10yr_se = []
max_aod_acc_10yr_tr = []
max_aod_acc_10yr_extr = []
max_aod_acc_10yr_db = []

for i in np.arange(0,189,1):
    max_aod_acc_10yr_all.append(aod_acc_10yr_all[i][-1])

for i in np.arange(0,135,1):
    max_aod_acc_10yr_se.append(aod_acc_10yr_se[i][-1])
    
for i in np.arange(0,79,1):
    max_aod_acc_10yr_tr.append(aod_acc_10yr_tr[i][-1])
    
for i in np.arange(0,55,1):
    max_aod_acc_10yr_extr.append(aod_acc_10yr_extr[i][-1])
    
for i in np.arange(0,54,1):
    max_aod_acc_10yr_db.append(aod_acc_10yr_db[i][-1])

## Find largest eruptions based on accumulated AOD

large_ser = np.where(np.array(max_aod_acc_10yr_se) > 0.6)[0]
large_db = np.where(np.array(max_aod_acc_10yr_db) > 0.6)[0]

## Make temperature anomaly composite

tas_lse_avg = np.zeros([20, 48, 192])
tas_ldb_avg = np.zeros([20, 48, 192])

tas_lse_novolc_std = np.zeros([48,192])
tas_ldb_novolc_std = np.zeros([48,192])

for years in np.arange(0,20,1):
	tas_lse_avg[years,:,:] = np.nanmean(tas_NH_detr[single_eruptions[large_ser]+years,:,:], axis = 0)
	tas_ldb_avg[years,:,:] = np.nanmean(tas_NH_detr[peaks[0][cluster][large_db]+years,:,:], axis = 0)
	
	tas_lse_novolc_std[:,:] = np.std(tas_NH_nv_detr[single_eruptions[large_ser]+years,:,:], axis = 0)
	tas_ldb_novolc_std[:,:] = np.std(tas_NH_nv_detr[peaks[0][cluster][large_db]+years,:,:], axis = 0)

## Make into xarray	
tas_lse_avg_xr = xr.DataArray(data = tas_lse_avg, coords = [np.arange(0,20,1), np.array(tas_NH.lat), np.array(tas_NH.lon)] ,dims = ['year','lat', 'lon'] , name = 'tas_avg')
tas_ldb_avg_xr = xr.DataArray(data = tas_ldb_avg, coords = [np.arange(0,20,1), np.array(tas_NH.lat), np.array(tas_NH.lon)] ,dims = ['year','lat', 'lon'] , name = 'tas_avg')

tas_lse_std_novolc_xr = xr.DataArray(data = tas_lse_novolc_std, coords = [np.array(tas_NH_nv.lat), np.array(tas_NH_nv.lon)], dims = ['lat', 'lon'], name = 'std')
tas_ldb_std_novolc_xr = xr.DataArray(data = tas_ldb_novolc_std, coords = [np.array(tas_NH_nv.lat), np.array(tas_NH_nv.lon)], dims = ['lat', 'lon'], name = 'std')

## Save data
tas_lse_avg_xr.to_netcdf('lse_tas_a_avg.nc')
tas_ldb_avg_xr.to_netcdf('ldb_tas_a_avg.nc')
tas_lse_std_novolc_xr.to_netcdf('lse_std_novolc.nc')
tas_ldb_std_novolc_xr.to_netcdf('ldb_std_novolc.nc')

