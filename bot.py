import os
import random
import json
import time
import tweepy
from dotenv import load_dotenv
from google import genai

# =========================
# ENV
# =========================
load_dotenv()

# =========================
# GEMINI SETUP
# =========================
use_ai=False

if os.getenv("GEMINI_API_KEY"):
    try:
        ai=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        use_ai=True
        print("AI Enabled")
    except:
        use_ai=False

# =========================
# TWITTER CLIENT
# =========================
client=tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_SECRET")
)

# =========================
# COOLDOWN SYSTEM
# =========================
COOLDOWN="cooldown.txt"
LIMIT_FILE="limit.txt"

def limit_active():
    if not os.path.exists(LIMIT_FILE):
        return False
    last=float(open(LIMIT_FILE).read())
    return time.time()-last<12*60*60  # 12 hour sleep after limit

def activate_limit():
    open(LIMIT_FILE,"w").write(str(time.time()))

def can_post():
    if limit_active():
        print("Rate-limit sleep active. Skipping.")
        return False

    if not os.path.exists(COOLDOWN):
        return True
    last=float(open(COOLDOWN).read())
    return time.time()-last>3*60*60  # 3 hours

def update_cooldown():
    open(COOLDOWN,"w").write(str(time.time()))

# =========================
# MEMORY SYSTEM
# =========================
MEMORY="memory.json"

if not os.path.exists(MEMORY):
    json.dump([],open(MEMORY,"w"))

def load_mem():
    return json.load(open(MEMORY))

def save_mem(m):
    json.dump(m,open(MEMORY,"w"))

# =========================
# MASSIVE TOPIC LIST
# =========================
topics=[
"AI tools","ChatGPT","generative AI","AI automation",
"AI startups","AI in business","future of AI",
"AI careers","AI productivity","AI agents",
"Python tips","JavaScript","coding careers",
"learning to code","clean code","debugging",
"system design","open source","GitHub projects",
"remote tech jobs","tech salaries","developer resumes",
"freelance coding","tech interviews","side hustles",
"SaaS ideas","bootstrapping","MVP building",
"indie hacking","no-code tools","startup growth",
"deep work","focus habits","time management",
"learning faster","developer discipline",
"cloud computing","AWS","data science",
"data analytics","big data",
"cybersecurity","ethical hacking","privacy",
"blockchain","Web3","crypto tech",
"coding bootcamps","self-taught devs","learning hacks"
]

# =========================
# TWEET STYLES
# =========================
styles=[
"Write a motivational tweet about {topic} with one hashtag.",
"Write a practical tip about {topic} with one hashtag.",
"Write a myth vs truth tweet about {topic} with one hashtag.",
"Write a career advice tweet about {topic} with one hashtag.",
"Write a short insight about {topic} with one hashtag."
]

# =========================
# FALLBACK
# =========================
fallback=[
"Build skills daily. Tech rewards consistency. #Developers",
"Projects > certificates in tech careers. #Coding",
"Small progress daily creates big results. #Tech",
"Focus on fundamentals first. #AI"
]

# =========================
# AI GENERATOR
# =========================
def ai_tweet():
    if not use_ai:
        return None

    topic=random.choice(topics)
    style=random.choice(styles)
    prompt=style.format(topic=topic)

    try:
        r=ai.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return r.text.strip()
    except:
        return None

# =========================
# UNIQUE TWEET
# =========================
def generate_tweet():
    mem=load_mem()

    for _ in range(5):
        t=ai_tweet()
        if not t:
            t=random.choice(fallback)

        if t not in mem:
            mem.append(t)
            if len(mem)>80:
                mem.pop(0)
            save_mem(mem)
            return t

    return random.choice(fallback)

# =========================
# POST FUNCTION
# =========================
def post():
    if not can_post():
        print("Cooldown active. Skipping.")
        return

    tweet=generate_tweet()

    try:
        client.create_tweet(text=tweet,user_auth=True)
        update_cooldown()
        print("Tweeted:",tweet)

    except tweepy.TooManyRequests:
        print("Rate limit hit. Sleeping 12 hours.")
        activate_limit()

    except Exception as e:
        print("Error:",e)

# =========================
# MAIN
# =========================
if __name__=="__main__":
    print("ADVANCED TECH BOT RUNNING")
    post()
