from flask import Flask, render_template, redirect, url_for, request, flash, session
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

@app.route("/")
def home():
    return render_template("index.html", active_page="home")

@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/projects")
def projects():
    return render_template("projects.html", active_page="projects")


@app.route("/testimonials")
def testimonials():
    #wil be updated soon
    return render_template("testimonials.html", active_page="testimonials")


@app.route("/contact")
def contact():
    return render_template("contact.html", active_page="contact")


@app.route("/quote")
def quote():
    return render_template("quote.html", active_page="quote")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_leads"))
        else:
            flash("Invalid credentials.", "danger")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))


@app.route("/admin/leads")
def admin_leads():
    if not session.get("is_admin"):
        flash("Please log in to access the admin panel.", "warning")
        return redirect(url_for("admin_login"))
    return render_template("admin_leads.html")

if __name__ == "__main__":
    app.run(debug=True)
