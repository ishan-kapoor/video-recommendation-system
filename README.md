# Video Recommendation Algorithm

## Overview
This project implements a personalized video recommendation system using data retrieved from APIs. The algorithm uses a hybrid approach, combining content-based filtering and collaborative filtering, to recommend videos based on user preferences, engagement patterns, and metadata.

## Features
- Fetch and preprocess data from APIs.
- Content-based filtering using TF-IDF and cosine similarity.
- Collaborative filtering using Nearest Neighbors.
- Hybrid model combining both approaches for improved accuracy.
- Handles cold start problem using user mood.
- Provides API endpoints to fetch recommended posts.

## Prerequisites
Ensure you have the following installed:
- Python 3.7 or above
- pip (Python package installer)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/ishan-kapoor/video-recommendation-system
   cd video-recommendation-system
2. Set up a virtual environment (optional but recommended):
    python -m venv recommendation_env
    source recommendation_env/bin/activate  # On Windows: recommendation_env\Scripts\activate
3. Install dependencies:
    pip install -r requirements.txt
4. Run the application:
    python app.py
5. Open a browser or use Postman to test the endpoints.

API Endpoints

1. Get Recommended Posts
    Endpoint: /feed

2. Query Parameters:
    username: (Required) The username of the user.
    category_id: (Optional) The category of videos the user wants to see.
    mood: (Optional) The user's current mood.

3. Examples:
    /feed?username=your_username
    /feed?username=your_username&category_id=1
    /feed?username=your_username&category_id=1&mood=happy
    Response: Returns a list of recommended posts in JSON format.

Implementation Details
1. Data Preprocessing
    Fetches data using APIs with pagination to ensure no duplicates.
    Handles missing values and normalizes data for model compatibility.
2. Recommendation Models
    -> Content-Based Filtering:
        Uses TF-IDF vectorization and cosine similarity to find videos with similar tags.
    -> Collaborative Filtering:
        Utilizes Nearest Neighbors to recommend videos based on user-item interactions.
    -> Hybrid Model:
        Combines the strengths of both approaches to improve recommendation quality.
3. Evaluation Metrics
    Mean Absolute Error (MAE)
    Root Mean Squared Error (RMSE)

Code Structure

├── data_preprocessing.py    # Data fetching and preprocessing logic

├── model.py                 # Recommendation models

├── app.py                   # Flask application and API endpoints

├── requirements.txt         # Python dependencies

├── sklearn.metrics          # Evaluation metrics

├── README.md                # Documentation


EXAMPLE REQUEST:- GET http://localhost:5000/feed?username=test_user&category_id=2&mood=happy
