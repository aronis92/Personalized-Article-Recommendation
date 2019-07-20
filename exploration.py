from exploration_functions import export_excel, create_directories
from random_serving import random_serve
from egreedy import e_greedy
from UCB import UCB
from LinUCB import LinUCB
from LinUCB_Hybrid import LinUCB_Hybrid
import xlsxwriter

#####################################################################
# This file contains the 3 rounds of explorations that were         #
# conducted in order to find the best parameter for each algorithm. #
# Also by changing the percentage we calculate how close can we     #
# get to the estimations of the whole tunning dataset (100%).       #
#####################################################################

create_directories() # Create the needed folders to save the exported excel files.

###################################
# Random Article Serving Results. #
###################################

# Create the excel file to export the results.
workbook = xlsxwriter.Workbook('./parameters exploration/random_results.xlsx')
worksheet = workbook.add_worksheet()

# Write the headers of the columns
row = 0
col = 0
worksheet.write(row, col, 'ctr')
worksheet.write(row, col + 1, 'total_reward')
worksheet.write(row, col + 2, 'T')
worksheet.write(row, col + 3, 'time')
row += 1

# Uncomment this to use averaging over 10 executions of random serving.
#sums = [0, 0, 0, 0] # List of sums of CTR, total_reward, T, time_elapsed respectively in over to average 10 executions.
#for j in range(10):
#    print(j + 1, end = " ") # Message to monitor progress.
#    ctr, total_reward, T, time_elapsed = random_serve() # run the algorithm and get the results.
#    sums = list( map(add, sums, [ctr, total_reward, T, time_elapsed]) ) # add the results to their respective sum.
#ctr, total_reward, T, time_elapsed = [v/10 for v in sums] # Calculate their average

# Comment this if you chose averaging.
ctr, total_reward, T, time_elapsed = random_serve()

# Write the results to the excel file and save it.
worksheet.write(row, col, ctr)
worksheet.write(row, col + 1, total_reward)
worksheet.write(row, col + 2, T)
worksheet.write(row, col + 3, time_elapsed)
row += 1
workbook.close()

##################################
# 1st exploration of parameters. #
##################################

percentage = 1 # Set the percentage to 1 for the whole dataset experiment
epsilons = [0.01, 0.1, 0.25, 0.5, 0.8, 1] # set list of parameters
averaging = True # Set whether to run policy multiple times and average
excel_name = '100%/e_greedy_exploration_1' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, epsilons, e_greedy, averaging, percentage) # Export results for e-greedy

averaging = False # Set whether to run policy multiple times and average
alphas = [0.5, 1, 2, 5, 7, 10] # set list of parameters
excel_name = '100%/UCB_exploration_1' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, UCB, averaging, percentage) # Export results for UCB

alphas = [0.5, 1, 2, 5, 7, 10] # set list of parameters
excel_name = '100%/LinUCB_exploration_1' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB, averaging, percentage) # Export results for LinUCB

alphas = [0.5, 1, 2, 5, 7, 10] # set list of parameters
excel_name = '100%/LinUCB_Hybrid_exploration_1' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB_Hybrid, averaging, percentage) # Export results for LinUCB Hybrid.

#########################################################################
# 2nd exploration of parameters after examining the results of the 1st. #
#########################################################################

epsilons = [0.02, 0.05, 0.075]
averaging = True
excel_name = '100%/e_greedy_exploration_2' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, epsilons, e_greedy, averaging, percentage) # Export results for e-greedy

averaging = False
alphas = [0.1, 0.25, 0.75]
excel_name = '100%/UCB_exploration_2' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, UCB, averaging, percentage) # Export results for UCB

alphas = [0.1, 0.25, 0.75]
excel_name = '100%/LinUCB_exploration_2' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB, averaging, percentage) # Export results for LinUCB

alphas = [0.1, 0.25, 0.75]
excel_name = '100%/LinUCB_Hybrid_exploration_2' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB_Hybrid, averaging, percentage) # Export results for LinUCB Hybrid.

######################################################################################
# 3rd exploration of parameters after examining the combined results of 1st and 2nd. #
######################################################################################

epsilons = [0.07]
averaging = True
excel_name = '100%/e_greedy_exploration_3' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, epsilons, e_greedy, averaging, percentage) # Export results for e-greedy

averaging = False
alphas = [0.2]
excel_name = '100%/UCB_exploration_3' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, UCB, averaging, percentage) # Export results for UCB

alphas = [0.05]
excel_name = '100%/LinUCB_exploration_3' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB, averaging, percentage) # Export results for LinUCB

alphas = [0.3]
excel_name = '100%/LinUCB_Hybrid_exploration_3' + '_' + str(percentage) + '.xlsx'
export_excel(excel_name, alphas, LinUCB_Hybrid, averaging, percentage) # Export results for LinUCB Hybrid.

##################################################
# Exploration of parameters with sparse dataset. #
##################################################

# Set the percentage of the dataset to keep.
percentages = [0.01, 0.1, 0.3]

# Iterate through the percentages and export excel files with the performance on tuning data.
for percentage in percentages: 
    epsilons = [0.01, 0.02, 0.05, 0.07, 0.075, 0.1, 0.25, 0.5, 0.8, 1]# set list of parameters
    averaging = False # Set whether to run policy multiple times and average
    excel_name = str(int(percentage*100)) + '%/e_greedy_exploration.xlsx'
    export_excel(excel_name, epsilons, e_greedy, averaging, percentage) # Export results for e-greedy
    
    averaging = False # Set whether to run policy multiple times and average
    alphas = [0.1, 0.2, 0.25, 0.5, 0.75, 1, 2, 5, 7, 10] # set list of parameters
    excel_name = str(int(percentage*100)) + '%/UCB_exploration.xlsx'
    export_excel(excel_name, alphas, UCB, averaging, percentage) # Export results for UCB
    
    alphas = [0.05, 0.1, 0.25, 0.5, 0.75, 1, 2, 5, 7, 10] # set list of parameters
    excel_name = str(int(percentage*100)) + '%/LinUCB_exploration.xlsx'
    export_excel(excel_name, alphas, LinUCB, averaging, percentage) # Export results for LinUCB
    
    alphas = [0.1, 0.25, 0.3, 0.5, 0.75, 1, 2, 5, 7, 10] # set list of parameters
    excel_name = str(int(percentage*100)) + '%/LinUCB_Hybrid_exploration.xlsx'
    export_excel(excel_name, alphas, LinUCB_Hybrid, averaging, percentage) # Export results for LinUCB Hybrid.







