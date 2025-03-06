import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("PULSE_URL")

def get(endpoint, headers={}):
    """Generic GET request"""
    response = requests.get(f"{API_BASE_URL}/{endpoint}", headers=headers)
    return response.json() if response.status_code == 200 else response.text

def post(endpoint, headers={}, data={}):
    """Generic POST request"""
    response = requests.post(f"{API_BASE_URL}/{endpoint}", headers=headers, data=data)
    return response.json() if response.status_code in [200, 201] else response.text

def patch(endpoint, headers={}, data={}):
    """Generic POST request"""
    response = requests.patch(f"{API_BASE_URL}/{endpoint}", headers=headers, data=data)
    return response.json() if response.status_code in [200, 201] else response.text