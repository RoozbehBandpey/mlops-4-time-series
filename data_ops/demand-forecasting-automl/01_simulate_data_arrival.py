# Databricks notebook source
# MAGIC %md
# MAGIC # Simulate Data Arrival

# COMMAND ----------

import pyspark.sql.functions as F

# COMMAND ----------

spark.conf.set("spark.sql.shuffle.partitions", 500 ) 

# COMMAND ----------

from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
print( 
  list(daterange( date(2017,12,1), date(2017,12,8)))
  )

# COMMAND ----------

SILVER_MOUNTPOINT = "/mnt/silver"
prodFolderName = "prod"
prodTableName = "kaggle_prod_data_delta"
prodTablePath = SILVER_MOUNTPOINT + f"/kaggle/{prodFolderName}"

# COMMAND ----------

spark.sql(f"DROP TABLE IF EXISTS {prodTableName}")
dbutils.fs.rm(prodTablePath, recurse=True)

trainDF = spark.table("kaggle_train_data_delta")

(trainDF.write
  .format("delta")
  .mode("overwrite")
  .option("path", prodTablePath)
  .saveAsTable(prodTableName))
prodDF = spark.table(prodTableName)

# COMMAND ----------


