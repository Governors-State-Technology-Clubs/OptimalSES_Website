from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_migrate import Migrate
from flask_mail import Mail, Message
from dotenv import load_dotenv
from pathlib import Path
from models import db , Lead
import os
load_dotenv()

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = INSTANCE_DIR / "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_PATH}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
db.init_app(app)
migrate = Migrate(app, db)

# Email configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", True)
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_FROM_EMAIL")

mail = Mail(app)

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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        #create reocrd in the database
        lead = Lead(
            form_type="contact",
            name=name,
            email=email,
            phone=phone,
            service = None,
            message=message
        )

        try:
            db.session.add(lead)
            db.session.commit()

            # Send email notification
            admin_email = os.environ.get("ADMIN_EMAIL")
            msg = Message(
                subject=f"New Contact Submission from {name}",
                recipients=[admin_email],
                body=f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
                """
            )
            mail.send(msg)

            flash("Thank you for reaching out! We'll get back to you soon.", "success")
            return redirect(url_for("contact"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting your message. Please try again.", "danger")
            return redirect(url_for("contact"))
    return render_template("contact.html", active_page="contact")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    if request.method == "POST":
        name = request.form.get("fullName")
        email = request.form.get("email")
        phone = request.form.get("phone")
        service = request.form.get("projectType")
        message = request.form.get("projectDetails")

        lead = Lead(
            form_type="quote",
            name=name,
            email=email,
            phone=phone,
            service=service,
            message=message
        )
        try:
            db.session.add(lead)
            db.session.commit()

            # Send email notification
            admin_email = os.environ.get("ADMIN_EMAIL")
            msg = Message(
                subject=f"New Quote Request from {name}",
                recipients=[admin_email],
                body=f"""
New quote form submission:

Name: {name}
Email: {email}
Phone: {phone}
Project Type: {service}

Project Details:
{message}
                """
            )
            mail.send(msg)

            flash("Your quote request has been submitted! We'll get back to you soon.", "success")
            return redirect(url_for("quote"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting your quote request. Please try again.", "danger")
            return redirect(url_for("quote"))
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

    leads = Lead.query.order_by(Lead.id.desc()).all()

    return render_template("admin_leads.html", leads=leads)


if __name__ == "__main__":
    app.run(debug=True)
