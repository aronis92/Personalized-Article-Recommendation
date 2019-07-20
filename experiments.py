import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#############################################################
# Experiment 1 functions - Figures for 3-phase grid search. #
#############################################################

# Function to create the necessary directories.
def create_directories():
    try:
        os.mkdir('parameters exploration/figs')
        print("Directory " , 'parameters exploration/figs' ,  " created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration/figs' ,  " already exists")

    p = ['100%', '30%', '10%', '1%']
    for percentage in p:
        try:
            os.mkdir('parameters exploration/figs/' + percentage)
            print("Directory " , 'parameters exploration/figs/' + percentage,  " created ") 
        except FileExistsError:
            print("Directory " , 'parameters exploration/figs/' + percentage,  " already exists")
   
    try:
        os.mkdir('evaluations/figs')
        print("Directory " , 'evaluations/figs' ,  " created.") 
    except FileExistsError:
        print("Directory " , 'evaluations/figs' ,  " already exists.")
   
# Function to export figures for the exploration on the 100% of the dataset.
def plot_exploration_100(algorithm, CTR_random_serving, parameter):
    # e-greedy 1st exploration results
    df = pd.read_excel('./parameters exploration/100%/' + algorithm + '_exploration_1.xlsx', sheet_name = 'Sheet1')
    
    # Plot exploration
    x_1 = np.array(df['parameter'])
    y_1 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_1),)) )
    
    plt.figure()
    title = algorithm + ' 1st exploration'
    plt.title(title)
    plt.plot(x_1, y_1)
    plt.plot(x_1, y_1, 'ro', markersize=6)
    plt.xlabel(parameter)
    plt.ylabel('CTR')
    plt.savefig('./parameters exploration/figs/100%/' + title + '.png')
    plt.close()
    
    # e-greedy 2nd exploration results
    df = pd.read_excel('./parameters exploration/100%/' + algorithm +  '_exploration_2.xlsx', sheet_name = 'Sheet1')
    
    # Plot exploration
    x_2 = np.array(df['parameter'])
    y_2 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_2),)) )
    
    x_all = np.concatenate((x_1, x_2))
    y_all = np.concatenate((y_1, y_2))
    t = np.argsort(x_all)
    x_all = x_all[t]
    y_all = y_all[t]
    
    plt.figure()
    title = algorithm + ' 2nd exploration'
    plt.title(title)
    plt.plot(x_all, y_all) # [:(len(x_all) - 2)]
    plt.plot(x_1, y_1, 'ro', markersize=5) # [:(len(x_1) - 2)]
    plt.plot(x_2, y_2, 'go', markersize=5)
    plt.xlabel(parameter)
    plt.ylabel('CTR')
    plt.savefig('./parameters exploration/figs/100%/' + title + '.png')
    plt.close()
    
    # e-greedy 3rd exploration results
    df = pd.read_excel('./parameters exploration/100%/' + algorithm +  '_exploration_3.xlsx', sheet_name = 'Sheet1')
    
    # Plot exploration
    x_3 = np.array(df['parameter'])
    y_3 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_3),)) )
    
    x_all = np.concatenate((x_all, x_3))
    y_all = np.concatenate((y_all, y_3))
    t = np.argsort(x_all)
    x_all = x_all[t]
    y_all = y_all[t]
    
    plt.figure()
    title = algorithm + ' 3rd exploration'
    plt.title(title)
    plt.plot(x_all, y_all) # [:(len(x_all) - 4)]
    plt.plot(x_1, y_1, 'ro', markersize=4) # [:(len(x_1) - 4)]
    plt.plot(x_2, y_2, 'go', markersize=4)
    plt.plot(x_3, y_3, 'bo', markersize=4)
    plt.xlabel(parameter)
    plt.ylabel('CTR')
    plt.savefig('./parameters exploration/figs/100%/' + title + '.png')
    plt.close()

##############################################
# Create directories to save exported files. #
##############################################
create_directories()
    
########################################################
# Create plots for experiment 1 - 3-phase grid search. #
########################################################

# Random Serving Results
df = pd.read_excel('./parameters exploration/random_serving_results.xlsx', sheet_name = 'Sheet1')
CTR_random_serving = df['ctr'][0]

plot_exploration_100('e_greedy', CTR_random_serving, 'epsilon')
plot_exploration_100('UCB', CTR_random_serving, 'alpha')
plot_exploration_100('LinUCB', CTR_random_serving, 'alpha')
plot_exploration_100('LinUCB_Hybrid', CTR_random_serving, 'alpha')

#########################################################
# Experiment 2 & 3 - Performance on evaluation data for #
# the estimated parameters on the 100% of tuning data.  #
#########################################################

df = pd.read_excel('./evaluations/evaluation_results_best_param_100%.xlsx', sheet_name = 'Sheet1')

algorithms = np.array(df['Algorithm'])[1:]
ctr = np.array(df['relative CTR'])[1:]
time = np.array(df['time (ms)'])[1:]

# Bar Graph for performance - relative CTR
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, ctr, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/CTR_best_params_100%.png')
plt.close()

# Bar Graph for execution time (ms)
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, time, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/Time_best_params_100%.png')
plt.close()

