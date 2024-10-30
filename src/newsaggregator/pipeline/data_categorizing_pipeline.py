from src.newsaggregator.config.configuration import ConfigurationManager
from src.newsaggregator.components.data_categorizing import DataCategorizing
from src.newsaggregator import logger

STAGE_NAME = "Data categorizing Stage"

class DataCategorizingTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_categorizing(self):
        try:
            # Load configuration
            config = ConfigurationManager()
            data_labelling_config = config.get_data_categorizing_config()
            data_labelling = DataCategorizing(data_labelling_config)

            # Determine fake news
            results = data_labelling.categorize()
            logger.info("Data get_data_categorizing_config completed successfully.")
            data_labelling.save_output()
            
            # You can now use `results` for further processing
            print(results.head())
            print(results.value_counts())

        except Exception as e:
            logger.error(f"An error occurred during data labelling: {e}")

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataCategorizingTrainingPipeline()
        pipeline.initiate_data_categorizing()
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<")
    except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e
