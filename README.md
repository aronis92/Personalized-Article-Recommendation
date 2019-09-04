1) In order to run the experiment you will need to have installed Python >= 3.6 and the following libraries.
import matplotlib.pyplot as plt
import xlsxwriter
import psycopg2
import random
import pandas as pd
import numpy as np
import xlrd
import math
import time
import os
from operator import add 

2) The database that was used in our implementation is version 11 of postgreSQL so you need to have this installation as well
   You will need to create a user with username=postgres and password=postgres (default) and a clean database named DB_Project.

3) The dataset is provided in raw files located in Webscope/R6A/ which can be used in combination with fill_database.py to create the data from scratch.
   We also provide a restore file for faster insertion in the database. The restore file could not be uploaded to GitHub due to its volume
   but you can find it in our shared google drive folder: https://drive.google.com/open?id=1-LBLXnDqgYZN4tTV4pqwRwT3T1cbWLpZ

4) After the database is created and filled with our data you can run the experiments by executing the python files
   exploration.py, evaluation.py and experiments.py in that order.
   After they are successfully executed the directories "parameters exploration" and "evaluations" will be created containing
   the corresponding excel files and figures.
   Inside each folder you will find subfolders named after percentages that correspond to the experiments regarding this percentage.
   For example in the folder "parameters exploration/30%"" you will find the excel files that were exported during the parameter
   exploration on the 30% of the tuning dataset.
   The figures are inside different subfolders named figs.

5) However, we have already uploaded all the results in our GitHub folder since the
   explorations and evaluations make need a lot of time to run.