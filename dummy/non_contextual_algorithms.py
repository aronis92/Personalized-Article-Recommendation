from __future__ import division
import numpy as np
import pandas as pd
import random
import math

# Importing the dataset
dataset = pd.read_csv('./ads-ctr-optimisation/Ads_CTR_Optimisation.csv')

# Implementing Random Selection
def random_selection():
    iterations = 10000
    n_articles = 10
    ads_selected = []
    total_reward = 0
    for i in range(iterations):
        ad = random.randrange(n_articles)
        ads_selected.append(ad)
        reward = dataset.values[i, ad]
        total_reward = total_reward + reward
    return total_reward

def epsilon_greedy(epsilon):
    iterations = 10000 # Number of times that we will train for.
    n_articles = 10 # Pool of articles to choose from.
    ads_selected = [] # The selected ads in each step.
    numbers_of_selections = np.zeros(n_articles) # How many times each article was chosen.
    sums_of_reward = np.zeros(n_articles) # The reward each article resulted.
    q_val = np.zeros(n_articles) # Stores the expected payment of each arm for a round.
    total_reward = 0 # The total reward.
    for i in range(iterations):
        ad = 0 # Initialization of variable pointing to an ad index.
        rand = np.random.random_sample() # 
        if rand <= epsilon:
            ad = random.randrange(n_articles)
        else:
            q_val = sums_of_reward / (numbers_of_selections + (numbers_of_selections == 0)*1 )
            ad = np.argmax(q_val)
        ads_selected.append(ad)
        numbers_of_selections[ad] += 1
        reward = dataset.values[i, ad]
        sums_of_reward[ad] += reward
        total_reward += reward
    return total_reward

def ucb(cf):
    iterations = 10000
    n_articles = 10
    ads_selected = []
    numbers_of_selections = np.zeros(n_articles) # How many times each article was chosen.
    sums_of_reward = np.zeros(n_articles) # The reward each article resulted.
    average_reward = np.zeros(n_articles)
    delta_i = np.zeros(n_articles)
    upper_bound = np.zeros(n_articles)
    total_reward = 0
    for i in range(iterations):
        ad = 0
        average_reward = sums_of_reward / (numbers_of_selections + (numbers_of_selections == 0)*1 )
        delta_i = cf * np.sqrt(2 * math.log(i + 1) / (numbers_of_selections + (numbers_of_selections == 0)*1 ))
        upper_bound = (average_reward + delta_i) * (numbers_of_selections > 0 ) + 1000 * (numbers_of_selections == 0 )
        ad = np.argmax(upper_bound)
        ads_selected.append(ad)
        numbers_of_selections[ad] += 1
        reward = dataset.values[i, ad]
        sums_of_reward[ad] += reward
        total_reward += reward
    return total_reward

# Observe reward of choosing ads randomly and never exploiting the optimal one.
random_result = random_selection()
print('Random Selection Result : ', random_result)

# Observe reward of choosing ads according to an epsilon-greedy policy.
epsilon = 0.1
epsilon_result = epsilon_greedy(epsilon)
print('Epsilon-Greedy Result: ', epsilon_result)

# Observe reward of choosing ads according to an UCB policy.
corrective_factor = 0.05
ucb_result = ucb(corrective_factor)
print('UCB Result : ', ucb_result)














