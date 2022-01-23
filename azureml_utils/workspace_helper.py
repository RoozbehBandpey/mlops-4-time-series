import os
import logging
import sys
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication, MsiAuthentication, InteractiveLoginAuthentication, ServicePrincipalAuthentication
from azureml.core import Keyvault
sys.path.append(os.getcwd())
from environment.env_variables import Env



_logger = logging.getLogger(__name__)


class WorkspaceHelper():
	"""
   	Workspace helper class which facilitates working with Workspace objects
	This consists of
		- Getting the worksace from config file
		- ...
		- ...
	"""

	def __init__(self, auth_type='sp'):
		"""Initializes an AML workspace object"""

		e = Env()
		
		if auth_type == 'sp':
			auth = ServicePrincipalAuthentication(tenant_id=e.tenant_id, service_principal_id=e.sp_id, service_principal_password=e.sp_password)
		elif auth_type == 'int':
			auth=InteractiveLoginAuthentication(tenant_id=e.tenant_id)
		elif auth_type == 'cli':
			auth=AzureCliAuthentication()
		elif auth_type == 'msi':
			auth=MsiAuthentication()
		else:
			raise(Exception)
		
		self.ws = Workspace(subscription_id=e.subscription_id, resource_group=e.resource_group, workspace_name=e.workspace_name, auth=auth)
		print(f"Found workspace {self.ws.name} \n\tat location {self.ws.location}\n\t with the id:{self.ws._workspace_id}")


	def get_workspace(self):
		return self.ws

	def __repr__(self):
		print(self.ws)


