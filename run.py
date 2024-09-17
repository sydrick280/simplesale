import datetime
import pandas
import numpy as np
import os
import pickle
from utils import load_config
from sales_system import (get_new_customers, predict_purchases)

now_str = datetime.datetime.now().strftime('%Y_%m_%d %H_%M_%S')


#  Loading configuration file
config_file_name = "baseline"

settings = load_config(config_file_name)




#  Setting variables from configuration file
starting_seed = settings['seed']
iterations = settings['iterations']
months = settings['months']
shirt_price = settings['shirt_price']
cost_per_shirt = settings['cost_per_shirt']
monthly_inflation_rate = settings['inflation_rate'] / 12

starting_existing_customers = settings['n_existing_customers']

campaigns = settings['campaigns']
#  Identifying the months when campaigns will be applied based on the set cadence
for key, value in campaigns.items():
    cur_campaign_months = list(range(0, months, months // value['n_times'])) 
    campaigns[key].update({'campaign_months': cur_campaign_months})

seed = starting_seed

big_res = {}
#  Looping over the campaigns

for key, value in campaigns.items():

    iter_res = pd.DataFrame()
    for i in range(iterations):
        #  Resetting profits and cost per shirt, and starting customer base at the start of each iteration
        profits = []
        cur_shirt_cost = cost_per_shirt
        n_existing_customers = starting_existing_customers
        #  Creating a random number generator that we'll use to sample in an iteration
        #  Ensures simulation results are reproducible 
        cur_rng = np.random.default_rng(seed)
        for t in range(months):
            #  Sales step -----------------------------------------------------------------------------
            cur_n_new_customers = get_new_customers(t)

            #  Determining how many of the new customers make a purchase
            #  this month
            n_new_purchases = predict_purchases(cur_n_new_customers,
                                                p_purchase=0.01)

            if t in value['campaign_months']:
                n_existing_purchases = predict_purchases(n_existing_customers, 
                                                         p_purchase=value['prob_purchase'],
                                                         rng=cur_rng)
                cur_existing_discount = value['discount']
            else:
                #  10% of existing customers visit the website during 
                #  non-campaign months driven by traditional email 
                #  messaging (with no discounts)
                cur_n_existing_customers = np.round(n_existing_customers * 0.1)
                n_existing_purchases = predict_purchases(cur_n_existing_customers,
                                                         p_purchase=0.05,
                                                         rng=cur_rng)
                cur_existing_discount = 0

            #  Simulating the quantity of shirts in each order for purchases
            n_new_quantity = predict_quantities(n_new_purchases, rng=cur_rng)
            n_existing_quantity = predict_quantities(n_existing_purchases, rng=cur_rng)

            total_sales = n_new_quantity * shirt_price * (1 - 0.1) + n_existing_quantity * shirt_price * (1 - cur_existing_discount)
            
            #  Cost step -------------------------------------------------------------------------------
            total_cost = cur_shirt_cost * (n_new_quantity + n_existing_quantity)
            
            #  Accounting step -------------------------------------------------------------------------
            #  Calculating the profit in this month
            cur_profit = total_sales - total_cost
            profits.append(cur_profit)

            #  Updating the shirt cost with inflation 
            cur_shirt_cost = cur_shirt_cost * (1 + monthly_inflation_rate)

            #  Adding the new customers who made a purchase to the existing customer base
            n_existing_customers += n_new_purchases
        #  Incrementing the seed so we can create a new, reproducible random number generator for the
        #  next iteration    
        seed += 1    
        iter_res = pd.concat([iter_res, pd.Series(profits)], axis=1, ignore_index=True)

    big_res[key] = iter_res.copy()    

run_path = os.path.join('runs', '{}.pickle'.format(now_str))
with open(run_path, 'wb') as handle:
    pickle.dump(big_res, handle, protocol=pickle.HIGHEST_PROTOCOL)