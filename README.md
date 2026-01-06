# OptimalSES_Website

**Website for Optimal SES**, a family-owned construction company providing comprehensive construction solutions throughout the Chicago area.

Built by the **GSU Software Engineering Club** using **Flask**, **SQLAlchemy**, and modern web technologies.

---

## 🎯 Project Overview

Optimal SES Website is a professional web presence for a construction company with:

- **Lead Generation**: Contact and quote forms with database persistence
- **Admin Dashboard**: View and manage all submissions
- **Email Notifications**: Automatic email alerts when leads submit forms
- **Bilingual Support**: English/Spanish interface highlighting Spanish language capabilities
- **Security**: CSRF protection, rate limiting, input validation, email sanitization
- **Professional Design**: Dark theme with orange accent color

---

## 🛠️ Tech Stack

### Backend

- **Flask** 3.0.0 - Web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Migrate** - Database migrations
- **Flask-Mail** - Email sending via Gmail SMTP
- **Flask-Limiter** - Rate limiting on forms and login
- **Flask-WTF** - CSRF protection

### Database

- **SQLite** - Local development
- **PostgreSQL** (Supabase) - Production on Render

### Frontend

- **HTML5** - Semantic markup
- **CSS3** - Custom dark theme with responsive design
- **Vanilla JavaScript** - Mobile menu toggle

### Deployment

- **Render** - Hosting and auto-deployment
- **GitHub** - Version control with branch protection
- **Gmail SMTP** - Email sending

---

## ✨ Features

### For Visitors

- 📄 **Home** - Hero section with service cards
- 📋 **About** - Company mission, values, and credentials
- 🏗️ **Projects** - Showcase of completed work
- ⭐ **Testimonials** - Client reviews and statistics
- 📞 **Contact** - Direct contact form
- 💬 **Quote** - Detailed project quote request form
- 🌐 **Bilingual** - Spanish language messaging

### For Admins

- 🔐 **Admin Login** - Secure authentication
- 📊 **Leads Dashboard** - View all form submissions
- 📧 **Email Notifications** - Automatic alerts when leads submit
- ⏱️ **Session Management** - 2-hour session timeout
- 🔒 **Security** - Rate limiting, CSRF protection

### Security

- ✅ **Rate Limiting** - 3 form submissions/hour, 5 login attempts/minute
- ✅ **CSRF Protection** - Token validation on all forms
- ✅ **Input Validation** - Strict checks on all user inputs
- ✅ **Email Sanitization** - Prevents header injection attacks
- ✅ **Session Security** - 2-hour timeout, automatic refresh
- ✅ **Email Validation** - Format checking on all email addresses
- ✅ **Payload Limits** - Maximum message length (5000 chars)

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.12+
- Git
- GitHub account
- Gmail account (with 2FA and app password)
- Render account (for deployment)

### Step 1: Clone Repository

```bash
git clone https://github.com/Governors-State-Technology-Clubs/OptimalSES_Website.git
cd OptimalSES_Website
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=<generate-via-command-below>

# Database (SQLite for local development)
DATABASE_URL=sqlite:///app.db

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-password-16-chars>

# Email Configuration (Gmail SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USERNAME=<your-gmail-account>
MAIL_PASSWORD=<gmail-app-password>
MAIL_FROM_EMAIL=<your-email>
ADMIN_EMAIL=<your-email>
```

#### Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output to SECRET_KEY
```

#### Get Gmail App Password

1. Go to https://myaccount.google.com/
2. Click **Security**
3. Enable **2-Step Verification** (if not already enabled)
4. Go to **App passwords**
5. Select **Mail** and **Windows Computer**
6. Copy the 16-character password

### Step 5: Initialize Database

```bash
flask db upgrade
```

If migrations folder doesn't exist:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 6: Run Locally

```bash
python app.py
```

Visit http://localhost:5000

---

## 🧪 Testing

### Test Quote Form

1. Visit http://localhost:5000/quote
2. Fill in all fields
3. Submit
4. Check your email inbox (~10 seconds)

### Test Contact Form

1. Visit http://localhost:5000/contact
2. Fill in all fields
3. Submit
4. Check your email inbox

### Test Admin Panel

1. Visit http://localhost:5000/admin/login
2. Username: `admin`
3. Password: (from your `.env`)
4. View all submitted leads
5. Click logout

### Test Rate Limiting

1. Submit 4 quotes in 1 hour
2. 4th submission should fail with "Rate limit exceeded"

---

## 🚀 Deployment to Render

### Step 1: Push to GitHub

```bash
git add .
git commit -m "feat: initial production setup"
git push origin main
```

### Step 2: Create Render Service

1. Go to https://render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `optimal-ses`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 3: Set Environment Variables

In Render dashboard → Settings → Environment:

```
SECRET_KEY=<your-secret-key>
DATABASE_URL=sqlite:///app.db
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<your-password>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USERNAME=<gmail-account>
MAIL_PASSWORD=<app-password>
MAIL_FROM_EMAIL=<email>
ADMIN_EMAIL=<email>
```

### Step 4: Deploy

Click **Deploy** and wait for build to complete (~2 minutes)

### Step 5: Test Production

1. Visit your Render URL: `https://optimal-ses.onrender.com`
2. Test quote/contact forms
3. Check email inbox
4. Test admin panel

