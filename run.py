import pandas as pd
import numpy as np
from Network import Network
from Controller import MaxPressureController
from Controller import dqnController
import traci
import os
import sys
import json
from data_logger import Data_Logger

if __name__ == "__main__":

    controller_type = "max_pressure"

    # LOAD SUMO STUFF
    # cfgfilename = "test_1110.sumo.cfg"
    cfgfilename = "SUMO_Network.sumocfg"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "network", cfgfilename)
    print(filepath)

    sumoCmd = ["sumo", "-c", filepath]
    # sumoCmd = ["sumo-gui", "-c", filepath]  # if you want to see the simulation
    runID = 'AAA'
#create data logger, pass in runID
    logger = Data_Logger(runID)
    # initialize the network object and controller object
    tracilabel = "sim1"
    traci.start(sumoCmd, label=tracilabel)
    conn = traci.getConnection(tracilabel)

    network = Network(filepath, conn)
    controller = "max_pressure"
    if controller_type == "max_pressure":
        controller = MaxPressureController()
    else:
        controller = dqnController()

    step = 0

    while conn.simulation.getMinExpectedNumber() > 0:
        conn.simulationStep()
        if step > 1 and step % 30 == 0:

            # get current state

            intersections = list(network.network.keys())
            print("intersections" + str(intersections))
            print("in step " + str(step))
            for i in range(len(intersections)):
                intersection = intersections[i]
                state = network.getState(conn, intersection)
                geometry = network.getGeometry(intersection)

                # get maxpressure controller
                control = controller.getController(geometry, state)
                print("   " + intersection + " light list : " + str(control))
                # update the state of the network
                network.applyControl(control,conn,intersection)      
                
                #########write_state_to_file(state)   
                #metrics = updateMetrics(conn,metrics,state,geometry)
            print()
            print()

            # write_state_to_file(state)
            logger.updateLane(step, conn, network.allLaneId)
            logger.updateVeh(step, conn, state)

        # RUN Data Analysis
        step += 1

    

    

    logger.close()



    traci.close(False)

# save csv files with special names
# add to csv and dont save 