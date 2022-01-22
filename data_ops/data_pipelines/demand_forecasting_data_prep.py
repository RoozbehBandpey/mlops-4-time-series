import os
import sys
import os
import azureml.core
from azureml.core import Workspace, Experiment
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import DatabricksStep
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference

# Check core SDK version number
print("SDK version:", azureml.core.VERSION)

sys.path.append(os.getcwd())
from azureml_utils.workspace_helper import WorkspaceHelper
from azureml_utils.compute_helper import ComputeHelper


wsh = WorkspaceHelper()
ws = wsh.get_workspace()


ch = ComputeHelper(ws)
# compute_instance = ch.get_compute_instance('cpu8c-ram28gb-rb', 'STANDARD_D4_V2')
compute_cluster = ch.get_compute_cluster(compute_name='pipelineclstr04', vm_size='Standard_DS3_v2', min_nodes=0, max_nodes=4)
databricks_compute= ch.get_databricks_compute(compute_name='databricks-cpu', db_resource_group='MLE-Demos', db_workspace_name='dbw-mlops-forecasting')

print(databricks_compute)

eda_notebook_path = '/Repos/roozbeh.bandpey@accenture.com/mlops-forecasting/data_ops/demand-forecasting-dev/01_eda'
ingest_notebook_path = '/Repos/roozbeh.bandpey@accenture.com/mlops-forecasting/data_ops/demand-forecasting-dev/03_azureml_ingest'
# Syntax
# DatabricksStep(
#                 name,
#                 inputs=None,
#                 outputs=None,
#                 existing_cluster_id=None,
#                 spark_version=None,
#                 node_type=None,
#                 instance_pool_id=None,
#                 num_workers=None,
#                 min_workers=None,
#                 max_workers=None,
#                 spark_env_variables=None,
#                 spark_conf=None,
#                 init_scripts=None,
#                 cluster_log_dbfs_path=None,
#                 notebook_path=None,
#                 notebook_params=None,
#                 python_script_path=None,
#                 python_script_params=None,
#                 main_class_name=None,
#                 jar_params=None,
#                 python_script_name=None,
#                 source_directory=None,
#                 hash_paths=None,
#                 run_name=None,
#                 timeout_seconds=None,
#                 runconfig=None,
#                 maven_libraries=None,
#                 pypi_libraries=None,
#                 egg_libraries=None,
#                 jar_libraries=None,
#                 rcran_libraries=None,
#                 compute_target=None,
#                 allow_reuse=True,
#                 version=None,
#                 permit_cluster_restart=None)


try:
    dbfs_ds = Datastore.get(workspace=ws, datastore_name='dbfs_datastore')
    print('DBFS Datastore already exists')
except Exception as ex:
    dbfs_ds = Datastore.register_dbfs(ws, datastore_name='dbfs_datastore')

step_1_input = DataReference(datastore=dbfs_ds, path_on_datastore="bronze/kaggle-data/", data_reference_name="input")
step_1_output = PipelineData("output", datastore=dbfs_ds)


dataset_cleansing_step = DatabricksStep(
    name="exploratory-data-analysis",
    inputs=[step_1_input],
    notebook_path=eda_notebook_path,
    run_name='DB_Notebook_Run_EDA',
    compute_target=databricks_compute,
    existing_cluster_id= "0119-094446-s7gn0dcd",
    allow_reuse=True
)

azureml_ingest = DatabricksStep(
    name="azure-ml-ingest",
    # inputs=[dataset_cleansing_step],
    notebook_path=ingest_notebook_path,
    run_name='DB_Notebook_Run_Ingest',
    compute_target=databricks_compute,
    existing_cluster_id= "0119-094446-s7gn0dcd",
    allow_reuse=True
)

source_directory = './'
print('Source directory for the step is {}.'.format(os.path.realpath(source_directory)))

# Syntax
# PythonScriptStep(
#     script_name, 
#     name=None, 
#     arguments=None, 
#     compute_target=None, 
#     runconfig=None, 
#     inputs=None, 
#     outputs=None, 
#     params=None, 
#     source_directory=None, 
#     allow_reuse=True, 
#     version=None, 
#     hash_paths=None)
# This returns a Step
dataset_registration_step = PythonScriptStep(
    name="dataset_registration_step",
    script_name="data_ops/data_pipelines/register_aml_dataset.py", 
    compute_target=compute_cluster, 
    source_directory=source_directory,
    allow_reuse=True
    )
print("dataset_registration_step created")

steps = [dataset_cleansing_step, azureml_ingest, dataset_registration_step]
steps = [dataset_registration_step]
dataset_prep_pipeline = Pipeline(workspace=ws, steps=steps)
print ("Pipeline is built")

dataset_prep_pipeline.validate()
print("Pipeline validation complete")

dataset_prep_pipeline.publish(name="dataset_prep_pipeline", description="dataset_prep_pipeline", version="0.0.1", continue_on_step_failure=False)

pipeline_run = Experiment(ws, 'dataset_prep_pipeline').submit(dataset_prep_pipeline)
pipeline_run.wait_for_completion()