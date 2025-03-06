import click
from pulse.admin.attendance.commands import attendance
from pulse.admin.user.commands import user

@click.group()
def admin():
    """Admin commands"""
    pass

admin.add_command(user)
admin.add_command(attendance)
