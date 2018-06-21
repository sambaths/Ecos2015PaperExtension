###########################################################################
#
###########		ENERGY AND EXERGY ANALYSIS OF A CRUISE SHIP		###########
#
###########################################################################

# This is the main script of the project "Energy and Exergy analysis of a cruise ship"

# The main objective of this project is to analyze the energy and exergy flows of the cruise ship "MS Birka", selected as case study.

# The main objective of this library of Python scripts is, therefore;
# - Load the data
# - Appropriately filter and clean the dataset
# - Process data so to generate the variables of interest: in particular, energy and exergy flows
# - Statistically analyze the data so to produce appropriate results

# The main.py script calls other scripts and functions. It is divided in the following sections:
# - INPUT
# - DATA READING
# - DATA CLEANING
# - DATA PROCESSING
# - EXPLORATORY DATA ANALYSIS
# - ENERGY ANALYSIS
# - EXERGY ANALYSIS


do_processed_data_preparation = "no"
do_data_processing = "no"




#%%
######################################
## INPUT			##
######################################

# Loading appropriate modules
import sys
import os
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
project_path = os.getcwd()
path_files = project_path + os.sep + 'Python files' + os.sep
sys.path.append(path_files)
# Loading local modules
import input
import plotting as plot
import datareading as dr
import unitstructures as us
import Constants as kk
import fillerfunctions as ff
import consistencycheck as cc
import preprocessingAE as ppa
import preprocessingME as ppm
import preprocessingO as ppo
import energyanalysis as ea
import auxiliaryDemand as aux
import coolingsystems as cs
from helpers import d2df
import export as ex
import clustering
import postProcessing as post

#%%
######################################
## DATA READING			##
######################################
# Responsible: FA
# Setting the filenames
filenames = input.filenames(project_path) # Note: this is just a test
# Reading the input data (measurements)
dataset_raw = pd.read_hdf(filenames["dataset_raw"] ,'table')
# load the dictionary with the header names
header_names = dr.keysRenaming(dataset_raw, filenames["headers_translate"])


######################################
## DATA PROCESSING		##
######################################
# Responsible: FB
#%%
# Setting the important constants
CONSTANTS = kk.constantsSetting()
CONSTANTS["filenames"] = filenames
(dict_structure, processed) = us.structurePreparation(CONSTANTS, dataset_raw.index, CONSTANTS["filenames"]["dataset_output_empty"], do_processed_data_preparation)
processed = kk.seasons(dataset_raw, processed, CONSTANTS)
erase_old_file = "yes"
try:
    processed_temp = pd.read_hdf(CONSTANTS["filenames"]["dataset_output"], 'processed')
except FileNotFoundError:
    if do_data_processing == "no":
        do_data_processing = "yes"
    erase_old_file = "no"

# Running the code
if do_data_processing == "no":
    # If the file exists AND we want to use it, we just assign the "processed" variable to it
    processed = processed_temp
elif do_data_processing == "yes":
    # Otherwise, we simply do as if it didn't exist
    if erase_old_file != "no":
        os.remove(CONSTANTS["filenames"]["dataset_output"])
    # First updating the "CONSTANTS" dictionary with the some additional information
    processed = input.assumptions(dataset_raw, processed, CONSTANTS, header_names)
    # Updating the fields of the MainEngines and the auxiliary engines
    processed = ppm.mainEngineProcessing(dataset_raw, processed, dict_structure, CONSTANTS, header_names)
    processed = ppa.auxEngineProcessing(dataset_raw, processed, dict_structure, CONSTANTS, header_names)
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Other-1")
    # Calculating the auxiliary power demands: heating and electric power
    processed = aux.auxPowerAnalysis(processed, CONSTANTS, dict_structure, dataset_raw, header_names)
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Other-2")
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Other-3")
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Demands", "Demands-1")
    # Calculating the central cooling systems
    processed = cs.centralCoolingSystems(processed, CONSTANTS)
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Other-4")
    processed = cs.seaWaterCoolers(processed, CONSTANTS, dict_structure)
    # Calculating energy and exergy properties
    processed = ea.energyAnalysisLauncher(processed, dict_structure, CONSTANTS)
    # Re-doing the calculation of the connected points
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Other-5")
    processed = ff.systemFill(processed, dict_structure, CONSTANTS, "Other", "Demands-2")
    # Saving the processed data
    processed.to_hdf(CONSTANTS["filenames"]["dataset_output"], "processed", format='fixed', mode='w')
    # Result check log
    cc.systemCheck(processed, CONSTANTS, dict_structure, dataset_raw)
    # Efficiency results export


#%%
######################################
## POSTPROCESSING	##
######################################


#processed = ppo.seasonCalculator(processed)
#exported = ex.exportAggregatedEyergyFlows(processed, CONSTANTS, dict_structure)
#clusteringExport = ex.exportClusteringFlows(processed, CONSTANTS, dict_structure)
#clusteringExportFB = ex.exportClusteringFlowsFB(processed, CONSTANTS, dict_structure)
#clusteringEvaluation = clustering.punctualClustering(exported, "kmeans")
#clustering.clusteringTest(exported, "kmeans", 10, (1,20))

######################################
## PLOTTING	##
######################################
plot.predefinedPlots(processed, dataset_raw, CONSTANTS, dict_structure,["Pie:DemandFull"])

# processed = ea.efficiencyCalculator(processed, dict_structure, CONSTANTS)



