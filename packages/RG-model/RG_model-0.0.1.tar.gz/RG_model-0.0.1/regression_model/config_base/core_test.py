from pyexpat import features
from strictyaml import YAML, load
from typing import Dict, List, Sequence
from pydantic import BaseModel
from pathlib import Path
import regression_model

PACKAGE_ROOT = Path(regression_model.__file__).resolve().parent
config_file_path = PACKAGE_ROOT / 'config.yaml'
Datasets = PACKAGE_ROOT / 'datasets'
trained_model_directory = PACKAGE_ROOT / 'trained_models'

class Appconfig(BaseModel):
  
  data_directory: str
  data_name: str
  test_data_name: str
  pipeline_save_file: str
  package_name: str
  
class ModelConfig(BaseModel):
  
  target: str
  features: List[str]
  test_size: float
  random_state: int
  drop_feature: str
  
class Config(BaseModel):
#     """Master config object."""

    app_config: Appconfig
    model_config: ModelConfig


def find_config_file_path():
  if config_file_path.is_file():
    return config_file_path 
def fetch_config_from_yaml(confg_path: Path = None):
  if not confg_path:
    confg_path = find_config_file_path()
  if confg_path:
    with open(confg_path,'r') as file:
      parsed_file = load(file.read())
      return parsed_file
def create_and_validate_config(parsed_config: YAML = None):
    if parsed_config is None:
      parsed_config = fetch_config_from_yaml()
      
    _config = Config(app_config=Appconfig(**parsed_config.data),model_config=ModelConfig(**parsed_config.data))
    return _config
  
config = create_and_validate_config()







  