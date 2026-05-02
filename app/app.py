from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/greet/<name>")
def greet(name):
    return render_template("result.html", name=name)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "stranger")
    return render_template("result.html", name=name)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
