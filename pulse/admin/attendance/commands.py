import click
from tabulate import tabulate

@click.group()
def attendance():
    """Manage attendances"""
    pass

@attendance.command()
@click.option("--user", required=True, help="User ID")
def list(user):
    """Get attendance by date"""
    from pulse.utils.api import get
    from pulse.utils.token import validate_token
    token = validate_token()
    data = get(f"admin/attendance?userId={user}", headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, dict):
        if (data["attendances"] == None or len(data["attendances"]) == 0):
            click.echo("No attendances found for the given user.")
            return
        clean_data = [
            {key: (value if value is not None else "N/A") for key, value in attendance.items()} for attendance in data["attendances"]
        ]
        click.echo(tabulate(clean_data, headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")
