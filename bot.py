import os
import random
import time
import tweepy
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

# ---------- LOAD ENV ----------
load_dotenv()

print("Bot starting...")

# ---------- GEMINI CLIENT ----------
client_ai = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- TWITTER CLIENT ----------
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

    try:
        print("Generating tweet with Gemini...")
        response = client_ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        tweet = response.text.strip()
        print("AI tweet:", tweet)
        return tweet

    except ClientError as e:
        print("Gemini failed:", e)
        return random.choice(fallback_tweets)


# ---------- POST TWEET ----------
def post_tweet():
    try:
        tweet = generate_tweet()

        print("Posting tweet...")
        client.create_tweet(text=tweet)

        print("Tweet posted successfully!")
        print("Tweet content:", tweet)

    except Exception as e:
        print("Twitter error:", e)


# ---------- MAIN ----------
if __name__ == "__main__":
    post_tweet()
    print("Bot finished.")
