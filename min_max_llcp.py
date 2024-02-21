import numpy as np
import xarray as xr
import pandas as pd
from scipy import signal
from scipy.ndimage import uniform_filter1d
#from skyfield import api #time before CE
from scipy.signal import find_peaks
from numpy.polynomial import Polynomial

# Open data
tas_NH_fm = xr.open_dataset('slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_167_NH_ymean_fldmean.nc')
tas_NH_novolc_fm = xr.open_dataset('novolc/slo0043_echam6_BOT_mm_1001-8850_167_NH_ymean_fldmean.nc')

# Fit curve to data --> remove trend
poly2 = Polynomial.fit(tas_NH_fm['time'], tas_NH_fm['var167'][:,0,0], deg=2)
poly2_nv = Polynomial.fit(tas_NH_novolc_fm['time'], tas_NH_novolc_fm['var167'][:,0,0], deg=2)

tas_NH_fm_detr = tas_NH_fm['var167'][:,0,0] - poly2(tas_NH_fm['time'])
tas_NH_fm_novolc_detr = tas_NH_novolc_fm['var167'][:,0,0] - poly2_nv(tas_NH_novolc_fm['time'])

# Calculate 200y running mean
tas_NH_fm_detr_200yr = uniform_filter1d(tas_NH_fm_detr, size=200, axis=0, origin = -100)
tas_NH_fm_nv_detr_200yr = uniform_filter1d(tas_NH_fm_novolc_detr, size=200, axis=0, origin = -100)

# Find peaks min max
peaks_tas_200y = find_peaks((tas_NH_fm_detr_200yr[:-200]*-1), height = 0.058, distance = 200)
peaks_tas_200y_max = find_peaks((tas_NH_fm_detr_200yr[:-200]), height = 0.049, distance = 200)

# Open spatial data
tas_NH = xr.open_dataset('slo0042+slo0046+slo0050_echam6_BOT_mm_1001_8850_167_NH_ymean.nc')

# Detrend spatial data
poly_grid = tas_NH['var167'].polyfit('time', deg=2)
poly_trend = xr.polyval(tas_NH['time'],poly_grid['polyfit_coefficients'])

tas_NH_detr = tas_NH['var167'][:,:,:] - poly_trend[:,:,:]

# Calculate 200yr running mean
tas_NH_detr_200yr = uniform_filter1d(tas_NH_detr[:,:,:], size=200, axis=0, origin = -100)

# Take out peaks 
tas_NH_detr_200yr_LIA = tas_NH_detr_200yr[peaks_tas_200y[0][-1],:,:]
tas_NH_detr_200yr_LALIA = tas_NH_detr_200yr[peaks_tas_200y[0][-2],:,:]
tas_NH_detr_200yr_3800BCE = tas_NH_detr_200yr[peaks_tas_200y[0][3],:,:]
tas_NH_detr_200yr_MWP = tas_NH_detr_200yr[peaks_tas_200y_max[0][-1],:,:]
tas_NH_detr_200yr_RWP = tas_NH_detr_200yr[peaks_tas_200y_max[0][-2],:,:]
tas_NH_detr_200yr_4000BCE = tas_NH_detr_200yr[peaks_tas_200y_max[0][3],:,:]

# Create xarray
tas_NH_detr_200yr_LIA_xr = xr.DataArray(data = tas_NH_detr_200yr_LIA, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')
tas_NH_detr_200yr_LALIA_xr = xr.DataArray(data = tas_NH_detr_200yr_LALIA, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')
tas_NH_detr_200yr_3800BCE_xr = xr.DataArray(data = tas_NH_detr_200yr_3800BCE, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')
tas_NH_detr_200yr_MWP_xr = xr.DataArray(data = tas_NH_detr_200yr_MWP, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')
tas_NH_detr_200yr_RWP_xr = xr.DataArray(data = tas_NH_detr_200yr_RWP, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')
tas_NH_detr_200yr_4000BCE_xr = xr.DataArray(data = tas_NH_detr_200yr_4000BCE, coords = [np.array(tas_NH.lat), np.array(tas_NH.lon)], dims = ['lat', 'lon'], name = 'var167')

# Save to netcdf
tas_NH_detr_200yr_LIA_xr.to_netcdf('tas_NH_detr_200yr_LIA.nc')
tas_NH_detr_200yr_LALIA_xr.to_netcdf('tas_NH_detr_200yr_LALIA.nc')
tas_NH_detr_200yr_3800BCE_xr.to_netcdf('tas_NH_detr_200yr_3800BCE.nc')
tas_NH_detr_200yr_MWP_xr.to_netcdf('tas_NH_detr_200yr_MWP.nc')
tas_NH_detr_200yr_RWP_xr.to_netcdf('tas_NH_detr_200yr_RWP.nc')
tas_NH_detr_200yr_4000BCE_xr.to_netcdf('tas_NH_detr_200yr_4000BCE.nc')



