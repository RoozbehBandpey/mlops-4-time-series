# MLOps Demo for time series analysis


## Use cases
|Pipeline|Build & Release Status|
|-----------------|-----------------|
|Value at Risk|[![Build Status](https://dev.azure.com/accenture-ai-mle/mlops-demo/_apis/build/status/value-at-risk-cicd?branchName=main)](https://dev.azure.com/accenture-ai-mle/mlops-demo/_build/latest?definitionId=3&branchName=main)|
|Demand Forecasting|[![Build Status](https://dev.azure.com/accenture-ai-mle/mlops-demo/_apis/build/status/demand-forecasting-cicd?branchName=master)](https://dev.azure.com/accenture-ai-mle/mlops-demo/_build/latest?definitionId=4&branchName=master)|




## MLOps System Design on Azure

![Overall MLOps Architecture](documentation/architecture/mlops-overall-architecture.drawio.png)

## Contribution
* Best practices to create cluster

| Cluster properties | Description|Best practice|
|-----------------|-----------------|-----------------|
|Cluster mode|depending upon requirement|Standard|
|Runtime version|depending on workload requirements (standard or ML)|If choosing ML, make sure to use 10.4 LTS ML (includes Apache Spark 3.2.1, Scala 2.12)|
|Naming convention| make sure to include ml in convention if choosing runtime type ML|mlops-demo-ml-jd for (Name : John Doe)|
|Worker type|Depending upon requirement|Standard_DS3_v2 with min=1 and max=4 workers nodes|
|Advanced options|For user-level data access|Enable credential passthrough|

