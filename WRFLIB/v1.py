import matplotlib.pyplot as plt
import os,glob
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from geopy import distance
import datetime
import re
import xarray as xr
import cartopy.crs as crs
#from cartopy.feature import NaturalEarthFeature
from matplotlib.cm import get_cmap
import pyproj

def _coords_(var):#----- AUSILIARIA VERIFICATA
    ncfile=xr.open_dataset(LISTNC[0])
    T=ncfile.variables[var].values
    cc=[]
    for x in list(ncfile.coords):
        y=ncfile.variables[x]
        if y.shape[-2:]==T.shape[-2:]:
            cc.append(x)
            continue
        else:
            continue
    lat=ncfile.variables[cc[0]].values.squeeze()
    lon=ncfile.variables[cc[1]].values.squeeze()
    return lat,lon

def _initvar_(var):#----- AUSILIARIA VERIFICATA
    ncfile=xr.open_dataset(LISTNC[0])
    dims=list(ncfile.variables[var].dims)
    Dsize=[]
    for x in range(len(dims)):
        if dims[x]=='Time':
            Dsize.append(0)
            continue
        Dsize.append(ncfile[dims[x]].size)
    T=np.empty(Dsize[:],dtype=float)
    return T

def _initvarB_(var):#----- AUSILIARIA VERIFICATA
    if len(var.shape)==2:
        T=np.empty([var.shape[0],var.shape[1]])
    elif len(var.shape)==3:
        T=np.empty([var.shape[0],var.shape[1],var.shape[2]])
    elif len(var.shape==4):
        T=np.empty([var.shape[0],var.shape[1],var.shape[2],var.shape[3]])
    return T


def open_wrfout(DirPath,dom,varout=1): #----- VERIFICATA
    # varout must be int (1,3,0)
    dom=int(dom)
    global LISTNC
    global lats
    global lons
    global latss
    global lonss
    global search_criteria
    global vert_lev
    search_criteria = "wrfout_d0"+str(dom)+"*"
    q = os.path.join(DirPath, search_criteria)
    LISTNC = sorted(glob.glob(q))
    ncfile=xr.open_dataset(LISTNC[0])
    vert_lev=ncfile.attrs['BOTTOM-TOP_GRID_DIMENSION']
    lats=ncfile.variables['XLAT'][0,:,:].values.squeeze()
    lons=ncfile.variables['XLONG'][0,:,:].values.squeeze()
    latss=np.array(lats).reshape(lats.size)
    lonss=np.array(lons).reshape(lons.size)
    D={'LISTNC':LISTNC,'lats':lats,'lons':lons,'latss':latss, 'lonss':lonss, 'vert_lev':vert_lev,'domain':dom}
    if varout==1:
        return LISTNC
    elif varout==3:
        return LISTNC, lats, lons
    elif varout==0:
        return D
    else:
        raise ValueError('Error in input: varout must be 0,1,3 (default = 1)')


def jointime(LISTNC): #-----VERIFICATA
    WRFdate2=np.empty(0,dtype='datetime64[m]')
    for x in range(len(LISTNC)):
        ncfile=xr.open_dataset(LISTNC[x])
        time=ncfile.variables['XTIME']
        WRFdate2=np.append(WRFdate2,time.values)
    return WRFdate2


def join2time_var3d(LISTNC,var,varout=1):#-----NEW VERIFICATA....DA VERICARE NEI PLOT
    Twrf2=_initvar_(var)
    if len(Twrf2.shape) != 3:
        raise ValueError('Error in input: incorrect var')
    for x in range(len(LISTNC)):
        ncfile=xr.open_dataset(LISTNC[x])
        T=ncfile.variables[var]
        if len(T.shape)==3:
            Twrf2=np.append(Twrf2,np.atleast_3d(T.values),axis=0)
        elif len(T.shape)==2:
            Twrf2=np.append(Twrf2,[T.values[:,:]],axis=0)
    if varout==3:
        lat,lon=_coords_(var)
        return Twrf2,lat,lon
    elif varout==1:
        return Twrf2
    else:
        raise ValueError('Error in input: varout must be 1 or 3')


def join2time_var4d(LISTNC,var,varout=1):#-----NEW VERIFICATA....DA VERICARE NEI PLOT
    #(PB + PHB)/g
    if var=='z':
        Z=_initvar_('PH')
    else:
        Z=_initvar_(var)
    if len(Z.shape) != 4:
        raise ValueError('Error in input: incorrect var')
    for x in range(len(LISTNC)):
        ncfile=xr.open_dataset(LISTNC[x])
        if var=='z':
            ph=ncfile.variables['PH']
            phb=ncfile.variables['PHB']
            z=(ph+phb)/9.81
        else:
            z=ncfile.variables[var]
        if len(z.shape)==4:
            Z=np.append(Z,np.atleast_3d(z.values),axis=0)
        elif len(z.shape)==3:
            Z=np.append(Z,[z.values[:,:,:]],axis=0)
    if varout==3:
        if var=='z':
            lat,lon=_coords_('PH')
        else:
            lat,lon=_coords_(var)
        return Z,lat,lon
    elif varout==1:
        return Z
    else:
        raise ValueError('Error in input: varout must be 1 or 3')


def nearcell_frompoint(LAT,LON): #----- NEW VERIFICATA
    latss=np.array(lats).reshape(lats.size)
    lonss=np.array(lons).reshape(lons.size)
    dist=np.ones(lats.shape[0]*lons.shape[1])
    point1=(LAT,LON)
    for w in range(len(dist)):
        point2=(latss[w],lonss[w])
        dist[w]=distance.distance(point1,point2).km
    dist=dist.reshape(lats.shape[0],lons.shape[1])
    dist=np.abs(dist)
    indexlatF,indexlonF=np.where(dist==np.min(dist))
    DF=dist[indexlatF,indexlonF]
    return indexlatF,indexlonF,DF


