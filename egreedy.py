from retrieve_data import retrieve_timestamps, retrieve_articles, retrieve_events, retrieve_candidates
import numpy as np
import random
import time

#############################################################################################
# This file contains the function e_greedy that receives as argument the parameter epsilon, #
# the percentage which indicates the fraction of the dataset to be used and the parameter   #
# sess which indicates if the algorithm will run on tuning or evaluation data.              #
# That parameter epsilon changes the balance between exploration and exploitation.          #
# The CTR, total_reward, T, time_elapsed are calculated are returned.                       #
#############################################################################################

def e_greedy(epsilon, percentage, sess):
    
    # Retrieve timestamps and article information.
    start, end = retrieve_timestamps(sess)
    all_article_ids, articles_features = retrieve_articles()
    
    # Initialize some variables
    n_articles = len(all_article_ids)
    indices_all = {} # Dictionary that keeps article ids and their corresponding indices.
    total_reward = 0 # Variable that keeps the total reward.
    T = 0 # Number of trials.
    
    # Necessary arrays to calculate the best arm at each step.
    numbers_of_selections = np.zeros(n_articles) # How many times each article was chosen.
    sums_of_reward = np.zeros(n_articles) # The reward each article resulted.
    q_val = np.zeros(n_articles) # Stores the expected payment of each arm for a round.
    
    # Create a dictionary that matches each article to its position in the global arrays.
    # Global arrays contain the information for all articles even if they are not candidates for the current tiimestamp.
    # For each timestamp only the positions of candidates are chosen from these global arrays.
    i = 0
    for article_id in all_article_ids:
        indices_all[article_id] = i
        i += 1
    
    # Run the algorithm.
    tick = time.time() # Start the timer.
    for timestamp_id in range(start, end): # Iterate through all timestamps.
        candidates = retrieve_candidates(timestamp_id) # Retrieve all candidates for current timestamp.
        events = retrieve_events(timestamp_id) # Retrieve events associated with the current timestamp.
        iterations = np.round(percentage*len(events)) # Number of times that we will train for.
        n_candidates = len(candidates) # The number of selected articles in each timestamp.
        
        # Create a list matching each position of the n_candidates to its global index
        # in order to update the right positions in the global arrays.
        indices_current_timestamp = [indices_all[article] for article in candidates]
        i = 0
        while i < iterations: # Iterate through the events
            rand = np.random.random_sample() # Generate a random value in [0, 1)
            if rand <= epsilon: # If this value is not greater than epsilon then 
                candidate_index = random.randrange(n_candidates) # select a random article to serve the user
                global_index = indices_current_timestamp[candidate_index] # Get it's global index
            # Otherwise select the article with the highest expected reward which is
            # the ratio of total reward an arm has contributed over the number of times it was selected.
            else: 
                # Calculate the denominator (add 1 if it has not been selected before to avoid division by zero).
                # If the number of selections is 0 then the total reward would be zero so the ration would be zero.
                # Apply this division only on the indices of the current timestamp.
                denominator = (numbers_of_selections + (numbers_of_selections == 0)*1 )[indices_current_timestamp]
                # Calculate the ratio for all timestamp candidates.
                q_val[indices_current_timestamp] = sums_of_reward[indices_current_timestamp] / denominator
                # Get the index of the maximum q_val for the indices of current timestamp.
                candidate_index = np.argmax(q_val[indices_current_timestamp])
                global_index = indices_current_timestamp[candidate_index] # Get it's global index.
                        
            found = False # Variable to stop moving to next events until we find a match.
            while not found and i < iterations: # While a match is not found and there are more events continue.
                # If the chosen article to be served matched the current event do the rest, otherwise move to the next event.
                if candidates[candidate_index] == events[i][0]:
                    numbers_of_selections[global_index] += 1 # Update the number of selections for the chosen article.
                    reward = events[i][1] # Reward 0 or 1.
                    sums_of_reward[global_index] += reward # Add the reward to the total reward of the chosen article.
                    total_reward += reward # Add it in the total reward.
                    found = True # Change variable to end internal loop.
                    T += 1 # Count the trial.
                i += 1 # Move to the next event-iteration.
    tock = time.time() # End timer.
    time_elapsed = tock - tick # Calculate elapsed time.
    click_through_rate = total_reward/T # Calculate the CTR.
    return click_through_rate, total_reward, T, time_elapsed # Return the results.

############################################################################
# Uncomment and run the following lines if you don't want an excel export. #
############################################################################

#epsilon = 0.1
#ctr, total_reward, T, time_elapsed = e_greedy(epsilon, 1, 'tuning')








