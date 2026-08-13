# MTN Complaint & Tracking System 🇳🇬

A cybersecurity-focused telecom complaint management portal built with **Django**.  
Features **two-step email OTP verification**, complaint tracking, geo-location support, and an admin analytics dashboard.

---

## 🚀 Features

- 📝 **User Registration** with two-step email OTP verification  
- 🔐 **Account Security** — one email per account, no duplicates  
- 🔑 **Forgot Password** — OTP-based password reset via email  
- 👁️ **Show/Hide Password** toggle on all password fields  
- 📍 **Geo-location** — captures complaint location on a map  
- 📊 **Admin Dashboard** with complaint analytics and charts  
- 📬 **Email Notifications** via Gmail SMTP  
- 🕐 **OTP Expiry** — codes expire after 10 minutes  
- 🗂️ **Complaint Status Tracking** — Pending / In Progress / Resolved  

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Backend    | Django 5.x        |
| Database   | SQLite3           |
| Email      | Gmail SMTP        |
| Geo        | Geopy / Nominatim |
| Frontend   | HTML, CSS, JS     |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/abdullahi5675/MTN-Complain-Tracker.git
cd MTN-Complain-Tracker
```

### 2. Create & Activate Virtual Environment

**Windows (CMD):**
```cmd
python -m venv env
env\Scripts\activate
```

**Linux / Mac:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Apply Database Migrations

```bash
cd backend
python manage.py migrate
```

### 5. Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Open in Browser

| Page             | URL                              |
|------------------|----------------------------------|
| 🌐 User Portal   | http://127.0.0.1:8000/           |
| 🔐 Login         | http://127.0.0.1:8000/login/     |
| 📝 Sign Up       | http://127.0.0.1:8000/signup/    |
| ⚙️ Admin Panel  | http://127.0.0.1:8000/admin/     |
| 🔑 Forgot Pass  | http://127.0.0.1:8000/forgot-password/ |

---

## 📧 Email Configuration

The system uses Gmail SMTP for sending OTP verification emails.  
To configure your own email, edit **`backend/backend/settings.py`**:

```python
EMAIL_HOST_USER     = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Gmail App Password
```

> **Note:** Use a [Gmail App Password](https://myaccount.google.com/apppasswords), not your regular Gmail password.

---

## 🔐 Security Features

| Feature                  | Description                                      |
|--------------------------|--------------------------------------------------|
| Email OTP Verification   | Account locked until email is verified           |
| OTP Expiry               | Codes expire after 10 minutes                    |
| Unique Email             | No two accounts can share the same email         |
| Login Protection         | Unverified accounts cannot log in                |
| Password Reset via OTP   | Secure reset without storing reset tokens in URL |
| Login Required           | Protected pages require authentication           |

---

## 📁 Project Structure

```
MTN-Complain-Tracker/
├── backend/
│   ├── backend/            # Django project config (settings, urls)
│   ├── telecomcomplaints/  # Main app
│   │   ├── models.py       # Complaint, EmailVerification, PasswordResetOTP
│   │   ├── views.py        # All views including OTP flows
│   │   ├── forms.py        # Custom forms with validation
│   │   ├── urls.py         # URL routing
│   │   ├── admin.py        # Admin dashboard customization
│   │   ├── templates/      # All HTML pages
│   │   └── migrations/     # Database migrations
│   ├── manage.py
│   └── requirements.txt
└── README.md
```

---

## 👥 Default Test Accounts

After setup, create your own accounts via `/signup/`.  
Use `python manage.py createsuperuser` for admin access.

---

## 📄 License

This project was developed as a **cybersecurity academic project** demonstrating secure user authentication, two-step verification, and complaint management.

---

*Built with ❤️ for MTN Nigeria*
