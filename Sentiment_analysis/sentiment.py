import pandas as pd
from transformers import pipeline

# Create a sentiment analysis pipeline using the "finiteautomata/bertweet-base-sentiment-analysis" model
sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

# Load the customer reviews from a CSV file (assuming the CSV has a 'review_text' column)
csv_file_path = "sentiment_nt.csv"
df = pd.read_csv(csv_file_path)

# Check if the 'sentiment' column exists; create it if not
if 'sentiment' not in df:
    df['sentiment'] = ""

# Analyze sentiment for each review and populate the 'sentiment' column
for index, row in df.iterrows():
    review_text = row['review_text']

    # Split the review text into smaller segments
    segments = [review_text[i:i+128] for i in range(0, len(review_text), 128)]

    sentiment_labels = []

    print(f"Processing review {index + 1} out of {len(df)}")

    for segment in segments:
        result = sentiment_pipeline(segment)
        if result:
            sentiment_label = result[0]['label']
            sentiment_labels.append(sentiment_label)
        print(f"Processed {len(sentiment_labels)} segments out of {len(segments)} segments.")

    # Combine sentiment labels from segments into a single label for the review
    final_sentiment_label = " ".join(sentiment_labels)
    df.at[index, 'sentiment'] = final_sentiment_label

# Save the updated DataFrame to a new CSV file with an absolute file path
output_csv_file = "customer_reviews_with_sentiment.csv"
df.to_csv(output_csv_file, index=False)
