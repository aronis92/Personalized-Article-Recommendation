from retrieve_data import retrieve_timestamps, retrieve_articles, retrieve_events, retrieve_candidates
import numpy as np
import time

############################################################################################
# This file contains the function LinUCB that receives as argument the parameter alpha,    #
# the percentage which indicates the fraction of the dataset to be used and the parameter  #
# sess which indicates if the algorithm will run on tuning or evaluation data.             #
# That parameter epsilon changes the balance between exploration and exploitation.         #
# The CTR, total_reward, T, time_elapsed are calculated are returned.                      #
############################################################################################

def LinUCB(alpha, percentage, sess):
    
    # Retrieve timestamps and article information.
    start, end = retrieve_timestamps(sess) # Retrieve timestamp ids.
    all_article_ids, articles_features = retrieve_articles() # Retrieve article ids and features.
    
    # Variable intialization.
    total_reward = 0 # Variable that keeps the total reward.
    d = len(articles_features[0]) # Dimensionality of the articles features (the constant 1 is missing but the id is present so we don't need to modify the result.)
    T = 0 # Number of trials.
    indices_all = {} # Dictionary that keeps article ids and their corresponding indices. 
    n_articles = len(all_article_ids) # The number of articles in the database.
    
    # Initialization of the needed matrices for the algorithm.
    A = np.zeros((n_articles, d, d)) # size (72, 6, 6)
    A_inv = np.zeros((n_articles, d, d)) # size (72, 6, 6)
    b = np.zeros((n_articles, d, 1)) # size (72, 6, 1)
    theta = np.zeros((n_articles, d, 1)) # size (72, 6, 1)
    
    # Create a dictionary that matches each article to its position in the global arrays.
    # Global arrays contain the information for all articles even if they are not candidates for the current tiimestamp.
    # These indices correspond to the position (0-71) each article occupies in the matrices above.
    # For each timestamp only the positions of candidates are chosen from these global arrays.
    i = 0
    for article_id in all_article_ids:
        indices_all[article_id] = i
        A[i] = np.identity(d)
        A_inv[i] = np.identity(d)
        i += 1
    
    # Run the algorithm on the dataset.
    tick = time.time() # Start the timer.
    for timestamp_id in range(start, end): # Iterate through all timestamps.
        candidates = retrieve_candidates(timestamp_id) # Retrieve all candidates for current timestamp.
        events = retrieve_events(timestamp_id) # Retrieve events associated with the current timestamp.
        iterations = np.round(percentage*len(events)) # Maximum number of iterations for this timestamp. 
        
        # Create a list matching each position of the n_candidates to its global index
        # in order to update the right positions in the global arrays.
        indices_current_timestamp = [indices_all[article] for article in candidates] 
        
        i = 0 # Position of the event we are processing.
        while i < iterations: # Iterate through the events.
            chosen_article = events[i,0] # The article that was chosen to be served to the user in the current event.
            reward = events[i,1] # The reward, 0 or 1.
            x = events[i,2:].reshape(d,1) # The user's features.
            # Update Theta for all candidates.
            theta[indices_current_timestamp] = np.matmul(A_inv[indices_current_timestamp], b[indices_current_timestamp]) 
            # Calculate some quantities needed to calculate p for all candidates.
            quantity_1 = np.matmul( np.transpose(theta[indices_current_timestamp],(0,2,1)), x )
            quantity_2 = np.sqrt(np.matmul(x.T, A_inv[indices_current_timestamp].dot(x)))
            p = (quantity_1 + alpha * quantity_2)[:,:,0] # Update UCB for all candidates
            # Choose which arm to show to the user.
            max_candidate_index = np.argmax(p) # Calculate the index (0-71) of the candidate with highest p.
            # Get the index of this candidate in the pool of arms [0, n_articles) of this timestamp.
            recommended_arm = indices_current_timestamp[max_candidate_index]
            recommended_article = candidates[max_candidate_index] # Get it's global index.
            # If the chosen article to be served matched the current event do the rest, otherwise move to the next event.
            if recommended_article == chosen_article:
                # Update some indices in the arrays.
                A[recommended_arm] += np.outer(x,x)
                A_inv[recommended_arm] = np.linalg.inv(A[recommended_arm])
                b[recommended_arm] += reward * x
                theta[recommended_arm] = A_inv[recommended_arm].dot(b[recommended_arm])
                total_reward += reward # Add it in the total reward.
                T += 1 # Count the trial.
            i += 1 # Move to the next event-iteration.
    tock = time.time() # End timer.
    click_through_rate = total_reward/T # Calculate the Click Through Rate for the Algorithm
    elapsed_time = tock - tick # Calculate elapsed time.
    return click_through_rate, total_reward, T, elapsed_time # Return the results.

############################################################################
# Uncomment and run the following lines if you don't want an excel export. #
############################################################################
    
#alpha = 5
#ctr, total_reward, T = LinUCB(alpha, 1, 'tuning')












