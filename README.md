# Real-Time Movie Recommendation System

## Project Overview

As a Data Developer, your role is to build a real-time movie recommendation system, covering the entire data pipeline from collecting data from movielens.org API to presenting recommendations to users. The key steps include:

### 1. Configuration of Kafka

Set up a Kafka cluster and configure producers to send user interaction data to specific topics.

### 2. Processing with Spark Streaming

Create pipelines to consume data from Kafka, apply transformations (e.g., data enrichment, normalization, and type conversion), and send the processed data to Elasticsearch.

Example Transformations:
- Enrichment: Combine title and overview to create a "description" field.
- Normalization: Normalize fields like average votes and popularity.
- Data Transformation: Convert date strings into date data types.

You can introduce additional transformations, such as flattening the genre ID, to enhance data visualization.

### 3. Modeling and Storage in Elasticsearch

Design data indices and models in Elasticsearch to store movie and user information efficiently.

### 4. Development of Recommendation API

Implement a RESTful API using a framework like Flask, interacting with Elasticsearch to retrieve and serve movie recommendations.

### 5. Visualization with Kibana

Create dashboards in Kibana for visualizations that aid decision-making.

Example Visualizations:
- Distribution of movies by release date.
- Top 10 popular movies.
- Average rating per genre.
- Language distribution of movies.
- Top 10 movies with the most votes.
- Distribution of movie ratings.

## Project Structure

- **`/kafka`**: Contains Kafka configuration files and scripts.
- **`/spark`**: Spark Streaming application for data processing.
- **`/elasticsearch`**: Elasticsearch index and mapping configurations.
- **`/api`**: Flask-based API for serving recommendations.
- **`/kibana`**: Kibana dashboard configurations.

## Setup and Configuration

1. Install and configure Kafka.
2. Set up Spark Streaming for data processing.
3. Configure and deploy Elasticsearch for data storage.
4. Develop and deploy the Flask API for serving recommendations.
5. Set up Kibana for visualizations.

## Usage

Provide instructions on how to run the different components of the system.

```bash
# Example command for starting Spark Streaming application
cd /path/to/spark
./submit_spark_job.sh
