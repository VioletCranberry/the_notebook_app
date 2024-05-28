from typing import Any, Tuple

import py_mini_racer
from flask import Flask, Request, Response, jsonify, render_template, request

from utils import get_arguments

app = Flask(__name__)

# Global variables to hold the configurable parameters.
hard_memory_limit = 10000000
soft_memory_limit = 10000000
timeout_sec = 10


def get_script_content(req: Request) -> str:
    """
    Extract the JavaScript script content from the JSON payload in the request.
    """
    data = req.get_json()
    return data.get("script", "")


def evaluate_script(script_content: str) -> Any:
    """
    Evaluate the provided JavaScript code.
    """
    ctx = py_mini_racer.MiniRacer()
    # Set evaluation memory limits
    ctx.set_hard_memory_limit(hard_memory_limit)
    ctx.set_soft_memory_limit(soft_memory_limit)
    return ctx.eval(script_content, timeout_sec=timeout_sec)


@app.route("/healthz", methods=["GET"])
def health_check() -> Tuple[Response, int]:
    """
    Health check endpoint to verify that the application is running.
    """
    return jsonify({"status": "healthy"}), 200


@app.route("/")
def index() -> str:
    """
    Render the index HTML page.
    """
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_script() -> Response:
    """
    Handle the POST request to run JavaScript code and return the result or error.
    """
    try:
        script_content = get_script_content(request)
        result = evaluate_script(script_content)
        return jsonify(result=result)
    except py_mini_racer.JSEvalException as e:
        return jsonify(error=f"JavaScript error: {e}")
    except Exception as e:
        return jsonify(error=f"Error: {e}")


if __name__ == "__main__":
    args = get_arguments()

    # Update global variables with parsed arguments
    hard_memory_limit = args.hard_memory_limit
    soft_memory_limit = args.soft_memory_limit
    timeout_sec = args.timeout_sec

    app.run(host=args.host, port=args.port, debug=args.debug)
