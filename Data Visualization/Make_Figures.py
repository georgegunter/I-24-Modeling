#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:51:33 2019

@author: George Gunter
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sc
import matplotlib as mt
mt.get_backend()

# %% Find What 
files = os.listdir()
data_files = []

Marker_Miles = []

direction = "E"

for file in files:
    if(file != ".DS_Store" and direction in file):
        if(file[0:3]=='I24'):
            if(file[4]=="0"):         
                m = float(file[5:9])
                if(m not in(Marker_Miles)):
                    Marker_Miles.append(m)
                    print(m)
            else:
                try:
                    m = float(file[4:8])
                    if(m not in(Marker_Miles)):
                        Marker_Miles.append(m)
                        print(m)
                except:
                    m = float(file[4:6])
                    if(m not in Marker_Miles):
                        Marker_Miles.append(m)
                        print(m)
            data_files.append(file)  
        
Marker_Miles.sort()
#%%   
def get_Mile_Marker(file_name):
    m = None
    if(file_name[0:3]=='I24'):
        if(file_name[4]=="0"):         
            m = float(file_name[5:9])
        else:
            try:
                m = float(file_name[4:8])
            except:
                m = float(file_name[4:6]) 
    return m

def get_Lane_Number(file_name):
    l = None
    if(file_name[0:3]=='I24'):
        l = int(file_name[-5])
    return l
    
def get_Time_Data(file_name):
    data = np.genfromtxt(file_name,delimiter=',')
    time = data[1:,0]
    return time

def get_Count_Data(file_name):
    data = np.genfromtxt(file_name,delimiter=',')
    count = data[1:,2]/12.0
    return count

def get_Speed_Data(file_name):
    data = np.genfromtxt(file_name,delimiter=',')
    speed = data[1:,1]
    return speed

def get_Data(file_name):
    data = np.genfromtxt(file_name,delimiter=',')
    time = data[1:,0]
    count = data[1:,2]/12.0
    speed = data[1:,1]
    return time,speed,count

def get_Time_Slots(time):
    slots = np.zeros(len(time))
    for t in range(len(time)):
        slots[t] = int(np.floor(time[t]*12))
    return slots
#%%
num_sensors = len(Marker_Miles)
count_values = np.zeros([288,num_sensors])
density_values = np.zeros([288,num_sensors])
speed_values = np.zeros([288,num_sensors])
flow_values = np.zeros([288,num_sensors])

num_lanes = np.zeros([num_sensors])

for file_name in data_files:
    time,speed,count = get_Data(file_name)
    slots = get_Time_Slots(time)
    marker_value = get_Mile_Marker(file_name)
    sensor_number = Marker_Miles.index(marker_value)
    num_lanes[sensor_number] += 1
    #count_values[:,sensor_number] += count
    if np.amax(count) > 333:
        for i in range(len(count)):
            count[i] = count[i] / 10
    for i in range(len(slots)):
        slot = int(slots[i])
        count_values[slot, sensor_number] += count[i]
        speed_values[slot, sensor_number] += speed[i] * count[i]
        #Temp
        flow_values[i, sensor_number] += count[i] * 12

for i in range(len(speed_values)):
    for j in range(len(speed_values[i])):
        speed_values[i, j] = speed_values[i, j] / count_values[i, j]

for i in range(len(flow_values)):
    for j in range(len(flow_values[i])):
        flow_values[i,j] = flow_values[i,j] / num_lanes[j]
        density_values[i,j] = flow_values[i,j] / speed_values[i,j]
        
def interpolate(x, y):
    plot_vals = []
    for i in range(len(y)):
        pc = sc.PchipInterpolator(x, y[i])
        plot_vals.append(pc([i / 10 for i in range(int(x[0] * 10), int(x[-1] * 10) + 1, 1)]))
    return plot_vals

plt.subplot(2, 2, 1)
density = interpolate(Marker_Miles, density_values)
plt.pcolor(np.transpose(density))
plt.colorbar(label='Density')
plt.ylabel('Mile Markers')
#plt.yticks([(i - Marker_Miles[0]) * 10 for i in Marker_Miles])

plt.subplot(2, 2, 2)
speed_plot = interpolate(Marker_Miles, speed_values)
plt.pcolor(np.transpose(speed_plot))
plt.colorbar(label='Speed')

plt.subplot(2, 2, 3)
flow_plot = interpolate(Marker_Miles, flow_values)
plt.pcolor(np.transpose(flow_plot))
plt.colorbar(label='Flow')

plt.subplot(2,2,4)
count_plot = interpolate(Marker_Miles, count_values)
plt.pcolor(np.transpose(count_plot))
plt.colorbar(label='Count')
plt.tight_layout()
plt.savefig('traffic.png', dpi = 300)
    
