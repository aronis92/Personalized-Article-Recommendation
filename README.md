<h1>Personalized News Article Recommendation through Contextual-Bandits</h1>

<h2>Problem Definition & Overview</h2>
<p>The problem that this repository is called to solve is the recommendation of well-suited articles to users with different profiles.
To do so, the algorithms of the paper "A Contextual-Bandit Approach to Personalized News Article Recommendation" are implemented along with other approaches that don't take into consideration the contextual features of users and articles.
Finally, a comparison of different approaches in terms of Click Through Rate rise and Time efficiency is conducted.</p>

<h2>Dataset</h2>
<p>The dataset that was used for the various experiments and parameter tunning was the R6A - Yahoo! Front Page Today Module User Click Log Dataset and it can be found: <a href="https://webscope.sandbox.yahoo.com/catalog.php?datatype=r&guccounter=1">here</a> </p>
<p>The dataset contains logged events of articles that were chosen to be shown to different users and their response (click or no-click).</p>

<h2>Solution</h2>
<p>At first the simpler algorithms (random serving, e-greedy, UCB) were implemented and tested using a "dummy" dataset.</p>
<p>The next step was to transform and store the Yahoo dataset into a postgreSQL database using the file fill_database.py.</p>
<p>After the dataset was inserted in the database the e-greedy and UCB algorithms were applied. After that the LinUCB and LinUCB Hybrid algorithms were implemented.</p>
<p>A series of experiments were conducted. At first a grid-search was conducted on the tunning data to find the parameter that maximizes the click through rate for each algorithm (exploration.py). Then using these best parameters we tested the results of each algorithm on the evaluation data (experiments.py).

<h2>Notes</h2>
<p>In order to run the experiment you will need to have installed Python >= 3.6 and the following libraries.
matplotlib.pyplot, xlsxwriter, psycopg2, random, pandas, numpy, xlrd, math, time, os, operator.add </p>

<p>The database that was used in our implementation is version 11 of postgreSQL so you need to have this installation as well. You will need to create a user with username=postgres and password=postgres (default) and a clean database named DB_Project.</p>

<p>After the database is created and filled with our data you can run the experiments by executing the python files exploration.py, evaluation.py and experiments.py in that order. After they are successfully executed the directories "parameters exploration" and "evaluations" will be created containing the corresponding excel files and figures. Inside each folder you will find subfolders named after percentages that correspond to the experiments regarding this percentage. For example in the folder "parameters exploration/30%"" you will find the excel files that were exported during the parameter exploration on the 30% of the tuning dataset. The figures are inside different subfolders named figs.</p>
