from pathlib import Path
from typing import Any, Dict, Optional

import jinja2
import yaml


class AgentConfigManager:
    """Manages agent configurations and instructions."""

    def __init__(
        self, config_dir: str, template_dir: str, environment: str = "production"
    ):
        """Initialize the config manager.

        Args:
            config_dir: Directory containing agent configuration files
            template_dir: Directory containing instruction templates
            environment: Current environment (development, staging, production)
        """
        self.config_dir = config_dir
        self.template_dir = template_dir
        self.environment = environment
        self.jinja_env = self._setup_jinja_environment()

        # Load app config for variable injection
        try:
            from config.app_config_loader import load_app_config

            self.app_config = load_app_config(environment)
        except ImportError:
            self.app_config = None

    def _setup_jinja_environment(self) -> jinja2.Environment:
        """Set up the Jinja2 environment with template loader."""
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def load_agent_config(self, agent_id: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file.

        Args:
            agent_id: Identifier for the agent

        Returns:
            Dictionary containing agent configuration

        Raises:
            FileNotFoundError: If agent configuration file doesn't exist
        """
        config_path = Path(self.config_dir) / f"{agent_id}.yaml"

        if not config_path.exists():
            raise FileNotFoundError(f"Agent configuration not found: {config_path}")

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        # Add environment-specific overrides if they exist
        env_config_path = Path(self.config_dir) / f"{agent_id}.{self.environment}.yaml"
        if env_config_path.exists():
            with open(env_config_path, "r") as f:
                env_config = yaml.safe_load(f)
                config.update(env_config)

        return config

    def render_instruction(self, template_path: str, variables: Dict[str, Any]) -> str:
        """Render an instruction template with provided variables.

        Args:
            template_path: Path to the template file (relative to template_dir)
            variables: Dictionary of variables to use in template rendering

        Returns:
            Rendered instruction string
        """
        template = self.jinja_env.get_template(template_path)

        # Add environment as a variable
        context = {"environment": self.environment, **variables}

        return template.render(**context)

    def get_agent_instruction(
        self, agent_id: str, state_variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """Get the fully rendered instruction for an agent.

        Args:
            agent_id: Identifier for the agent
            state_variables: Variables from the session state to include in rendering

        Returns:
            Fully rendered instruction string
        """
        config = self.load_agent_config(agent_id)

        # Start with template variables from config
        variables = config.get("variables", {})

        # Inject values from app config if available
        if self.app_config:
            course_config = self.app_config.courses.get("ai_marketing_platform", {})
            if course_config:
                variables.update(
                    {
                        "course_price": course_config.get(
                            "price", variables.get("course_price")
                        ),
                        "course_duration": f"{course_config.get('duration_weeks', 6)} weeks",
                        "refund_policy_days": course_config.get(
                            "refund_policy_days", variables.get("refund_policy_days")
                        ),
                        "course_name": course_config.get(
                            "name", "AI Marketing Platform"
                        ),
                    }
                )

        # Add state variables (these take precedence)
        if state_variables:
            variables.update(state_variables)

        return self.render_instruction(config["instruction_template"], variables)
