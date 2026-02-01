import os
import random
import json
import tweepy
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# =========================
# GEMINI SETUP
# =========================
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

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
# MEMORY (avoid repeats)
# =========================
MEMORY_FILE = "posted.json"

if not os.path.exists(MEMORY_FILE):
    json.dump([], open(MEMORY_FILE,"w"))

def load_memory():
    return json.load(open(MEMORY_FILE))

def save_memory(data):
    json.dump(data, open(MEMORY_FILE,"w"))

# =========================
# MASSIVE TECH NICHES
# =========================
topics = [
"AI tools","machine learning","deep learning","ChatGPT usage",
"coding careers","remote tech jobs","startup growth",
"SaaS building","developer productivity","programmer mindset",
"Web3","blockchain","crypto tech","tech salaries",
"learning to code","Python tips","JavaScript tips",
"software engineering","system design","open source",
"freelance tech","tech side hustles","automation",
"future of AI","AI replacing jobs","AI business ideas",
"data science","cloud computing","cybersecurity",
"tech interviews","resume tips for developers",
"coding bootcamps","self-taught developers",
"tech entrepreneurship","digital products",
"no-code tools","AI startups","productivity hacks"
]

# =========================
# GET SMART TOPIC
# =========================
def pick_topic():
    return random.choice(topics)

# =========================
# AI TWEET
# =========================
def ai_tweet():
    topic = pick_topic()

    prompt=f"""
Write a professional, insightful tweet about {topic}.

Rules:
- under 200 characters
- educational or motivational
- 1–2 relevant hashtags
- professional tone
- no emojis spam
- make it unique
"""

    try:
        r=model.generate_content(prompt)
        return r.text.strip()
    except:
        return None

# =========================
# FALLBACK
# =========================
fallback=[
"Consistency beats intensity in tech careers. #Developers",
"Strong fundamentals make great engineers. #Coding",
"Learning daily compounds over time. #Tech"
]

# =========================
# GENERATE UNIQUE TWEET
# =========================
def generate_tweet():
    memory = load_memory()

    for _ in range(3):
        tweet = ai_tweet()

        if not tweet:
            tweet = random.choice(fallback)

        if tweet not in memory:
            memory.append(tweet)

            if len(memory)>50:
                memory.pop(0)

            save_memory(memory)
            return tweet

    return random.choice(fallback)

# =========================
# POST
# =========================
def post_tweet():
    tweet=generate_tweet()

    try:
        client.create_tweet(text=tweet,user_auth=True)
        print("Tweeted:",tweet)

    except tweepy.Forbidden:
        print("Duplicate blocked — retrying")
        tweet=random.choice(fallback)
        client.create_tweet(text=tweet,user_auth=True)

# =========================
# MAIN
# =========================
if __name__=="__main__":
    print("PRO TECH BOT RUNNING")
    post_tweet()
