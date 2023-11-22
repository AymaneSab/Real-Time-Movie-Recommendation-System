import requests
import json
import logging
import os
from datetime import datetime


# Function to scrapp the last scrapped page
def save_last_page(page_number):
    with open("last_page.txt", "w") as file:
        file.write(str(page_number))

# Fucntion to get last scrapped page 
def load_last_page():
    try:
        with open("last_page.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 1

# Function to setup loggin
def setup_logging():
    log_directory = "Log/Producer_Log_Files"
    os.makedirs(log_directory, exist_ok=True)

    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_directory, log_filename)

    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    producer_logger = logging.getLogger(__name__)  
    
    return producer_logger

# Function to discover movies
def discover_movies(api_key, page , scrapperLogger):
    base_url = "https://api.themoviedb.org/3/discover/movie"
    api_url = f"{base_url}?api_key={api_key}&page={page}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for errors
        movie_data = response.json()
        return movie_data
    
    except requests.exceptions.HTTPError as errh:
        scrapperLogger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        scrapperLogger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        scrapperLogger.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        scrapperLogger.error(f"Request Error: {err}")

# Function to get scrapped movies reviews 
def get_movie_reviews(api_key, movie_id , scrapperLogger):
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
    api_url = f"{base_url}?api_key={api_key}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for errors
        reviews_data = response.json()
        return reviews_data

    except requests.exceptions.HTTPError as errh:
        scrapperLogger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        scrapperLogger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        scrapperLogger.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        scrapperLogger.error(f"Request Error: {err}")

# Main scrapping function that yield the comfirmed results immediatly
def get_movies():
    api_key = "b94550d27d581fc676beb262af7a97e1"
    current_page = load_last_page()

    scrapperLogger = setup_logging()

    try:
        while True:
            movie_data = discover_movies(api_key, current_page , scrapperLogger)

            if 'results' in movie_data:
                for movie in movie_data['results']:
                    movie_id = movie['id']
                    scrapperLogger.info(f"Film Scrapped in page {current_page}, Movie ID: {movie_id}")

                    # Get reviews for the current movie
                    reviews_data = get_movie_reviews(api_key, movie_id , scrapperLogger)
                    if 'results' in reviews_data:
                        scrapperLogger.info(f"Review Scrapped for {movie_id}")

                    # Combine movie_info_dict and reviews_dict into one dictionary
                    combined_data = {'movie': movie, 'review': reviews_data['results']}
                    json_data = json.dumps(combined_data)
                    
                    yield json_data
            
                current_page += 1
                save_last_page(current_page)

    except KeyboardInterrupt:
        scrapperLogger.info(f"Script paused. Last scraped page: {current_page}")
        save_last_page(current_page)

