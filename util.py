from google.cloud import secretmanager
import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def get_secret(resource_id: str) -> str:
    """
    Retrieve a secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"{resource_id}/versions/latest"

    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")

    return secret_payload


def get_user_info(access_token):
    """Given a Google access_token, retrieve user info from Google API.
    """
    try:
        headers = {
            "Authorization": "Bearer " + access_token
        }
        res = requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
                        headers=headers)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        logger.error(e)
        return None
