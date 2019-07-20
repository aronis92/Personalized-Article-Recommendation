import numpy as np
import psycopg2

###################################
# Insert Tuning Data in Database. #
###################################

loc = './Webscope/R6A/' # Relative folder directory.
file = 'ydata-fp-td-clicks-v1_0.20090502' # File name to insert

file = open(loc + file, "r", encoding="utf-8") # Open file
line = 'start' # Initialization to enter the loop.
count = 0 # Variable to monitor our progress.
line = file.readline() # Read 1st line.
# Value to monitor when timestamp on file changes in order
# to insert the new one and the candidates in the database.
old_timestamp = '' 
problem = '' # Value to save faulty candidates in order to avoid storing them.
try:
    # Connect to the database.
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    # Stop when the next time is empty (end of file).
    while line != '':
        # Print message every while to monitor our progress.
        if count==1000000 or count==2000000 or count==3000000 or count==4000000:
            print('checkpoint')
        count += 1
        parts = line.split('|') # Split input into a list containing 3 strings.
        event = parts[0].split() # The first one is the event. Split it further.
        
        user = np.array([c[2:] for c in parts[1].split()[1:]]) # The second is the User data. Keep the features
        candidates = [] # Initialize candidate articles to choose from.
        for i in range(2, len(parts)):
            cand = parts[i].split() # Split the values
            cand[1:] = [c[2:] for c in cand[1:]] # Remove the index of each attribute
            if len(cand)==7: # If length of attributes is 7 there is no fault in data.
                candidates.append(cand) # Append this article's attributes to the list.
            else: # If it isn't then do not keep this candidate and save its name as the problem for current timestamp.
                problem = cand[0]
        candidates = np.array(candidates) # Convert to array.

        # If this timestamp is not processed yet do the following.
        if old_timestamp != event[0]:
            
            # Fill articles table
            query = "SELECT article_id FROM articles"
            cursor.execute(query)
            results = cursor.fetchall()
            results = [c[0] for c in results]
            # Insert into articles the candidates which are not already inserted.
            for i in range(len(candidates)):
                if int(candidates[i,0]) not in results:
                    query = 'INSERT INTO articles (article_id, feature_1, feature_2, feature_3, feature_4, feature_5) VALUES ('\
                    + candidates[i,0] + ', ' + candidates[i,1] + ', ' + candidates[i,2] + ', ' + candidates[i,3] + ', '\
                    + candidates[i,4] + ', ' + candidates[i,5] + ');'
                    cursor.execute(query)
            
            # Fill timestamp table
            query = "INSERT INTO timestamps (timestamp) VALUES (" + event[0] + ");" # Insert into timestamps event[0].
            cursor.execute(query)
            
            # Fill candidates table
            query = "SELECT max(timestamp_id) FROM timestamps;"
            cursor.execute(query)
            result = cursor.fetchall()
            
            query = "INSERT INTO candidates(timestamp_id" 
            part1 = ''
            part2 = '(' + str(result[0][0])
            for i in range(len(candidates)):
                part1 += ", article_id_" + str(i + 1)
                part2 += ", " + str(candidates[i][0])
            query += part1 + ") VALUES " + part2 + ");"
            cursor.execute(query)
            conn.commit()
            old_timestamp = event[0] # Update the most recent inserted timestamp.

        # Fill event table
        query = "SELECT timestamp_id from timestamps WHERE timestamp = '" + event[0] + "';"
        cursor.execute(query)
        result = cursor.fetchall()
        timestamp_id = result[0][0]
        if event[1] != problem:
            query = " INSERT INTO events (timestamp_id, article_id, choice, user_feature_1, user_feature_2, user_feature_3,"\
            + "user_feature_4, user_feature_5 ) VALUES (" + str(timestamp_id) + ", " + event[1] + ", '" + event[2] + "'"
            for i in range(5):
                query += ", " + user[i]
            query += ");"
            cursor.execute(query)
            conn.commit()

        line = file.readline() # Read next line and repeat the same procedure.
    
