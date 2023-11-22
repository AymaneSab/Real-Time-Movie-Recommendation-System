# Movie Recommendation Flask App

This Flask application serves as an endpoint for recommending movies based on user input. It connects to Elasticsearch to retrieve movie recommendations.

## Dependencies

- `Flask`: Web framework for building the application.
- `elasticsearch`: Python client for Elasticsearch.

## Configuration

- **Elasticsearch Configuration**: Update the Elasticsearch connection details in the `Elasticsearch` instantiation.

## Routes

### 1. `/`

- **Method**: `GET`
- **Description**: Renders the main page (`index.html`) for the web application.

### 2. `/recommend`

- **Method**: `POST`
- **Description**: Receives a JSON payload containing the film name. Retrieves the genre ID for the specified film from Elasticsearch, then searches for movies with a similar genre. Returns a JSON response with movie recommendations based on the genre.

## Functions

### 1. `index()`

Renders the main page (`index.html`) for the web application.

### 2. `get_recommendations()`

Handles the `/recommend` route. Parses the JSON payload, retrieves the genre ID for the specified film from Elasticsearch, searches for movies with a similar genre, and returns recommendations in a JSON response.

## Usage

1. Ensure that Elasticsearch is running and accessible.
2. Update the Elasticsearch connection details in the `Elasticsearch` instantiation.
3. Run the Flask application.

Visit the web application in a browser and enter a film name. The application will recommend movies based on the genre of the specified film.

**Note**: This is a basic Flask application, and it's assumed that the `index.html` file is present in the templates directory. Customize the application further based on your specific requirements and improve error handling as needed.
