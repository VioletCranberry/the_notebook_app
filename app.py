from typing import Any

import py_mini_racer
from flask import Flask, Request, Response, jsonify, render_template, request

app = Flask(__name__)


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
    # set evaluation memory limits ~ 10 mb
    ctx.set_hard_memory_limit(10000000)
    ctx.set_soft_memory_limit(10000000)
    return ctx.eval(script_content, timeout_sec=10)


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
    app.run()
