import os
import random
import time
import tweepy
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# ---------- LOAD ENV ----------
load_dotenv()

# ---------- GEMINI CLIENT ----------
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- TWITTER V2 CLIENT ----------
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
)

# ---------- TOPICS ----------
topics = [
    "AI tools",
    "coding productivity",
    "tech careers",
    "developer mindset",
    "future tech",
]

fallback_tweets = [
    "Build skills daily. Tech rewards consistency 🚀 #Tech",
    "Small progress daily = big career growth 💡 #Coding",
    "Focus on fundamentals. Tools change, basics stay. #Developers",
]

# ---------- GENERATE TWEET ----------
def generate_tweet():
    topic = random.choice(topics)

    prompt = f"""
    One short tweet about {topic}.
    Under 200 characters.
    Include 1 hashtag.
    """

    for _ in range(2):
        try:
            response = client_ai.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
            )
            return response.text.strip()
        except ClientError:
            time.sleep(3)

    return random.choice(fallback_tweets)

# ---------- POST TWEET ----------
def post_tweet():
    tweet = generate_tweet()

    client.create_tweet(text=tweet)
    print("Tweeted:", tweet)

# ---------- MAIN ----------
if __name__ == "__main__":
    post_tweet()
