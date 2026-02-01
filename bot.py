import os
import random
import time
import tweepy
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv()

print("Bot starting...")

client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
)

topics = [
    "AI tools",
    "coding productivity",
    "tech careers",
    "developer mindset",
    "future tech",
]

fallback_tweets = [
    "Build skills daily. Tech rewards consistency 🚀",
    "Small progress daily = big career growth 💡",
    "Focus on fundamentals. Tools change, basics stay.",
]

def generate_tweet():
    topic = random.choice(topics)

    prompt = f"One short tweet about {topic}. Under 200 characters. 1 hashtag."

    try:
        response = client_ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        tweet = response.text.strip()

    except ClientError as e:
        print("Gemini failed:", e)
        tweet = random.choice(fallback_tweets)

    # Add randomness to avoid duplicates
    tweet += f" #{topic.replace(' ', '')}{random.randint(1,999)}"

    return tweet

def post_tweet():
    tweet = generate_tweet()

    try:
        client.create_tweet(text=tweet)
        print("Tweeted:", tweet)

    except Exception as e:
        print("Twitter error:", e)

if __name__ == "__main__":
    post_tweet()
    print("Bot finished.")