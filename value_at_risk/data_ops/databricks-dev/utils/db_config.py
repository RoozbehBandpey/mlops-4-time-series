# Databricks notebook source
# MAGIC %md
# MAGIC # Create schema

# COMMAND ----------

spark.conf.set("spark.databricks.io.cache.enabled", "true")

# COMMAND ----------

dbutils.widgets.text("widget_schema_name", "CRYPTO_DB", "schema")

# COMMAND ----------

dbutils.widgets.help()

# COMMAND ----------

schemaName = dbutils.widgets.get("widget_schema_name")

# COMMAND ----------

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schemaName} COMMENT 'Schema for incremental load of data from yfinance' LOCATION '/mnt'")

spark.sql(f"USE {schemaName}")

# COMMAND ----------

display(spark.sql(f"DESCRIBE SCHEMA EXTENDED {schemaName}"))

# COMMAND ----------

dbutils.notebook.exit(schemaName)

# COMMAND ----------


