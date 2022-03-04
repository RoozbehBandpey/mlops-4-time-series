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

# MAGIC %md
# MAGIC ### Compute value at risk

# COMMAND ----------

from matplotlib.ticker import StrMethodFormatter
simulations = np.zeros(runs_mc)
for i in range(0, runs_mc):
    simulations[i] = generate_prices(start_price)[days - 1]
    
mean = simulations.mean()
z = stats.norm.ppf(1-0.95)
m1 = simulations.min()
m2 = simulations.max()
std = simulations.std()
q1 = np.percentile(simulations, 5) # VAR95

x1 = np.arange(9,12,0.01)
y1 = stats.norm.pdf(x1, loc=mean, scale=std)
x2 = np.arange(x1.min(),q1,0.001)
y2 = stats.norm.pdf(x2, loc=mean, scale=std)

mc_df = pd.DataFrame(data = simulations, columns=['return'])
ax = mc_df.hist(column='return', bins=50, density=True, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)
ax = ax[0]

for x in ax:
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)
    x.axvline(x=q1, color='r', linestyle='dashed', linewidth=1)
    x.fill_between(x2, y2, zorder=3, alpha=0.4)
    x.plot(x1, y1, zorder=3)
    x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")
    vals = x.get_yticks()
    for tick in vals:
        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    x.set_title("VAR95 = {:.3f}".format(q1), weight='bold', size=15)
    x.set_xlabel("{} days returns".format(days), labelpad=20, weight='bold', size=12)
    x.set_ylabel("Density", labelpad=20, weight='bold', size=12)
    x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

# COMMAND ----------


