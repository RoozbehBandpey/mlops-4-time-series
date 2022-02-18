# Databricks notebook source
#azure-ml-storage-all-users
# stml-sas-token

dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list('azure-ml-storage-all-users')

# COMMAND ----------

MOUNTPOINT = "/mnt/azureml"
message = ""

STORAGE_ACCOUNT = "stmlwmlopsforecasting"
CONTAINER = "azureml-blobstore-bd63b639-8836-4d1b-823b-17738975655b"
SASTOKEN = dbutils.secrets.get(scope='azure-ml-storage-all-users', key='stml-sas-token')

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
