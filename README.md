# Accenture MLOps Demo

This repository contains code for orchestration of machine learning operations (MLOps) with Azure ML and Azure Databricks for demand forecasting use case


[![Build Status](https://dev.azure.com/accenture-ai-mle/mlops-demo/_apis/build/status/databricks-cicd?branchName=master)](https://dev.azure.com/accenture-ai-mle/mlops-demo/_build/latest?definitionId=2&branchName=master)


![Overall MLOps Architecture](documentation/architecture/mlops-overall-architecture.drawio.png)

## System Design

### Components
Following components are considered and provisioned for this solution:
#### Azure Data Lake Storage Gen 2.0
`dlsmlopsforecasting` is the main data storage, it has two container for curating data, it was primarily considered for Azure Databricks usage so it has been mounted to `dbw-mlops-forecasting` with credential passthrough with this script [mount_adls.py](./data_ops/demand-forecasting-dev/utils/mount_adls.py)
#### Azure Databricks
`dbw-mlops-forecasting` is considered the main place for data manipulation, dataset preparation and potentially training and QA serving
#### Azure Machine Learning
`mlw-mlops-forecasting` is the primary service to tackle experimentation, training, scoring, deploying and managing ML models. This architecture uses Azure ML python SDK to interact with Azure ML as well as creation of pipelines and submitting experiment runs.

Azure Machine Learning Compute is a cluster of virtual machines on-demand with automatic scaling and GPU and CPU node options. The training job is executed on this cluster.

Azure Machine Learning pipelines provide reusable machine learning workflows that can be reused across scenarios. Training, model evaluation, model registration, and image creation occur in distinct steps within these pipelines for this use case. The pipeline is published or updated at the end of the build phase and gets triggered on new data arrival.

#### Azure Container Registry
The scoring Python script is packaged as a Docker image and versioned in the registry.
#### Azure Key Vault
All operational secrets, and certificates are stored in key vault
#### Azure Storage

Blob containers are used to store the logs from the scoring service. In this case, both the input data and the model prediction are collected. After some transformation, these logs can be used for model retraining.
#### Azure Container Instances
As part of the release pipeline, the QA and staging environment is mimicked by deploying the scoring webservice image to Container Instances, which provides an easy, serverless way to run a container.
#### Azure Kubernetes Service

Once the scoring webservice image is thoroughly tested in the QA environment, it is deployed to the production environment on a managed Kubernetes cluster.
#### Azure Event Hubs

#### Azure Event Grid Subscription
This service is used to subscribe resource specific events:

Data Lake Event Types
* Microsoft.Storage.BlobCreated
* Microsoft.Storage.BlobDeleted
* Microsoft.Storage.BlobRenamed
* Microsoft.Storage.DirectoryCreated
* Microsoft.Storage.DirectoryRenamed
* Microsoft.Storage.DirectoryDeleted

Container Registry Event Types
* Microsoft.ContainerRegistry.ImagePushed
* Microsoft.ContainerRegistry.ImageDeleted
* Microsoft.ContainerRegistry.ChartPushed
* Microsoft.ContainerRegistry.ChartDeleted

Azure ML Event Types
* Microsoft.MachineLearningServices.ModelRegistered
* Microsoft.MachineLearningServices.ModelDeployed
* Microsoft.MachineLearningServices.RunCompleted
* Microsoft.MachineLearningServices.DatasetDriftDetected
* Microsoft.MachineLearningServices.RunStatusChanged
#### Azure Application Insights
This monitoring service is used to detect performance anomalies.

#### Azure DevOps
Azure Pipelines. This build and test system is based on Azure DevOps and used for the build and release pipelines. Azure Pipelines breaks these pipelines into logical steps called tasks. For example, the Azure CLI task makes it easier to work with Azure resources.

Azure Repos. Is the primary place for hosting code.
## Pipelines

## Flow

This design eliminates concept of landing zone to reduce costs, so the assumption is data arrives directly into data lake. In real world it is recommended to have a separate storage account called landing
ine zone to store data (source aligned data) as it arrives without any changes to them.
Data is being ingested from external sources, after that it has been available within `bronze` container of `dlsmlopsforecasting` is Delta format.

## Re-training

