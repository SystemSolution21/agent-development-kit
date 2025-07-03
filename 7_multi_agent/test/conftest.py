"""
Configuration file for pytest.
This file is automatically loaded by pytest.
"""

import sys
from pathlib import Path

# Add the parent directory to the path
parent_dir: Path = Path(__file__).parent.parent
sys.path.append(str(object=parent_dir))
