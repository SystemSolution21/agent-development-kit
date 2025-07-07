from pathlib import Path

# Create logs directory
current_dir: Path = Path(__file__).parent.parent.resolve()
print(current_dir)
logs_dir: Path = current_dir / "logs"
print(logs_dir)
logs_dir.mkdir(exist_ok=True)

# Configure log file
log_file: Path = logs_dir / "adk_application.log"
print(log_file)
