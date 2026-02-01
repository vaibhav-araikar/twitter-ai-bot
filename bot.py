import os
import random
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

# ---------- LOAD ENV ----------
load_dotenv()

# ---------- GEMINI ----------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- TWITTER CLIENT ----------
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
)

me = client.get_me().data
BOT_USER_ID = me.id

print("Logged in as:", me.username)

# ---------- VIRAL TOPICS ----------
topics = [
    "AI tools",
    "coding productivity",
    "tech careers",
    "developer mindset",
    "future of AI",
]

fallback_tweets = [
    "Consistency beats talent in tech 🚀 #AI",
    "Your future salary depends on your current skills 💡 #Coding",
    "Learn daily. Tech rewards action. #Developers",
]

# ---------- GENERATE VIRAL TWEET ----------
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
        r = model.generate_content(prompt)
        return r.text.strip()
    except:
        return random.choice(fallback_tweets)

# ---------- POST TWEET ----------
def post_tweet():
    tweet = generate_tweet()

    try:
        client.create_tweet(text=tweet)
        print("Tweeted:", tweet)
    except Exception as e:
        print("Tweet failed:", e)

# ---------- AI REPLY ----------
def ai_reply(text):
    prompt = f"""
Reply to this tweet in a smart, short, engaging way.

Tweet:
"{text}"

Rules:
- Detect tone
- Friendly or witty
- Under 120 characters
"""

    try:
        r = model.generate_content(prompt)
        return r.text.strip()
    except:
        return None

# ---------- AUTO ENGAGEMENT ----------
def engage_mentions():
    mentions = client.get_users_mentions(
        id=BOT_USER_ID,
        max_results=5
    )

    if not mentions.data:
        print("No mentions.")
        return

    for tweet in mentions.data:

        if tweet.author_id == BOT_USER_ID:
            continue

        text = tweet.text.lower()

        reply = ai_reply(text)

        if not reply:
            reply = random.choice([
                "Appreciate the input! 🚀",
                "Interesting take 😄",
                "Love the discussion 🔥"
            ])

        # Reply
        try:
            client.create_tweet(
                text=reply,
                in_reply_to_tweet_id=tweet.id
            )
            print("Replied:", reply)
        except:
            pass

        # Like
        try:
            client.like(tweet.id)
            print("Liked mention")
        except:
            pass

        # Follow author
        try:
            client.follow_user(tweet.author_id)
            print("Followed user")
        except:
            pass

# ---------- MAIN ----------
if __name__ == "__main__":
    print("GOD MODE V3 RUNNING")

    post_tweet()
    engage_mentions()

    print("Done.")
