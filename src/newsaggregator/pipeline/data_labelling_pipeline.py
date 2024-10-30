from src.newsaggregator.config.configuration import ConfigurationManager
from src.newsaggregator.components.data_labeling import DataLabelling
from src.newsaggregator import logger

STAGE_NAME = "Data Labelling Stage"

class DataLabellingTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_labelling(self):
        try:
            # Load configuration
            config = ConfigurationManager()
            data_labelling_config = config.get_data_labelling_config()
            data_labelling = DataLabelling(data_labelling_config)

            # Determine fake news
            results = data_labelling.determine_fake_news()
            logger.info("Data labelling completed successfully.")
            path = data_labelling.save_to_csv()
            logger.info(f"Data stored in {path}")
            # You can now use `results` for further processing
            print(results.value_counts())

        except Exception as e:
            logger.error(f"An error occurred during data labelling: {e}")

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<<<")
        pipeline = DataLabellingTrainingPipeline()
        pipeline.initiate_data_labelling()
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<")
    except Exception as e:
        logger.error(f"Error occurred in {STAGE_NAME} stage: {str(e)}")
        raise e
