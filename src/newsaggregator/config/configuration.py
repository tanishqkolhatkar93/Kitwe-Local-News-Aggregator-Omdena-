from src.newsaggregator.constants import *
from src.newsaggregator.utils.common import read_yaml , create_directories
from src.newsaggregator.entity.config_entity import (DataIngestionConfig,DataCleaningConfig)

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
            root_dir=Path(config['root_dir']), 
            input_path=Path(config['input_path']),  
            output_path=Path(config['output_path']) 
        )
        return data_ingestion_config
    
    
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH
                 ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)
        
        create_directories([self.config.artifacts_root])
        
    def get_data_cleaning_config(self) -> DataCleaningConfig:
        config = self.config.data_cleaning
        create_directories([config.root_dir])
        
        data_transformation_config = DataCleaningConfig(
            root_dir=Path(config['root_dir']), 
            input_path=Path(config['input_path']),  
            output_path=Path(config['output_path']),
            date_column = config['date_column'], 
            text_columns = config['text_columns']
        )
        return data_transformation_config
    
    
    
    
    
    
    