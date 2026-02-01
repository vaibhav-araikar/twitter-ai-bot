import os
import random
import json
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# GEMINI SAFE SETUP
# =========================
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

use_ai = False

if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        use_ai = True
        print("Gemini enabled")
    except:
        print("Gemini disabled")
        use_ai = False

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
# MEMORY (NO DUPLICATES)
# =========================
MEMORY_FILE="memory.json"

if not os.path.exists(MEMORY_FILE):
    json.dump([],open(MEMORY_FILE,"w"))

def load_memory():
    return json.load(open(MEMORY_FILE))

def save_memory(m):
    json.dump(m,open(MEMORY_FILE,"w"))

# =========================
# FALLBACK CONTENT
# =========================
hooks=[
"Most developers ignore this:",
"Unpopular tech truth:",
"If you want a tech career:",
"90% of coders do this wrong:"
]

tips=[
"Build projects, not just courses.",
"Master fundamentals deeply.",
"Consistency beats motivation.",
"Portfolio > certificates."
]

hashtags=["#Coding","#Developers","#Tech","#AI"]

fallback=[
f"{random.choice(hooks)} {random.choice(tips)} {random.choice(hashtags)}"
for _ in range(10)
]

# =========================
# AI GENERATOR
# =========================
topics=[
"AI tools","coding careers","developer productivity",
"tech salaries","learning to code","future of AI",
"remote tech jobs","startups","automation"
]

def ai_tweet():
    if not use_ai:
        return None

    topic=random.choice(topics)

    prompt=f"""
Write a professional tweet about {topic}.

Rules:
- under 300 chars
- helpful or motivational
- 2 hashtag
- professional and human tone
"""

    try:
        r=model.generate_content(prompt)
        return r.text.strip()
    except:
        print("Gemini quota/failure")
        return None

# =========================
# GENERATE TWEET
# =========================
def generate_tweet():
    memory=load_memory()

    for _ in range(5):
        tweet=ai_tweet()

        if not tweet:
            tweet=random.choice(fallback)

        if tweet not in memory:
            memory.append(tweet)

            if len(memory)>40:
                memory.pop(0)

            save_memory(memory)
            return tweet

    return random.choice(fallback)

# =========================
# POST
# =========================
def post():
    tweet=generate_tweet()

    try:
        client.create_tweet(text=tweet,user_auth=True)
        print("Tweeted:",tweet)

    except tweepy.Forbidden:
        print("Duplicate blocked")
    except Exception as e:
        print("Twitter error:",e)

# =========================
# MAIN
# =========================
if __name__=="__main__":
    print("STABLE AI BOT RUNNING")
    post()
