from src.newsaggregator.constants import *
from src.newsaggregator.utils.common import read_yaml , create_directories
from src.newsaggregator.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH
                 ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config['root_dir']),  # Convert to Path
            News_websites=config['News_websites'],  # Keep it as is, since it's a dict
            output_path=Path(config['output_path'])  # Convert to Path
        )
        return data_ingestion_config
    
    