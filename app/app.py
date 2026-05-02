from flask import Flask, render_template, request
import os

app = Flask(__name__)

SLOT = os.environ.get("SLOT", "unknown")
PORT = int(os.environ.get("PORT", 5000))


@app.route("/")
def index():
    return render_template("index.html", slot=SLOT)


@app.route("/greet/<name>")
def greet(name):
    return render_template("result.html", name=name, slot=SLOT)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "stranger")
    return render_template("result.html", name=name, slot=SLOT)


@app.route("/health")
def health():
    return {"status": "ok", "slot": SLOT}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)