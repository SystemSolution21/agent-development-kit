"""Application configuration loader."""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration using Pydantic BaseModel."""

    # App settings
    app_name: str = Field(..., description="Application name")
    app_description: str = Field(..., description="Application description")
    app_version: str = Field(..., description="Application version")

    # User settings
    default_user_id: str = Field(..., description="Default user ID")
    default_user_name: str = Field(..., description="Default user name")

    # Session settings
    session_service_type: str = Field(..., description="Type of session service")
    initial_state: Dict[str, Any] = Field(
        default_factory=dict, description="Initial session state"
    )

    # Environment settings
    environment: str = Field(..., description="Current environment")

    # Paths
    agents_config_dir: str = Field(..., description="Agents configuration directory")
    templates_dir: str = Field(..., description="Templates directory")

    # Course settings
    courses: Dict[str, Any] = Field(
        default_factory=dict, description="Course configuration"
    )

    class Config:
        """Pydantic configuration."""

        # Allow extra fields for flexibility
        extra = "allow"
        # Use enum values instead of enum objects
        use_enum_values = True


class AppConfigLoader:
    """Loads and manages application configuration."""

    def __init__(self, config_file_path: Optional[Union[str, Path]] = None):
        """Initialize the config loader.

        Args:
            config_file_path: Path to the config file. If None, uses default location.
        """
        if config_file_path is None:
            # Get the directory where this script is located
            script_dir = Path(__file__).parent
            config_file_path = script_dir / "app_config.yaml"

        self.config_file_path = Path(config_file_path)
        self._config_data = None

    def load_config(self, environment: Optional[str] = None) -> AppConfig:
        """Load configuration from file.

        Args:
            environment: Environment to load config for. If None, uses default.

        Returns:
            AppConfig instance with loaded configuration.
        """
        # Load base configuration
        with open(self.config_file_path, "r") as f:
            self._config_data = yaml.safe_load(f)

        # Determine environment
        if environment is None:
            environment = os.getenv(
                "ENVIRONMENT", self._config_data["environment"]["default"]
            )

        # Load environment-specific overrides if they exist
        env_config_path = self.config_file_path.with_suffix(f".{environment}.yaml")
        if env_config_path.exists():
            with open(env_config_path, "r") as f:
                env_config = yaml.safe_load(f)
                self._merge_configs(self._config_data, env_config)

        # Ensure environment is not None
        if environment is None:
            raise ValueError("Environment cannot be None")

        # Create AppConfig instance
        return AppConfig(
            app_name=self._config_data["app"]["name"],
            app_description=self._config_data["app"]["description"],
            app_version=self._config_data["app"]["version"],
            default_user_id=self._config_data["user"]["default_user_id"],
            default_user_name=self._config_data["user"]["default_user_name"],
            session_service_type=self._config_data["session"]["service_type"],
            initial_state=self._config_data["session"]["initial_state"],
            environment=environment,
            agents_config_dir=self._config_data["paths"]["agents_config_dir"],
            templates_dir=self._config_data["paths"]["templates_dir"],
            courses=self._config_data["courses"],
        )

    def _merge_configs(
        self, base_config: Dict[str, Any], env_config: Dict[str, Any]
    ) -> None:
        """Merge environment-specific config into base config.

        Args:
            base_config: Base configuration dictionary
            env_config: Environment-specific configuration dictionary
        """
        for key, value in env_config.items():
            if isinstance(value, dict) and key in base_config:
                self._merge_configs(base_config[key], value)
            else:
                base_config[key] = value


def load_app_config(environment: Optional[str] = None) -> AppConfig:
    """Convenience function to load application configuration.

    Args:
        environment: Environment to load config for.

    Returns:
        AppConfig instance with loaded configuration.
    """
    loader = AppConfigLoader()
    return loader.load_config(environment)
