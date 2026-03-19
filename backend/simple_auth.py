#simple_auth.py
#Dead simple authentication

import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException

SECRET_KEY = "ssn"
ALGORITHM = "HS256"

# HARDCODED USER - change these
VALID_EMAIL = "sidnad@gmail.com"
VALID_PASSWORD = "1234"

#Creating simple JWT token
def create_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"sub": email, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

#Verifying token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

#Login logic
def login_simple(email: str, password: str):
    if email == VALID_EMAIL and password == VALID_PASSWORD:
        token = create_token(email)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Wrong email or password")