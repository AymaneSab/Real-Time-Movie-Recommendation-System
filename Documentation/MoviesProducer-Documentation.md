# Real-Time Movie Recommendation System - Kafka Producer

This Python script serves as a Kafka producer for a Real-Time Movie Recommendation System. It produces movie information and reviews to Kafka topics.

## Dependencies

- `os`: Used for file operations and directory creation.
- `json`: Used for working with JSON data.
- `logging`: Used for logging events during the Kafka producing process.
- `time`: Used for introducing delays between producing messages.
- `datetime`: Used for generating timestamped log filenames.
- `confluent_kafka`: Used for interacting with Apache Kafka.

## Configuration

- **Kafka Broker Address**: Update the `bootstrap.servers` parameter in the `Producer` instantiation with the address of your Kafka broker.

- **Topics**: Modify the `topic1` and `topic2` variables with the desired Kafka topics for movie information and reviews.

## Functions

### 1. `setup_producer_logging()`

Sets up logging for the producer, creating a log directory and generating a log file with a timestamped filename. Logs contain information about the producer's actions.

### 2. `create_kafka_topic(topic, admin_client, producer_logger)`

Creates a Kafka topic if it does not already exist. Logs the outcome of the topic creation process.

### 3. `produce_to_Topics(movieTopic, reviewTopic, producer_logger)`

Generates movie data using the `get_movies` function and continuously produces messages to the specified Kafka topics. Logs successful production to each topic.

### 4. `runKafkaProducer(topic1, topic2)`

Main function that orchestrates the Kafka producer. Sets up logging, creates Kafka topics, and starts producing to the topics simultaneously.

## Usage

1. Update the Kafka broker address in the `Producer` instantiation.
2. Modify the `topic1` and `topic2` variables with the desired Kafka topics.
3. Run the script.

The producer will continuously fetch movie data using the `get_movies` function and produce messages to the specified Kafka topics.

**Note**: Ensure the Kafka broker is running, and the topics are created in the broker before running the producer script.
