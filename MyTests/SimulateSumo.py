"""
@author: Matthew Estopinal

Instructions: This script runs the simulation through Sumo WITHOUT Flow, and can run it with or 
without a GUI.

It requires two main components to be configured properly. The first is the XML files that detail
the scenario that is being simulated. These consist of the network, and detector files that should
be created via NetEdit or some other method, and the routes file and flow definitions that will be
generated from this script. The second component is the simulation parameters that are defined in
this simulation that control things like the duration of the simulation, vehicle following
parameters, the inflows, and things of that nature.

This script should be run in a folder such that it can access the XMLs, as well as import
from the TurnRouterTest and xml2csv scripts, and access traci.

When the simulation is run, it will create a folder whose name is controlled by the output variable
and will generate XML files from the detectors in the simulation. Once the simulation is finished
these XML files are replaced with CSV files that are easier to work with.

"""
import sys

#Directory that this script is stored in
my_path = '/home/mesto/flow/MyTests/'

#Path to save data to
output = my_path + 'SumoTest/'

#Paths of network definitions files
net_path = my_path + 'NoI440Edit.net.xml'
add_path = my_path + 'Detectors_NoI440Edit.xml'

#Paths of network files that will be created and used
routes_path = my_path + 'turnRoutes.rou.xml'
flow_def = my_path + 'flows.xml'

sys.path.append(my_path)

import traci
import os
import MyTests.xml2csv as XMLConvert
from MyTests.TurnRouterTest import TurnRouter

#Runs the turn router to generate the rou.xml file
#Flow and speed rates will be evenly divided across the time interval
#Takes a list of vehicle parameters (for the car following model)
#accel, decel, sigma, maxSpeed, minGap, speedDeviation, tau, emergencyDecel
#currently using Sumo default car following model
#turnPercent: what percentage of vehicles will exit
#flows: float or list of floats
#speed: float or list of floats
#duration: length of duration in seconds
#origin: string id of starting edge
def getRoutes(vParams, turnPercent, flows, speed, duration, origin):
    router = TurnRouter()
    router.CreateVTypeElem('human', vParams[0], vParams[1], vParams[2], vParams[3], vParams[4], vParams[5], vParams[6], vParams[7])
    
    if isinstance(flows, list) and isinstance(speed, list):
        if len(flows) != len(speed):
            print('Provided lists for speed and flows do not match length.')
            exit()
        else:
            print('Lists provided')
            for i in range(len(flows)):
                router.CreateFlowElem(origin, 'flow_' + str(i), str((duration / len(flows)) * (i)), str((duration / len(flows)) * (i+1)), str(flows[i]), 'human', str(speed[i]))
    elif isinstance(flows, list):
        for i in range(len(flows)):
            router.CreateFlowElem(origin, 'flow_' + str(i), str((duration / len(flows)) * (i)), str((duration / len(flows)) * (i+1)), str(flows[i]), 'human', str(speed))
    elif isinstance(speed, list):
        for i in range(len(speed)):
            router.CreateFlowElem(origin, 'flow_' + str(i), str((duration / len(speed)) * (i)), str((duration / len(speed)) * (i+1)), str(flows), 'human', str(speed[i]))
    else:
        router.CreateFlowElem(origin, 'flow_0', '0', str(duration), str(flows), 'human', str(speed))

    #router.CreateFlowElem(origin, 'flow_0', '1', '1500', '2156', 'human', '28.3')
    
    router.GenerateXMLs(filepath=flow_def)
    router.JTRRouter(net_path, routes_path, flow_def, duration, turnPercent)   

#Runs the simulation through sumo
#Input: (bool) gui: True to run the simulation gui, False to run in the command line.
#       (float) step_length: the length of a simulation time-step
#       (int) numStemps: the number of simulation steps
#Output: Does not return a value, generates XML files in the output folder
def simulate(gui, step_length, numSteps):
    if not os.path.isdir(output):
        os.mkdir(output)
    sumo = "sumo"
    if gui:
        sumo += "-gui"
    traci.start([sumo, "-n", net_path, "-r", routes_path, "-a", add_path, "--step-length", str(step_length), "--output-prefix", "SumoTest/"])

    #The simulation is running.
    for i in range(numSteps):
        traci.simulationStep()
    traci.close()

#Converts the detector output from XMLs to CSVs
#Input: takes no input
#Output: returns no output
def convertData():
    for data in os.listdir(output):
        if "e1Detector" in data:
            target = os.path.join(output, data)
            XMLConvert.convert(target)
            os.remove(target)

#Starts the simulation
#Input: (list) params: currently takes 13 items, and parsed out as below.
#       duration: int in seconds
#       stepLength: float in seconds
#       flows: float/int in veh / hour
#       speed: float in m/s
#       turnPercent: percentage of cars that exit right at each exit
#       origin: string - represents the edge of the network that cars will start on
#       vehicleParams is parsed out into accel, decel, sigma, maxSpeed, minGap, speedDeviation, tau, emergencyDecel
#Output: Returns no output, does result in CSVs being generate in the output folder.
def runSim(params):
    duration = params[0]
    stepLength = params[1]
    flows = params[2]
    speed = params[3]
    turnPercent = params[4]
    origin = params[5]
    vehicleParams = [str(i) for i in params[6:14]]
    getRoutes(vehicleParams, turnPercent, flows, speed, duration, origin)
    simulate(False, stepLength, int(duration / stepLength))
    convertData()

#Runs the simulation when the script is called.
if __name__ == "__main__":
    params = [86400, 0.1, 3000, 30, 2, '121304377#0', 2.6, 4.5, 0.5, 70, 2.5, 0, 2, 4.5]
    runSim(params)
    '''
    #Above is equivalent to the following:
    vehicleParams = ['2.6', '4.5', '0.5', '70', '2.5', '0', '2', '4.5']
    duration = 3000
    step = 0.1
    flows = [2000, 2500, 3000]
    speed = 30
    turnPercent = 25
    origin = '121304377#0'
    getRoutes(vehicleParams, turnPercent, flows, speed, duration, origin)
    simulate(True, step, int(duration / step))
    convertData()
    '''