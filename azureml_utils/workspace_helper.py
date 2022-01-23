import os
import logging
from azureml.core import Workspace
from azureml.core import Keyvault
from azureml.core.authentication import AzureCliAuthentication, MsiAuthentication, InteractiveLoginAuthentication, ServicePrincipalAuthentication
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential



_logger = logging.getLogger(__name__)


class WorkspaceHelper():
	"""
   	Workspace helper class which facilitates working with Workspace objects
	This consists of
		- Getting the worksace from config file
		- ...
		- ...
	"""

	def __init__(self, ws_config_file='config.json', auth_type='sp'):
		"""Initializes an AML workspace object"""
		self.ws_config_file = ws_config_file
		
		if auth_type='sp':
			auth = ServicePrincipalAuthentication(tenant_id=os.environ.get("TENANT_ID"), service_principal_id=os.environ.get("SP_ID"), service_principal_password=os.environ.get("SP_PASSWORD"))
		else if auth_type='int':
			auth=InteractiveLoginAuthentication(tenant_id=os.environ.get("TENANT_ID"))
		else if auth_type='cli':
			auth=AzureCliAuthentication()
		else if auth_type='msi':
			auth=MsiAuthentication()
		else:
			raise(Exception)
		
		self.ws = Workspace.from_config(
			auth=auth,
			path=os.path.join(
				os.path.dirname(os.path.realpath(__file__)),
				self.ws_config_file
			)
		)
		print(f"Found workspace {self.ws.name} \n\tat location {self.ws.location}\n\t with the id:{self.ws._workspace_id}")


	def get_workspace(self):
		return self.ws

	def __repr__(self):
		print(self.ws)


