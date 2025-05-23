from fabric import Connection, task
from fabric.transfer import Transfer
from invoke import run
from termcolor import cprint

APP_NAME = "klimaathelpdeskfabfile"


def get_db_dump_for_env(username):
    """Dump the database of the specified environment, and download it.

    Returns the filename.
    """
    connection = Connection(f"admin@container-db01.fourdigits.nl")

    filename = f"{username}.psql"

    # To make this run without a password prompt, place a .pgpass file
    # in the user's home directory.
    print(f"Dumping database...")
    connection.run(
        f"pg_dump --host container-db01 --port 5432 {username} --username {username} --clean --no-owner --no-privileges  > {filename}"
    )

    print(f"Dumped database to {filename} on server, downloading...")
    transfer = Transfer(connection)
    transfer.get(filename)
    connection.run(f"rm {filename}")
    print(f"Downloaded and removed {filename}")
    return filename


def load_database_for_env(username):
    """Load a database from an environment locally."""
    filename = get_db_dump_for_env(username)

    # Replace local db with the downloaded one
    run(f"dropdb {APP_NAME}")
    run(f"createdb {APP_NAME}")
    run(f"psql {APP_NAME} < {filename}")
    print(f"Replaced local db {APP_NAME} with the one from {filename}")
    run(f"rm {filename}")
    print(f"Removed {filename}")


@task
def get_data(context, environment):
    """Get database."""
    load_database_for_env(f"{APP_NAME}_{environment}")


@task
def deploy(context, environment, ref=None):
    if not ref and environment == "test":
        # Get latest short commit hash
        ref = run("git rev-parse --short HEAD").stdout.strip()
    elif not ref:
        # Get latest tag
        ref = run("git describe --tags --abbrev=0").stdout.strip()

    cprint(f"🚀 Deploying {ref} to {environment} environment...", "green")
    run(f"fourdigits exonet deploy {environment} {ref}")
