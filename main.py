from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import jwt
import datetime

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from util import get_secret, get_user_info

app = FastAPI()

# Allow CORS for your frontend (localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig()
logger = logging.getLogger(__name__)

# Secret key used for signing the JWT
SECRET_KEY = get_secret(
    "projects/745799261495/secrets/SECURITY_MANAGER_SECRET_KEY")


def generate_jwt(username: str, email: str, expiration_minutes: int = 120) -> str:
    """
    Generate a JWT token with the given username and email.
    """
    payload = {
        "username": username,
        "email": email,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expiration_minutes),
        "iat": datetime.datetime.now(datetime.UTC),  # Issued at time
        "iss": "SecurityManager",  # Issuer
    }

    # Encode the payload using the secret key
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


@app.get("/exchange_token_with_google_id")
async def exchange_token_with_google_id(request: Request, client_id: str):
    """Given an ID_TOKEN from google login and CLIENT_ID, generate a security token
    with scopes along with user info verified by google.
    """
    try:
        token = request.headers.get("Authorization").split()[1]
    except Exception as e:
        logger.error(e)
        return {"error": "Authorization header missing"}, 401

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        email = idinfo['email']
        username = idinfo['name']
    except ValueError:
        # Invalid token
        logger.error("Invalid token")
        return {"error": "Invalid token"}, 401
    
    # generate security token
    jwt_token = generate_jwt(username, email)

    return {"userinfo": idinfo, "token": jwt_token}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
