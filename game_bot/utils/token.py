import hashlib
import time

class TokenManager:
    def __init__(self, secret_key: str = "secret"):
        self.secret_key = secret_key

    def generate_token(self, chat_id: int) -> str:
        """Generates a token for a chat using its ID and the current timestamp."""
        data = f"{chat_id}-{int(time.time())}-{self.secret_key}"
        return hashlib.sha256(data.encode()).hexdigest()

    def verify_token(self, chat_id: int, token: str) -> bool:
        """Verifies if a token is valid for the given chat."""
        expected_token = self.generate_token(chat_id)
        return token == expected_token
