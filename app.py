from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World"


@app.route("/about")
def about():
    return "This is the about page."


@app.route("/user/<username>")
def user_profile(username):
    return f"Welcome, {username}!"


if __name__ == "__main__":
    app.run(debug=True)

