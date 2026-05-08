from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
import os

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_API_URL = os.getenv("BASE_API_URL")

ACCESS_CODE = os.getenv("ACCESS_CODE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

TOKEN = None


def get_token():

    global TOKEN

    url = f"{BASE_API_URL}/register"

    payload = {
        "accessCode": ACCESS_CODE,
        "clientID": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }

    response = requests.post(url, json=payload)

    data = response.json()

    TOKEN = data["token"]

    return TOKEN


def get_headers():

    global TOKEN

    if TOKEN is None:
        get_token()

    return {
        "Authorization": f"Bearer {TOKEN}"
    }

@app.get("/notifications")
def notifications():
    headers = get_headers()

    response = requests.get(
        f"{BASE_API_URL}/notifications",
        headers=headers
    )
    
    notifications = response.json()
    return notifications