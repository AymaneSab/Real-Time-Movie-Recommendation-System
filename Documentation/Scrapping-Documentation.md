# Movie Scraper

This Python script is designed to scrape movie data and reviews from The Movie Database (TMDb) API. It consists of functions to discover movies, retrieve movie reviews, and perform the scraping in a controlled manner.

## Setup

### Dependencies

- `requests`: Used for making HTTP requests to the TMDb API.
- `json`: Used for working with JSON data.
- `logging`: Used for logging events during the scraping process.
- `os`: Used for handling file operations and creating directories.
- `datetime`: Used for generating timestamped log filenames.

### API Key

The script requires a TMDb API key for authentication. Replace `api_key` with your valid API key.

## Functions

### 1. `setup_logging()`

This function sets up logging, creating a log directory and generating a log file with a timestamped filename. Logs contain information about HTTP errors, connection errors, timeouts, and general request errors.

### 2. `discover_movies(api_key, page=1)`

This function queries the TMDb API to discover movies. It takes an API key and an optional page parameter. It handles HTTP errors and returns movie data.

### 3. `get_movie_reviews(api_key, movie_id)`

This function retrieves reviews for a given movie ID using the TMDb API. It handles HTTP errors and returns review data.

### 4. `save_last_page(page_number)`

Saves the last scraped page number to a text file named `last_page.txt`.

### 5. `load_last_page()`

Loads the last scraped page number from the `last_page.txt` file. If the file doesn't exist, it defaults to page 1.

### 6. `get_movies()`

The main scraping function that yields confirmed results immediately. It continuously discovers movies, retrieves reviews, and logs the progress. The scraping can be paused by interrupting the script (Ctrl+C), and the last scraped page is saved.

## Usage

Replace the `api_key` variable with your TMDb API key. Run the script, and it will continuously scrape movies and their reviews until interrupted.

**Note**: Make sure to handle your API key securely and respect TMDb's usage policies.
