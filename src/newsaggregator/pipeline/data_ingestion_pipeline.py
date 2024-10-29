from src.newsaggregator.config.configuration import ConfigurationManager
from src.newsaggregator.components.data_ingestion import DataIngestion
from src.newsaggregator import  logger


STAGE_NAME = "Data Ingestion Stage"
class DataIngestionTrainingPipeline:
    def __init__(self):
        pass
    def initiate_data_ingestion(self):
        try:
            config = ConfigurationManager()
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)

            # Call the extract_data method
            data = data_ingestion.load_and_save_data()

            # You can now use `data` for further processing
        except Exception as e:
            logger.error(f"An error occurred during data ingestion: {e}")
            

            
            
if __name__ == "__main__":
    try:
        logger.info(f">>>>>>Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.initiate_data_ingestion()
        logger.info(f">>>>>>>>>>>>>>>{STAGE_NAME} completed <<<<<<<<<<<<")
    except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e
    