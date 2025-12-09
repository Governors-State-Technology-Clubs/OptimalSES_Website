from flask import Flask, redirect, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("testimonials.html")

@app.route("/user/<name>")
def user(name):
    return f"Hello{name}"

@app.route("/admin")
def admin():
    return redirect(url_for('user'))

if __name__ == "__main__":
    app.run()