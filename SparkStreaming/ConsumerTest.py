from confluent_kafka import Consumer
import logging
from logging.handlers import RotatingFileHandler
import time
import os
import time

def get_log_filename(topic_name):
    
    current_datetime = time.strftime("%Y%m%d%H%M%S")
    current_date = time.strftime("%Y%m%d")
    log_directory = "Log/Consumer_Log_File"
    
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, f'kafka_consumer_{topic_name}_{current_date}_{current_datetime}.log')
    return log_file

def kafkaConsumer(topicName):
    # Configure the Kafka consumer
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',  # Kafka broker address
        'group.id': 'my-group',  # Consumer group ID
        'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
    }

    # Create a Kafka consumer instance
    consumer = Consumer(consumer_config)

    # Subscribe to the Kafka topic
    topic = topicName  # Replace with your actual topic
    consumer.subscribe([topic])

    # Get the log file name with a timestamp
    log_file = get_log_filename(topic)

    log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=3)
    handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    empty_poll_count = 0  # Initialize the empty poll count

    try:
        logging.info(f"Kafka Consumer Configuration: {consumer_config}")
        while True:
            msg = consumer.poll(5.0)  # Poll for messages, waiting up to 1 second for new messages

            if msg is None:
                empty_poll_count += 1
                if empty_poll_count >= 3:  # Exit the loop if there are 3 consecutive empty polls
                    logging.info("No new messages received. Exiting.")
                    break
            else:
                empty_poll_count = 0  # Reset the empty poll count

                if msg.error():
                    # Log errors with timestamp and topic information
                    logging.error(f"{topic}: Error while consuming: {msg.error()}")
                else:
                    # Log received messages with timestamp and topic information
                    logging.info(f"{topic}: Received message: {msg.value().decode('utf-8')}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    except KeyboardInterrupt:
        logging.info("Kafka Consumer Stopped")
        consumer.close()
        pass

    finally:
        consumer.close()

def runKafkaConsumer(topic_name):
    try:
        kafkaConsumer(topic_name)
        
    except KeyboardInterrupt:
        logging.info("Kafka Consumer Stopped")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.info(f"An unexpected error occurred in Kafka Consumer: {e}")

runKafkaConsumer("Movies")
