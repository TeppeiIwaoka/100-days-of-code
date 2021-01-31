from pprint import pprint

from flask import Flask, render_template
import requests

app = Flask(__name__)

api_endpoint = "https://api.npoint.io/43644ec4f0013682fc0d"
blog_data = requests.get(api_endpoint).json()

@app.route("/")
def home():
    return render_template("index.html", posts=blog_data)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<num>")
def post(num):
    target_data = {}
    for post in blog_data:
        if post["id"] == int(num):
            target_data = post
    return render_template("post.html", data=target_data)

if __name__ == "__main__":
    app.run(debug=True)