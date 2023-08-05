import click

from cricket_cookie.login.login import lightning_login


@click.group()
def main():
    pass


@main.command()
@click.option('--username', type=str, help='Username used in Grid')
@click.option('--key', type=str, help='API Key from Grid')
def login(username, key):
    """Authorize the CLI to access Grid AI resources for a particular user.
    If no username or key is provided, the CLI will prompt for them. After
    providing your username, a web browser will open to your account settings
    page where your API key can be found.
    """

    try:
        status = lightning_login(username=username, api_key=key)
    except ConnectionRefusedError:  # only relevant until we have gQL
        raise click.ClickException('Invalid username or API key')
    except Exception as e:
        raise click.ClickException(str(e))
    if status:
        click.echo('Login successful. Welcome to the lightning cloud.')
