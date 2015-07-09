__author__ = 'akauer'

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid


nc_file = '/media/sf_D/akauer/markus/ESACCI-L3S_SOILMOISTURE-SSMV-COMBINED-1978-2013-fv01.2_3.nc'
fh = Dataset(nc_file, mode='r')

# specific parameters for testing

day = 12852  # 2013-12-31

bbox_long_s = 67.5
bbox_long_s_i = int(bbox_long_s/0.25 + 720)
bbox_long_e = 90
bbox_long_e_i = int(bbox_long_e/0.25 + 720)

bbox_lat_s = 22.5
bbox_lat_s_i = int(360-bbox_lat_s/0.25)
bbox_lat_e = 0
bbox_lat_e_i = int(360-bbox_lat_e/0.25)

# get the data from the netCDF file according to parameters

lons = fh.variables['longitude'][bbox_long_s_i:bbox_long_e_i]
lats = fh.variables['latitude'][bbox_lat_s_i:bbox_lat_e_i]
time = fh.variables['time'][:]
sm = fh.variables['sm'][day,bbox_lat_s_i:bbox_lat_e_i,bbox_long_s_i:bbox_long_e_i]
print(str(sm.shape))
#sm_noise = fh.variables['sm_noise'][:]

sm_units = fh.variables['sm'].units

fh.close()

# create plot
figprops = dict(figsize=(3.2, 3.2), dpi=80, facecolor='white')

fig = plt.figure(1,**figprops)
ax = fig.add_axes([0, 0, 1, 1])
# Mercator basemap for entire world

m = Basemap(projection='merc', llcrnrlat=bbox_lat_e, urcrnrlat=bbox_lat_s, llcrnrlon=bbox_long_s,
            urcrnrlon=bbox_long_e, resolution='c', lon_0=0, ax=ax)

# 2D array for basemap

lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data

cs = m.contourf(xi, yi, sm, 10, cmap=plt.cm.Spectral_r)
plt.axis('off')
fig.savefig('tile.png', dpi=80, pad_inches=0, transparent=True)
