#continuazione di v2.py
#https://www.cawcr.gov.au/projects/verification/
import matplotlib.pyplot as plt
import os,glob
import numpy as np
import pandas as pd
import datetime

def crosstab(obs_time,obs_var,sim_time,sim_var,S=None,toll=0):
    obs_time=np.array(obs_time,dtype='datetime64[m]').squeeze()
    obs_idx=np.empty(0,dtype=int)
    sim_idx=np.empty(0,dtype=int)
    for x in range(len(obs_time)):
        pos=np.where(obs_time[x]==sim_time)
        if np.any(pos):
            pos=int(pos[0])
            sim_idx=np.append(sim_idx,pos)
            obs_idx=np.append(obs_idx,x)
        else:
            continue
    if S==None:    
        S=np.median(obs_var[obs_idx])
    P=pd.DataFrame(columns=['HIT','MISS','FALSE_ALLARM','CORRECT_NEGATIVE'],index=[len(sim_idx)])
    Nh,Nm,Nfa,Ncn=0,0,0,0
    for x in range(len(sim_idx)):
        if (obs_var[obs_idx[x]]>=S) and (sim_var[sim_idx[x]]-toll>=S):
            Nh+=1
        elif (obs_var[obs_idx[x]]>=S) and (sim_var[sim_idx[x]]+toll<S):
            Nm+=1
        elif (obs_var[obs_idx[x]]<S) and (sim_var[sim_idx[x]]-toll>=S):
            Nfa+=1
        else:
            Ncn+=1
    P['HIT']=Nh/len(sim_idx)
    P['MISS']=Nm/len(sim_idx)
    P['FALSE_ALLARM']=Nfa/len(sim_idx)
    P['CORRECT_NEGATIVE']=Ncn/len(sim_idx)
    return P

def dichotomous(df,method='ETS'):
    if method=='all':
        st=['ETS (default)','FAR','FBIAS','POD','POFD','TS']
        print(st)
        return
    T=int(df.sum().sum())
    Nh=df['HIT']
    Nm=df['MISS']
    Nfa=df['FALSE_ALLARM']
    Ncn=df['CORRECT_NEGATIVE']
    if method=='ETS':
        ref=(Nh+Nfa)*(Nh+Nm)/T
        ETS=(Nh-ref)/(Nh+Nfa+Nm-ref)
        print('Equitable threat score: ',ETS)
        return ETS
    elif method=='FAR':
        FAR=Nfa/(Nh+Nfa)
        print('False allarm ratio: ',FAR)
        return FAR
    elif method=='FBIAS':
        FBIAS=(Nh+Nfa)/(Nh+Nm)
        print('Frequency bias: ',FBIAS)
        return FBIAS
    elif method=='POD':
        POD=Nh/(Nh+Nm)
        print('Probability of detection: ',POD)
        return POD
    elif method=='POFD':
        POFD=Nfa/(Nfa+Ncn)
        print('Probability of false detection: ',POFD)
        return POFD
    elif method=='TS':
        TS=Nh/(Nh+Nm+Nfa)
        print('Threat score: ',TS)
        return TS
    else:
        raise ValueError('Error in input: invalid method')
        return

def continuous(obs_time,obs_var,sim_time,sim_var,method='RMSE'):
    obs_time=np.array(obs_time,dtype='datetime64[m]').squeeze()
    obs_idx=np.empty(0,dtype=int)
    sim_idx=np.empty(0,dtype=int)
    for x in range(len(obs_time)):
        pos=np.where(obs_time[x]==sim_time)
        if np.any(pos):
            pos=int(pos[0])
            sim_idx=np.append(sim_idx,pos)
            obs_idx=np.append(obs_idx,x)
        else:
            continue
    obs=obs_var[obs_idx]
    sim=sim_var[sim_idx]
    if len(obs)!=len(sim):
        raise ValueError('Different size for obs and sim arrays')
        return
    try:
        if method=='scatter':
            m=np.min([sim[0],obs[0]])
            fig,ax=plt.subplots(1,1)
            plt.scatter(sim,obs)
            ax.axline((m, m),slope=1,color='r')
            plt.xlabel('Simulation',fontsize='medium')
            plt.ylabel('Observation',fontsize='medium')
            plt.grid(True)
            return fig
        elif method=='box':
            data={'observation':obs,'simulation':sim}
            fig,ax=plt.subplots(1,1)
            ax.boxplot(data.values(), 0, '')
            ax.set_xticklabels(data.keys())
            plt.grid(True)
            return fig
        elif method=='bias':
            bi=np.mean(sim)/np.mean(obs)
            return bi
        elif method=='MAE':
            mae=np.mean(np.abs(sim-obs))
            return mae
        elif method=='MSE':
            mse=np.mean((sim-obs)**2)
            return mse
        elif method=='RMSE':
            rmse=np.sqrt(np.mean((sim-obs)**2))
            return rmse
        elif method=='MBE':
            mbe=np.mean(sim-obs)
            return mbe
        elif method=='r':
            r=np.sum((sim-np.mean(sim))*(obs-np.mean(obs)))/(np.sqrt(np.sum((sim-np.mean(sim))**2))*np.sqrt(np.sum((obs-np.mean(obs))**2)))
            return r
    except BaseException as err:
        message=f"Unexpected {err=}, {type(err)=}"
    else:
        raise ValueError(message)
        return
    