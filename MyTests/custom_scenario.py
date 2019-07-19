from flow.core.experiment import Experiment

from flow.scenarios import Scenario
from flow.controllers import IDMController
from flow.core.params import VehicleParams
from flow.core.params import NetParams
from flow.core.params import InitialConfig
from flow.core.params import EnvParams, InFlows
from flow.core.params import SumoParams
	
from flow.envs.test import TestEnv

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
        if self.step_counter == 1:
            self.k.simulation.kernel_api.edge.setMaxSpeed("634155175", self.getSpeed())

class Custom_Scenario(Scenario):

    '''
    def specify_routes(self, net_params):

        return {"634155175": ["634155175"]}
    '''

def run_scenario(render=False,
                 emissions="/home/mesto/flow/data/",
                 output="/home/mesto/flow/data/",
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
	'''
	vehicles.add(
	    veh_id="human",
	    acceleration_controller=(car_following_model, {}),
	    num_vehicles=20)
	inflow.add(
	    veh_type="human",
	    end=100,
	    edge="634155175",
	    vehs_per_hour=flow_rate,
	    departLane="free",
	    departSpeed=speed)
	inflow.add(
	    veh_type="human",
	    begin=101,
	    edge="gneE0",
	    vehs_per_hour=flow_rate,
	    departLane="free",
	    departSpeed=speed)
	'''
        #Parameters for the network.
        #Template( net: file path for the sumo network. rou: path to the routes xml file
        #vtype: path to vehicle types xml. 
        #e1det: Requires modified traci simulation python file. Points to where detector definitions are stored
        #location that output will be saved. Also requires modified traci.py
	net_params = NetParams(inflows=inflow, template= {
	                       "net" : "/home/mesto/flow/MyTests/FinalNetwork.net.xml",
                               "rou" : "/home/mesto/flow/MyTests/turnRoutes.rou.xml",
                               "vtype": "/home/mesto/flow/MyTests/flows.xml",
                               #"net" : "/home/mesto/flow/MyTests/I24-62.net.xml",
	                       #"e1Det": "/home/mesto/flow/MyTests/I24-62.add.xml",
                               "output": output
	                       },
	                       no_internal_links=False)
	initial_config = InitialConfig(
	    edges_distribution=["634155175"])

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