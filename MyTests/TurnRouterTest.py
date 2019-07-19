from lxml import etree
elem = etree.Element
from flow.core.util import makexml, printxml, ensure_dir
import subprocess
import os

#TODO: add inputs for the variables
def GenerateXMLs(filepath="/home/mesto/flow/MyTests/flows.xml"):
    flows = makexml('routes', 'http://sumo.dlr.de/xsd/routes_file.xsd')
    flows.append(CreateVTypeElem('human', '2.6', '4.5', '0.5', '70', '2.5', '0.0'))
    flows.append(CreateFlowElem('634155175', 'flow_0', '1', '20000000', '28000', 'human', '30'))
    
    printxml(flows, filepath)

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


def CreateFlowElem(origin, id, begin, end, rate, type, speed):
    item = elem('flow')
    item.set("from", origin)
    item.set('id', id)
    item.set('begin', begin)
    item.set('end', end)
    item.set('vehsPerHour', rate)
    item.set('type', type)
    item.set('departSpeed', speed)
    item.set('departPos', '0')
    item.set('departLane', 'random')
    return item

def JTRRouter(net, output, flows, steps):
    cmd = '/home/mesto/sumo_binaries/bin/jtrrouter '
    cmd += '--net-file=' + net + ' '
    cmd += '--output-file=' + output + ' '
    cmd += '--flow-files=' + flows + ' '
    cmd += '-s ' + str(steps) + ' '
    cmd += '-T 10,90'
    os.system(cmd)

flowFile = '/home/mesto/flow/MyTests/flows.xml'
outputFile = '/home/mesto/flow/MyTests/turnRoutes.rou.xml'
netFile = '/home/mesto/flow/MyTests/FinalNetwork.net.xml'
GenerateXMLs(filepath=flowFile)
JTRRouter(netFile, outputFile, flowFile, 200)

'''
turnFile = makexml('turns', 'http://sumo.dlr.de/xsd/turns_file.xsd')
#turns = elem('turns')
interval = etree.Element('interval')
interval.set('begin', '1')
interval.set('end', '2000000')
fromEdge = etree.SubElement(interval, 'fromEdge')
fromEdge.set('id', 'gneE0')
toEdge = etree.SubElement(fromEdge, 'toEdge')
toEdge.set('id', 'gneE1')
toEdge.set('probability', '0.9')
toEdge = etree.SubElement(fromEdge, 'toEdge')
toEdge.set('id', 'gneE3')
toEdge.set('probability', '0.1')
turnFile.append(interval)
printxml(turnFile, "/home/mesto/flow/MyTests/turns.xml")
'''
#os.system('/home/mesto/sumo_binaries/bin/jtrrouter --net-file=/home/mesto/flow/MyTests/turnNet.net.xml --output-file=/home/mesto/flow/MyTests/turnRoutes.rou.xml --flow-files=/home/mesto/flow/MyTests/flows.xml -T 10,90')