---

## 🗄️ Database Setup (Optional: Supabase PostgreSQL)

### For Production (If Using Supabase Instead of SQLite)

#### Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Sign up with GitHub
3. Create project (save database password)
4. Wait for database creation (~30 sec)

#### Step 2: Get Connection String

1. In Supabase dashboard → Settings → Database
2. Copy URI connection string
3. Replace `[YOUR-PASSWORD]` with your database password

Example:

```
postgresql://postgres:YourPassword@db.xxxxx.supabase.co:5432/postgres
```

#### Step 3: Update `.env`

```env
DATABASE_URL=postgresql://postgres:YourPassword@db.xxxxx.supabase.co:5432/postgres
```

#### Step 4: Install PostgreSQL Driver

```bash
pip install psycopg2-binary==2.9.9
```

#### Step 5: Create Tables

```bash
flask db upgrade
```

#### Step 6: Update Render

Update `DATABASE_URL` in Render environment variables with Supabase connection string.

**Note**: Local development works fine with SQLite. Only use Supabase in production if needed.

---

## 📧 Email Configuration

### Gmail SMTP Setup

1. **Enable 2FA** on your Gmail account
2. **Generate App Password**:

   - Go to https://myaccount.google.com/security
   - Click **App passwords**
   - Select **Mail** and **Windows Computer**
   - Copy 16-character password

3. **Update `.env`**:

   ```env
   MAIL_USERNAME=your-gmail@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

4. **Test** by submitting a form

### Port Configuration

- **Port 465** (SSL) - Recommended, works for most networks
- **Port 587** (TLS) - Alternative if 465 blocked

Current setup uses **Port 465 (SSL)**.

---

## 👨‍💼 Admin Panel Usage

### Access Admin Dashboard

1. Visit `/admin/login`
2. Enter credentials (from `.env`)
3. View all form submissions in table format

### Manage Leads

- **View all submissions** - Contact and quote forms
- **Click "View Message"** - Read full submission details
- **Export data** - Copy submission info for CRM

### Security Notes

- Session times out after **2 hours** of inactivity
- Failed login attempts are **logged** for security monitoring
- **Rate limiting**: Max 5 login attempts per minute

---

## 🔒 Security Features

### Protection Against

| Threat             | Protection             |
| ------------------ | ---------------------- |
| Bot spam           | Rate limiting (3/hour) |
| Brute force login  | Rate limiting (5/min)  |
| Email injection    | Header sanitization    |
| CSRF attacks       | Token validation       |
| Session hijacking  | 2-hour timeout         |
| Invalid data       | Input validation       |
| Oversized payloads | Message length limits  |

### Best Practices

- ✅ Never commit `.env` to GitHub
- ✅ Use strong admin password (16+ chars)
- ✅ Regenerate Gmail app password every 6 months
- ✅ Monitor admin login attempts in logs
- ✅ Keep dependencies updated

---

## 🤝 Contributing

### Branch Workflow

1. **Create feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   git checkout -b fix/bug-name
   ```

2. **Make changes** and commit:

   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/your-feature-name
   ```

3. **Open Pull Request**:

   - Go to GitHub
   - Click "Compare & pull request"
   - Fill out PR template
   - Add screenshots (desktop + mobile)
   - Request review

4. **Code Review**:
   - At least **1 approval** required
   - Address feedback
   - Merge when approved

### Commit Message Format

```
feat: add new feature
fix: fix bug
docs: update documentation
style: code style changes
refactor: code refactoring
```

### Testing Before Push

```bash
# Test locally
python app.py

