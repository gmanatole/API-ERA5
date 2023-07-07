import cdsapi
from datetime import date, datetime
import os
import calendar
from tqdm import tqdm
from netCDF4 import Dataset
import numpy as np
import pandas as pd

get_epoch_time = lambda x : calendar.timegm(x.timetuple()) if isinstance(x, datetime) else x

def make_cds_file(key, udi, path):
	os.chdir(os.path.expanduser("~"))
	try :
 	   os.remove('.cdsapirc')
	except FileNotFoundError :
	    pass

	cmd1 = "echo url: https://cds.climate.copernicus.eu/api/v2 >> .cdsapirc"
	cmd2 = "echo key: {}:{} >> .cdsapirc".format(udi, key)
	os.system(cmd1)
	os.system(cmd2)



	if path == None:
		try :
		   os.mkdir('api')
		except FileExistsError:
		    pass
		path_to_api = os.path.join(os.path.expanduser("~"), "api/")
	else :
		try :
		   os.mkdir(path+'api')
		except FileExistsError:
		    pass
		path_to_api = os.path.join(path, 'api')

	os.chdir(path_to_api)
	os.getcwd()



def return_cdsapi(filename, key, variable, year, month, day, time, area):

  filename = filename + '.nc'

  c = cdsapi.Client()
  
  if day == 'all':
    day = ['01', '02', '03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
  if month == 'all':
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
  if time == 'all':
    time = ['00:00','01:00','02:00','03:00','04:00','05:00','06:00','07:00','08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']

  r = c.retrieve('reanalysis-era5-single-levels',
            {
              'product_type' : 'reanalysis',
              'variable' : variable,
              'year' : year,
              'month' : month,
              'day' : day,
              'time' : time,
              'area' : area,
              'format' : 'netcdf',
              'grid':[0.25, 0.25],
            },
            filename,
            )
  r.download(filename)



def format_nc(filename):

  downloaded_cds = filename + '.nc'
  fh = Dataset(downloaded_cds, mode='r')

  variables = list(fh.variables.keys())[3:]
  single_levels = np.zeros((len(variables), fh.dimensions.get('time').size, fh.dimensions.get('latitude').size, fh.dimensions.get('longitude').size))

  lon = fh.variables['longitude'][:]
  lat = fh.variables['latitude'][:]
  time_bis = fh.variables['time'][:]
  for i in range(len(variables)):
    single_levels[i] = fh.variables[variables[i]][:]

  time_units = fh.variables['time'].units

  def transf_temps(time) :
    time_str = float(time)/24 + date.toordinal(date(1900,1,1))
    return date.fromordinal(int(time_str))

  time_ = list(time_bis)

  data = pd.DataFrame()
  data['time'] = time_
  data['time'] = data['time'].apply(lambda x : transf_temps(x))
  hours = np.array(time_)%24
  dates = np.array([datetime(elem.year, elem.month, elem.day, hour) for elem, hour in list(zip(data['time'], hours))])

  return dates, lon, lat, single_levels, variables



def save_results(dates, lat, lon, single_levels, variables, filename):
	for i in range(len(variables)):
		np.save(variables[i]+'_'+filename, np.ma.filled(single_levels[i], fill_value=float('nan')), allow_pickle = True)

	np.savez('stamps', timestamps = np.array(dates), timestamps_epoch = np.array(list(map(get_epoch_time, np.array(dates)))), latitude = np.array(lat), longitude = np.array(lon))
#	np.save('timestamps.npy', np.array(dates))
#	np.save('latitude.npy', np.array(lat))
#	np.save('longitude.npy', np.array(lon))
#	np.save('timestamps_epoch.npy', np.array(list(map(get_epoch_time, np.array(dates)))))
#	stamps = np.zeros((len(dates), len(lat), len(lon), 3), dtype=object)
#	for i in range(len(dates)):
#		for j in range(len(lat)):
#			for k in range(len(lon)):
#				stamps[i,j,k] = [dates[i], lat[j], lon[k]]
#	np.save('stamps_'+filename, stamps, allow_pickle = True)




def final_creation(df1, filename, key, variable, year, month, day, time, area) :
  return_cdsapi(filename, key, variable, year, month, day, time, area)
  with tqdm(total = 100) as pbar :
    pbar.update(33)
    dates, lon, lat, single_levels, variables = format_nc(filename)
    pbar.update(33)
    test = save_results(dates, lat, lon, single_levels, variables, filename)
    pbar.update(33)
  return test

