 WRFLIB
=============

WRFLIB is a Python package that contains a set of functions, developed to help WRF-ARW output in the post-processing phase.

## Installation
```shell
pip install git+https://github.com/NicMan89/wrflib.git
```

## prime
### open_wrfout (Dirpath, dom, varout=1)
#### input:
<p> 
<ul>
<li>Dirpath is a path to the WRF-ARW output NetCDF data,</li>
<li>dom must be a integer and indicate the WRF domain to be analyzed,</li>
<li>varout (optional) must be only one of the following values (default=1): 1, 3 or 0.</li>
</ul>

#### output:
<p>
Depends of varout. 1 returns list of WRF-ARW NetCDF files data (datetime ordered);
3 add at the previous output, latitude and longitude 2d numpy.array (XLAT, XLONG
variables); 0 return a dict wich contains: the first 3 output described above, latitude and
longitude in 1d numpy.array, vertical bottom to top grid dimension and the domain used for
the analysis.

### jointime (LISTNC)
#### input:
<p> 
<ul>
<li>LISTNC must be an ordered list of a WRF-ARW NetCDF output files.</li>
</ul>

#### output:
<p>
The function performs a union of the Time variable from each input file in LISTNC,
and returns a 1d numpy.array data type datetime64[m].

### j2t_3d (LISTNC, var)
#### input:
<p>
<ul>
<li>LISTNC must be an ordered list of a WRF-ARW NetCDF output files,</li>
<li>var must be a string indicating one WRF-ARW output variable 3d (see WRF-ARW
user guide).</li>
</ul>

#### output:
<p>
The function performs a union (over time dimension) from each input file in LISTNC, and
returns a 3d numpy.array.

### j2t_4d (LISTNC, var)
#### input:
<p>
<ul>
<li>LISTNC must be a ordered list of a WRF-ARW NetCDF output files,</li>
<li>var must be a string indicating one WRF-ARW output variable 4d (see WRF-ARW user guide) or ‘z’ for compute the model height for mass grid [m].</li>
</ul>

#### output:
<p>
The function performs a union (over time dimension) from each input file in LISTNC, and
returns a 4d numpy.array.

### nearestcell_fp (LAT, LON)
#### input:
<p>
<ul>
<li>LAT and LON are the geographic coordinates of a generic point of interest. The
function only works with lats and lons outputs from open_wrfout (global variable).</li>
</ul>

#### output:
<p>
Return positional indexes for the cell closest to the input point in WRF-ARW domain
to south-north and west-east dimension. It also returns the distance in km between
input point and the center of the nearest cell mass grid.

### wrfrun_info (LISTNC, varlist=’’)
#### input:
<p>
<ul>
<li>LISTNC must be a ordered list of a WRF-ARW NetCDF output files,</li>
<li>varlist should be a unique string with different WRF-ARW output variables.</li>
</ul>

#### output:
<p>
Return different information about WRF specific run: start time simulation, end time
simulation, current study domain, latitude and longitude length and boundary, number
of vertical levels, available variables list, and metadata for each variable in varlist if
present (default value of varlist is empty).

### SpatCutBox (var, latlim, lonlim)
#### input:
<p> 
<ul>
<li>var must be a 3d or 4d numpy.array contains one variable from a WRF-ARW output, in each case the last two dimensions of var must be spatial dimension (usually latitude and longitude),</li>
<li>latlim and lonlim must be a list of 2 numeric elements, respectively the smallest and biggest boundary box limits.</li>
</ul>

#### output:
<p>
Returns a numpy.array with the same shape as the input array var. The output array
will have nan values out of the box identified by latlim and lonlim.

### SpatCutVect (LISTNC, var, gdf, flag=True)
#### input:
<p>
<ul>
<li>LISTNC must be a ordered list of a WRF-ARW NetCDF output files,</li>
<li>var must be a 2d, 3d or 4d numpy.array contains one variable from WRF-ARW output, in each case the last two dimensions of var must be spatial dimension (usually latitude and longitude),</li>
<li>gdf must be a geopandas GeoDataFrame used to cut the WRF-ARW variable in var,</li>
<li>flag (optional, default = True) used to decide the function output(s), must be boolean data type.</li>
</ul>

#### output:
<p>
Returns a numpy.array with the same shape as the input array var. The output array
will have nan values out of the polygon identified by gdf.geometry. If flag input is set
to True, is also returned a 2d boolean numpy.array to use as a mask for other cuts.

### SpatRepFromWRF (LISTNC, gdf, flag=2)
#### input:
<p>
<ul>
<li>LISTNC must be a ordered list of a WRF-ARW NetCDF output files,</li>
<li>gdf must be a geopandas GeoDataFrame to reprojected in the WRF-ARW custom projection,</li>
<li>flag (optional, default=2) used to decide the function output(s), must be set to 2 or 1 or -1.</li>
</ul>

#### output:
<p>
if flag is set to 2, the function returns the reprojected GeoDataFrame, and the
WRF-ARW projection string. Else if flag is set to 1 the function returns only a
reprojected GeoDataFrame. If flag is set to -1 the function returns only a WRF-ARW
projection string.

