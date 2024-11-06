READ ME FILE FOR THE API CODES USED TO DOWNLOAD CDS DATA FROM ECMWF

This code has been implemented in the OSmOSE project. 

I - Getting Started

These codes are used to download data from the CDS (Climate Data Store).
More precisely it can download any hourly single level data since 1940 anywhere in the world.
A list of the variables that can be downloaded is accessible here : https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview
So far, the code has names of variables for surface temperature, u10 and v10 wind speed, total precipitation and wave direction and period.

Adding variables :
Other variables can be added by looking for their correct names in : 
https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=download
After checking the desired variables, click on 'Show API request' and copy the variable list and paste it as the data list in the jupyter notebook.

Getting access to the CDS data requires an account. You can create one here :
https://cds.climate.copernicus.eu/user/login
After your account is created, clicking on the same link above gives you access to the personnal access token that you need to enter in the jupyter notebook. You can also find this information by clicking on your name in the upper right corner.

Make sure all the packages are installed, you can install them using conda in a terminal.


II - Using the Jupyter Notebook

This code is meant to be used locally, not on datamor for example. Both the jupyter notebook and the python script need to be in the same directory. 

The area from where to download data is defined by a 'square' whose borders are the cardinal boundaries.

The filename you define is only attributed to the raw data file downloaded from the cds. Additionnal formatted files are also created.
Downloaded files will be in a zip file located at the indicated path and filename.

If you want to download data in the GRIB format please change the Api_ERA.py file directly by modifying data_format in request.
Otherwise data will be downloaded in netCDF format.

III - Using the downloaded data

The data you have downloaded is three dimensional (space+time). Therefore, it is stored as a 3D numpy array you can read using np.read().
Each individual variable is saved in its own array.
All arrays have the same dimensions and shapes.
One other arrays is saved containing : 'timestamps', 'timestamps_epoch', 'latitude', 'longitude'
To read this stamps.npz array enter the following line : stamps = np.load('stamps.npz')
The line stamps.files will return the arrays stored inside the stamps files (ie. timestamps, timestamps_epoch, latitude, longitude).
To access a desired array, enter for exemple the line stamps['latitude'] or stamps['timestamps_epoch']
timestamps saves time data as a datetime, while timestamps_epoch saves time as an epoch time or the time in seconds since January 1, 1970, 00:00:00 at UTC.
Be advised that latitude data are stored in decreasing order, and longitude data stored in increasing order.
For chosen i,j,k values corresponding to time, latitude and longitude you will have  :
tp[i,j,k] = 3.2 (m/h)
The entire tp array will look like this :
> array([[[8.67361738e-19, 8.67361738e-19, 8.67361738e-19, ...,
         1.02081993e-06, 1.02081993e-06, 5.68742531e-06],
        [8.67361738e-19, 8.67361738e-19, 8.67361738e-19, ...,
         8.67361738e-19, 8.67361738e-19, 4.81243680e-06],
        [8.67361738e-19, 8.67361738e-19, 8.67361738e-19, ...,
         8.67361738e-19, 8.67361738e-19, 1.02081993e-06],
         ...
While stamps will be in the following format :
> timestamps = array([datetime.datetime(2019, 10, 1, 0, 0), ... , datetime.datetime(2019, 10, 8, 2, 0) ])
> latitude = array([ -41., -41.25, ... , -50.25, -50.5 ], dtype=float32)
> longitude = array([ 3.25, 3.5, ... , 11., 11.25 ], dtype=float32)

## Code to plot 2D image of one variable (here u10) :

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

variable_name= 'u10'

if not os.path.exists(os.path.join(path,'api',variable_name+'_'+filename+'.npy')):
print('no ERA data with this variable')
sys.exit()

var1 = np.load(os.path.join(path,'api',variable_name+'_'+filename+'.npy'))
stamps = np.load(os.path.join(path,'api','stamps.npz'), allow_pickle=True)

mat_lat, mat_lon = np.meshgrid(stamps['latitude'],stamps['longitude'])

fig = plt.figure(figsize=(6,5))
if var1.shape[1:]==(1,1):
plt.plot(stamps['timestamps'],var1[:,0,0])
else:
plt.pcolormesh(mat_lon,mat_lat, var1[0,:,:].T, cmap=cm.jet)
plt.title('tp variable at time '+str(stamps['timestamps'][0]))
plt.colorbar()
plt.show()
