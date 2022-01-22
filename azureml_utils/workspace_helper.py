import os
import logging
from azureml.core import Workspace
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
			# auth=AzureCliAuthentication(), # TODO: Replace with MsiAuthentication for production workload
			# auth=MsiAuthentication(), # TODO: Replace with MsiAuthentication for production workload
			auth=ServicePrincipalAuthentication(tenant_id="ec0c3cd0-5bd6-4c13-87c2-f45543cab0e1", service_principal_id="0549311d-d674-41e0-b4bf-ccf623df35c4", service_principal_password="P5w7Q~dh6g_MjARbxvCe-DRfMlWDiBFI7c63L"),
			path=os.path.join(
				os.path.dirname(os.path.realpath(__file__)),
				ws_config_file
			)
		)
		print(f"Found workspace {self.ws.name} \n\tat location {self.ws.location}\n\t with the id:{self.ws._workspace_id}")

	def get_workspace(self):
		return self.ws

	def __repr__(self):
		print(self.ws)


