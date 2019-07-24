import sys
flow_path = ''
script_path = ''
sumo_binary_path = ''
sys.path.append(script_path)
sys.path.append(flow_path)


from lxml import etree
elem = etree.Element
from flow.core.util import makexml, printxml, ensure_dir
import subprocess
import os

#TODO: add inputs for the variables
#Creates the flow XML file
def GenerateXMLs(filepath="/home/mesto/flow/MyTests/flows.xml"):
    flows = makexml('routes', 'http://sumo.dlr.de/xsd/routes_file.xsd')
    flows.append(CreateVTypeElem('human', '2.6', '4.5', '0.5', '70', '2.5', '0.0'))

    

    flows.append(CreateFlowElem('121304377#0', 'flow_0', '1', '900', '2156', 'human', '28.3'))
    flows.append(CreateFlowElem('121304377#0', 'flow_1', '900', '1200', '2100', 'human', '29.5'))
    flows.append(CreateFlowElem('121304377#0', 'flow_2', '1200', '1500', '2016', 'human', '28.3'))
    flows.append(CreateFlowElem('121304377#0', 'flow_3', '1500', '1800', '2100', 'human', '27.1'))
    flows.append(CreateFlowElem('121304377#0', 'flow_4', '1800', '2100', '2212', 'human', '21.5'))
    flows.append(CreateFlowElem('121304377#0', 'flow_5', '2100', '2400', '2156', 'human', '8.3'))
    flows.append(CreateFlowElem('121304377#0', 'flow_6', '2400', '2700', '3360', 'human', '14.1'))
    flows.append(CreateFlowElem('121304377#0', 'flow_7', '2700', '3000', '2548', 'human', '16.9'))
    flows.append(CreateFlowElem('121304377#0', 'flow_8', '3000', '3300', '2324', 'human', '8.3'))
    flows.append(CreateFlowElem('121304377#0', 'flow_9', '3300', '3600', '2716', 'human', '9.1'))
    flows.append(CreateFlowElem('121304377#0', 'flow_10', '3600', '3900', '2548', 'human', '10.2'))
    flows.append(CreateFlowElem('121304377#0', 'flow_11', '3900', '4200', '2716', 'human', '9.3'))
    
    printxml(flows, filepath)

#Creates XML Element with vehicle parameters
#Accepts parameters describing the vehicles control model.
#Vehicles with this same ID follow these parameters
def CreateVTypeElem(id, accel, decel, sigma, maxSpeed, minGap, speedDev):
    vehicle = elem('vType')
    vehicle.set('id', id)
    vehicle.set('accel', accel)
    vehicle.set('decel', decel)
    vehicle.set('sigma', sigma)
    vehicle.set('length', '5')
    vehicle.set('maxSpeed', maxSpeed)
    vehicle.set('minGap', minGap)
    vehicle.set('speedDev', speedDev)
    return vehicle

#Creates XML Element with the flow parameter
#Define the starting edge, start and end times, flow rate, type of vehicle, and start speed
def CreateFlowElem(origin, id, begin, end, rate, type, speed):
    item = elem('flow')
    item.set("from", origin)
    item.set('id', id)
    item.set('begin', begin)
    item.set('end', end)
    item.set('vehsPerHour', rate)
    item.set('type', type)
    item.set('departSpeed', speed)
    item.set('departPos', 'base')
    #item.set('departLane', 'random')
    return item

#Takes the defined flow and network XML files, and creates a routes xml file
def JTRRouter(net, output, flows, steps):
    cmd = '/home/mesto/sumo_binaries/bin/jtrrouter '
    cmd += '--net-file=' + net + ' '
    cmd += '--output-file=' + output + ' '
    cmd += '--flow-files=' + flows + ' '
    cmd += '--departlane free '
    cmd += '-s ' + str(steps) + ' '
    cmd += '-T 1,99'
    os.system(cmd)

if __name__ == "__main__":
    flowFile = '/home/mesto/flow/MyTests/flows.xml'
    outputFile = '/home/mesto/flow/MyTests/turnRoutes.rou.xml'
    netFile = '/home/mesto/flow/MyTests/NoI440Edit_V2.net.xml'
    GenerateXMLs(filepath=flowFile)
    JTRRouter(netFile, outputFile, flowFile, 4200)