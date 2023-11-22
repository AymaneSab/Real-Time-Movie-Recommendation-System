import findspark
findspark.init()

import logging
from datetime import datetime
import time
import os
import threading
from uuid import uuid4
from elasticsearch import Elasticsearch
from elasticsearch_sender import elastic_setup_logging , connectToelastic , createMovieIndex , createReviewsIndex

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, from_json
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, ArrayType, IntegerType, FloatType , DoubleType , DateType
from pyspark.sql.functions import explode
from pyspark.sql.functions import col, date_format
from pyspark.sql.functions import col, to_date


def setup_logging():
    log_directory = "Log/SparkStreaming"

    os.makedirs(log_directory, exist_ok=True)

    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_directory, log_filename)

    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    consumer_logger = logging.getLogger(__name__)  
    
    return consumer_logger

def sparkSessionInitialiser():
        packages = [
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0",
            "org.elasticsearch:elasticsearch-spark-30_2.12:8.4.2",
            #"org.apache.spark.serializer.KryoSerializer"  
        ]

        # Initialize SparkSession for Elasticsearch
        spark = SparkSession.builder \
            .appName("Spark Treatment") \
            .config("spark.jars.packages", ",".join(packages)) \
            .getOrCreate()
        
        return spark

def sparkTreatment_movies(topicname, kafka_bootstrap_servers , consumer_logger):
    try:

        elastic_logger = elastic_setup_logging()

        spark = sparkSessionInitialiser()

        consumer_logger.info("----------> sparkTreatment_movies Initialized Successfully")

        # Define the schema for Kafka messages
        kafka_schema = StructType([
            StructField("adult", BooleanType(), True),
            StructField("backdrop_path", StringType(), True),
            StructField("genre_ids", ArrayType(IntegerType()), True),
            StructField("id", IntegerType(), True),
            StructField("original_language", StringType(), True),
            StructField("original_title", StringType(), True),
            StructField("overview", StringType(), True),
            StructField("popularity", FloatType(), True),
            StructField("poster_path", StringType(), True),
            StructField("release_date", DateType(), True),
            StructField("title", StringType(), True),
            StructField("video", BooleanType(), True),
            StructField("vote_average", FloatType(), True),
            StructField("vote_count", IntegerType(), True)
        ])

        # Read data from Kafka topic with defined schema
        kafka_stream_df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", topicname) \
            .load() \
            .selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", kafka_schema).alias("data")) \
            .select("data.*")

        consumer_logger.info("----------> Kafka Stream Data Loaded Successfully")

        # Perform transformations
        enriched_df = kafka_stream_df.withColumn("description", expr("concat(title, ' - ', overview)"))

        normalized_df = enriched_df.withColumn("normalized_vote_average", col("vote_average") / 10.0)

        transformed_df = normalized_df.withColumn("release_date", date_format(col("release_date"), "yyyy-MM-dd").cast("date"))

        #flattened_df = transformed_df.withColumn("genre_id", expr("explode(genre_ids)")).drop("genre_ids")

        checkpoint_location = "Elasticsearch/Checkpoint/Movies"

        if not os.path.exists(checkpoint_location):
            os.makedirs(checkpoint_location)

        # Add logging statement for Elasticsearch connection
        consumer_logger.info("----------> Connecting to Elasticsearch")

        es = connectToelastic(elastic_logger)

        createMovieIndex(es , elastic_logger)

        # Write to Elasticsearch
        transformed_df.writeStream \
            .format("org.elasticsearch.spark.sql") \
            .outputMode("append") \
            .option("es.nodes", "localhost") \
            .option("es.port", "9200") \
            .option("es.resource", "movie/_doc") \
            .option("checkpointLocation", checkpoint_location) \
            .start().awaitTermination()

    except Exception as e:
        consumer_logger.error(f"An error occurred: {str(e)}")
    finally:
        # Stop SparkSession
        spark.stop()
        consumer_logger.info("----------> SparkSession Stopped")
        
def sparkTreatment_reviews(topicname, kafka_bootstrap_servers , consumer_logger):
    try:
        elastic_logger = elastic_setup_logging()

        spark = sparkSessionInitialiser()

        consumer_logger.info("----------> Packages Loaded Successfully ")

        kafka_schema = StructType([
            StructField("author", StringType(), True),
            StructField("author_details", StructType([
                StructField("name", StringType(), True),
                StructField("username", StringType(), True),
                StructField("avatar_path", StringType(), True),
                StructField("rating", DoubleType(), True)
            ]), True),
            StructField("content", StringType(), True),
            StructField("created_at", StringType(), True),
            StructField("id", StringType(), True),
            StructField("updated_at", StringType(), True),
            StructField("url", StringType(), True)
        ])

        # Read data from Kafka topic with defined schema
        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", topicname) \
            .load() \
            .selectExpr("CAST(value AS STRING)") \
            .select(explode(from_json("value", ArrayType(kafka_schema))).alias("data")) \
            .select("data.*")
        
        checkpoint_location = "Elasticsearch/Checkpoint/Reviews"

        if not os.path.exists(checkpoint_location):
            os.makedirs(checkpoint_location)

        es = connectToelastic(elastic_logger)

        createReviewsIndex(es , elastic_logger)

        # Write to Elasticsearch
        df.writeStream \
            .format("org.elasticsearch.spark.sql") \
            .outputMode("append") \
            .option("es.nodes", "localhost") \
            .option("es.port", "9200") \
            .option("es.resource", "review/_doc") \
            .option("checkpointLocation", checkpoint_location) \
            .start().awaitTermination()

    except Exception as e:
        consumer_logger.error(f"An error occurred: {str(e)}")
    finally:
        spark.stop()

# Example usage
def runSparkTreatment():
    try:
        log_file = setup_logging()

        # Create threads for sparkTreatment_movies and sparkTreatment_reviews
        movies_thread = threading.Thread(target=sparkTreatment_movies, args=("Movies", "localhost:9092" , log_file))
        reviews_thread = threading.Thread(target=sparkTreatment_reviews, args=("Reviews", "localhost:9092" , log_file))

        # Start the threads
        movies_thread.start()
        reviews_thread.start()

        # Wait for both threads to finish
        movies_thread.join()
        reviews_thread.join()

    except KeyboardInterrupt:
        logging.info("Spark Treatment Stopped")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.exception("An unexpected error occurred in Spark")

runSparkTreatment()