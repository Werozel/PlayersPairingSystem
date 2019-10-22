from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        return redirect(url_for("login"))
    else:
        return app.send_static_file("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():

    return app.send_static_file("login.html")


if __name__ == "__main__":
    app.run(debug=True)