def wrfrun_info(LISTNC,varlist=''):
    #varlist: unique str with comma separate for each variable
    WRFdate=jointime(LISTNC)
    ncfile=xr.open_dataset(LISTNC[0])
    print('----------------------------\n')
    print('Start time: ',WRFdate[0],'\tEnd time: ',WRFdate[-1],'\n')
    print('Current domain: ',search_criteria,'\n')
    print('Latitude dim, Longitude dim: ',lats.shape,'\n')
    print('Lat max, min value: ',np.max(lats),' ',np.min(lats),'\n')
    print('Lon max, min value: ',np.max(lons),' ',np.min(lons),'\n')
    print('Vertical levels: ',ncfile.attrs['BOTTOM-TOP_GRID_DIMENSION'],'\n')
    if len(varlist)==0:
        print('Variables list:\n\n',str(list(ncfile.variables)))
        return
    else:
        varia=varlist.split(',')
        for x in range(len(varia)):
            print('\n',ncfile.variables[varia[x].strip()])


def spat_CutFromBox(var,latlim,lonlim):#---- NEW VERIFICATA
    loncut=(lons>=lonlim[0])&(lons<=lonlim[1])
    latcut=(lats>=latlim[0])&(lats<=latlim[1])
    cut=np.array(loncut*latcut)
    if (np.unique(np.min(lats))[0]>latlim[0]) | (np.unique(np.max(lats))[0]<latlim[1]) | (np.unique(np.min(lons))[0]>lonlim[0]) | (np.unique(np.max(lons))[0]<lonlim[1]):
        raise ValueError('Latitude or Longitude boundary out of range')
    if len(var.shape)==3:
        OU=_initvarB_(var)*np.nan
        cut=np.tile(cut,[var.shape[0],1,1])
        OU[cut==True]=var[cut==True]
        return OU
    elif len(var.shape)==4:
        OU=_initvarB_(var)*np.nan
        cut=np.tile(cut,[var.shape[0],var.shape[1],1,1])
        OU[cut==True]=var[cut==True]
        return OU
    else:
        raise ValueError('Array var must be 3d or 4d')


def spat_ReprojectFromWRF(LISTNC,gdf,flag=2): #----- DA VERIFICARE
    ncfile=xr.open_dataset(LISTNC[0])
    map_proj = int(ncfile.MAP_PROJ)
    # Lambert Conformal Conic
    if map_proj == 1:
        wrf_proj = pyproj.Proj(proj='lcc',units='m',a=6370000,b=6370000,
            lat_1=ncfile.TRUELAT1,
            lat_2=ncfile.TRUELAT2,
            lat_0=ncfile.MOAD_CEN_LAT,
            lon_0=ncfile.STAND_LON,)
    # Polar Stereographic
    elif map_proj == 2:
        hemi = -90.0 if ncfile.TRUELAT1 < 0 else 90.0
        wrf_proj = pyproj.Proj(proj='stere',units='m',a=6370000,b=6370000,
            lat_0=hemi,
            lon_0=ncfile.STAND_LON,
            lat_ts=ncfile.TRUELAT1,)
    # Mercator
    elif map_proj == 3:
        wrf_proj = pyproj.Proj(proj='merc',units='m',a=6370000,b=6370000,
            lon_0=ncfile.STAND_LON,
            lat_ts=ncfile.TRUELAT1,)
    # Latlong - Equidistant Cylindrical
    elif map_proj == 6:
        wrf_proj = pyproj.Proj(proj='eqc',units='m',a=6370000,b=6370000,
            lon_0=ncfile.STAND_LON,)
    if flag==2:
        gdf1=gdf.to_crs('EPSG:4326')#str(wrf_proj)
        return gdf1,str(wrf_proj)
    elif flag==1:
        gdf1=gdf.to_crs('EPSG:4326')#str(wrf_proj)
        return gdf1
    elif flag==-1:
        return str(wrf_proj)
    else:
        raise ValueError('Error in input: flag must be -1,1,2 (default = 2)')


def spat_CutFromVect(LISTNC,var,gdf,flag=True): 
    #----- NEW DA VERIFICARE la proiezione con 4326 sembra funzioni meglio
    '''
    ncfile is a xarray DataFrame, var is a xarray DataArray
    varcut is a xarray DataArray with np.nan outside the polygon in gdf
    '''
    if gdf.crs!='epsg:4326':
        print('GeoDataFrame Reprojection...')
        gdf=gdf.to_crs('epsg:4326')
    if len(var.shape)>4 or len(var.shape)<2:
        raise Exception(f'Error in variable shape length: len(var.shape)={len(var.shape)} expect 2, 3 or 4 ')
    
    #lat,lon=_coords_(var)
    shape=lats.shape
    lat=lats.reshape(lats.size)
    lon=lons.reshape(lats.size)
    pin=[]#posizione dei punti interni al poligono
    cells=int(lat.size)
    for cell in range(cells):
        point=Point(lon[cell],lat[cell])
        if gdf.geometry.contains(point)[0]==True:
            pin.append(cell)
        else:
            continue
    cut=np.ones(len(lat))*np.nan
    cut[pin]=1
    cut=cut.reshape(shape[0],shape[1])
    if len(var.shape)==2:
        varcut=var*cut
    elif len(var.shape)==3:
        varcut=var*cut[None,:,:]
    elif len(var.shape)==4:
        varcut=var*cut[None,None,:,:]
    if flag:
        return varcut,cut
    else:
        return varcut
        
