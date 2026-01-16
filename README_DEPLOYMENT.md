# 🎓 Smart Internship & Placement Portal

## 📋 Overview

A comprehensive Django-based placement management system with advanced features for students, recruiters, and educational institutions (TPO).

### ✨ Key Features

- **Placement Credit Score (PCS)** - Track student accountability throughout placement cycle
- **Dream Company Roadmap** - Personalized career path with readiness tracking
- **Prep Vault** - Community-driven interview experience sharing
- **Eligibility Gatekeeper** - Smart job matching with real-time verification
- **Recruiter Rating System** - Performance metrics for recruiter accountability
- **Historical Hiring Analytics** - Data-driven insights for decision making
- **Role-Based Access Control** - Separate dashboards for Student, Recruiter, TPO
- **Professional UI** - Responsive design with Bootstrap 5

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip
- virtualenv
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/placement-portal.git
   cd placement-portal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   ```bash
   python manage.py makemigrations accounts jobs
   python manage.py migrate
   ```

5. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the portal**
   - Open browser: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 📁 Project Structure

```
placement-portal/
├── accounts/                    # User authentication & profiles
│   ├── models.py               # User, Student, Recruiter models
│   ├── views.py                # Auth views & dashboards
│   ├── forms.py                # Registration & profile forms
│   ├── decorators.py           # Role-based decorators
│   └── urls.py                 # URL routing
│
├── jobs/                        # Job & placement management
│   ├── models.py               # Job, Application, PCS models
│   ├── views.py                # Job views & advanced features
│   ├── admin.py                # Admin configurations
│   └── urls.py                 # Job URL routes
│
├── placement_portal/           # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI config
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template with navbar
│   ├── home.html               # Home page
│   ├── about.html              # About page
│   ├── contact.html            # Contact page
│   ├── accounts/               # Auth templates
│   └── jobs/                   # Job templates
│
├── static/                     # Static files (CSS, JS, Images)
├── media/                      # User uploads (Resumes, Photos)
├── db.sqlite3                  # SQLite database
├── requirements.txt            # Python dependencies
├── manage.py                   # Django CLI
└── README.md                   # This file
```

---

## 🎯 User Roles & Workflows

### Student
- Browse available jobs (auto-filtered by eligibility)
- Apply to jobs
- Track PCS score (accountability system)
- Set dream company & track readiness
- Share/view interview experiences in Prep Vault
- Download placement certificate

### Recruiter
- Post job openings with eligibility criteria
- Review & shortlist applications
- Schedule interviews
- Track recruiter performance rating
- View hiring analytics

### TPO (Admin)
- Verify students & recruiters
- Monitor all placements in real-time
- View system analytics & trends
- Post announcements
- Generate placement reports

---

## 💻 Technical Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0.1 |
| **Frontend** | Bootstrap 5, Tailwind CSS |
| **Database** | SQLite3 |
| **Icons** | Font Awesome 6.4.0 |
| **Python Version** | 3.12+ |

---

## 🔐 Security Features

- ✅ CSRF protection on all forms
- ✅ Password hashing with Django's system
- ✅ Session management
- ✅ Role-based access control (RBAC)
- ✅ Login required decorators
- ✅ User type verification

---

## 📊 Database Models

### Core Models
- **User** - Django's built-in user model
- **StudentProfile** - Student details with PCS score
- **RecruiterProfile** - Company & recruiter information
- **Job** - Job postings with eligibility criteria
- **Application** - Student job applications
- **InterviewSchedule** - Interview tracking

### Advanced Feature Models
- **DreamCompany** - Student's target company roadmap
- **HistoricalHiringData** - Hiring trends & analytics
- **InterviewExperience** - Community interview database
- **PrepVault** - Interview preparation resources
- **RecruiterResponseRating** - Performance metrics

---

## 🌐 API Endpoints

### Authentication
- `GET/POST` `/accounts/login/` - User login
- `GET/POST` `/accounts/register/` - Student registration
- `GET/POST` `/accounts/register/recruiter/` - Recruiter registration
- `GET` `/accounts/logout/` - User logout

### Dashboards
- `GET` `/accounts/student/dashboard/` - Student dashboard
- `GET` `/accounts/recruiter/dashboard/` - Recruiter dashboard
- `GET` `/accounts/tpo/dashboard/` - TPO admin panel

### Jobs
- `GET` `/jobs/` - Browse jobs
- `GET/POST` `/jobs/create/` - Post new job
- `POST` `/jobs/<id>/apply/` - Apply to job
- `GET` `/jobs/applications/` - View applications

### Advanced Features
- `GET` `/accounts/student/pcs-dashboard/` - PCS System
- `GET` `/jobs/dream-company/` - Dream Company Roadmap
- `GET` `/jobs/prep-vault/` - Prep Vault

### Static Pages
- `GET` `/` - Home page
- `GET` `/about/` - About page
- `GET` `/contact/` - Contact page

---

## 📱 Responsive Design

- ✅ Desktop (1024px+) - Full sidebar + content
- ✅ Tablet (768px-1023px) - Compact sidebar
- ✅ Mobile (<768px) - Hidden menu + full content

---

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

Run specific test:
```bash
python manage.py test accounts.tests.UserAuthTest
```

---

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Vaibhav Kadam**
- GitHub: [@VaibhavKadam2004](https://github.com/VaibhavKadam2004)

---

## 🤝 Support

For support, email your-email@example.com or open an issue in the repository.

---

## 🎉 Acknowledgments

- Built with Django framework
- UI powered by Bootstrap 5
- Icons from Font Awesome
- Community-driven development approach

---

**Last Updated:** January 16, 2026  
**Status:** ✅ Production Ready
