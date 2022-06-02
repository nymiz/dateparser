from flask import Flask, jsonify, request
import os
from main import *

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    date_string = request.args.get('date_string')

    data = main_func(date_string)

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
