import xlsxwriter
from operator import add
import os

#######################################################################################################
# Function that receives as parameters                                                                #
#  - A string value which is the name of the excel file to be exported.                               #
#  - A list containing the real valued parameters to be explored by the Bandit algorithm.             # 
#  - The name of the function that will be used as testing policy.                                    #
#  - A logical value describing the need for averaging in order to produce a more trustworthy result. #
#######################################################################################################

def export_excel(excel_name, param_list, function, averaging, percentage):
    
    # Create workbook (excel file)
    workbook = xlsxwriter.Workbook('./parameters exploration/' + excel_name)
    worksheet = workbook.add_worksheet()
    
    # Write the headers of the columns
    row = 0
    col = 0
    worksheet.write(row, col, 'parameter')
    worksheet.write(row, col + 1, 'ctr')
    worksheet.write(row, col + 2, 'total_reward')
    worksheet.write(row, col + 3, 'T')
    worksheet.write(row, col + 4, 'time')
    row += 1 # Move to the next line.
    
    # Iterate through every parameter in the list.
    for param in param_list:
        sums = [0, 0, 0, 0] # Initialization of sums of CTR, total_reward, T, time_elapsed respectively.
        print('\nparameter : ', param) # Message to monitor process while running.
        
        # If averaging is needed the process is repeated 10 times to calculate the average values.
        if averaging:
            for j in range(10):
                print(j + 1, end = " ") # Message to monitor process while running.
                ctr, total_reward, T, time_elapsed = function(param, percentage) # Run the given algorithm with the current parameter.
                sums = list( map(add, sums, [ctr, total_reward, T, time_elapsed]) ) # Add the results to the sums.
            ctr, total_reward, T, time_elapsed = [v/10 for v in sums] # Calculate the mean value of the sums.
        # If no average is needed the given algorithm is executed one time.
        else:
            ctr, total_reward, T, time_elapsed = function(param, percentage) # Run the given algorithm with the current parameter.

        worksheet.write(row, col, param) # Write the given parameter on the excel.
        # Write the CTR, total_reward, T, time_elapsed results in the same line
        worksheet.write(row, col + 1, ctr)
        worksheet.write(row, col + 2, total_reward)
        worksheet.write(row, col + 3, T)
        worksheet.write(row, col + 4, time_elapsed)
        row += 1 # Move to the next line.
    
    workbook.close() # Close and save the excel file.

################################################################
# Function to create needed directories to export excel files. #
################################################################
    
def create_directories():
    
    try:
        os.mkdir('parameters exploration')
        print("Directory " , 'parameters exploration' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration' ,  " already exists")
        
    try:
        os.mkdir('parameters exploration/100%')
        print("Directory " , 'parameters exploration/100%' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration/100%' ,  " already exists")
        
    try:
        os.mkdir('parameters exploration/1%')
        print("Directory " , 'parameters exploration/1%' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration/1%' ,  " already exists")
        
    try:
        os.mkdir('parameters exploration/10%')
        print("Directory " , 'parameters exploration/10%' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration/10%' ,  " already exists")
        
    try:
        os.mkdir('parameters exploration/30%')
        print("Directory " , 'parameters exploration/30%' ,  " Created ") 
    except FileExistsError:
        print("Directory " , 'parameters exploration/30%' ,  " already exists")
    
    