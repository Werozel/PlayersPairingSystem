from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Main Page")


@app.route("/login")
def login():
    return render_template("login.html", title="Login Page")


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/register")
def register():
    return render_template("register.html", title="Register Page")




if __name__ == "__main__":
    app.run(debug=True)
