"""
@author: Matthew Estopinal

Instructions: This script runs the simulation defined by the custom_scenario.py script. It must
be in a folder where it can import the custom_scenario, and also access the Flow files in order
to use Flow's car following models. It also must be in a place to import xml2csv.

In order to run the simulation, one calls the run() method with the given parameters. It can be run
with a GUI to view the simulation or not depending on the parameters. One defines the length,
car following model, car speed, step_length, and inflow rate in this script to run on the network
defined by custom_scenario.py.

Once the simulation is run, it calls the get_error function. Currently the get error function averages
the flows read by all the detectors in the network and compares it to the given inflow rate via
a simple percent error. This is not a very good error metric of simulation, so it should be changed.

Note: This script uses Flow to run the Sumo simulation. However, the custom_scenario does not use
much from Flow, so the simulation should run just as fast as only using Sumo, but that is currently
not the case. Until that problem can be solved I would reccomend using the SimulateSumo script
to run the simulation without Flow so that it can run in a reasonable time.

"""
import sys
my_path = '/home/mesto/flow/MyTests/'
sys.path.append(my_path)

import MyTests.custom_scenario as CS
import os
import MyTests.xml2csv as XMLConvert
from flow.controllers import OVMController
import time
import csv

#Takes scenario parameters
#Runs the sumo simulation
#Calls getError and prints it to console
def run(gui=False,
        output = my_path + 'TEST/",
        step=0.1,
        duration=10000,
        car_following_model=OVMController,
        flow_rate=2800,
        speed=30):
        
        

    CS.run_scenario(render=gui,
                    step=step,
                    duration=duration,
                    flow_rate=flow_rate,
                    output=output,
                    car_following_model=car_following_model)

    if gui:
        input('Press Enter after closing SUMO to generate CSVs')
    print('Converting XMLs to CSVs')
    #Pauses to let sumo close before accessing XMLs
    time.sleep(1)
    for data in os.listdir(output):
        print(data)
        if "e1Detector" in data:
            target = os.path.join(output,data)
            XMLConvert.convert(os.path.join(output,data))
            os.remove(os.path.join(output ,data))
    print(GetError(output, flow_rate))

#Takes the folder where the e1detector files are stored
#Also takes the inflow rate of vehicles
#Outputs a percent error between detected and input flows
#TODO: Modify error function
def GetError(data_path, flow):
    error = 0
    errSum = 0
    for file in os.listdir(data_path):
        flowSum = 0
        count = 0
        if file.endswith('.csv'):# and '(out)' in file:

            with open(os.path.join(data_path, file)) as f:
                reader = csv.reader(f)
                firstLine = True
                for line in reader:
                    if not firstLine:
                        flowSum += float(line[2])
                        count += 1
                    else:
                        firstLine = False
            flowAvg = flowSum / count
            errSum += flowAvg
            #os.remove(os.path.join(data_path, file))
    error = ((errSum - flow) / flow) * 100 
    return error

if __name__ == "__main__":
    run(gui=True, speed=30, duration=2000)