import numpy as np
import psycopg2

##############################################################################################
# This file contains 4 functions that are responsible for retrieving data from the database. #
# - retrieve_candidates receives as an argument a timestamp_id and retrieves                 #
#   the articles that correspond to that specific timestamp.                                 #
# - retrieve_events receives also a timestamp_id as an argument                              #
#   and retrieves the recorded events for that timestamp.                                    #                                                                       #
# - retrieve_timestamps receives the argument sess and retrieves the minimum and             #
#   maximum timestamp ids of the tuning or evaluation datasets.                              #
#   Note that the timestamp ids are the primary key (SERIAL) and thus every timestamp        #
#   between these min and max exists.                                                        #
# - retrieve_articles receives also no arguments and retrieves the whole pool of articles    #
#   (72) i.e. id and features regardless of their timestamp in order to initialize           #
#   the arrays accordingly.                                                                  #
##############################################################################################

def retrieve_candidates(timestamp_id):
    
    # Connect to the database.
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    
    # Retrieve candidates for current timestamp
    query = "SELECT * FROM candidates WHERE timestamp_id = " + str(timestamp_id) + ";"
    cursor.execute(query)
    candidates = cursor.fetchall()[0] # Each timestamp id is one row in this array so we go into [0] position since there are no others.
    
    # Close Connection to Database and return the results
    cursor.close()
    conn.close()
    
    # Return the array of candidates.
    try:
        last = candidates.index(None) # Find the position of the last None element (if there are less articles than 24)
    except:
        last = len(candidates) # Otherwise keep the length of the candidates which is one more .
    candidates = np.array(candidates[1:last]) # Keep from the second element (1st is timestamp_id), up to the one before last position.
    return candidates

def retrieve_events(timestamp_id):
    
    # Connect to the database.
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    
    # Retrieve Events for current timestamp
    query = "SELECT article_id, choice, user_feature_1, user_feature_2, user_feature_3, user_feature_4, user_feature_5 "\
    + "FROM events WHERE timestamp_id = " + str(timestamp_id) + ";"
    cursor.execute(query)
    results = cursor.fetchall() # Get the results of the query
    
    # Close Connection to Database and return the results
    cursor.close()
    conn.close()
    
    # Results processing.
    events = [] # Empty list that we will add each event after some processing.
    for i in range(len(results)): # Iterate through the results.
        # Create a new event and insert in the event the article_id and the click, no-click response from the user.
        event = [results[i][0], int(results[i][1])]
        # Extend the list adding the features of the user after converting from string to float.
        event.extend([float(c) for c in results[i][2:]]) 
        event.append(1) # Append the constant value of 1 in each vector.
        events.append(event) # Append the processed event.
    events = np.array(events) # Convert to numpy array.
    return events

def retrieve_timestamps(sess):
    
    # Choose which timestamps to return
    if sess == 'tuning':
        rest = "WHERE timestamp_id <= 528"
    elif sess == 'evaluation':
        rest = "WHERE timestamp_id > 528;"
    
    # Connect to the database.
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    
    # Retrieve the range of timestamps.
    query = "SELECT min(timestamp_id), max(timestamp_id) FROM timestamps " + rest
    cursor.execute(query)
    results = cursor.fetchall() # There are 2 results
    
    # Close connection to the database.
    cursor.close()
    conn.close()
    
    # Return the first and last timestamp
    start = results[0][0] # The first one is the minimum timestamp_id
    end = results[0][1] # The second is the maximum timestamp_id
    return start, end

def retrieve_articles():
    
    # Connect to the database.
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    
    # Retrieve all articles' ids and features.
    query = "SELECT * FROM articles;"
    cursor.execute(query)
    all_articles = cursor.fetchall()
    
    # Close connection to the database.
    cursor.close()
    conn.close()
    
    # Process the results.
    all_article_ids = [value[0] for value in all_articles] # Create a list containing only the ids
    n_articles = len(all_article_ids) # Number of articles in the pool to choose from.
    temp = [list(value[1:]) for value in all_articles] # List of lists containing only the features of each article as Decimals
    articles_features = np.array([float(v) for v in temp[0]]) # Create an array converting to float all values of first article.
    for i in range(1, len(temp)): # Then do the same for the rest one by one and append the results verticaly. 
        articles_features = np.vstack((articles_features, np.array([float(v) for v in temp[i]])))
    # This will produce a matrix of size (n_articles, 5).
    # These vectors do not contain the constant of 1 so we add it now as a column to the right side of the matrix.
    articles_features = np.column_stack((articles_features, np.ones((n_articles,1)))) 
    return all_article_ids, articles_features



    
