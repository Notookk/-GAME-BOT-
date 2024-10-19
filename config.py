import os
from dotenv import load_dotenv

# Load environment variables from .env (optional but recommended)
load_dotenv()

# Telegram Bot Token (Store this securely in a .env file)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Constants
MIN_PLAYERS = 6  # Minimum number of players to start the game
GAME_TIMEOUT = 300  # Timeout (in seconds) for voting and decision-making
ALLOWED_TOPICS = [
    "SPORTS", 
    "ANIMALS/PLANTS/NATURE", 
    "FOOD", 
    "CHARACTER/PROFESSION", 
    "RANDOM"
]

# Token Manager Settings
TOKEN_SECRET = os.getenv("TOKEN_SECRET", "your-secret-key")  # For generating secure tokens
TOKEN_EXPIRATION = 600  # Expiration time for tokens in seconds

# Debug Mode (Useful for local testing)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")

# Utility: Helper function to validate the config settings
def validate_config():
    if not BOT_TOKEN:
        raise ValueError("Bot token is missing! Please set BOT_TOKEN in the environment variables.")
