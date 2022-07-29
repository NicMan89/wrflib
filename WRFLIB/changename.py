import pandas as pd
import numpy as np
import glob,os

def open_TS(DirPath,dom,pfx):
    dom=int(dom)
    #point=str(point).zfill(3)
    search_criteria = pfx+'.d0'+str(dom)+'.TS'
    q = os.path.join(DirPath, search_criteria)
    LISTNC = sorted(glob.glob(q))
    print("Files number: ",len(LISTNC))
    colnames=['id_ls','ts_hour','id_tsloc','ix','iy','t','q','u','v','psfc','glw','gsw','hfx','lh','tsk','tslb(1)','rainc','rainnc','clw']
    with open(LISTNC[0]) as i:#Apre il primo file .TS
        info=i.readline()[:-1]
    d=info.split(' ')
    f=pd.read_csv(LISTNC[0],sep='\s+',names=colnames,skiprows=1,index_col=False)
    first=np.array(d[-1].replace('_','T'),dtype='M8[ms]').astype('O')
    timets=np.array(f.ts_hour)
    date=np.empty(0,dtype='datetime64[ns]')
    for y in range(len(timets)):
        delta=datetime.timedelta(hours=timets[y])
        date=np.append(date,np.array(first+delta,dtype='datetime64[ns]'))
    f['ts_hour']=date
    return f

def Profile(DirPath,dom,pfx,levels,ext='TH',return_time=False):
    levels=int(levels)
    dom=int(dom)
    #point=str(point).zfill(3)
    search_criteria = pfx+'.d0'+str(dom)+ '.'+ext
    q = os.path.join(DirPath, search_criteria)
    LISTNC = sorted(glob.glob(q))
    colnames=['time']
    for x in range(levels):
        colnames.append('lev '+str(x+1))
    u=pd.read_csv(LISTNC[0],sep='\s+',skiprows=1,names=colnames,index_col=False)
    if not return_time:
        u.drop(u.columns[0],axis=1,inplace=True)
        u=u.to_numpy(dtype=float)
        return u
    else:
        with open(LISTNC[0]) as i:#Apre il primo file di LISTNC
            info=i.readline()[:-1]
        d=info.split(' ')
        first=np.array(d[-1].replace('_','T'),dtype='M8[ms]').astype('O')
        timets=np.array(f.ts_hour)
        date=np.empty(0,dtype='datetime64[ns]')
        for y in range(len(timets)):
            delta=datetime.timedelta(hours=timets[y])
            date=np.append(date,np.array(first+delta,dtype='datetime64[ns]'))
        u.drop(u.columns[0],axis=1,inplace=True)
        u=u.to_numpy(dtype=float)
        return u, date
        
