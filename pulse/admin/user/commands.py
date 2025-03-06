import click
from tabulate import tabulate

@click.group()
def user():
    """Manage users"""
    pass

@user.command()
def list():
    """List all users"""
    from pulse.utils.api import get
    from pulse.utils.token import validate_token
    token = validate_token()
    data = get("admin/user", headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, dict):
        click.echo(tabulate(data["users"], headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")
