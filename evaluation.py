from random_serving import random_serve
from egreedy import e_greedy
from UCB import UCB
from LinUCB import LinUCB
from LinUCB_Hybrid import LinUCB_Hybrid
import pandas as pd
import numpy as np
import xlsxwriter
import os

############################################################################
# This file produces results based on 100% of the evaluation data using:   #
# - The parameters providing the best CTR on the 100 % of tuning data.     #
# - The parameters providing the 2nd best CTR on the 100 % of tuning data. #
# - The parameters providing the best CTR on the 30 % of tuning data.      #
# - The parameters providing the best CTR on the 10 % of tuning data.      #
# - The parameters providing the best CTR on the 1 % of tuning data.       #
############################################################################

######################################################################################
# Function to evaluate the best parameters estimated by the 100% of the tuning data. #
######################################################################################

def evaluate_best_parameters():      
    sess = 'evaluation' # Dataset to use for evaluation
    percentage = 1 # Run on this percentage = 100%
    
    # Run random article serving and keep the results.
    CTR_random_serving, _, _, time_elapsed = random_serve(sess)
    results = np.array(['random serving', '-', CTR_random_serving, '1', time_elapsed])
    
    # Run e-greedy and append the results.
    epsilon = 0.07
    CTR, _, _, time_elapsed = e_greedy(epsilon, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['e-greedy', epsilon, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run UCB and append the results.
    alpha = 0.2
    CTR, _, _, time_elapsed = UCB(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['UCB', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run LinUCB and append the results.
    alpha = 0.1
    CTR, _, _, time_elapsed = LinUCB(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['LinUCB', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run LinUCB Hybrid and append the results.
    alpha = 0.25
    CTR, _, _, time_elapsed = LinUCB_Hybrid(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['LinUCB_Hybrid', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Create workbook (excel file)
    workbook = xlsxwriter.Workbook('./evaluations/evaluation_results_best_param_100%.xlsx')
    worksheet = workbook.add_worksheet()
    
    # Write the headers of the columns
    row = 0
    col = 0
    worksheet.write(row, col, 'Algorithm')
    worksheet.write(row, col + 1, 'parameter')
    worksheet.write(row, col + 2, 'CTR')
    worksheet.write(row, col + 3, 'relative CTR')
    worksheet.write(row, col + 4, 'time (ms)')
    row += 1 # Move to the next line.
    
    for row in range(5):
        for col in range(5):
            worksheet.write(row + 1, col, results[row, col])
            
    workbook.close()

############################################################################################
# Function to evaluate the parameters estimated by various experiments on the tuning data. #
# It receives as arguments the parameter_list which contains the different parameters for  #
# each algorithm, the file_name which will be used as the name of the expored excel file.  #
############################################################################################

def evaluate_rest(parameter_list, file_name):
    sess = 'evaluation' # Dataset to use for evaluation
    percentage = 1 # Run on this percentage = 100%
    
    # Load random article serving results.
    df = pd.read_excel('./evaluations/evaluation_results_best_param_100%.xlsx', sheet_name = 'Sheet1')
    CTR_random_serving = df['CTR'][0]
    CTR_time = df['time (ms)'][0]
    results = np.array(['random serving', '-', CTR_random_serving, '1', CTR_time])
    
    # Run e-greedy and append the results.
    epsilon = parameter_list[0]
    CTR, _, _, time_elapsed = e_greedy(epsilon, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['e-greedy', epsilon, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run UCB and append the results.
    alpha = parameter_list[1]
    CTR, _, _, time_elapsed = UCB(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['UCB', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run LinUCB and append the results.
    alpha = parameter_list[2]
    CTR, _, _, time_elapsed = LinUCB(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['LinUCB', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Run LinUCB Hybrid and append the results.
    alpha = parameter_list[3]
    CTR, _, _, time_elapsed = LinUCB_Hybrid(alpha, percentage, sess)
    relative_ctr = CTR/CTR_random_serving
    x = np.array(['LinUCB_Hybrid', alpha, CTR, relative_ctr, time_elapsed])
    results = np.vstack((results, x))
    
    # Create workbook (excel file)
    workbook = xlsxwriter.Workbook('./evaluations/' + file_name)
    worksheet = workbook.add_worksheet()
    
    # Write the headers of the columns
    row = 0
    col = 0
    worksheet.write(row, col, 'Algorithm')
    worksheet.write(row, col + 1, 'parameter')
    worksheet.write(row, col + 2, 'CTR')
    worksheet.write(row, col + 3, 'relative CTR')
    worksheet.write(row, col + 4, 'time (ms)')
    row += 1 # Move to the next line.
    
    for row in range(5):
        for col in range(5):
            worksheet.write(row + 1, col, str(results[row, col]))   
    workbook.close()

##################################################################
# Execute the above functions to produce the evaluation results. #
##################################################################
    
try:
    os.mkdir('evaluations')
    print("Directory " , 'evaluations' ,  " created ") 
except FileExistsError:
    print("Directory " , 'evaluations' ,  " already exists")

evaluate_best_parameters()
    
parameter_list = [0.075, 0.25, 0.25, 0.5]
file_name = 'evaluation_results_near_best_param_100%.xlsx'
evaluate_rest(parameter_list, file_name)

parameter_list = [0.02, 0.1, 0.05, 0.3]
file_name = 'evaluation_results_best_param_30%.xlsx'
evaluate_rest(parameter_list, file_name)

parameter_list = [0.02, 0.1, 0.1, 0.1]
file_name = 'evaluation_results_best_param_10%.xlsx'
evaluate_rest(parameter_list, file_name)

parameter_list = [0.1, 0.5, 0.1, 0.1]
file_name = 'evaluation_results_best_param_1%.xlsx'
evaluate_rest(parameter_list, file_name)












