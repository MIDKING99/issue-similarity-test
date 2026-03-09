import jwt
import time
import requests

APP_ID = "2956914"

with open("private-key.pem", "r") as f:
    PRIVATE_KEY = f.read()


def generate_jwt():

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "iss": APP_ID
    }

    encoded_jwt = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

    return encoded_jwt


def get_installation_token():

    jwt_token = generate_jwt()

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github+json"
    }

    # 获取 installation id
    response = requests.get(
        "https://api.github.com/app/installations",
        headers=headers
    )

    installation_id = response.json()[0]["id"]

    # 创建 token
    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers=headers
    )

    return response.json()["token"]