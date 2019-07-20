from retrieve_data import retrieve_timestamps, retrieve_articles, retrieve_events, retrieve_candidates
import numpy as np
import time

############################################################################################
# This file contains the function random_serve that receives the argument sess with values #
# 'tuning' or 'evaluation' which indicate the dataset the algorithm will run on.           #
# It calculates and returns the CTR, total_reward, number of trials T                      #
# and time_elapsed for a random article serving policy.                                    #
############################################################################################

def random_serve(sess):
    
    # Retrieve timestamps and article information.
    start, end = retrieve_timestamps(sess)
    all_article_ids, _ = retrieve_articles()
    
    # Initialize some variables.
    total_reward = 0 # Variable that keeps the total reward.
    T = 0 # Number of trials.
    
    # Run the algorithm.
    tick = time.time() # Start timer
    for timestamp_id in range(start, end): # Iterate through all timestamps.
        candidates = retrieve_candidates(timestamp_id) # Retrieve all candidates for current timestamp.
        events = retrieve_events(timestamp_id) # Retrieve events associated with the current timestamp.
        iterations = len(events) # Number of times that we will train for.
        n_candidates = len(candidates) # The number of selected articles in each timestamp.
        i = 0
        while i < iterations: # Iterate through the events.
            # Generate a random number between [0, n_candidates) which is the article that will be served.
            candidate_index = np.random.randint(0, n_candidates) 
            found = False # Variable to stop moving to next events until we find a match.
            while not found and i < iterations: # While a match is not found and there are more events continue.
                # If the chosen article to be served matched the current event do the rest, otherwise move to the next event.
                if candidates[candidate_index] == events[i][0]: 
                    reward = events[i][1] # Reward 0 or 1.
                    total_reward += reward # Add it in the total reward.
                    found = True # Change variable to end internal loop.
                    T += 1 # Count the trial.
                i += 1 # Move to the next event-iteration.
    tock = time.time() # End timer.
    time_elapsed = tock - tick # Calculate elapsed time.
    click_through_rate = total_reward/T # Calculate the CTR.
    return click_through_rate, total_reward, T, time_elapsed # Return the results.

###########################################################################
# Uncomment and run the following line if you don't want an excel export. #
###########################################################################
    
#ctr, total_reward, T, time_elapsed = random_serve() 























