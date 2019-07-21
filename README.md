# I-24-Modeling
This repository is run on two main scripts:
The first is the custom_scenario.py file,
the second is MySimulator.py.

    Custom_Scenario defines how our simulation will interact with SUMO through the FLOW packages.
A simulation running in flow is defined by a few main components. The first is the scenario. Each
scenario inherits the Scenario class from Base_Scenario.py, located in the scenarios folder of flow.
The scenario defines the network, vehicle, and route parameters of the simulation. In our simulation,
the traci.py file located in flow/core/simulation/traci.py has been modified to add functionality to
the net_params attribute of Scenario.
    Currently, I have created a Custom_Scenario class that does not differ from the base class, but
is defined in custom_scenario anyways in case any modifications should be made. The scenario is instantiated
with an initial_config, determining the initial distribution of vehicles. There is also a net_params
component defining features of the network. Inflows can be added to the net_params, as seen in custom_scenario.py
further info on inflows is located in flow/core/params.py.
    Net_params also has a template attribute. In our current simulation we predefine the network, routes,
and vehicles in xml scripts outside of flow. While flow can define networks through code, it is easier
to do in Netedit which comes with flow. In order to generate routes, I use the script TurnRouterTest.py
(the name will probably edited later to remove 'Test'). This script generates an xml for routes, and vehicle 
types. I plan to call this script from MySimulator.py to generate the routes at runtime soon. It makes use 
of the jtrrouter that comes with SUMO.
    The simulation also requires an environment to be defined. This environment typically deals
with reinforcement learning agents, but also handles interacting with the simulation during runtime.
Right now the script defines a new environment inheriting from the TestEnv, in order to determine the
additional_commands() method, which is called each time step. It currently has an example of changing
edge speed at runtime.
    Lastly, the experiment is called using the defined environment. This runs the simulation, and generates the desired outputs.
If detectors have been defined in the net_params.template dictionary, they will output CSV files with
macroscopic simulation data. Right now the script only takes data from the detectors whose file contains
'(out)' in the name, which is changed in NetEdit, but I plan to change this.

    MySimulator.py takes the simuation parameters, runs the simulation as defined by custom_scenario.py
and then calls the GetError method with the CSV output of the detectors, as well as the predefined inflow.
The GetError method will be changed to give a better sense of how well the simulation performs.
    Currently one runs the TurnRouterTest.py, then MySimulator.py, and the percent error is printed out,
but I plan to have the MySimulator.py be the only thing that has to run, where it will take all parameters,
run the TurnRouterTest.py, then return the error given by GetError. At that point, one should be able
to run an optimization routine.

    In order to run the simulation, one should be able to copy and paste the files in the GitHub into the flow directory
and change the filepaths in the three scripts MySimulator.py, custom_scenario.py, and TurnRouterTest.py to
reflect their local machine. To get output from detectors, you also must place the traci.py script into flow.
Its path in the github should match where it goes in the actual flow directories.
