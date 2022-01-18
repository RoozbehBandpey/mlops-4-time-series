# Databricks notebook source
df = spark.sql("""SELECT * FROM variables.stml""")
MOUNTPOINT = "/mnt/azureml"
message = ""

STORAGE_ACCOUNT = df.take(1)[0][2]
CONTAINER = df.take(1)[0][3]
SASTOKEN = df.take(1)[0][1]

SOURCE = "wasbs://{container}@{storage_acct}.blob.core.windows.net/".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)
URI = "fs.azure.sas.{container}.{storage_acct}.blob.core.windows.net".format(container=CONTAINER, storage_acct=STORAGE_ACCOUNT)


if MOUNTPOINT in [mnt.mountPoint for mnt in dbutils.fs.mounts()]:
    message = f"{MOUNTPOINT} is already mounted"
else:
    try:
        dbutils.fs.mount(
                        source=SOURCE,
                        mount_point=MOUNTPOINT,
                        extra_configs={URI:SASTOKEN})
        message = f"{MOUNTPOINT} has been mounted"
    except Exception as e:
        message = f"Something went wrong"
        dbutils.fs.unmount(MOUNTPOINT)
        message += f"<br/>{MOUNTPOINT} has been unmounted"
        dbutils.fs.mount(
                        source=SOURCE,
                        mount_point=MOUNTPOINT,
                        extra_configs={URI:SASTOKEN})
        message += f"<br/>{MOUNTPOINT} has been mounted"


# COMMAND ----------

displayHTML(f"<h3>{message}</h3>")
