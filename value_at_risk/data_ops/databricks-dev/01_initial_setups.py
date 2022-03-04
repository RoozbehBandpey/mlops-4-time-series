# Databricks notebook source
# MAGIC %md
# MAGIC # Setting some control parameters

# COMMAND ----------

# time horizon
days = 365
dt = 1/float(days)
 
# volatility
sigma = 0.04 
 
# drift (average growth rate)
mu = 0.05  
 
# initial starting price
start_price = 10
 
# number of simulations
runs_gr = 500
runs_mc = 10000

# COMMAND ----------

# MAGIC %md
# MAGIC ### Plot example Monte Carlo simulations for 365 days return

# COMMAND ----------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def generate_prices(start_price):
    shock = np.zeros(days)
    price = np.zeros(days)
    price[0] = start_price
    for i in range(1, days):
        shock[i] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
        price[i] = max(0, price[i - 1] + shock[i] * price[i - 1])
    return price

plt.figure(figsize=(16,6))
for i in range(1, runs_gr):
    plt.plot(generate_prices(start_price))

plt.title('Simulated price')
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()

# COMMAND ----------


