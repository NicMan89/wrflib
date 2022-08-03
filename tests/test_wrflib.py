import WRFLIB

from WRFLIB.prime import (
    open_wrfout, jointime, j2t_3d, j2t_4d, nearestcell_fp, wrfrun_info, SpatCutBox, SpatCutVect, SpatRepFromWRF)

from WRFLIB.Mver import (
    crosstab, dichotomous, continuous)

from WRFLIB.TimeSeries import(
    open_TS, Profile)

import sys
import numpy as np
import pandas as pd
import geopandas as gpd

IN=r"/home/nicola/Scrivania/test/"

#open_wrfout
Dictionary=open_wrfout(IN,1,varout=0)
files0,lats0,lons0=open_wrfout(IN,1,varout=3)
files=open_wrfout(IN,1)
assert len(files)==len(files0)==1, 'Error in open_wrfout'
print('open_wrfout test successed...')

#jointime
date=jointime(files)
assert len(date)==1, 'Error in jointime'
print('jointime test successed...')

#j2t_3d
T0,lats,lons=j2t_3d(files,'T2',varout=3)
T=j2t_3d(files,'T2')
assert (len(T.shape)==3 and np.unique(T0==T)), 'Error in j2t_3d var'
assert (np.unique(lats==lats0) and np.unique(lons==lons0)), 'Error in j2t_var3d varout=3'
print('j2t_3d test successed...')

#j2t_4d
P0,latsp,lonsp=j2t_4d(files,'P',varout=3)
V,latsw,lonsw=j2t_4d(files,'V',varout=3)
P=j2t_4d(files,'P')
z=j2t_4d(files,'z')
assert (len(P.shape)==4 and np.unique(P0==P)), 'Error in j2t_4d var'
assert (len(z.shape)==len(V.shape)==len(P.shape)), 'Error in j2t_4d var'
assert (np.unique(lats==latsp) and np.unique(lons==lonsp)), 'Error in j2t_var4d varout=3'
assert (np.unique(latsw!=lats) and np.unique(lonsw!=lons)),'Error in j2t_4d spatial coordinates'
print('j2t_4d test successed...')

#nearestcell_fp
Coord=[51.5049,-0.1311]
indexlat,indexlon,D=nearestcell_fp(Coord[0],Coord[1])
assert (int(indexlat)<=int(T.shape[1])) and (int(indexlon)<=int(T.shape[2])), 'Error index in nearestcell_fp'
print('nearestcell_fp test successed...')

#SpatCutBox
latlim=[50,52]
lonlim=[-1,.1]
Tcut=SpatCutBox(T,latlim,lonlim)
Pcut=SpatCutBox(P,latlim,lonlim)
assert Tcut.shape==T.shape,'Error in SpatCutBox shape 3d'
assert np.unique(Tcut[0,:,:]).size!=0, 'Error in SpatCutBox cut 3d'
assert Pcut.shape==P.shape,'Error in SpatCutBox shape 4d'
assert np.unique(Pcut[0,0,:,:]).size!=0, 'Error in SpatCutBox cut 4d'
print('SpatCutBox test successed...')

#SpatCutVect
gla_dir=r"/home/nicola/Scrivania/test/UNIBoroughs.gpkg"
gdf=gpd.read_file(gla_dir)
Tcut,mask=SpatCutVect(files,T,gdf)
Tcut2=SpatCutVect(files,T,gdf,flag=False)
assert Tcut2.shape==Tcut.shape==T.shape,'Error in SpatCutVect shape 3d'
assert np.unique(Tcut[0,:,:]).size!=0, 'Error in SpatCutBox cut 3d'
assert np.unique(Tcut2[0,:,:]).size!=0, 'Error in SpatCutBox cut 3d flag False'
Pcut,mask0=SpatCutVect(files,P,gdf)
Pcut2=SpatCutVect(files,P,gdf,flag=False)
assert Pcut2.shape==Pcut.shape==P.shape,'Error in SpatCutVect shape 4d'
assert np.unique(Pcut[0,:,:]).size!=0, 'Error in SpatCutBox cut 4d'
assert np.unique(Pcut2[0,:,:]).size!=0, 'Error in SpatCutBox cut 4d flag False'
m=np.where(mask==1)
m0=np.where(mask0==1)
assert np.unique(np.array(m)==np.array(m0)), 'Error in mask cut --3d vs 4d--'
print('SpatCutVect test successed...')

