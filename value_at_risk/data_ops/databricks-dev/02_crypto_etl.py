# Databricks notebook source
dbutils.notebook.run("./utils/db_config", 30, {"schema": "CRYPTO_DATA"})

# COMMAND ----------

# MAGIC %md
# MAGIC ## Configure Environment

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

portfolio_table = 'portfolio'
stock_table = 'stock'
stock_return_table = 'stock_return'
market_table = 'market'
market_return_table = 'market_return'

# COMMAND ----------


