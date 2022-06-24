# Databricks notebook source
# MAGIC %md
# MAGIC # Data ETL and EDA
# MAGIC 
# MAGIC In this notebook, I use `yfinance` to download crypto data for **n** coins for someone's portfolio. I use `pandas UDF` paradigm to distribute this process efficiently and store all of our output data as a **Delta Lake** table so that our data is analytic ready at every point in time.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run DB Setup

# COMMAND ----------

dbutils.notebook.run("./utils/db_config", 30, {"schema": "MARKET_DB"})

# COMMAND ----------

# MAGIC %run ./utils/mount_adls

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Install `yfinance`
# MAGIC Use `%pip` to install `yfinance` to all nodes in the cluster, but only for this SparkSession.
# MAGIC 
# MAGIC Or install it directly on the running cluster

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configure Environment
# MAGIC 
# MAGIC We'll import a number of libraries and define the table names we'll be using throughout our notebooks.

# COMMAND ----------

BRONZE_MOUNTPOINT = "/mnt/bronze"
SILVER_MOUNTPOINT = "/mnt/silver"

# COMMAND ----------

import yfinance as yf
import pandas as pd
import numpy as np
from io import StringIO
import pyspark.sql.functions as F
from pyspark.sql import Window
from pyspark.sql.functions import udf
from pyspark.sql.functions import pandas_udf
from datetime import datetime, timedelta

portfolio_table = 'MARKET_DB.portfolio'
crypto_table = 'MARKET_DB.crypto'
crypto_return_table = 'MARKET_DB.crypto_return'
market_table = 'MARKET_DB.market'
market_return_table = 'MARKET_DB.market_return'

# COMMAND ----------

portfolio_table_path = BRONZE_MOUNTPOINT+'/market-data/portfolio'
crypto_table_path = BRONZE_MOUNTPOINT+'/market-data/crypto'
crypto_return_table_path = BRONZE_MOUNTPOINT+'/market-data/crypto_return'
market_table_path = BRONZE_MOUNTPOINT+'/market-data/market'
market_return_table_path = BRONZE_MOUNTPOINT+'/market-data/market_return'

# COMMAND ----------

# MAGIC %md
# MAGIC ## `STEP1` Create our portfolio
# MAGIC 
# MAGIC We'll be using a handful of crypto curnencies for our fake portfolio.

# COMMAND ----------

portfolio = """
exchange,ticker
CCC,ETH-EUR
CCC,BTC-EUR
CCC,BNB-EUR
CCC,XRP-EUR
CCC,SOL-EUR
CCC,ADA-EUR
CCC,HEX-EUR
"""

portfolio_df = pd.read_csv(StringIO(portfolio))

# COMMAND ----------

# import yfinance as yf

# msft = yf.Ticker("HEX-EUR")
# msft.info

# COMMAND ----------

# MAGIC %md
# MAGIC We'll save these as a Delta Lake table so that they're accessible from any notebook in our workspace.

# COMMAND ----------

(spark
  .createDataFrame(portfolio_df)
  .select('exchange', 'ticker')
  .write
  .format('delta')
  .mode('overwrite')
  .saveAsTable(portfolio_table, path=portfolio_table_path))

display(spark.read.table(portfolio_table))

# COMMAND ----------

# MAGIC %sql DESCRIBE EXTENDED market_db.portfolio

# COMMAND ----------

# MAGIC %md
# MAGIC ## `STEP2` Download stock data
# MAGIC We'll use an open source Python package to download historical ticker data from Yahoo Finance, which we'll be using for our modeling purposes.
# MAGIC 
# MAGIC We will apply this function as a pandas Grouped Map  which enables the efficient application of pandas functionality to grouped data in a Spark DataFrame.

# COMMAND ----------

schema = """
  ticker string, 
  date date,
  open double,
  high double,
  low double,
  close double,
  volume double
"""

