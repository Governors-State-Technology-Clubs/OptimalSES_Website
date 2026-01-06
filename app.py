from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_limiter.errors import RateLimitExceeded
from dotenv import load_dotenv
from pathlib import Path
from models import db, Lead
from datetime import timedelta
from email_validator import validate_email, EmailNotValidError
import os
import logging

load_dotenv()

app = Flask(__name__)

# ===== LOGGING =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== CONFIGURATION =====
BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = INSTANCE_DIR / "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_PATH}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ===== SECURITY: SECRET_KEY =====
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "❌ CRITICAL: SECRET_KEY not set in environment.\n"
        "Generate one:\n"
        "  python -c \"import secrets; print(secrets.token_urlsafe(32))\"\n"
        "Add to .env: SECRET_KEY=<generated-value>"
    )

# ===== SECURITY: SESSION =====
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)
app.config["SESSION_REFRESH_EACH_REQUEST"] = True

# ===== EMAIL CONFIGURATION =====
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_FROM_EMAIL")

# Handle both port 465 (SSL) and 587 (TLS)
if app.config["MAIL_PORT"] == 465:
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USE_TLS"] = False
else:
    app.config["MAIL_USE_TLS"] = True
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

# ===== SECURITY: CSRF PROTECTION =====
csrf = CSRFProtect(app)

# ===== SECURITY: RATE LIMITING =====
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)

# ===== ADMIN CREDENTIALS =====
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# ===== INPUT VALIDATION & SANITIZATION =====
def sanitize_for_email(text):
    """Remove/escape newlines and control characters that could inject headers"""
    if not text:
        return ""
    # Replace line breaks with spaces
    text = text.replace("\n", " ").replace("\r", " ")
    # Remove other control characters
    text = "".join(c for c in text if ord(c) >= 32 or c in "\t")
    return text.strip()

def validate_quote_submission(name, email, phone, service, message):
    """Validate quote form submission. Returns list of errors."""
    errors = []

    # Name: 2-100 chars
    if not name or len(name) < 2 or len(name) > 100:
        errors.append("Name must be 2-100 characters.")

    # Email: valid format
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        errors.append("Please enter a valid email address.")

    # Phone: optional, but if provided must be reasonable length
    if phone and len(phone) > 20:
        errors.append("Phone number is too long.")

    # Service: must be from allowed list
    allowed_services = [
        "New Construction", "Renovation", "Commercial Building",
        "Residential Home", "Interior Remodel", "Deck Installation",
        "Outdoor Structure", "Other Specialty Service"
    ]
    if service not in allowed_services:
        errors.append("Invalid project type selected.")

    # Message: 10-5000 chars (prevent spam, oversized payloads)
    if not message or len(message) < 10 or len(message) > 5000:
        errors.append("Project details must be 10-5000 characters.")

    return errors

def validate_contact_submission(name, email, phone, message):
    """Validate contact form submission. Returns list of errors."""
    errors = []

    # Name: 2-100 chars
    if not name or len(name) < 2 or len(name) > 100:
        errors.append("Name must be 2-100 characters.")

    # Email: valid format
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        errors.append("Please enter a valid email address.")

    # Phone: optional
    if phone and len(phone) > 20:
        errors.append("Phone number is too long.")

    # Message: 10-5000 chars
    if not message or len(message) < 10 or len(message) > 5000:
        errors.append("Message must be 10-5000 characters.")

    return errors

# ===== ROUTES =====

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
    return render_template("testimonials.html", active_page="testimonials")

@app.route("/contact", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def contact():
    if request.method == "POST":
        # ✅ Extract and clean inputs
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        # ✅ Validate
        errors = validate_contact_submission(name, email, phone, message)
        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for("contact"))

        # ✅ Create lead record
        lead = Lead(
            form_type="contact",
            name=name,
            email=email,
            phone=phone,
            service=None,
            message=message
        )

        try:
            db.session.add(lead)
            db.session.commit()

            # ✅ Send email with sanitized content
            admin_email = os.environ.get("ADMIN_EMAIL")
            msg = Message(
                subject=f"New Contact Submission from {sanitize_for_email(name)}",
                recipients=[admin_email],
                body=f"""
New contact form submission:

Name: {sanitize_for_email(name)}
Email: {sanitize_for_email(email)}
Phone: {sanitize_for_email(phone)}

Message:
{sanitize_for_email(message)}
                """
            )
            mail.send(msg)

            logger.info(f"Contact submission from {email}")
            flash("Thank you for reaching out! We'll get back to you soon.", "success")
            return redirect(url_for("contact"))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Contact submission error: {e}")
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("contact"))

    return render_template("contact.html", active_page="contact")

@app.route("/quote", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def quote():
    if request.method == "POST":
        # ✅ Extract and clean inputs
        name = request.form.get("fullName", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("projectType", "").strip()
        message = request.form.get("projectDetails", "").strip()

        # ✅ Validate
        errors = validate_quote_submission(name, email, phone, service, message)
        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for("quote"))

        # ✅ Create lead record
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

            # ✅ Send email with sanitized content
            admin_email = os.environ.get("ADMIN_EMAIL")
            msg = Message(
                subject=f"New Quote Request from {sanitize_for_email(name)}",
                recipients=[admin_email],
                body=f"""
New quote form submission:

Name: {sanitize_for_email(name)}
Email: {sanitize_for_email(email)}
Phone: {sanitize_for_email(phone)}
Project Type: {sanitize_for_email(service)}

Project Details:
{sanitize_for_email(message)}
                """
            )
            mail.send(msg)

            logger.info(f"Quote submission from {email} for {service}")
            flash("Your quote request has been submitted! We'll get back to you soon.", "success")
            return redirect(url_for("quote"))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Quote submission error: {e}")
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("quote"))

    return render_template("quote.html", active_page="quote")

@app.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # Max 5 login attempts per minute
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True
            session["is_admin"] = True
            logger.info(f"Successful admin login from {request.remote_addr}")
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_leads"))
        else:
            logger.warning(f"Failed admin login attempt from {request.remote_addr}: username={username}")
            flash("Invalid credentials.", "danger")

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    logger.info(f"Admin logout from {request.remote_addr}")
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))

@app.route("/admin/leads")
def admin_leads():
    if not session.get("is_admin"):
        flash("Please log in to access the admin panel.", "warning")
        return redirect(url_for("admin_login"))

    leads = Lead.query.order_by(Lead.id.desc()).all()
    logger.info(f"Admin accessed leads dashboard from {request.remote_addr}")
    return render_template("admin_leads.html", leads=leads)

# ===== ERROR HANDLERS =====

@app.errorhandler(RateLimitExceeded)
def ratelimit_handler(e):
    flash(f"Rate limit exceeded: {e.description}. Please try again later.", "danger")
    return redirect(request.referrer or url_for("home"))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=False)
