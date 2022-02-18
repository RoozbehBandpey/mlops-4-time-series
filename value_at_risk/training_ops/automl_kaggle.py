from azureml.core import Workspace
from azureml.core.authentication import MsiAuthentication

msi_auth = MsiAuthentication() # MSI does not work! configuration problem

ws = Workspace(subscription_id = "2ee39d18-86c8-4eee-854c-ed31d7b88111", resource_group = "rg-mlops-forecasting-dev", workspace_name = "mlw-mlops-forecasting-dev")

print("Found workspace {} at location {}".format(ws.name, ws.location))



# az ad sp create-for-rbac --sdk-auth --name sp-ml-auth --role Contributor