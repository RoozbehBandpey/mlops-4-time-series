# Databricks notebook source
# MAGIC %run ./utils/mount_stml

# COMMAND ----------

# MAGIC %run ./utils/mount_adls

# COMMAND ----------

trainDF = spark.table("default.kaggle_train_data_delta")
testDF = spark.table("default.kaggle_test_data_delta")

# COMMAND ----------

trainPath = "mnt/azureml/kaggle/train.parquet"
testPath = "mnt/azureml/kaggle/test.parquet"

(trainDF.write
  .format("parquet")
  .mode("overwrite")
  .save(trainPath))

(testDF.write
  .format("parquet")
  .mode("overwrite")
  .save(testPath))

# COMMAND ----------


