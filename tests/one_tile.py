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
bbox_long_s = int(bbox_long_s/0.25 + 720)
bbox_long_e = 90
bbox_long_e = int(bbox_long_e/0.25 + 720)

bbox_lat_s = 22.5
bbox_lat_s = int(360-bbox_lat_s/0.25)
bbox_lat_e = 0
bbox_lat_e = int(360-bbox_lat_e/0.25)

# get the data from the netCDF file according to parameters

lons = fh.variables['longitude'][bbox_long_s:bbox_long_e]
lats = fh.variables['latitude'][bbox_lat_s:bbox_lat_e]
time = fh.variables['time'][:]
sm = fh.variables['sm'][day,bbox_lat_s:bbox_lat_e,bbox_long_s:bbox_long_e]
print(str(sm[0,0]))
#sm_noise = fh.variables['sm_noise'][:]

sm_units = fh.variables['sm'].units

fh.close()

# create plot

fig = plt.figure()
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)

# Mercator basemap for entire world

m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, resolution='c', lon_0=0)

# 2D array for basemap

lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data

cs = m.contourf(xi, yi, sm, 10, cmap=plt.cm.Spectral_r)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawcountries()


# Add Colorbar
cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)
cbar.set_label(sm_units)

# Add Title
plt.title('Surface Soil Moisture')

plt.show()