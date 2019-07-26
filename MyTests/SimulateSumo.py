import traci
import os
import MyTests.xml2csv as XMLConvert
from MyTests.TurnRouterTest import TurnRouter

my_path = '/home/mesto/flow/MyTests/'

output = my_path + 'SumoTest/'
net_path = my_path + 'NoI440Edit.net.xml'
routes_path = my_path + 'turnRoutes.rou.xml'
add_path = my_path + 'Detectors_NoI440Edit.xml'
flow_def = my_path + 'flows.xml'

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
def convertData():
    for data in os.listdir(output):
        if "e1Detector" in data:
            target = os.path.join(output, data)
            XMLConvert.convert(target)
            os.remove(target)

#def runSim(gui, stepLength, numSteps,

#Runs the simulation when the script is called.
if __name__ == "__main__":
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