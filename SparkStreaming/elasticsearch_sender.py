from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType, ArrayType
from elasticsearch import Elasticsearch
from datetime import datetime
from elasticsearch.exceptions import RequestError
import os
import logging

def elastic_setup_logging():
    log_directory = "Log/ElasticSearch"

    os.makedirs(log_directory, exist_ok=True)

    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_directory, log_filename)

    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    consumer_logger = logging.getLogger(__name__)  
    
    return consumer_logger

def connectToelastic(elastic_logger):
    # We can directly do all Elasticsearch-related operations in our Spark script using this object.
    es = Elasticsearch("http://localhost:9200")

    if es:
        elastic_logger.info("Connected to elastic search Successfully")

        return es
    
def createMovieIndex(esconnection , elastic_logger):
    my_index_body = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        },
        "mappings": {
            "properties": {
                "adult": {"type": "boolean"},
                "backdrop_path": {"type": "text"},
                "genre_ids": {"type": "integer"},
                "id": {"type": "integer"},
                "original_language": {"type": "keyword"},
                "original_title": {"type": "text"},
                "overview": {"type": "text"},
                "popularity": {"type": "float"},
                "poster_path": {"type": "text"},
                "release_date": {
                    "type": "date"
                },
                "title": {"type": "keyword"},
                "video": {"type": "boolean"},
                "vote_average": {"type": "float"},
                "vote_count": {"type": "integer"}
            }
        }
    }

    try:
        esconnection.indices.create(index="movie", body=my_index_body)
        elastic_logger.info("Index 'movie' created successfully.")
    except RequestError as e:
        if "resource_already_exists_exception" in str(e):
            elastic_logger.info("Index 'movie' already exists.")
        else:
            elastic_logger.error(f"Error creating index: {e}")

def createReviewsIndex(esconnection  , elastic_logger):
    my_index_body = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        },
        "mappings": {
            "properties": {
                "author": {"type": "keyword"},
                "author_details": {
                    "type": "nested",
                    "properties": {
                        "name": {"type": "keyword"},
                        "username": {"type": "keyword"},
                        "avatar_path": {"type": "text"},
                        "rating": {"type": "double"}
                    }
                },
                "content": {"type": "text"},
                "created_at": {"type": "text"},
                "id": {"type": "text"},
                "updated_at": {"type": "text"},
                "url": {"type": "text"}
            }
        }
    }

    try:
        esconnection.indices.create(index="review", body=my_index_body)
        elastic_logger.info("Index 'movie' created successfully.")
    except RequestError as e:
        if "resource_already_exists_exception" in str(e):
            elastic_logger.info("Index 'review' already exists.")
        else:
            elastic_logger.error(f"Error creating index: {e}")
