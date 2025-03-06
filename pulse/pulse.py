import os
import click
import webbrowser
from tabulate import tabulate
from http.server import BaseHTTPRequestHandler, HTTPServer
from pulse.utils.token import save_token, TOKEN_FILE
from pulse.utils.api import post, API_BASE_URL

# commands based on user roles
# admin commands
from pulse.admin.commands import admin
# user commands
from pulse.attendance.commands import attendance

class OAuthHandler(BaseHTTPRequestHandler):
    """Handles OAuth callback to receive JWT token."""
    def do_GET(self):
        if "/oauth-success" in self.path:
            token = self.path.split("token=")[-1]
            save_token(token)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Login Successful! You can close this tab.</h1>")
        else:
            self.send_response(404)
        self.end_headers()

@click.group()
def cli():
    """CLI tool for authentication and API requests."""
    pass

@click.command()
@click.option("--name", required=True, help="Name of the organization.")
@click.option("--email", required=True, help="Email for the primary admin.")
@click.option("--phone", required=True, help="Phone for the primary admin.")
@click.option("--address", required=True, help="Address of the organization.")
@click.option("--domain", required=True, help="Default whitelisted domain.")
def setup(name, email, phone, address, domain):
    """Login using root admin."""    
    body = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "domain": domain
    }
    data = post("auth/setup", headers={}, data=body)
    if isinstance(data, dict):
        if isinstance(data, dict):
            click.echo("Organization:")
            click.echo(tabulate([data["organization"]], headers="keys", tablefmt="grid"))
            click.echo("Organization Domain:")
            click.echo(tabulate([data["domain"]], headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")

@click.command()
def login():
    """Login using Google OAuth (opens browser)."""
    click.echo("Opening browser for Google login...")
    click.echo("If the browser does not open, visit the following URL:")
    click.echo(f"{API_BASE_URL}/public/auth/google")
    webbrowser.open(f"{API_BASE_URL}/public/auth/google")

    click.echo("Waiting for authentication...")
    server = HTTPServer(("localhost", 5000), OAuthHandler)
    server.handle_request()
    click.echo("Authentication complete!")

@click.command()
def logout():
    """Logout and remove stored token."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        click.echo("Logged out successfully ✅")
    else:
        click.echo("You are not logged in.")

# Register CLI commands
cli.add_command(setup)
cli.add_command(login)
cli.add_command(logout)

cli.add_command(attendance)
cli.add_command(admin)

if __name__ == "__main__":
    cli()