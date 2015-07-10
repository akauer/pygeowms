__author__ = 'akauer'

import numpy as np
from datetime import datetime
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from urlparse import urlparse

# todo: general: split up in functions -get_tile -wms_reader

WMS_ARGUMENTS = ['request', 'bbox', 'cmap', 'layers',
                 'width', 'height', 'transparent', 'time']

url = 'http://127.0.0.1:8001/ESACCI-L3S_SOILMOISTURE-SSMV-COMBINED-1978-2013-fv01.2_3.nc.wms?LAYERS=sm&' \
      'cmap=cpa_SWI_ASCAT_Dataviewer&TIME=2013-12-31T00:00:00&COLORBARRANGE=0.0,1.0&TRANSPARENT=TRUE&' \
      'SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&FORMAT=image%2Fpng&SRS=EPSG%3A4326&' \
      'BBOX=67.5,0,90,22.5&WIDTH=256&HEIGHT=256'

# parse parameter from URL
# todo: request, cmap

query = urlparse(url).query

params = query.split('&')
req = { }
for k in params:
    n, v = k.split('=')
    if n.lower() in WMS_ARGUMENTS:
            req[n.lower()] = v

nc_file = '/media/sf_D/akauer/markus/ESACCI-L3S_SOILMOISTURE-SSMV-COMBINED-1978-2013-fv01.2_3.nc'
fh = Dataset(nc_file, mode='r')

# calculate days from epoch

epoch = datetime.utcfromtimestamp(0)
d = datetime.strptime(req['time'].split('T')[0],'%Y-%m-%d') - epoch

# todo: find closest index in list

bbox_list = req['bbox'].split(',')

bbox_long_s = float(bbox_list[0])
bbox_long_s_i = int(bbox_long_s/0.25 + 720)
bbox_long_e = float(bbox_list[2])
bbox_long_e_i = int(bbox_long_e/0.25 + 720)

bbox_lat_s = float(bbox_list[3])
bbox_lat_s_i = int(360-bbox_lat_s/0.25)
bbox_lat_e = float(bbox_list[1])
bbox_lat_e_i = int(360-bbox_lat_e/0.25)

# get the data from the netCDF file according to parameters

lons = fh.variables['longitude'][bbox_long_s_i:bbox_long_e_i]
lats = fh.variables['latitude'][bbox_lat_s_i:bbox_lat_e_i]
time = fh.variables['time'][:]

# find index of time
day = int(np.where(time == d.days)[0])

sm = fh.variables[req['layers']][day, bbox_lat_s_i:bbox_lat_e_i, bbox_long_s_i:bbox_long_e_i]

#sm_noise = fh.variables['sm_noise'][:]

sm_units = fh.variables['sm'].units

fh.close()

# create plot

# calculate x and y dim in inches of the tile

dpi=80
h, w = float(req['height']), float(req['width'])
dim_x = h/dpi
dim_y = w/dpi
figprops = dict(figsize=(dim_x, dim_y), dpi=dpi, facecolor='white')

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

# get transparent boolean value

if req['transparent'] == 'TRUE':
    trans = True
else:
    trans = False

# save tile

fig.savefig('tile.png', dpi=80, pad_inches=0, transparent=trans)
