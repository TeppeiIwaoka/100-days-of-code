from pprint import pprint
import smtplib

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_endpoint = "https://api.npoint.io/43644ec4f0013682fc0d"
blog_data = requests.get(api_endpoint).json()
my_email = "XXX"
password = "XXX"
mail_to = "XXX"


@app.route("/")
def home():
    return render_template("index.html", posts=blog_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    method_type = request.method
    if method_type == 'POST':
        form = request.form
        name = form["name"]
        mail = form["email"]
        phone = form["phone"]
        message = form["message"]
        mail_content = f"Message from {name}, phone numes {phone}, email address {mail} \n {message}"
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=mail_to,
                                msg=f'Subject:Message from your blog\n\n {mail_content}'
                                )
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/post/<num>")
def post(num):
    target_data = {}
    for post in blog_data:
        if post["id"] == int(num):
            target_data = post
    return render_template("post.html", data=target_data)


if __name__ == "__main__":
    app.run(debug=True)
