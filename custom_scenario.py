"""
@author: Matthew Estopinal

Instructions: This script defines the network simulated by MySimulator. It can be modified
by giving commands every step on the addition_command() method in myEnv, or by editing the
XML files that define the network. To generate the routes file, I typically call the TurnRouterTest.py
script, although in the future I would probably implement that into this script.

This script should not be called by itself in the terminal, instead it is used by the MySimulator.py
script.

For information that was used to help make a script like this, I used the tutorials for flow
at https://github.com/flow-project/flow/tree/master/tutorials

Note: If this script is not working, you might need to call a sys.path.append() pointing
to the directory that flow is stored in. For some reason, it seems that other computers might
need to do this, but mine hasn't so it is a little hard to test.

"""
my_path = '/home/mesto/flow/MyTests/'

import sys
sys.path.append(my_path)

net_path = my_path + 'NoI440Edit_V2.net.xml",
route_path = my_path + 'turnRoutes.rou.xml",
vtype_path = my_path + 'flows.xml",
detector_path = my_path + 'Detectors_NoI440Edit.xml",
output_path = my_path + 'data/'

from flow.core.experiment import Experiment

from flow.scenarios import Scenario
from flow.controllers import IDMController
from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams, InFlows
from flow.core.params import SumoParams
	
from flow.envs.test import TestEnv

#Starting edge of the network where vehicles will originate
starting_edge = "121304377#0"

#Defines an environment for the cars to run in
#This is done to have access to the additional_command() method
#Can be used to edit the simulation while running at certain steps
class myEnv(TestEnv):
    roadSpeed = 30
    def getSpeed(self):
        return self.roadSpeed
    def setSpeed(self, num):
        self.roadSpeed = num
    def additional_command(self):
        pass
        #if self.step_counter == 1:
            #self.k.simulation.kernel_api.edge.setMaxSpeed("634155175", self.getSpeed())

#Defines a custom scenario class deriving from the base scenario class.
#Currently does not really do anything, but the scenario can be modified further
#by modifying this class.
class Custom_Scenario(Scenario):
    #These routes are overwritten by the template routes during initialization
    def specify_routes(self, net_params):
        return {starting_edge: [starting_edge]}

#Runs the scenario
#Input: (bool) render: default False, controls whether or not to run Simulation with GUI
#       (string) emissons: default none, path to save microscopic data output (uses lots of space)
#       (float) step: length of a time_step
#       (int) duration: number of timesteps to simulate
#       (int) flow_rate: inflow rates in veh / hour
#       car_following_model: car following model from flow -> see flow/controllers/car_following_models.py
#       (float/int) speed: speed of cars as the spawn in
#Output: returns no output
def run_scenario(render=False,
                 emissions=None,#"/home/mesto/flow/data/",
                 output=output_path,
                 step=0.1,
                 duration=1000,
                 flow_rate=2800,
                 car_following_model=IDMController,
                 speed=30
                 ):

	env_params = EnvParams()
	initial_config = InitialConfig()
	vehicles = VehicleParams()

	sim_params = SumoParams(render=render, sim_step=step, emission_path=emissions)

	vehicles = VehicleParams()
	inflow = InFlows()

        #Parameters for the network.
        #Template( net: file path for the sumo network. rou: path to the routes xml file
        #vtype: path to vehicle types xml. 
        #e1det: Requires modified traci simulation python file. Points to where detector definitions are stored
        #location that output will be saved. Also requires modified traci.py
	net_params = NetParams(inflows=inflow, template= {
	                       "net" : net_path,
                               "rou" : route_path,
                               "vtype": vtype_path,
	                       "e1Det": detector_path,
                               "output": output
	                       },
	                       no_internal_links=False)
	initial_config = InitialConfig(
	    edges_distribution=[starting_edge])

	scenario = Custom_Scenario(
	    name="template",
	    net_params=net_params,
	    initial_config=initial_config,
	    vehicles=vehicles
	)
	
	#The following determines which lanes vehicles spawn in. By default they spawn in rightmost lane
        #possibles are: int (number of lane), free (which lane is open), best, random
	for key in scenario.template_vehicles:
	    scenario.template_vehicles[key]['departLane'] = 'free'

	env = myEnv(
	    env_params=env_params,
	    sim_params=sim_params,
	    scenario=scenario
	)
	env.setSpeed(speed)

	exp = Experiment(env=env)
	_ = exp.run(1, duration)