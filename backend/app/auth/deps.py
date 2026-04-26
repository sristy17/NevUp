from fastapi import Depends, Request
from app.auth.jwt import verify_token

def get_current_user(request: Request):
    return verify_token(request)