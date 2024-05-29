import argparse
import os

from dotenv import load_dotenv


def get_arguments() -> argparse.Namespace:
    """
    Parse and return command line arguments.
    """
    # Load environment variables from .env file
    load_dotenv()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--hard-memory-limit",
        type=int,
        required=False,
        help="JS hard memory limit (in bytes).",
        default=os.getenv("JS_HARD_MEMORY_LIMIT", 10000000),
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        required=False,
        help="JS eval timeout (in seconds).",
        default=os.getenv("JS_EVAL_TIMEOUT_SEC", 10),
    )
    parser.add_argument(
        "--soft-memory-limit",
        type=int,
        required=False,
        help="JS soft memory limit (in bytes).",
        default=os.getenv("JS_SOFT_MEMORY_LIMIT", 10000000),
    )

    parser.add_argument(
        "--host",
        type=str,
        required=False,
        help="Bind socket to this host.",
        default=os.getenv("HOST", "0.0.0.0"),
    )
    parser.add_argument(
        "--port",
        type=int,
        required=False,
        help="Bind socket to this port.",
        default=int(os.getenv("PORT", 5000)),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        required=False,
        help="Enable debug mode?",
        default=os.getenv("DEBUG", "false").lower() == "true",
    )

    parser.add_argument(
        "--image",
        type=str,
        required=False,
        help="Image to use for application instances.",
        default=os.getenv(
            "INSTANCE_IMAGE", "docker.io/library/the_notebook_app"
        ),
    )

    return parser.parse_args()
