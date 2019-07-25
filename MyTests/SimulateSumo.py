import traci
import os
import MyTests.xml2csv as XMLConvert

my_path = '/home/mesto/flow/MyTests/'

output = my_path + 'SumoTest/'
net_path = my_path + 'NoI440Edit.net.xml'
routes_path = my_path + 'turnRoutes.rou.xml'
add_path = my_path + 'Detectors_NoI440Edit.xml'

#Runs the simulation through sumo
def simulate(gui, step_length, numSteps):
    if not os.path.isdir(output):
        os.mkdir(output)
    sumo = "sumo"
    if gui:
        sumo += "-gui"
    traci.start([sumo, "-n", net_path, "-r", routes_path, "-a", add_path, "--step-length", str(step_length), "--output-prefix", "SumoTest/"])
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
    simulate(False, 0.1, 42000)
    convertData()