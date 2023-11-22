# Real-Time Movie Recommendation System - Spark Streaming

This Python script is part of a Real-Time Movie Recommendation System, responsible for processing and enriching streaming data from Kafka topics and storing the results in Elasticsearch.

## Dependencies

- `findspark`: Used for initializing Spark in a non-Spark environment.
- `logging`: Used for logging events during the Spark Streaming process.
- `datetime`: Used for generating timestamped log filenames.
- `time`: Used for introducing delays between producing messages.
- `os`: Used for file operations and directory creation.
- `threading`: Used for parallel execution of Spark Streaming for movies and reviews.
- `uuid4`: Used for generating unique identifiers.
- `elasticsearch`: Python client for Elasticsearch.
- `elasticsearch_sender`: Custom module for interacting with Elasticsearch.
- `pyspark`: PySpark library for working with Spark.

## Configuration

- **Kafka Bootstrap Servers**: Update the `kafka_bootstrap_servers` parameter in the `sparkTreatment_movies` and `sparkTreatment_reviews` functions with the address of your Kafka broker.
- **Elasticsearch Configuration**: Update the Elasticsearch connection details in the `writeStream` options of both functions.

## Functions

### 1. `setup_logging()`

Sets up logging, creating a log directory and generating a log file with a timestamped filename. Logs contain information about Spark Streaming initialization and any errors that occur.

### 2. `sparkSessionInitialiser()`

Initializes SparkSession for Spark Streaming. Specifies necessary packages for Spark, including the Kafka and Elasticsearch dependencies.

### 3. `sparkTreatment_movies(topicname, kafka_bootstrap_servers, consumer_logger)`

Processes movie streaming data from a Kafka topic, performs transformations, and writes the results to Elasticsearch.

### 4. `sparkTreatment_reviews(topicname, kafka_bootstrap_servers, consumer_logger)`

Processes review streaming data from a Kafka topic, performs transformations, and writes the results to Elasticsearch.

### 5. `runSparkTreatment()`

Main function that creates threads for `sparkTreatment_movies` and `sparkTreatment_reviews` and starts their execution in parallel. It logs any unexpected errors that occur.

## Usage

1. Update the Kafka bootstrap servers and Elasticsearch connection details in the `sparkTreatment_movies` and `sparkTreatment_reviews` functions.
2. Run the script.
3. Spark Streaming processes movies and reviews from Kafka topics concurrently and stores the enriched data in Elasticsearch.

**Note**: Ensure that your Kafka broker, Elasticsearch, and other dependencies are properly configured and running before executing the script.
