#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:51:33 2019

@author: George Gunter, edited by Matthew Estopinal, Daniel Shin

Instructions: Use the CleanDayData.py script to filter out the CSVs of the TDOT
data into a cleaner format. Make sure all these clean CSVs are in a folder by themselves.
If other CSVs are present in the folder the program will produce an error. Next,
place a copy of this script into the folder and run it, either from the editor or
in the terminal. This will generate a graph that can be viewed in the editor, and
also saves an image named traffic.png in the folder.

In order to pick which mile markers are plotted, simply select which CSVs are present
in the folder with the script
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

#Choose which direction of Highway that you want to graph
#For I24 choose 'E' or 'W'
direction = "E"

#Loops through all the files in the folder to get all the Mile Markers that will
#be plotted
#Has special cases for if there is a 0 before the file name ie I24-052.1
#Also has a special case for no decimal point, or no value after decimal
#i.e. I24-44E or I24-56.
for file in files:
    if(file != ".DS_Store" and direction in file and 'WE' not in file and 'EW' not in file):
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
#Creates arrays filled with zeros to be replaced with data
num_sensors = len(Marker_Miles)
count_values = np.zeros([288,num_sensors])
density_values = np.zeros([288,num_sensors])
speed_values = np.zeros([288,num_sensors])
flow_values = np.zeros([288,num_sensors])

num_lanes = np.zeros([num_sensors])

#Loops through the files in the local folder
#Gets the data from each CSV to get the count, time, and speed data
#Calculates slots in order to properly align the data when some timesteps are missing
#Also gets lane number / mile marker from the name
for file_name in data_files:
    if direction in file_name and 'EW' not in file_name and 'WE' not in file_name:
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

#Loops through the speed_values and divides by the count to yield the average speed
for i in range(len(speed_values)):
    for j in range(len(speed_values[i])):
        speed_values[i, j] = speed_values[i, j] / count_values[i, j]

#Loops through the flow_values to divide by the lane numbers to get average flow / lane
#Calculates density based on speed, yields density / lane / mile
for i in range(len(flow_values)):
    for j in range(len(flow_values[i])):
        flow_values[i,j] = flow_values[i,j] / num_lanes[j]
        density_values[i,j] = flow_values[i,j] / speed_values[i,j]
  
#Takes two one-dimensional arrays, x and y:
#x: the input array, in our case it is the Marker_Miles typically
#y: the known output, i.e. the density or speeds at those given markers
#If y is a 2D array, each row corresponds to the output array at the given timestep
def interpolate(x, y):
    plot_vals = []
    for i in range(len(y)):
        pc = sc.PchipInterpolator(x, y[i])
        plot_vals.append(pc([i / 10 for i in range(int(x[0] * 10), int(x[-1] * 10) + 1, 1)]))
    return plot_vals

#Plots the density graph in the top left
plt.subplot(2, 2, 1)
density = interpolate(Marker_Miles, density_values)
plt.pcolor(np.transpose(density))
plt.colorbar(label='Density')
plt.ylabel('Mile Markers')

#Plots the speed in the top right
plt.subplot(2, 2, 2)
speed_plot = interpolate(Marker_Miles, speed_values)
plt.pcolor(np.transpose(speed_plot))
plt.colorbar(label='Speed')

#Plots the flow in the bottom left
plt.subplot(2, 2, 3)
flow_plot = interpolate(Marker_Miles, flow_values)
plt.pcolor(np.transpose(flow_plot))
plt.colorbar(label='Flow')

#Plots the count data in bottom right
plt.subplot(2,2,4)
count_plot = interpolate(Marker_Miles, count_values)
plt.pcolor(np.transpose(count_plot))
plt.colorbar(label='Count')

#Saves the figure, dpi controls the resolution, "dots per inch"
plt.tight_layout()
plt.savefig('traffic.png', dpi=500)
    
