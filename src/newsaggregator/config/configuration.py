from src.newsaggregator.constants import *
from src.newsaggregator.utils.common import read_yaml, create_directories
from src.newsaggregator.entity.config_entity import (
    DataIngestionConfig,
    DataCleaningConfig,
    DataCategorizingConfig,
    DataLabellingConfig,
)
from pathlib import Path

class ConfigurationManager:

    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH,
                 schema_filepath=SCHEMA_FILE_PATH):
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

    def get_data_categorizing_config(self) -> DataCategorizingConfig:
        config = self.config.data_categorizer
        create_directories([config.root_dir])

        # Access the categories_keywords dictionary directly
        data_categorizing_config = DataCategorizingConfig(
            root_dir=Path(config['root_dir']),
            input_path=Path(config['input_path']),
            output_path=Path(config['output_path']),
            categories_keywords=config['categories_keywords']  # Ensure this is a dict
        )

        return data_categorizing_config

    def get_data_labelling_config(self) -> DataLabellingConfig:
        config = self.config.data_labelling
        create_directories([config['root_dir']])

        data_labelling_config = DataLabellingConfig(
            root_dir=Path(config.root_dir),
            input_path=Path(config['input_path']),
            output_path=Path(config['output_path']),
            model_path=Path(config['model_path']),
            reputable_sources=config['reputable_sources'],
            suspicious_domain_patterns=config['suspicious_domain_patterns'],
            sensational_keywords=config['sensational_keywords'],
            thresholds=config['thresholds']
        )
        return data_labelling_config

    def get_data_cleaning_config(self) -> DataCleaningConfig:
        config = self.config.data_cleaning
        create_directories([config.root_dir])

        data_cleaning_config = DataCleaningConfig(
            root_dir=Path(config['root_dir']),
            input_path=Path(config['input_path']),
            output_path=Path(config['output_path']),
            date_column=config['date_column'],
            text_columns=config['text_columns']
        )
        return data_cleaning_config