def fetch_tick(group, pdf):
  tick = group[0]
  try:
    raw = yf.download(tick, start="2017-01-01", end="2022-05-05")[['Open', 'High', 'Low', 'Close', 'Volume']]
    # fill in missing business days
    idx = pd.date_range(raw.index.min(), raw.index.max(), freq='B')
    # use last observation carried forward for missing value
    output_df = raw.reindex(idx, method='pad')
    # Pandas does not keep index (date) when converted into spark dataframe
    output_df['date'] = output_df.index
    output_df['ticker'] = tick    
    output_df = output_df.rename(columns={"Open": "open", "High": "high", "Low": "low", "Volume": "volume", "Close": "close"})
    return output_df
  except:
    return pd.DataFrame(columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])
  
(spark
  .read
  .table(portfolio_table)
  .groupBy("ticker")
  .applyInPandas(fetch_tick, schema=schema)
  .write
  .format("delta")
  .mode("overwrite")
  .saveAsTable(crypto_table, path=crypto_table_path))

display(spark.read.table(crypto_table))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Use widgets to access a specific ticker

# COMMAND ----------

# dbutils.widgets.remove('crypto')
tickers = spark.read.table(portfolio_table).select('ticker').toPandas()['ticker']
dbutils.widgets.dropdown('crypto', 'BTC-EUR', tickers)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Display a sorted view of a crypto data

# COMMAND ----------

display(spark
    .read
    .table(crypto_table)
    .filter(F.col('ticker') == dbutils.widgets.get('crypto'))
    .orderBy(F.asc('date'))
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## `STEP3` Download market factors
# MAGIC 
# MAGIC We'll be using overall market trends as our predictive variables.

# COMMAND ----------

# factors = {
#   '^GSPC':'SP500',
#   '^NYA':'NYSE',
#   '^XOI':'OIL',
#   '^TNX':'TREASURY',
#   '^DJI':'DOWJONES'
# }

# # Create a pandas dataframe where each column contain close index
factors_df = pd.DataFrame()
for tick in tickers:
    msft = yf.Ticker(tick)
    raw = msft.history(period="2y")
    # fill in missing business days
    idx = pd.date_range(raw.index.min(), raw.index.max(), freq='B')
    # use last observation carried forward for missing value
    pdf = raw.reindex(idx, method='pad')
    factors_df[tick] = pdf['Close'].copy()
        
# Pandas does not keep index (date) when converted into spark dataframe
factors_df['Date'] = idx

# Overwrite delta table (bronze) with information to date
(spark.createDataFrame(factors_df)
  .write
  .format("delta")
  .mode("overwrite")
  .saveAsTable(market_table, path=market_table_path))

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {market_table}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## `STEP4` Compute daily log return
# MAGIC 
# MAGIC We'll log transform the returns for our stocks, as well as those for our market indicators.

# COMMAND ----------

# our market factors easily fit in memory, use pandas for convenience
df = spark.table(market_table).toPandas()

# add date column as pandas index for sliding window
df.index = df['Date']
df = df.drop(columns = ['Date'])

# compute daily log returns
df = np.log(df.shift(1)/df)

# add date columns
df['date'] = df.index

# overwrite log returns to market table (gold)
(spark.createDataFrame(df)
  .write
  .format("delta")
  .mode("overwrite")
  .saveAsTable(market_return_table, path=market_return_table))

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {market_return_table}"))

# COMMAND ----------

# MAGIC %md
# MAGIC We will be using a `Window` to create a tumbling window for our measurements.

# COMMAND ----------

# Create UDF for computing daily log returns
@udf("double")
def compute_return(first, close):
  return float(np.log(close / first))

# Apply a tumbling 1 day window on each instrument
window = Window.partitionBy('ticker').orderBy('date').rowsBetween(-1, 0)

# apply sliding window and take first element
# compute returns
# make sure we have corresponding dates in market factor tables
sdf = (spark.table(crypto_table)
  .filter(F.col('close').isNotNull())
  .withColumn("first", F.first('close').over(window))
  .withColumn("return", compute_return('first', 'close'))
  .select('date', 'ticker', 'return')
  .join(spark.table(market_return_table), 'date')
  .select('date', 'ticker', 'return'))

# overwrite log returns to market table (gold)
(sdf.write
  .format("delta")
  .mode("overwrite")
  .saveAsTable(crypto_return_table, path=crypto_return_table_path))

# COMMAND ----------

display(spark.table(crypto_return_table).filter(F.col('ticker') == dbutils.widgets.get('crypto')))

# COMMAND ----------


