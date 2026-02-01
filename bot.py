import os
import random
import time
import tweepy
from dotenv import load_dotenv
from google import genai

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# GEMINI CLIENT
# =========================
ai = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =========================
# TWITTER CLIENT
# =========================
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# =========================
# CONFIG
# =========================
topics = [
    "AI tools",
    "coding productivity",
    "tech careers",
    "future technology",
    "developer mindset"
]

fallback_tweets = [
    "Build skills daily. Tech rewards consistency 🚀 #Tech",
    "Small progress daily = big career growth 💡 #Coding",
    "Focus on fundamentals. Tools change, basics stay. #Developers"
]

# =========================
# VIRAL TWEET GENERATOR
# =========================
def generate_tweet():
    topic = random.choice(topics)

    prompt = f"""
Write a viral tweet about {topic}.

Rules:
- Under 200 characters
- 1 strong hook
- 1 actionable tip
- 1 trending hashtag
- Motivational tone
- End with a question
"""

    try:
        res = ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        tweet = res.text.strip()

        if len(tweet) > 240:
            return random.choice(fallback_tweets)

        return tweet

    except Exception as e:
        print("Gemini failed:", e)
        return random.choice(fallback_tweets)

# =========================
# POST TWEET
# =========================
def post_tweet():
    print("Posting tweet...")
    tweet = generate_tweet()

    try:
        client.create_tweet(text=tweet)
        print("Tweeted:", tweet)

    except tweepy.Forbidden:
        print("Duplicate tweet detected. Using fallback.")
        tweet = random.choice(fallback_tweets)
        client.create_tweet(text=tweet)

    except Exception as e:
        print("Twitter error:", e)

# =========================
# TONE DETECTION
# =========================
def detect_tone(text):
    text = text.lower()

    if any(x in text for x in ["bad","stupid","hate","worst"]):
        return "roast"
    elif any(x in text for x in ["love","great","awesome"]):
        return "positive"
    else:
        return "neutral"

# =========================
# AUTO REPLY (SAFE MODE)
# =========================
def auto_reply():
    print("Checking mentions...")

    try:
        me = client.get_me().data.id

        mentions = client.get_users_mentions(
            id=me,
            max_results=5
        )

        if not mentions.data:
            print("No mentions.")
            return

        for m in mentions.data:
            tone = detect_tone(m.text)

            if tone == "roast":
                reply = "Haha 😄 I'll try to improve. Appreciate the feedback!"
            elif tone == "positive":
                reply = "Glad you liked it! 🚀 More value coming!"
            else:
                reply = "Thanks for engaging! 🙌"

            client.create_tweet(
                text=reply,
                in_reply_to_tweet_id=m.id
            )

            print("Replied to:", m.id)

    except tweepy.Unauthorized:
        print("Mentions access not allowed on your X plan — skipping auto-reply.")

    except Exception as e:
        print("Auto-reply error:", e)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("Bot starting...")

    post_tweet()

    # OPTIONAL (safe)
    auto_reply()

    print("Bot finished.")
