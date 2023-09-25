# -*- coding: utf-8 -*-
"""EarthQuake-Faradilah Ade.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TkzS_7a9snkfMil-DXMvgJIq-yLuN3kO
"""

import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from scipy.stats import norm
import seaborn as sns; sns.set(style = 'whitegrid')
from scipy.stats import genpareto
import scipy.special as sm
import math as mt
from scipy import stats
import time
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/Data Workshop/Data/raw_data_qgis.csv')

df['magType'].unique()

def conversion(row):
  if row['magType'] == 'mb':
    m = 1.0107*row['mag']+0.0801
  elif row['magType'] == 'ms' and 2.8 <= row['mag']<=6.1:
    m = 0.6016*row['mag']+2.4760
  elif row['magType'] == 'ms' and 6.2 <= row['mag']<=8.7:
    m = 0.9239*row['mag']+0.5671
  elif row['magType'] == 'md' :
    m = 0.7170*row['mag']+1.003
  else:
    m = row['mag']
  return m


df['mag'] = df.apply(conversion, axis =1)
df['magType'] = df['magType'].replace(['mb','mww','mwb','mwc','ms'],'mw')

from math import sin, cos, sqrt, atan2, radians, asin

def distance(lat_1,lon_1,lat_2,lon_2):
  R = 6371.08 #Radius bumi

  lat1 = radians(lat_1)
  lon1 = radians(lon_1)
  lat2 = radians(lat_2)
  lon2 = radians(lon_2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  #rumus heaversine
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1-a))

  return R*c

#membuat sebuah fungsi untuk mencaril setiap nilal unik di suatu array dikembalikan menjadi list
def unique(list1):
  x = np.array(list1)
  r = np.unique(x).tolist()
  return r

def declustering(df):
  df['mag']=df.apply(conversion, axis=1)
  df = df.sort_values(by=['mag'],ascending=False, ignore_index=True)
  df['time']=pd.to_datetime(df['time'], format='%Y/%m/%d %H:%M:%S')
  df['month']=df['time'].dt.month
  df['year']=df['time'].dt.year
  df['date']=df['time'].dt.date
  nonmain = [] #Array untuk menampung gempa bumi yang bukan mainshock
  for i in range (len(df)-1): #Nama dataset disesuaikan
    d = 10**(0.1238*df[ 'mag'][i]+0.983)
    if df ['mag'][i]>=6.5:
      t = 10**(0.032*df[ 'mag'][i]+2.7389)
    else:
      t = 10**(0.5409*df[ 'mag' ][i]-0.547)
    for j in list(range(i+1, len(df))):
      dis = distance(df[ 'latitude' ][i],df[ 'longitude' ][i],df['latitude'][j],df['longitude'][j])
      date1 = df['date'][i]
      date2 = df['date'][j]
      tim = abs((date1-date2).days)
      if tim < t and dis < d:
        nonmain.append(j) #mencari index gempa bumi yang dependent

  df.drop(unique(nonmain),axis=0,inplace=True)#Mendrop gempa nonmain dari dataset
  df.reset_index(inplace=True,drop=True)
  return df


df=declustering(df)

#untuk kepentingan format penamaan
df=df[['latitude','longitude','depth','mag']]
df.rename(columns={'depth': 'Kedalaman (km)', 'latitude': 'Latitude', 'longitude': 'Longitude', 'mag': 'Mw'}, inplace=True)



EventID = []
TipeGempa = []
for i in range(len(df)):
  EventID.append(i+1)
  if df["Kedalaman (km)"][i] <= 50:
    TipeGempa.append("Interface")
  else:
    TipeGempa.append("Interaslab")

df.insert(0, "Event ID", EventID)
df.insert(5, "Tipe Gempa", TipeGempa)
df
df.shape

(>) def MRL(sample):
mag = sample.sort_values()
maxx = mag.max()
minn = mag.min()
x = np.arange(minn, maxx, 8.001).tolist()

yn =[]

for i in np.arange(minn, maxx, 0.001):
e_u = mean(mag[mag>i]) - i
y.append(e_u)
plt.scatter(x, y, s=0.5)
plt.vlines(x=np.quantile(mag, ©.95), ymin=min(y), ymax=max(y), colors='r', linestyle='dashed")
plt.xlabel('u")
plt.ylabel( mean excess, e(u)')
plt.title('Mean Residual Life Plot’)

plt.show()
return x,y,mag

x,y,mag = MRL(df['Mw'])

!pip install rpy2==3.5.1

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector
from rpy2.robjects.packages import importr
import rpy2.robjects.packages as rpackages

import warnings
def function_that_warns():
  warnings.warn("deprecated",DeprecationWarning)

with warnings.catch_warnings():
  warnings.simplefilter("ignore")
  function_that_warns()

base = importr("base")
utils = importr("utils")
utils.chooseCRANmirror(ind=1)
utils.install_packages("POT")

POT = importr('POT')

shape, scale = gpdfit(df['Mw'], threshold, "mle")

data = genpareto.rvs(c=shape ,loc = threshold , scale =scale , size=10000)

sns.histplot(data.stat='density', bins=30, kde=True)
plt.title('Histogram Distribusi GPD Dengan Parameter Hasil Taksiran')

plt.xlabel('Moment Magnitude')
plt.ylabel('Density')