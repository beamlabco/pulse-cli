import os
import json
import click

TOKEN_FILE = os.path.expanduser("~/.pulse.json")

def save_token(token):
    """Save JWT token locally."""
    with open(TOKEN_FILE, "w") as f:
        json.dump({"token": token}, f)

def load_token():
    """Load JWT token from local storage."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f).get("token")
    return None

def validate_token():
    token = load_token()
    if not token:
        click.echo("You are not logged in. Use `pulse login`.")
        return
    return token
    