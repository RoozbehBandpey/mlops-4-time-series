import os
import sys
import os
import azureml.core
from azureml.core import Datastore, Dataset
from azureml.data.dataset_factory import DataType

# Check core SDK version number
print("SDK version:", azureml.core.VERSION)

sys.path.append(os.getcwd())
from azureml_utils.workspace_helper import WorkspaceHelper

wsh = WorkspaceHelper()
ws = wsh.get_workspace()
    
datastore = Datastore.get_default(ws)

print(datastore)

# create a TabularDataset from 3 file paths in datastore
datastore_test_paths = [(datastore, 'kaggle/test.parquet/*.snappy.parquet')]

demand_test_ds = Dataset.Tabular.from_parquet_files(path=datastore_test_paths, set_column_types={'date': DataType.to_datetime(formats='%Y-%m-%d %H:%M:%S')})
demand_test_ds.register(ws, 'demand-forecasting-kaggle-test', 'Demand forecasting data from kaggle, One month of data December 2017', create_new_version=True)
