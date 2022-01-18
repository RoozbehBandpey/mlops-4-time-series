# Data preparation pipeline

Our main data preparation scripts are in Azure Databricks, in order to stich those steps together in a pipeline, either Azure Data factory or Azure Machine learning can be used.

## Using Databricks as a Compute Target from Azure Machine Learning Pipeline
To use Databricks as a compute target from Azure Machine Learning Pipeline, a `DatabricksStep` is used.

With this you can:
* Run an arbitrary Databricks notebook in Databricks workspace
* Run an arbitrary Python script in DBFS
* Run an arbitrary Python script that is available on local computer (will upload to DBFS, and then run in Databricks)
* Run a JAR job in DBFS.
* Get run context in a Databricks interactive cluster


> Before you begin: Create PAT (access token): Manually create a Databricks access token at the Azure Databricks portal.

### Attach Databricks compute target
Next, you need to add your Databricks workspace to Azure Machine Learning as a compute target and give it a name. You will use this name to refer to your Databricks workspace compute target inside Azure Machine Learning.

* Resource Group - The resource group name of your Azure Machine Learning workspace
* Databricks Workspace Name - The workspace name of your Azure Databricks workspace
* Databricks Access Token - The access token you created in ADB
The Databricks workspace need to be present in the same subscription as your AML workspace
