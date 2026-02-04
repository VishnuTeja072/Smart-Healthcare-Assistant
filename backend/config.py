



import os
import logging
import redis
from dotenv import load_dotenv

# Optional imports (loaded lazily)

# Load .env variables (explicitly from backend folder)
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)
# logger may not be initialized yet depending on import order; avoid using it here
print(f"Loaded environment variables from {env_path}")

# 1. Initialize Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 2. Redis Connection with Error Handling
# We try to ping Redis; if it fails, we set cache to None so the app stays online
try:
    cache = redis.Redis(
        host=os.getenv("REDIS_HOST", "127.0.0.1"), 
        port=int(os.getenv("REDIS_PORT", 6379)), 
        db=0, 
        decode_responses=True, 
        socket_connect_timeout=2
    )
    # The .ping() is the critical part that checks the actual connection
    if cache.ping():
        logger.info("✅ Redis connected successfully")
except (redis.ConnectionError, redis.TimeoutError):
    logger.warning("⚠️ Redis not found or connection timed out. Running in 'Degraded Mode' (No Cache).")
    cache = None

# 3. Vertex AI / Gemini Setup (with fallback to Gemini API key)
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1") 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Prefer Vertex AI when Project ID is provided, otherwise try Gemini API key
model = None

if PROJECT_ID:
    try:
        # Import vertex libraries lazily so the app can run without them if not required
        import vertexai
        from vertexai.generative_models import GenerativeModel
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        # Using the flash model when running on Vertex
        model = GenerativeModel("gemini-2.0-flash")
        logger.info(f"🚀 Vertex AI Model initialized (Project: {PROJECT_ID})")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Vertex AI: {e}")
        model = None

# Fallback: use Google Generative API (Gemini) if user provided an API key
if model is None and GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        import asyncio

        genai.configure(api_key=GEMINI_API_KEY)

        # Shim to provide async generate_content_async compatible with existing code
        class GoogleGenModel:
            def __init__(self, candidates=None):
                # Try a list of candidate model names until one works
                self.candidates = candidates or [
                    'models/gemini-2.5-flash',
                    'models/gemini-2.0-flash',
                    'models/gemini-flash-latest',
                    'gemini-2.0-flash'
                ]
                self._model = None
                for name in self.candidates:
                    try:
                        self._name = name
                        self._model = genai.GenerativeModel(self._name)
                        logger.info(f"Selected Gemini model: {self._name}")
                        break
                    except Exception as e:
                        logger.debug(f"Model {name} not available: {e}")
                if not self._model:
                    raise RuntimeError("No supported Gemini model available for this API key")

            async def generate_content_async(self, prompt: str):
                # Run sync call in threadpool
                def _call():
                    return self._model.generate_content(prompt)

                resp = await asyncio.to_thread(_call)

                # The returned object can vary; prefer .text or first candidate
                text = getattr(resp, 'text', None)
                if not text:
                    # attempt to extract from candidates
                    try:
                        text = resp.candidates[0].output
                    except Exception:
                        text = str(resp)

                # Create a simple object with 'text' attribute to match existing usage
                class Resp:
                    def __init__(self, text):
                        self.text = text
                return Resp(text)

        try:
            model = GoogleGenModel()
            logger.info("🚀 Gemini API configured via GEMINI_API_KEY")
        except Exception as e:
            logger.error(f"❌ Failed to initialize any Gemini model: {e}")
            model = None
    except Exception as e:
        logger.error(f"❌ Failed to initialize Gemini via GEMINI_API_KEY: {e}")

if model is None:
    logger.warning("⚠️ No AI model configured. Behaviour will fall back to mock responses.")