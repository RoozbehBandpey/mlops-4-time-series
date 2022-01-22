import os
import logging
from azureml.core import Workspace
from azureml.core import Keyvault
from azureml.core.authentication import AzureCliAuthentication, MsiAuthentication, InteractiveLoginAuthentication, ServicePrincipalAuthentication

_logger = logging.getLogger(__name__)


class WorkspaceHelper():
	"""
   	Workspace helper class which facilitates working with Workspace objects
	This consists of
		- Getting the worksace from config file
		- ...
		- ...
	"""

	def __init__(self, ws_config_file='config.json'):
		"""Initializes an AML workspace object"""
		self.ws = Workspace.from_config(
			# auth=InteractiveLoginAuthentication(tenant_id='ffbaf41d-7dbb-476e-bd38-2c12e2c319f7'), # TODO: Replace with MsiAuthentication for production workload
			auth=AzureCliAuthentication(), # TODO: Replace with MsiAuthentication for production workload
			# auth=MsiAuthentication(), # TODO: Replace with MsiAuthentication for production workload
			path=os.path.join(
				os.path.dirname(os.path.realpath(__file__)),
				ws_config_file
			)
		)
		print(f"Found workspace {self.ws.name} \n\tat location {self.ws.location}\n\t with the id:{self.ws._workspace_id}")

	def authenticate_with_sp(self, ws_config_file='config.json'):
		keyvault = self.ws.get_default_keyvault()
		sp_tenant_id = keyvault.get_secret(name='sp-tenant-id')
		sp_client_id = keyvault.get_secret(name='sp-client-id')
		sp_password = keyvault.get_secret(name='sp-password')

		sp_auth = ServicePrincipalAuthentication(tenant_id=sp_tenant_id, service_principal_id=sp_client_id, service_principal_password=sp_password)
		print(f"Authenticated with Service Principal with session: \n\t{sp_auth.signed_session()}")
		self.ws = Workspace.from_config(
			auth=sp_auth,
			path=os.path.join(
				os.path.dirname(os.path.realpath(__file__)),
				ws_config_file
			)
		)

	def get_workspace(self):
		return self.ws

	def __repr__(self):
		print(self.ws)