#########################################################
# Experiment 4 - Figures for exploration on fractions   #
# of the tuning dataset.                                #
#########################################################

algorithm = 'e_greedy'
parameter = 'epsilon'
algorithm = ['e_greedy', 'UCB', 'LinUCB', 'LinUCB_Hybrid']
parameter = ['epsilon', 'alpha', 'alpha', 'alpha']

df = pd.read_excel('./evaluations/evaluation_results_best_param_100%.xlsx', sheet_name = 'Sheet1')
CTR_random_serving = df['CTR'][0]
for j in range(4):
    
    df = pd.read_excel('./parameters exploration/100%/' + algorithm[j] + '_exploration_1.xlsx', sheet_name = 'Sheet1')
    x_1 = np.array(df['parameter'])
    y_1 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_1),)) )
    
    df = pd.read_excel('./parameters exploration/100%/' + algorithm[j] +  '_exploration_2.xlsx', sheet_name = 'Sheet1')
    x_2 = np.array(df['parameter'])
    y_2 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_2),)) )
    x_all = np.concatenate((x_1, x_2))
    y_all = np.concatenate((y_1, y_2))
    t = np.argsort(x_all)
    x_all = x_all[t]
    y_all = y_all[t]
    
    df = pd.read_excel('./parameters exploration/100%/' + algorithm[j] +  '_exploration_3.xlsx', sheet_name = 'Sheet1')
    x_3 = np.array(df['parameter'])
    y_3 = np.array(df['ctr'])/ ( CTR_random_serving * np.ones((len(x_3),)) )
    
    x_all = np.concatenate((x_all, x_3))
    y_all = np.concatenate((y_all, y_3))
    t = np.argsort(x_all)
    x_all = x_all[t]
    y_all = y_all[t]
    
    colors = ['r', 'g', 'orange']
    percent = ['30%', '10%', '1%']
    for i in range(3):
        plt.figure()
        title = algorithm[j] + ' exploration on ' + percent[i] + ' of the dataset'
        plt.title(title)
        plt.plot(x_all, y_all)
        plt.xlabel(parameter[j])
        plt.ylabel('CTR')
    
        df = pd.read_excel('./parameters exploration/' + percent[i] + '/' + algorithm[j] +  '_exploration.xlsx', sheet_name = 'Sheet1')
        x = np.array(df['parameter'])
        y = np.array(df['ctr']) / ( CTR_random_serving * np.ones((len(x),)) )
        plt.plot(x, y, colors[i])
        plt.savefig('./parameters exploration/figs/' + percent[i] + '/' + title + '.png')
        plt.close()

####################################################
# Experiment 5 - Evaluation of 2nd best parameters #
# estimated on 100% of the tuning dataset.         #
####################################################

df = pd.read_excel('./evaluations/evaluation_results_near_best_param_100%.xlsx', sheet_name = 'Sheet1')
algorithms = np.array(df['Algorithm'])[1:]
ctr = np.array(df['relative CTR'])[1:]
time = np.array(df['time (ms)'])[1:]

# Bar Graph for performance on 2nd best parameters estimated by 100% of the dataset - relative CTR
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, ctr, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/CTR_near_best_params_100%.png')
plt.close()

######################################################
# Experiment 6.1 - Evaluation of 2nd best parameters #
# estimated on 30% of the tuning dataset.            #
######################################################

df = pd.read_excel('./evaluations/evaluation_results_best_param_30%.xlsx', sheet_name = 'Sheet1')
algorithms = np.array(df['Algorithm'])[1:]
ctr = np.array(df['relative CTR'])[1:]
time = np.array(df['time (ms)'])[1:]

# Bar Graph for performance on 2nd best parameters estimated by 100% of the dataset - relative CTR
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, ctr, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/CTR_best_params_30%.png')
plt.close()

######################################################
# Experiment 6.2 - Evaluation of 2nd best parameters #
# estimated on 10% of the tuning dataset.            #
######################################################

df = pd.read_excel('./evaluations/evaluation_results_best_param_10%.xlsx', sheet_name = 'Sheet1')
algorithms = np.array(df['Algorithm'])[1:]
ctr = np.array(df['relative CTR'])[1:]
time = np.array(df['time (ms)'])[1:]

# Bar Graph for performance on 2nd best parameters estimated by 100% of the dataset - relative CTR
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, ctr, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/CTR_best_params_10%.png')
plt.close()

######################################################
# Experiment 6.3 - Evaluation of 2nd best parameters #
# estimated on 1% of the tuning dataset.             #
######################################################

df = pd.read_excel('./evaluations/evaluation_results_best_param_1%.xlsx', sheet_name = 'Sheet1')
algorithms = np.array(df['Algorithm'])[1:]
ctr = np.array(df['relative CTR'])[1:]
time = np.array(df['time (ms)'])[1:]

# Bar Graph for performance on 2nd best parameters estimated by 100% of the dataset - relative CTR
y_pos = np.arange(len(algorithms))
plt.bar(y_pos, ctr, width = 0.4) # Create bars
plt.xticks(y_pos, algorithms) # Create names on the x-axis
plt.savefig('./evaluations/figs/CTR_best_params_1%.png')
plt.close()









