# Databricks notebook source
BRONZE_MOUNTPOINT = "/mnt/bronze"
SILVER_MOUNTPOINT = "/mnt/silver"
message = ""

STORAGE_ACCOUNT = "dlsmlopsforecastingdev"
BRONZE_CONTAINER = "bronze"
SILVER_CONTAINER = "silver"

configs = {
  "fs.azure.account.auth.type": "CustomAccessToken",
  "fs.azure.account.custom.token.provider.class": spark.conf.get("spark.databricks.passthrough.adls.gen2.tokenProviderClassName")
}

if BRONZE_MOUNTPOINT in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
    message = f"{BRONZE_MOUNTPOINT} is already mounted"
else:
    try:
        dbutils.fs.mount(
          source = f"abfss://{BRONZE_CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/",
          mount_point = BRONZE_MOUNTPOINT,
          extra_configs = configs)
        message = f"{BRONZE_MOUNTPOINT} has been mounted"
    except Exception as e:
        message = f"Something went wrong"
        dbutils.fs.unmount(BRONZE_MOUNTPOINT)
        message += f"<br/>{BRONZE_MOUNTPOINT} has been unmounted"
        dbutils.fs.mount(
          source = f"abfss://{BRONZE_CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/",
          mount_point = BRONZE_MOUNTPOINT,
          extra_configs = configs)
        message += f"<br/>{BRONZE_MOUNTPOINT} has been mounted"
        
        
if SILVER_MOUNTPOINT in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
    message += f"<br/>{SILVER_MOUNTPOINT} is already mounted"
else:
    try:
        dbutils.fs.mount(
          source = f"abfss://{SILVER_CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/",
          mount_point = SILVER_MOUNTPOINT,
          extra_configs = configs)
        message += f"<br/>{SILVER_MOUNTPOINT} has been mounted"
    except Exception as e:
        message += f"<br/>Something went wrong"
        dbutils.fs.unmount(SILVER_MOUNTPOINT)
        message += f"<br/>{SILVER_MOUNTPOINT} has been unmounted"
        dbutils.fs.mount(
          source = f"abfss://{SILVER_CONTAINER}@{STORAGE_ACCOUNT}.dfs.core.windows.net/",
          mount_point = SILVER_MOUNTPOINT,
          extra_configs = configs)
        message += f"<br/>{SILVER_MOUNTPOINT} has been mounted"

# COMMAND ----------

displayHTML(f"<h3>{message}</h3>")