#SpatRepFromWRF
gdf1,wrf_crs=SpatRepFromWRF(files,gdf,flag=2)
gdf2=SpatRepFromWRF(files,gdf1,flag=1)
wrf_crs2=SpatRepFromWRF(files,gdf2,flag=-1)
assert gdf1.crs=='epsg:4326', 'Error in gdf reprojection flag 2'
assert gdf2.crs=='epsg:4326', 'Error in gdf reprojection flag 1'
assert wrf_crs==wrf_crs2, 'Error in wrf_crs flag -1'
print('SpatRepFromWRF test successed...')

#open_TS
TS=open_TS(IN,3,'T001')
assert TS.shape==(155520, 19), 'Error in open_TS'
print('open_TS test successed...')

#Profile
u=Profile(IN,1,'T009',51,ext='UU',return_time=False)
u0,date=Profile(IN,1,'T009',51,ext='UU',return_time=True)
assert np.unique(u==u0), 'Error in Profile'
print('Profile test successed...')

#crosstab
obs_dir=r"/home/nicola/Scrivania/test/StJames2020.csv"
sim_var=np.array(TS.t)-273.15
sim_time=np.array(TS.ts_hour)
p=pd.read_csv(obs_dir,header=280)
p=p[:-1]
obs_time=np.array(p.ob_time,dtype='datetime64')
obs_var=np.array(p.air_temperature)
df=crosstab(obs_time,obs_var,sim_time,sim_var,S=30,toll=0.5)
assert (df.size==4 and df.index==144 and df.sum(axis=1)[144]==1), 'Error in crosstab'
print ('crosstab test successed...')

#dichotomous(df,method='ETS'):
j=dichotomous(df,method='ETS')
assert (-.3<=j.values<=1), 'Error in dichotomous, ETS'
j=dichotomous(df,method='FAR')
assert (0<=j.values<=1), 'Error in dichotomous, FAR'
j=dichotomous(df,method='FBIAS')
assert (0<=j.values), 'Error in dichotomous, FBIAS'
j=dichotomous(df,method='POD')
assert (0<=j.values<=1), 'Error in dichotomous, POD'
j=dichotomous(df,method='POFD')
assert (0<=j.values<=1), 'Error in dichotomous, POFD'
j=dichotomous(df,method='TS')
assert (0<=j.values<=1), 'Error in dichotomous, TS'
print('\ndichotomous test successed...')

#continuous
r=continuous(obs_time,obs_var,sim_time,sim_var,method='RMSE')
assert (r>=0), 'Error in continuous, RMSE' 
r=continuous(obs_time,obs_var,sim_time,sim_var,method='scatter')
r=continuous(obs_time,obs_var,sim_time,sim_var,method='box')
r=continuous(obs_time,obs_var,sim_time,sim_var,method='bias')
r=continuous(obs_time,obs_var,sim_time,sim_var,method='MAE')
assert (r>=0), 'Error in continuous, MAE' 
r=continuous(obs_time,obs_var,sim_time,sim_var,method='MSE')
assert (r>=0), 'Error in continuous, MSE' 
r=continuous(obs_time,obs_var,sim_time,sim_var,method='MBE')
r=continuous(obs_time,obs_var,sim_time,sim_var,method='r')
assert (-1<=r<=1), 'Error in continuous, r'
print('continuous test successed...')

#
print('\n__________________\nversion:\t'+sys.version)