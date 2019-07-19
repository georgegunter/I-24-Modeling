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
        output = "/home/mesto/flow/MyTests/TEST/",
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
        if "(out)" in data:
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
        if file.endswith('.csv') and '(out)' in file:

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
            os.remove(os.path.join(data_path, file))
    error = ((errSum - flow) / flow) * 100 
    return error

'''
def ObjFunc(Params):

	run(
	gui=False,
        output = "/home/mesto/flow/MyTests/TEST/",
        step=0.1,
        duration=10000,
        car_following_model=OVMController,
        flow_rate=Params(1),
        speed=Params(2))

	func_val = GetError(data_Path,
'''
run(gui=True, speed=30, duration=36000)