except (Exception, psycopg2.Error) as error :
    print ("An error occured : ", error)
finally:
    if(conn):
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")

#####################################
# Repeat procedure for Tuning Data. #
#####################################
        
loc = './Webscope/R6A/'
file = 'ydata-fp-td-clicks-v1_0.20090502'

file = open(loc + file, "r", encoding="utf-8")
line = 'start'
count = 0
line = file.readline()
old_timestamp = ''
problem = ''
try:
    conn = psycopg2.connect(host="localhost", database="DB_Project", user="postgres", password="postgres")
    cursor = conn.cursor()
    while line != '':
        if count==1000000 or count==2000000 or count==3000000 or count==4000000:
            print('checkpoint')
        count += 1
        parts = line.split('|') # Split input into 3 strings
        event = parts[0].split() # The first one is the event
        
        if int(event[0]) != 1241247300:
            user = np.array([c[2:] for c in parts[1].split()[1:]]) # The second is the User data
            candidates = [] # Initialize candidate articles to choose from.
            for i in range(2, len(parts)):
                cand = parts[i].split() # Split the values
                cand[1:] = [c[2:] for c in cand[1:]] # Remove the index of each attribute
                if len(cand)==7:
                    candidates.append(cand) # Append this article's attributes to the list.
                else:
                    problem = cand[0]
            candidates = np.array(candidates)
    
            # If this timestamp is not processed yet do the following.
            if old_timestamp != event[0]:
                
                # Fill articles table
                query = "SELECT article_id FROM articles"
                cursor.execute(query)
                results = cursor.fetchall()
                results = [c[0] for c in results]
                # Insert into articles the candidates which are not already recorded.
                for i in range(len(candidates)):
                    if int(candidates[i,0]) not in results:
                        query = 'INSERT INTO articles (article_id, feature_1, feature_2, feature_3, feature_4, feature_5) VALUES ('\
                        + candidates[i,0] + ', ' + candidates[i,1] + ', ' + candidates[i,2] + ', ' + candidates[i,3] + ', '\
                        + candidates[i,4] + ', ' + candidates[i,5] + ');'
                        cursor.execute(query)
                
                # Fill timestamp table
                query = "INSERT INTO timestamps (timestamp) VALUES (" + event[0] + ");" # Insert into timestamps event[0].
                cursor.execute(query)
                
                # Fill candidates table
                query = "SELECT max(timestamp_id) FROM timestamps;"
                cursor.execute(query)
                result = cursor.fetchall()
                
                query = "INSERT INTO candidates(timestamp_id" 
                part1 = ''
                part2 = '(' + str(result[0][0])
                for i in range(len(candidates)):
                    part1 += ", article_id_" + str(i + 1)
                    part2 += ", " + str(candidates[i][0])
                query += part1 + ") VALUES " + part2 + ");"
                cursor.execute(query)
                conn.commit()
                old_timestamp = event[0] # Update the most recent inserted timestamp.
    
            # Fill event table
            query = "SELECT timestamp_id from timestamps WHERE timestamp = '" + event[0] + "';"
            cursor.execute(query)
            result = cursor.fetchall()
            timestamp_id = result[0][0]
            if event[1] != problem:
                query = " INSERT INTO events (timestamp_id, article_id, choice, user_feature_1, user_feature_2, user_feature_3,"\
                + "user_feature_4, user_feature_5 ) VALUES (" + str(timestamp_id) + ", " + event[1] + ", '" + event[2] + "'"
                for i in range(5):
                    query += ", " + user[i]
                query += ");"
                cursor.execute(query)
                conn.commit()
            # End if here
        line = file.readline()
    
except (Exception, psycopg2.Error) as error :
    print ("An error occured : ", error)
finally:
    if(conn):
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")


