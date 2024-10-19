import jwt
import time
from config import TOKEN_SECRET

class TokenManager:
    @staticmethod
    def generate_token(user_id):
        """Generates a token for secure access."""
        payload = {"user_id": user_id, "exp": time.time() + 600}
        return jwt.encode(payload, TOKEN_SECRET, algorithm="HS256")

    @staticmethod
    def verify_token(token):
        """Verifies a token and returns the user ID."""
        try:
            decoded = jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return None
