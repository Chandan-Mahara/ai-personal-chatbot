from dotenv import load_dotenv
from openai import OpenAI
import os

# -------------------- LOAD ENV --------------------
load_dotenv(override=True)

# -------------------- VALIDATE ENV --------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is missing in .env")

# -------------------- OPENAI CLIENT --------------------
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize OpenAI client: {e}")

# -------------------- PUSHOVER CONFIG --------------------
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

def is_pushover_configured():
    return bool(PUSHOVER_USER and PUSHOVER_TOKEN)