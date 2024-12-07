import pandas as pd
from flask import Flask, request, jsonify
from data_preprocessing import fetch_all_data, preprocess_data
from model import content_based_recommendations, collaborative_filtering
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Hybrid model combining content-based and collaborative filtering
def hybrid_model(user_data, posts_df):
    # Get content-based recommendations
    content_recommendations = content_based_recommendations(user_data, posts_df)
    logging.debug(f"Content-based recommendations: {content_recommendations.head()}")

    # Get collaborative filtering recommendations
    collaborative_recommendations = collaborative_filtering(user_data, posts_df)
    logging.debug(f"Collaborative filtering recommendations: {collaborative_recommendations.head()}")

    # Combine both recommendations with weighted averaging
    combined_recommendations = pd.concat([content_recommendations, collaborative_recommendations])
    combined_recommendations = combined_recommendations.drop_duplicates(subset='post_id')
    combined_recommendations['combined_score'] = combined_recommendations['content_score'] * 0.6 + \
                                                 combined_recommendations['collab_score'] * 0.4
    combined_recommendations = combined_recommendations.sort_values(by='combined_score', ascending=False)
    
    return combined_recommendations

@app.route('/feed', methods=['GET'])
def get_recommended_posts():
    username = request.args.get('username')
    category_id = request.args.get('category_id', None)
    mood = request.args.get('mood', None)

    try:
        # Fetch and preprocess data
        logging.info("Fetching and preprocessing data...")
        posts_data = fetch_all_data()
        posts_df = preprocess_data(posts_data)

        # Apply filtering for the user data
        user_data = posts_df[posts_df['username'] == username]
        if user_data.empty:
            return jsonify({"error": "User data not found"}), 404

        # Generate recommendations
        recommendations = hybrid_model(user_data, posts_df)

        # Filter recommendations based on category and mood if provided
        if category_id:
            recommendations = recommendations[recommendations['category_id'] == int(category_id)]
        if mood:
            recommendations = recommendations[recommendations['mood'] == mood]

        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        logging.error(f"Error generating feed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
