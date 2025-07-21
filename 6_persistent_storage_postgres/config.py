import configparser
import os
from pathlib import Path

# Create a parser
config = configparser.ConfigParser()

# Get the directory of the current script to locate the config file
_current_dir: Path = Path(__file__).parent.resolve()
_config_file_path: Path = _current_dir / "app_config.ini"

# Read the config file
if not _config_file_path.exists():
    raise FileNotFoundError(f"Configuration file not found at {_config_file_path}")

config.read(filenames=_config_file_path)

# Application constants from the [Application] section
APP_NAME: str = config.get("Application", "AppName", fallback="Persistent Agent")

# --- Database Configuration ---
DB_TYPE: str = config.get("Database", "DB_TYPE", fallback="sqlite")

DB_URL: str

if DB_TYPE.lower() == "postgresql":
    # It's good practice to get credentials from environment variables in production.
    # Environment variables will override settings in app_config.ini.
    pg_host = os.environ.get(
        "PG_HOST", config.get("Database", "PG_HOST", fallback="localhost")
    )
    pg_port = os.environ.get(
        "PG_PORT", config.get("Database", "PG_PORT", fallback="5432")
    )
    pg_user = os.environ.get("PG_USER", config.get("Database", "PG_USER"))
    pg_password = os.environ.get("PG_PASSWORD", config.get("Database", "PG_PASSWORD"))
    pg_dbname = os.environ.get("PG_DBNAME", config.get("Database", "PG_DBNAME"))

    if not all([pg_user, pg_password, pg_dbname]):
        raise ValueError(
            "For PostgreSQL, PG_USER, PG_PASSWORD, and PG_DBNAME must be set "
            "in app_config.ini or as environment variables."
        )

    # The ADK's DatabaseSessionService uses peewee, which uses psycopg2 for postgresql:// URLs
    DB_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}"
else:
    # Fallback to SQLite
    DB_NAME: str = config.get("Database", "DatabaseName", fallback="my_agent_data.db")
    DB_URL = f"sqlite:///./{DB_NAME}"

# --- User Configuration ---
USER_ID: str = config.get("Database", "UserID", fallback="john_doe")
USER_NAME: str = config.get("Database", "UserName", fallback="John Doe")
