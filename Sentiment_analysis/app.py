from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from transformers import pipeline
import os

app = Flask(__name__)

# Create a sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

# Path to the original customer reviews database
reviews_db_file = 'customer_reviews.db'

# Path to the sentiment database (where you want to store sentiment data)
sentiment_db_file = 'sentiment_data.db'

def create_database_if_not_exists(db_file):
    # Create the database and reviews table if they don't exist
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found. Creating a new database.")
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE reviews (id INTEGER PRIMARY KEY, review_text TEXT, sentiment TEXT)''')
        conn.commit()
        conn.close()
    else:
        print(f"Using existing database file: {db_file}")

create_database_if_not_exists(reviews_db_file)
create_database_if_not_exists(sentiment_db_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    if request.method == 'POST':
        try:
            if not os.path.exists(reviews_db_file):
                return "Error: Original database file not found."

            if not os.path.exists(sentiment_db_file):
                return "Error: Sentiment database file not found."

            # Connect to the SQLite databases
            conn_reviews = sqlite3.connect(reviews_db_file)
            conn_sentiment = sqlite3.connect(sentiment_db_file)

            cursor_reviews = conn_reviews.cursor()
            cursor_sentiment = conn_sentiment.cursor()

            # Fetch a review from the original database
            cursor_reviews.execute('SELECT id, review_text FROM reviews WHERE sentiment IS NULL LIMIT 1')
            row = cursor_reviews.fetchone()

            if row:
                review_id, review_text = row
                result = sentiment_pipeline(review_text)

                if result:
                    sentiment_label = result[0]['label']

                    # Update the original database with sentiment data
                    cursor_reviews.execute('UPDATE reviews SET sentiment = ? WHERE id = ?', (sentiment_label, review_id))
                    conn_reviews.commit()

                    # Insert sentiment data into the sentiment database, including review text
                    cursor_sentiment.execute('INSERT INTO sentiment_data (review_id, review_text, sentiment_label) VALUES (?, ?, ?)', (review_id, review_text, sentiment_label))
                    conn_sentiment.commit()

            return redirect(url_for('index'))

        except Exception as e:
            return str(e)

        finally:
            conn_reviews.close()
            conn_sentiment.close()

if __name__ == '__main__':
    app.run(debug=True)
