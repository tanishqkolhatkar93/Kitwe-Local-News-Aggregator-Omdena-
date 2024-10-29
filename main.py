from src.newsaggregator import logger
from src.newsaggregator.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.newsaggregator.pipeline.data_cleaning_pipeline import DataCleaningTrainingPipeline

STAGE_NAME ="Data Ingestion stage"

try:
        logger.info(f">>>>>>Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataIngestionTrainingPipeline()
        pipeline.initiate_data_ingestion()
        logger.info(f">>>>>>>>>>>>>>>{STAGE_NAME} completed <<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e

STAGE_NAME = "Data Cleaning Stage"

try:
        logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataCleaningTrainingPipeline()
        pipeline.initiate_data_cleaning()  # Fixed method name here
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<")
except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e
