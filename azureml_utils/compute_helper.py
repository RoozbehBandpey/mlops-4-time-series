import os
import logging
from azureml.core import Keyvault
from azureml.core.compute import ComputeTarget, AmlCompute, ComputeInstance, DatabricksCompute
from azureml.core.compute_target import ComputeTargetException

_logger = logging.getLogger(__name__)


class ComputeHelper():
	"""
   	Compute helper class which facilitates working with variety of Azure ML computes
	This consists of
		- Getting the worksace from config file
		- ...
		- ...
	"""

	def __init__(self, workspace):
		"""Initializes an AML Compute object"""
		self.workspace = workspace


	def get_compute_instance(self, compute_name, vm_size):
		try:
			self.compute_instance = ComputeInstance(self.workspace, compute_name)
			print("found existing compute target.")
		except ComputeTargetException:
			print("creating new compute target")
			
			provisioning_config = ComputeInstance.provisioning_configuration(vm_size = vm_size)    
			self.compute_instance = ComputeTarget.create(self.workspace, compute_name, provisioning_config)
			self.compute_instance.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)	
			print("Azure Machine Learning Compute instance attached")
		return self.compute_instance

	def get_compute_cluster(self, compute_name, vm_size, min_nodes, max_nodes):
		try:
			self.compute_cluster = ComputeTarget(workspace=self.workspace, name=compute_name)
			print('Found existing cluster, use it.')
		except ComputeTargetException:
			compute_config = AmlCompute.provisioning_configuration(vm_size=vm_size,
																idle_seconds_before_scaledown=300,
																min_nodes=min_nodes,
																max_nodes=max_nodes)
			self.compute_cluster = ComputeTarget.create(self.workspace, compute_name, compute_config)
			self.compute_cluster.wait_for_completion(show_output=True)
			print("Azure Machine Learning Compute instance attached")
		return self.compute_cluster

	def get_databricks_compute(self, compute_name, db_resource_group, db_workspace_name):
		try:
			self.databricks_compute = DatabricksCompute(workspace=self.workspace, name=compute_name)
			print('Compute target {} already exists'.format(compute_name))
		except ComputeTargetException as e:
			print('Compute not found, will use below parameters to attach new one')
			print('db_compute_name {}'.format(compute_name))
			print('db_resource_group {}'.format(db_resource_group))
			print('db_workspace_name {}'.format(db_workspace_name))
			keyvault = self.workspace.get_default_keyvault()
			# db_access_token = keyvault.get_secret(name='databricks-access-token-4-aml')
			db_access_token = "dapibeb40bebe4b4566c2e7ca38fc495dc3e-2"

		
			config = DatabricksCompute.attach_configuration(
				resource_group = db_resource_group,
				workspace_name = db_workspace_name,
				access_token= db_access_token)
			self.databricks_compute=ComputeTarget.attach(self.workspace, compute_name, config)
			self.databricks_compute.wait_for_completion(True)
			print("Databricks Compute attached")
		return self.databricks_compute