# Test quote form
# Test contact form
# Test admin login
# Test rate limiting
```

---

## 🐛 Troubleshooting

### Forms Not Sending Email

**Check**:

1. Gmail app password is correct
2. 2FA is enabled on Gmail
3. Port 465 is not blocked on your network
4. `MAIL_USERNAME` and `MAIL_PASSWORD` match `.env`

**Fix**:

```bash
python -c "
import smtplib, ssl
context = ssl.create_default_context()
server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
server.login('your-email@gmail.com', 'app-password')
print('✅ Email works!')
server.quit()
"
```

### Database Errors

**SQLite table doesn't exist**:

```bash
flask db upgrade
```

**PostgreSQL connection failed**:

- Check DATABASE_URL in `.env`
- Verify password doesn't have special characters (use `%40` for `@`)
- Confirm Supabase is reachable

### Rate Limiting Issues

You're submitting too many forms. Wait 1 hour or:

- Clear browser cookies
- Use incognito/private window
- Wait for rate limit to reset

### Admin Login Not Working

- Check username/password in `.env`
- Clear browser cookies
- Try incognito window
- Rate limited? (max 5 attempts/min)

---

## 📊 Project Structure

```
OptimalSES_Website/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── base.html         # Base template (navbar, footer)
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── projects.html     # Projects page
│   ├── testimonials.html # Testimonials page
│   ├── contact.html      # Contact form
│   ├── quote.html        # Quote form
│   ├── admin_login.html  # Admin login
│   ├── admin_leads.html  # Admin dashboard
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/               # Static files
│   └── css/
│       └── style.css     # Main stylesheet
├── migrations/           # Database migrations
├── instance/             # Instance files (app.db, etc)
└── README.md            # This file
```

---

## 📝 Configuration Reference

### Environment Variables

```env
# Required
SECRET_KEY                # Flask session encryption key
ADMIN_USERNAME            # Admin login username
ADMIN_PASSWORD            # Admin login password
MAIL_USERNAME             # Gmail account
MAIL_PASSWORD             # Gmail app password
ADMIN_EMAIL               # Email to receive submissions

# Optional
DATABASE_URL              # Database connection (default: SQLite)
MAIL_SERVER               # SMTP server (default: smtp.gmail.com)
MAIL_PORT                 # SMTP port (default: 465)
MAIL_USE_TLS              # Use TLS (default: False for port 465)
MAIL_FROM_EMAIL           # From email address
```

### Flask Configuration

Located in `app.py`:

- **Session timeout**: 2 hours
- **Rate limits**: 3 forms/hour, 5 logins/minute
- **Message length**: 10-5000 characters
- **Name length**: 2-100 characters
- **Phone length**: Max 20 characters

---

## 🚀 Performance & Scalability

### Current Capacity

- ✅ Handles 100+ monthly form submissions
- ✅ Database scales to 10,000+ leads
- ✅ Email sending <1 second
- ✅ Form validation <10ms

### To Scale Further

**When you need more**:

1. Upgrade to Supabase paid tier (auto-scaling)
2. Add Redis for caching
3. Implement queue system for emails (Bull, Celery)
4. Add CDN for static assets (CloudFlare)
5. Monitor with Sentry or New Relic

---

## 📞 Support & Questions

- **Issues**: Create GitHub issue with details
- **Questions**: Ask in PR comments
- **Security**: Never commit sensitive data (.env, passwords)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👥 Contributors

Built by the **GSU Software Engineering Club**

### Current Team

- Mario Mendez - Backend/Setup
- GSU SWE Club Members

### How to Contribute

1. Fork repository
2. Create feature branch
3. Make changes
4. Open pull request
5. Get approval and merge

---

## 🎯 Roadmap

- [ ] Individual user accounts (vs shared admin)
- [ ] SMS notifications for leads
- [ ] Mobile app
- [ ] CRM integration
- [ ] Payment processing
- [ ] Live chat support
- [ ] Email campaign system
- [ ] Advanced analytics

---

## ✅ Checklist: Deploying to Production

- [ ] All `.env` variables set
- [ ] Email tested locally
- [ ] Admin panel tested locally
- [ ] Quote/contact forms tested locally
- [ ] Code pushed to main branch
- [ ] Render build successful
- [ ] Email working in production
- [ ] Admin panel working in production
- [ ] Forms working in production

---

**Last Updated**: January 6, 2026
**Status**: ✅ Production Ready
