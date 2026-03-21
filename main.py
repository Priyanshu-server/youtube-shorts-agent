from dotenv import load_dotenv

from settings import config
from src.agents.html_poster_agent import get_html_poster_agent, invoke_html_poster_agent
from src.utils.logging import bind_context, configure_logging, get_logger

# Loading environment variables from .env file
load_dotenv()

# Configure logging for environment
configure_logging(enable_console=True)
bind_context(service=config.service_name, request_id=f"{config.env}-run")
log = get_logger(config.logger_name)


# Main function
def main() -> None:
    agent = get_html_poster_agent(
        agent_name="HTMLPosterAgent",
        model_parent="openai",
        model_name="gpt-4o-mini",
        model_args=None,
        model_kwargs={"temperature": 1},
        metadata={"purpose": "html_poster_generation"},
    )
    log.info(f"agent created {agent.agent_name}")
    log.info(f"agent model ready {agent.model.model_name}")

    output = invoke_html_poster_agent(
        agent,
        "Create a social media HTML poster about cows. Use modern visual design and inline CSS.",
        output_path="outputs/html_poster_cow.html",
    )
    print(f"Output : {output}")


if __name__ == "__main__":
    main()
