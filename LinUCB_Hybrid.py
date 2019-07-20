from retrieve_data import retrieve_timestamps, retrieve_articles, retrieve_events, retrieve_candidates
import numpy as np
import time

##########################################################################################
# This file contains the function LinUCB_Hybrid that receives as argument the parameter  #
# alpha, the percentage which indicates the fraction of the dataset to be used and the   #
# parameter sess which indicates if the algorithm will run on tuning or evaluation data. #
# That parameter epsilon changes the balance between exploration and exploitation.       #
# The CTR, total_reward, T, time_elapsed are calculated are returned.                    #
##########################################################################################

def LinUCB_Hybrid(alpha, percentage, sess):
    
    # Retrieve timestamps and article information
    start, end = retrieve_timestamps(sess)
    all_article_ids, articles_features = retrieve_articles()
    
    # Initialize some variables
    total_reward = 0 # Variable that keeps the total reward.
    d = len(articles_features[0]) # Dimensionality of the articles features (the constant 1 is missing but the id is present so we don't need to modify the result.)
    k = d**2 # Dimensionality of the shared features
    T = 0 # Number of trials
    indices_all = {} # Dictionary that keeps article ids and their corresponding indices. 
    n_articles = len(all_article_ids) # The number of articles in the database
    
    # Initialization of the needed matrices for the algorithm.
    A0 = np.identity(k) # Matrix to compute hybrid part, size (k, k)
    A0_inv = np.identity(k) # Inverse of A0, stored for efficiency, size (k, k)
    b0 = np.zeros((k, 1)) # Vector to compute hybrid part, size (k, 1)
    A = np.zeros((n_articles, d, d)) # Matrix for the disjoint part, size (72, 6, 6)
    A_inv = np.zeros((n_articles, d, d)) # Matrix Aa storing the inverse of A for efficiency, size (72, 6, 6)
    B = np.zeros((n_articles, d, k)) # Matrix Ba, size (72, 6, 36)
    B_T = np.zeros((n_articles, k, d)) # Transpose of B for efficiency, size (72, 36, 6)
    b = np.zeros((n_articles, d, 1)) # Matrix ba, size (72, 6, 1)
    theta = np.zeros((n_articles, d, 1)) # Matrix storing thetas, size (72, 6, 1)
    beta = np.zeros((k, 1)) # Matrix storing b_hat, size (36, 1)
    
    # Initialization of matrices containing quantities needed for calculations
    A_inv_b = np.zeros((n_articles, d, 1)) # A_inv * b, size (72, 6, 1)
    A_inv_B = np.zeros((n_articles, d, k)) # A_inv * B, size (72, 6, 36)
    A0_inv_B_T_A_inv = np.zeros((n_articles, k, d)) # A0_inv * B_T * A_inv, size (72, 36, 6)
    
    # Fill the dictionary with article ids and their index
    # These indices correspond to the position (0-71) each article occupies in the matrices above
    i = 0
    for article_id in all_article_ids:
        indices_all[article_id] = i
        A[i] = np.identity(d) # Initialize slices of A corresponding to each article as identity matrices.
        A_inv[i] = np.identity(d) # Do the same for the inverse of A.
        i += 1
    
    tick = time.time() # Start the timer.
    for timestamp_id in range(start, end): # Iterate through the timestamps
        
        # Load candidates and events for current timestamp from database.
        candidates = retrieve_candidates(timestamp_id)
        events = retrieve_events(timestamp_id) 
        iterations = np.round(percentage*len(events)) # Maximum number of iterations for this timestamp.
        n_candidates = len(candidates) # Number of articles in the pool for this timestamp.
        
        # Keep the indices of this timestamp's candidates only. We will need only them for all iterations.
        indices_current_timestamp = [indices_all[article] for article in candidates] 
        
        i = 0 # Position of the event we are processing, starting at 0 for each timestamp.
        while i < iterations: #Repeat till there are no more events.
            
            # Process the current event
            chosen_article = events[i,0] # Pick the event's article_id
            reward = events[i,1] # 0 (no-click) or 1 (click)
            x = events[i,2:].reshape(d,1) # The User features, size (6,1)
            
            # Calculate shared features for each article. It is the outer product of current user and articles features
            z = np.outer(articles_features[indices_current_timestamp], x).reshape((n_candidates, k, 1)) # (n_articles, 36, 1)
            z_T = np.transpose(z,(0,2,1)) # (n_articles, 1, 36)
            
            # Calculate some quantities needed to calculate s
            A0_inv_z = np.matmul(A0_inv, z) # (n_articles, 36, 1)
            A0_inv_B_T_A_inv_x = np.matmul(A0_inv_B_T_A_inv[indices_current_timestamp], x) # (n_articles, 36, 1)
            A_inv_x = A_inv[indices_current_timestamp].dot(x) # (n_articles, 6, 1)
            A_inv_B_A0_inv_B_T_A_inv_x = np.matmul(A_inv_B[indices_current_timestamp], A0_inv_B_T_A_inv_x) # n_articles, 6, 1)
            # Calculate St,a 
            s = np.matmul(z_T, A0_inv_z - 2*A0_inv_B_T_A_inv_x) + np.matmul(x.T, A_inv_x + A_inv_B_A0_inv_B_T_A_inv_x) # (n_articles, 1, 1)
            s[s<0] = 0 # remove negative values since s will be used in a squared root.
            
            # Calculate p
            p = z_T.dot(beta) + np.matmul(x.T, theta[indices_current_timestamp]) + alpha * np.sqrt(s) # (n_articles, 1, 1)
            
            # Choose which arm to show to the user.
            max_candidate_index = np.argmax(p) # Calculate the index (0-71) of the candidate with highest p.
            
            # Get the index of this candidate in the pool of arms [0, n_articles) of this timestamp.
            recommended_arm = indices_current_timestamp[max_candidate_index]
            recommended_article = candidates[max_candidate_index] # Get the id of the recommended article
            
            # If the recommended article is the same as the current logged event continue with the updates.
            # Otherwise move to the next logged event and repeat the above.
            if recommended_article == chosen_article:
                # Update the matrices.
                A0 += B_T[recommended_arm].dot(A_inv_B[recommended_arm])
                b0 += B_T[recommended_arm].dot(A_inv_b[recommended_arm])
                A[recommended_arm] += np.dot(x, x.T)
                A_inv[recommended_arm] = np.linalg.inv(A[recommended_arm])
                B[recommended_arm] += np.dot(x, z_T[max_candidate_index])
                B_T[recommended_arm] = np.transpose(B[recommended_arm])
                b[recommended_arm] += reward * x
                A_inv_b[recommended_arm] = np.dot(A_inv[recommended_arm], b[recommended_arm])
                A_inv_B[recommended_arm] = np.dot(A_inv[recommended_arm], B[recommended_arm])
                A0 += np.dot(z[max_candidate_index], z_T[max_candidate_index]) - np.dot(B_T[recommended_arm], A_inv_B[recommended_arm])
                b0 += reward * z[max_candidate_index] - np.dot(B_T[recommended_arm], A_inv_b[recommended_arm])
                A0_inv = np.linalg.inv(A0)
                A0_inv_B_T_A_inv[recommended_arm] = A0_inv.dot(B_T[recommended_arm]).dot(A_inv[recommended_arm])
                beta = np.dot(A0_inv, b0)
                theta = A_inv_b - np.dot(A_inv_B, beta)
                total_reward += reward # Update the total reward.
                T += 1 # Record the trial.
            i += 1 # Move to the next iteration - event.
    tock = time.time() # End timer.
    click_through_rate = total_reward/T # Calculate the Click Through Rate for the Algorithm.
    elapsed_time = tock - tick # Calculate elapsed time.
    return click_through_rate, total_reward, T, elapsed_time # Return the results.

############################################################################
# Uncomment and run the following lines if you don't want an excel export. #
############################################################################
    
#alpha = 0.5
#ctr, total_reward, T = LinUCB_Hybrid(alpha, 1, 'tuning')



