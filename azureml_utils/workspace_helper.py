import os
import logging
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication, MsiAuthentication, InteractiveLoginAuthentication

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
			auth=MsiAuthentication(), # TODO: Replace with MsiAuthentication for production workload
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


