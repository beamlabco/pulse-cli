import click
from tabulate import tabulate

@click.group()
def attendance():
    """Manage attendances for admin"""
    pass

@attendance.command()
def checkin():
    """Attendance checkin"""
    from pulse.utils.api import post
    from pulse.utils.token import validate_token
    token = validate_token()
    data = post("user/attendance/check-in", headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, dict):
        clean_data = [
            {key: (value if value is not None else "N/A") for key, value in attendance.items()} for attendance in [data["attendance"]]
        ]
        click.echo(tabulate(clean_data, headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")

@attendance.command()
def checkout():
    """Attendance checkout"""
    from pulse.utils.api import patch
    from pulse.utils.token import validate_token
    token = validate_token()
    data = patch("user/attendance/check-out", headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, dict):
        clean_data = [
            {key: (value if value is not None else "N/A") for key, value in attendance.items()} for attendance in [data["attendance"]]
        ]
        click.echo(tabulate(clean_data, headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")

@attendance.command()
@click.option("--date", required=True, help="Date in YYYY-MM-DD format")
def find(date):
    """Get attendance by date"""
    from pulse.utils.api import get
    from pulse.utils.token import validate_token
    token = validate_token()
    data = get(f"user/attendance?date={date}", headers={"Authorization": f"Bearer {token}"})
    if isinstance(data, dict):
        if (data["attendance"] == None or len(data["attendance"]) == 0):
            click.echo("No attendance found for the given date.")
            return
        clean_data = [
            {key: (value if value is not None else "N/A") for key, value in attendance.items()} for attendance in [data["attendance"]]
        ]
        click.echo(tabulate(clean_data, headers="keys", tablefmt="grid"))
    else:
        click.echo(f"❌ Error: {data}")
