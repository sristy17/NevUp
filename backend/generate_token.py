import os
import time
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

payload = {
    "sub": "f412f236-4edc-47a2-8f54-8763a6ed2ce8",
    "iat": int(time.time()),
    "exp": int(time.time()) + 86400,
    "role": "trader"
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(token)