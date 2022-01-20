# Databricks notebook source
# MAGIC %md
# MAGIC # Exploratory Data Analysis

# COMMAND ----------

# MAGIC %run ./utils/mount_adls

# COMMAND ----------

BRONZE_MOUNTPOINT = "/mnt/bronze"
SILVER_MOUNTPOINT = "/mnt/silver"

# COMMAND ----------

# MAGIC %fs ls mnt/bronze/kaggle-data/

# COMMAND ----------

trainDataPath = BRONZE_MOUNTPOINT + "/kaggle-data/train.csv"
testDataPath = BRONZE_MOUNTPOINT + "/kaggle-data/test.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Examine the Data
# MAGIC 
# MAGIC Begin by defining the schema and registering a DataFrame from the CSV.

# COMMAND ----------

rawSchema = """
  date DATE,
  store INT,
  item INT,
  sales INT"""

rawDF = (spark.read
  .format("csv") 
  .option("header", True) 
  .schema(rawSchema)
  .load(trainDataPath))

# COMMAND ----------

# MAGIC %md
# MAGIC Preview the first 5 lines to make sure that your data loaded correct

# COMMAND ----------

display(rawDF.head(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Training and Test Sets
# MAGIC 
# MAGIC We'll hold out a month of data for our test set.
# MAGIC 
# MAGIC Start by finding the max date for the data.

# COMMAND ----------

import pyspark.sql.functions as F

display(rawDF.select(F.max("date")))

# COMMAND ----------

# MAGIC %md
# MAGIC Create 2 new DataFrames:
# MAGIC - `trainDF`: all but the last month of data
# MAGIC - `testDF`: the date for December 2017

# COMMAND ----------

trainDF = rawDF.filter(F.col("date") < "2017-12-01")
testDF = rawDF.filter(F.col("date") >= "2017-12-01")

print(f"Our training set represents {trainDF.count() / rawDF.count() * 100:.2f}% of the total data")

# COMMAND ----------

trainDeltaPath = SILVER_MOUNTPOINT + "/kaggle/train/"
testDeltaPath = SILVER_MOUNTPOINT + "/kaggle/test/"

# COMMAND ----------

# write to Delta Lake
trainDF.write.mode("overwrite").format("delta").partitionBy("date").save(trainDeltaPath)
testDF.write.mode("overwrite").format("delta").save(testDeltaPath)

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS kaggle_train_data_delta

# COMMAND ----------

spark.sql("""
  CREATE TABLE kaggle_train_data_delta
  USING DELTA
  LOCATION '{}'
""".format(trainDeltaPath))

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS kaggle_test_data_delta

# COMMAND ----------

spark.sql("""
  CREATE TABLE kaggle_test_data_delta
  USING DELTA
  LOCATION '{}'
""".format(testDeltaPath))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM kaggle_train_data_delta

# COMMAND ----------

# MAGIC %md
# MAGIC ## Examine the Data
# MAGIC We'll use our training data during EDA; as such, our trend analyses will be missing the month of December 2017.
# MAGIC 
# MAGIC Note that the results of SQL queries in Databricks notebooks are equivalent to the results of a `display()` function on a DataFrame. We'll use [Databricks built-in plotting](https://docs.databricks.com/notebooks/visualizations/index.html#plot-types) to visualize our trends.
# MAGIC 
# MAGIC When performing demand forecasting, we are often interested in general trends and seasonality. Let's start our exploration by examing the annual trend in unit sales:

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   year(date) as year, 
# MAGIC   sum(sales) as sales
# MAGIC FROM kaggle_train_data_delta
# MAGIC GROUP BY year(date)
# MAGIC ORDER BY year;

# COMMAND ----------

# MAGIC %md
# MAGIC It's very clear from the data that there is a generally upward trend in total unit sales across the stores. If we had better knowledge of the markets served by these stores, we might wish to identify whether there is a maximum growth capacity we'd expect to approach over the life of our forecast.  But without that knowledge and by just quickly eyeballing this dataset, it feels safe to assume that if our goal is to make a forecast a few days, weeks or months from our last observation, we might expect continued linear growth over that time span.
# MAGIC 
# MAGIC Now let's examine seasonality.  If we aggregate the data around the individual months in each year, a distinct yearly seasonal pattern is observed which seems to grow in scale with overall growth in sales:

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT 
# MAGIC   TRUNC(date, 'MM') as month,
# MAGIC   SUM(sales) as sales
# MAGIC FROM kaggle_train_data_delta
# MAGIC GROUP BY TRUNC(date, 'MM')
# MAGIC ORDER BY month;

# COMMAND ----------

# MAGIC %md
# MAGIC Aggregating the data at a weekday level, a pronounced weekly seasonal pattern is observed with a peak on Sunday (weekday 0), a hard drop on Monday (weekday 1) and then a steady pickup over the week heading back to the Sunday high.  This pattern seems to be pretty stable across the five years of observations, increasing with scale given the overall annual trend in sales growth:

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC SELECT
# MAGIC   YEAR(date) as year,
# MAGIC   DAYOFWEEK(date) % 7 as weekday,
# MAGIC   AVG(sales) as sales
# MAGIC FROM (
# MAGIC   SELECT 
# MAGIC     date,
# MAGIC     SUM(sales) as sales
# MAGIC   FROM kaggle_train_data_delta
# MAGIC   GROUP BY date
# MAGIC  ) x
# MAGIC GROUP BY year, DAYOFWEEK(date)
# MAGIC ORDER BY year, weekday;

# COMMAND ----------

# MAGIC %md
# MAGIC Below, define a Python method that returns monthly sales for a single item, grouped by store. The function accept a single argument for item `sku`.

# COMMAND ----------

def monthlyItemSales(sku:int):
  display(spark.sql(f"""
    SELECT
      MONTH(month) as month,
      store,
      AVG(sales) as sales
    FROM (
      SELECT 
        TRUNC(date, 'MM') as month,
        store,
        SUM(sales) as sales
      FROM kaggle_train_data_delta
      WHERE item={sku}
      GROUP BY TRUNC(date, 'MM'), store
      ) x
    GROUP BY MONTH(month), store
    ORDER BY month, store;
   """))

# COMMAND ----------

# MAGIC %md
# MAGIC The cell below defined a dropdown widget that includes all 50 of our item SKUs.

# COMMAND ----------

dbutils.widgets.dropdown("sku", "1", [str(x) for x in range(1,51)])

# COMMAND ----------

# MAGIC %md
# MAGIC Use your function to visually explore trends of several items. Make a line chart with the following specifications:
# MAGIC - keys: `month`
# MAGIC - series groupings: `store`
# MAGIC - values: `sales`

# COMMAND ----------

monthlyItemSales(dbutils.widgets.get("sku"))

# COMMAND ----------

# MAGIC %md
# MAGIC This data exploration reveals the fundamental issue we wish to tackle in this demonstration.  When we examine our data at an aggregate level, i.e. summing sales across stores or individual products, the aggregation hides what could be some useful variability in our data.  By analyzing our data at the store-item level, we hope to be able to construct forecasts capable of picking up on these subtle differences in behaviours.
