import os
import random
import time
import tweepy
from dotenv import load_dotenv
from datetime import datetime

# =========================
# LOAD ENV
# =========================
load_dotenv()

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
# LOCAL VIRAL GENERATOR
# (No AI quota needed)
# =========================

hooks = [
    "Most developers ignore this:",
    "Nobody tells you this in tech:",
    "Want to grow faster in tech?",
    "Hard truth for developers:",
]

tips = [
    "Code daily for 30 mins.",
    "Build projects, not just courses.",
    "Master one skill at a time.",
    "Focus on fundamentals first.",
]

hashtags = [
    "#Coding",
    "#Developers",
    "#TechTips",
    "#100DaysOfCode",
]

questions = [
    "Agree?",
    "Your thoughts?",
    "Do you do this?",
    "What's your experience?",
]

# =========================
# GENERATE UNIQUE TWEET
# =========================
def generate_tweet():
    tweet = f"{random.choice(hooks)} {random.choice(tips)} {random.choice(hashtags)} {random.choice(questions)}"

    # Make it UNIQUE always
    unique_id = datetime.utcnow().strftime("%H%M%S")

    return f"{tweet} [{unique_id}]"

# =========================
# POST TWEET SAFE
# =========================
def post_tweet():
    print("Posting tweet...")

    for attempt in range(3):
        tweet = generate_tweet()

        try:
            client.create_tweet(text=tweet)
            print("Tweeted:", tweet)
            return

        except tweepy.Forbidden:
            print("Duplicate detected, retrying...")
            time.sleep(2)

        except Exception as e:
            print("Twitter error:", e)
            return

    print("Failed after retries.")

# =========================
# SAFE AUTO-REPLY
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
            return

        for m in mentions.data:
            reply = random.choice([
                "Appreciate your reply 🙌",
                "Thanks for engaging 🚀",
                "Glad you joined the convo 😄",
            ])

            client.create_tweet(
                text=reply,
                in_reply_to_tweet_id=m.id
            )

            print("Replied to:", m.id)

    except:
        print("Auto-reply skipped (plan limitation).")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("Bot starting...")

    post_tweet()
    auto_reply()

    print("Bot finished.")