## TimeSeries
### open_TS (DirPath, dom, point)
#### input:
<p>
<ul>
<li>Dirpath is the path to the WRF-ARW output tslist files,</li>
<li> dom must be a integer and indicate the WRF domain to be analyzed,</li>
<li>pfx is the string matching the pfx column in the tslist file. pfx must be a string.</li>
</ul>

#### output:
<p>
Return a pandas.DataFrame with 19 columns: grid ID, time in datetime64[ns] data type, time series ID, grid location (nearest grid to the weather station), 2 m Temperature (K), 2 m vapor mixing ratio (kg/kg), 10 m U wind (earth-relative), 10 m V wind (earth-relative), surface pressure (Pa), downward longwave radiation flux at the ground (W/m^2, downward is positive), net shortwave radiation flux at the ground (W/m^2, downward is positive), surface sensible heat flux (W/m^2, upward is positive), surface latent heat flux (W/m^2, upward is positive), skin temperature (K), top soil layer temperature (K), rainfall from a cumulus scheme (mm), rainfall from an explicit scheme (mm), total column-integrated water vapor and cloud variables. 

### Profile (DirPath, dom, pfx, levels, ext='TH', return_time=False)
#### input:
<p>
<ul>
<li>Dirpath is the path to the WRF-ARW output tslist files,</li>
<li>dom must be a integer and indicate the WRF domain to be analyzed,</li>
<li>pfx is the string matching the pfx column in the tslist file. pfx must be a string,</li>
<li>levels indicates the number of the grid dimension from bottom to top, must be an integer,</li>
<li>ext indicate the file extension to be read, the options available are: TH (default), UU, VV, WW, PH, PR, QV,</li>
<li>return_time is a flag that adds the numpy.array time to the result, the default is False.</li>
</ul>

#### output:
<p>
With return_time set to False, the function returns a numpy.array 2d which contains the vertical profile values ​​provided by the input extension, for each time step. For return_time set to True the function adds the numpy.array time at the previous result.

## Mver
### crosstab (obs_time, obs_var, sim_time, sim_var, S=None, toll=0)
#### input:
<p>
<ul>
<li>obs_time must be a numpy.array that contains the time values ​​of an observed variable to be analyzed (related to obs_var),</li>
<li>obs_var must be a numpy.array that contains the values of an observed variable, related to obs_time,</li>
<li>sim_time must be a numpy.array that contains the time values of a WRF-ARW simulation,</li>
<li>sim_var must be a numpy.array that contains the values of a WRF-ARW output variable (related to sim_time and obs_var, with the same units as the last one),</li>
<li>S must be a float or an integer value to provide a threshold used to compute the contingency table in output. Default value is None, in this case S will be set to be equal to the median value of the obs_var array (in the same units as obs_var and sim_var),</li> 
<li>toll specifies a tollerance value and must be a float or an integer data type (in the same units as obs_var and sim_var). This value will be added and subtracted in each value of a sim_var array. The default value is 0.
</ul>

#### output:
<p>
The result is a pandas.Dataframe that contains the percentage of the HIT, FALSE ALARM, MISS and CORRECT NEGATIVE values ​​of the contingency table, relative to the input threshold and the tolerance value.

### dichotomous (df, method='ETS')
#### input:
<p>
<ul>
<li>df must be the pandas.Dataframe from crosstab function described above,</li>
<li>method must be an available string, and indicate the dichotomous verification method to be compute for the output. The default value is ETS.</li>
</ul>

#### output:
<p>Depend to the specified method: ETS is a equitable threat score (Gilbert skill score), FAR is a false alarm ratio, FBIAS is a frequency bias, POD is a probability of detection (hit rate), POFD is a probability of false detection (false alarm rate) and TS is a threat score.

### continuous (obs_time, obs_var, sim_time, sim_var, method='RMSE')
#### input:
<p>
<ul>
<li>obs_time must be a numpy.array that contains the time values ​​of an observed variable to be analyzed (related to obs_var),</li>
<li>obs_var must be a numpy.array that contains the values of an observed variable, related to obs_time,</li>
<li>sim_time must be a numpy.array that contains the time values of a WRF-ARW simulation,</li>
<li>sim_var must be a numpy.array that contains the values of a WRF-ARW output variable (related to sim_time and obs_var, with the same units as the last one),</li>
<li>method must be an available string, and indicate the verification method to be compute for the output. The default value is RMSE.</li>
</ul>

#### output:
<p>Depend to the specified method: RMSE is the root mean square error, scatter return a scatter plot figure, box return a box plot figure, MAE is the mean absolute error, MSE is the mean square error, MBE is the mean bias error, r is the correlation coefficient and at last bias is a deviation of the expected value. 

## Appendix links
[Forecast Verification methods Across Time and Space Scales](https://www.cawcr.gov.au/projects/verification/)

[WRF-ARW 4.3 user guide](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.3/contents.html)

[WRF-ARW 4.3 README.tslist](https://github.com/wrf-model/WRF/blob/master/run/README.tslist)