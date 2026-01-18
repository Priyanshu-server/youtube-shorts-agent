from src.agents.simple_react_agent import get_agent
from src.utils.logging import configure_logging, get_logger, bind_context
from dotenv import load_dotenv
from settings import config

# Loading environment variables from .env file
load_dotenv()

# Configure logging for environment
configure_logging(enable_console=True)
bind_context(service=config.service_name, request_id=f"{config.env}-run")
log = get_logger(config.logger_name)


# Main function
def main() -> None:
    agent = get_agent(
        agent_name="TestAgent",
        model_parent="openai",
        model_name="gpt-4o-mini",
        model_args={},
        model_kwargs={"temperature": 0.7},
        metadata={"purpose": "testing"},
    )
    log.info(f"agent created {agent.agent_name}")
    log.info(f"agent model ready {agent.model.model_name}")


if __name__ == "__main__":
    main()
