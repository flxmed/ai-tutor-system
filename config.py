import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PRIMARY_MODEL = "llama-3.3-70b-versatile"   # explanations, curriculum, hard reasoning
FAST_MODEL = "llama-3.1-8b-instant"         # simple routing, cheap small tasks
EVAL_MODEL = "llama-3.3-70b-versatile"      # evaluation should be high quality, not weak


CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 6

EXPLANATION_TEMPERATURE = 0.4
QUESTION_TEMPERATURE = 0.5
EVAL_TEMPERATURE = 0.0

MAX_EXPLANATION_TOKENS = 1200
MAX_QUESTION_TOKENS = 700
MAX_EVAL_TOKENS = 500

PASS_SCORE = 0.80
REVIEW_SCORE = 0.55
MAX_RETRIES_PER_TOPIC = 3