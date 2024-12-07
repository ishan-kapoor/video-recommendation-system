import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://api.socialverseapp.com"
HEADERS = {"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"}

# Cache for API results
cache = {}

def fetch_data(endpoint, params):
    data = []
    page = 1
    while True:
        params.update({"page": page, "page_size": 1000})
        cache_key = f"{endpoint}_{page}"
        if cache_key in cache:
            logging.debug(f"Using cached data for {cache_key}")
            new_data = cache[cache_key]
        else:
            response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params)
            if response.status_code == 200:
                new_data = response.json().get('data', [])
                cache[cache_key] = new_data  # Cache results
            else:
                logging.error(f"Error fetching data from {endpoint}: {response.status_code}")
                break
        if not new_data:
            break
        data.extend(new_data)
        page += 1
    return data

def fetch_all_data():
    try:
        logging.info("Fetching all data from API...")
        posts = {
            "viewed": fetch_data("posts/view", {}),
            "liked": fetch_data("posts/like", {}),
            "inspired": fetch_data("posts/inspire", {}),
            "rated": fetch_data("posts/rating", {}),
            "summary": fetch_data("posts/summary/get", {}),
            "users": fetch_data("users/get_all", {}),
        }
        logging.info("Data fetch complete.")
        return posts
    except Exception as e:
        logging.error(f"Error fetching all data: {e}")
        return {}

def preprocess_data(posts_data):
    try:
        # Convert posts data into a DataFrame
        logging.info("Preprocessing posts data...")
        posts_df = pd.DataFrame(posts_data['summary'])

        # Check if 'rating' column exists, and if not, create it with default values
        if 'rating' not in posts_df.columns:
            posts_df['rating'] = posts_df['category_id'].apply(lambda x: 3.0)  # Default rating
        
        # Fill missing values for 'rating' column with its mean
        posts_df.fillna({'rating': posts_df['rating'].mean()}, inplace=True)

        # Normalize the 'rating' between 0 and 5
        posts_df['rating'] = posts_df['rating'].apply(lambda x: max(0, min(x, 5)))

        logging.info(f"Preprocessing complete. Columns: {posts_df.columns}")
        return posts_df
    except Exception as e:
        logging.error(f"Error in preprocessing: {e}")
        return pd.DataFrame()
