import configparser
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

# Configuration from the [Database] section
DB_NAME: str = config.get("Database", "DatabaseName", fallback="my_agent_data.db")
DB_URL: str = f"sqlite:///./{DB_NAME}"
USER_ID: str = config.get("Database", "UserID", fallback="john_doe")
USER_NAME: str = config.get("Database", "UserName", fallback="John Doe")
