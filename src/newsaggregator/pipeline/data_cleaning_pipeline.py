from src.newsaggregator.config.configuration import ConfigurationManager
from src.newsaggregator.components.data_cleaning import DataCleaning
from src.newsaggregator import logger

STAGE_NAME = "Data Cleaning Stage"

class DataCleaningTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_cleaning(self):
        """Initiates the data cleaning process."""
        try:
            config = ConfigurationManager()
            data_cleaning_config = config.get_data_cleaning_config()  

            data_cleaning = DataCleaning(data_cleaning_config)
            data_cleaning.clean()

            cleaned_data = data_cleaning.get_cleaned_data()
            if cleaned_data is not None:
                logger.info("Cleaned Data Head:\n" + str(cleaned_data.head()))  
            else:
                logger.warning("No cleaned data returned.")

        except Exception as e:
            logger.error(f"An error occurred during data cleaning: {e}")

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataCleaningTrainingPipeline()
        pipeline.initiate_data_cleaning()  # Fixed method name here
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<")
    except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e
