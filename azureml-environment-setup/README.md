# Environment Setup



## Resource Group

Resource Grouprg-mlops-forecasting-dev]

dbw-mlops-forecasting-dev

mlw-mlops-forecasting-dev

crmlopsforecastingdev

kv-mlops-forecasting-dev


aci-mlops-forecasting-dev

aks-mlops-forecasting-dev

evh-mlops-forecasting-dev

dlsmlopsforecastingdev

stmlwmlopsforecastingdev

ins-mlops-forecasting-dev


## Setup dev environment

### Azure ML Compute
Turn the compute on from [compute tab of Azure ML workspace](https://ml.azure.com/compute/list?wsid=/subscriptions/5e54cdea-5cda-46ba-af31-b1c1b15430e6/resourcegroups/MLE-Demos/workspaces/mlw-mlops-forecasting&tid=ec0c3cd0-5bd6-4c13-87c2-f45543cab0e1), head over to notebooks and open terminal.
> Make sure your terminal is attached to the compute.
#### Generate a new SSH key

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

```
This creates a new ssh key, using the provided email as a label.
```bash
$ Generating public/private rsa key pair.
```
When you're prompted to "Enter a file in which to save the key" press Enter. This accepts the default file location.

Verify that the default location is '/home/azureuser/.ssh' and press enter. 



```bash
$ Enter a file in which to save the key (/home/azureuser/.ssh/id_rsa): [Press enter]
```
At the prompt, type a secure passphrase or leave it empty.

```bash
$ Enter passphrase (empty for no passphrase): [Type a passphrase]
$ Enter same passphrase again: [Type passphrase again]
```

Add the public key to Git Account
In your terminal window, copy the contents of your public key file. If you renamed the key, replace id_rsa.pub with the public key file name.
Bash

Copy
cat ~/.ssh/id_rsa.pub