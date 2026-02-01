import os
import json
import random
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# ======================
# GEMINI SETUP
# ======================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ======================
# TWITTER CLIENT
# ======================
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET"),
    wait_on_rate_limit=True
)

# ======================
# STORAGE
# ======================
DATA_FILE="data.json"

if not os.path.exists(DATA_FILE):
    json.dump({"tweets":[]},open(DATA_FILE,"w"))

def load_data():
    return json.load(open(DATA_FILE))

def save_data(d):
    json.dump(d,open(DATA_FILE,"w"))

# ======================
# FALLBACK CONTENT
# ======================
hooks=[
"Most devs ignore this:",
"Unpopular tech truth:",
"If you want a tech career:",
"90% of coders do this wrong:"
]

tips=[
"Build projects, not just courses.",
"Master one skill deeply.",
"Consistency beats motivation.",
"Portfolio > certificates."
]

hashtags=["#Coding","#Developers","#Tech","#AI"]

# ======================
# GEMINI GENERATOR
# ======================
def ai_tweet():
    prompt="""
Write a professional viral tech tweet.

Rules:
- under 180 chars
- helpful insight
- 1 hashtag
- human tone
"""

    try:
        r=model.generate_content(prompt)
        return r.text.strip()

    except:
        return None

# ======================
# LOCAL FALLBACK
# ======================
def local_tweet():
    return f"{random.choice(hooks)} {random.choice(tips)} {random.choice(hashtags)}"

# ======================
# GENERATE TWEET
# ======================
def generate_tweet():
    t=ai_tweet()

    if not t:
        t=local_tweet()

    return t

# ======================
# POST THREAD
# ======================
def post_thread():
    print("Posting thread...")

    main=generate_tweet()

    t=client.create_tweet(text=main,user_auth=True)
    tid=t.data["id"]

    replies=[
    "Skill > hype.",
    "Deep work creates growth.",
    "Small progress compounds.",
    "What do you think?"
    ]

    last=tid
    for r in replies:
        tw=client.create_tweet(
            text=r,
            in_reply_to_tweet_id=last,
            user_auth=True
        )
        last=tw.data["id"]

    data=load_data()
    data["tweets"].append({
        "id":tid,
        "text":main,
        "likes":0,
        "retweets":0
    })
    save_data(data)

# ======================
# ANALYTICS
# ======================
def update_metrics():
    data=load_data()

    for t in data["tweets"]:
        try:
            r=client.get_tweet(
                t["id"],
                tweet_fields=["public_metrics"]
            )
            m=r.data.public_metrics
            t["likes"]=m["like_count"]
            t["retweets"]=m["retweet_count"]
        except:
            pass

    save_data(data)

# ======================
# MAIN
# ======================
if __name__=="__main__":
    print("SMART BOT RUNNING")

    update_metrics()
    post_thread()

    print("DONE")
