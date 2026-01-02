# HostelMS - Hostel Management System

A comprehensive, full-stack web application for managing university hostel operations. Built with Django 5.0, SQLite/Oracle Database, and Bootstrap 4, this system show enterprise-level software development practices, database management, and modern web design.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-4.3.1-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---


## Overview

**HostelMS** is a production-ready hostel management system that streamlines hostel operations including room allocation, complaint management, and administrative oversight. The system features role-based access control, real-time analytics, and a professional user interface.


### Key Highlights

- **Secure Authentication** - Custom user model with role-based access control
- **Real-time Analytics** - Interactive dashboards with Chart.js visualizations
- **Complete Hostel Management** - From application to room allocation
- **Complaint Tracking** - Student complaint submission and admin resolution workflow
- **Professional UI** - Responsive Bootstrap 4 design with custom styling
- **Flexible Database** - Works with both Oracle and SQLite
- **Production Ready** - Environment variables, logging, error handling

---

## Features

### Admin Dashboard

- **Real-time Statistics Dashboard**
  - Total students, rooms, and hostels
  - Pending/approved applications counter
  - Complaint tracking (pending/in-progress/resolved)
  - Live occupancy rate calculation

- **Interactive Data Visualizations**
  - Application status pie chart (Chart.js)
  - Complaint status bar chart (Chart.js)
  - System overview panel

- **Management Features**
  - View and manage all applications
  - Track and update complaint status
  - Room allocation management
  - Student information overview

- **Quick Actions Panel**
  - One-click access to all management functions
  - Responsive navigation system

### 👨Student Dashboard

- **Personal Profile Management**
  - View student details and current status
  - Semester and contact information

- **Application Tracking**
  - Submit room applications
  - Real-time application status updates
  - View allocated room details
  - Duplicate application prevention

- **Complaint Management**
  - Lodge new complaints with descriptions
  - Track complaint status in real-time
  - View complete complaint history
  - Interactive modals for detailed views

- **Quick Actions**
  - Apply for rooms
  - Lodge complaints
  - Download fee vouchers
  - View room allocation

### Security Features

- **Environment-Based Configuration**
  - All secrets stored in `.env` file
  - Secret key, database credentials protected
  - Debug mode configuration

- **Role-Based Access Control (RBAC)**
  - Custom decorators: `@student_required`, `@admin_required`
  - Student/Admin separation enforced
  - Students only see their own data

- **Authentication & Authorization**
  - Secure login/signup system
  - Password hashing (Django default)
  - Session management
  - CSRF protection

- **Input Validation**
  - Form validation on all user inputs
  - Duplicate prevention mechanisms
  - SQL injection protection via ORM

- **Comprehensive Logging**
  - All actions logged to `logs/hostel.log`
  - Error tracking and debugging
  - User activity monitoring

### Database Excellence

- **Dual Database Support**
  - SQLite for development/testing
  - Oracle with PL/SQL procedures for production
  - Easy database switching via configuration

- **Performance Optimization**
  - 28+ database indexes for fast queries
  - `select_related()` and `prefetch_related()` usage
  - Efficient query optimization

- **Clean Abstraction Layer**
  - Python wrappers for stored procedures
  - Django ORM for clean, readable code
  - Transaction handling

- **Data Integrity**
  - Proper foreign key relationships
  - Cascade delete protection
  - Unique constraints



## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Django 5.0** - High-level web framework
- **cx_Oracle 8.3.0** - Oracle database driver (optional)
- **django-crispy-forms** - Beautiful form rendering
- **python-decouple** - Environment variable management
- **django-filter** - Advanced filtering capabilities
- **django-extensions** - Additional Django utilities

### Database
- **SQLite** - Default development database
- **Oracle 11g/12c/19c** - Enterprise database (optional)
- **Django ORM** - Object-relational mapping
- **PL/SQL** - Stored procedures (Oracle only)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling and animations
- **Bootstrap 4.3.1** - Responsive CSS framework
- **JavaScript/jQuery** - Interactive features
- **Chart.js 3.9.1** - Data visualization library
- **Font Awesome 5.15.4** - Icon library

### Development Tools
- **Git** - Version control
- **Django Admin** - Database management interface
- **Python Logging** - Application monitoring
- **Django Debug Toolbar** - Development debugging (optional)

---


## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Oracle Database (optional, for production use)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/hostelms.git
cd hostelms
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here-generate-with-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For SQLite (default)
# No additional configuration needed

# For Oracle (optional)
DB_NAME=xe
DB_USER=system
DB_PASSWORD=your-oracle-password
DB_HOST=localhost
DB_PORT=1521
```

### Step 5: Database Setup

#### For SQLite (Recommended for Testing):

```bash
# Apply migrations
python manage.py migrate

# Create sample data
python manage.py create_sample_data
```

#### For Oracle (Production):

```bash
# Connect to Oracle
sqlplus system/password@localhost:1521/xe

# Run database scripts
@database/oracle_procedures.sql
@database/indexes.sql
EXIT;

# Apply Django migrations
python manage.py migrate

# Create sample data
python manage.py create_sample_data
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000 in your browser.

---

### Common Tasks

#### As a Student:

1. **Apply for a Room**
   - Login → Student Dashboard → "Apply for Room"
   - Select room type and occupancy
   - Submit application

2. **Lodge a Complaint**
   - Login → Student Dashboard → "Lodge Complaint"
   - Enter complaint description
   - Submit and track status

3. **Check Application Status**
   - Login → Student Dashboard
   - View application status card (Pending/Approved)

#### As an Admin:

1. **View Dashboard Statistics**
   - Login → Admin Dashboard
   - View real-time statistics and charts

2. **Manage Applications**
   - Admin Dashboard → "View Applications"
   - Review student applications
   - Approve or manage requests

3. **Track Complaints**
   - Admin Dashboard → "View Complaints"
   - Review all complaints
   - Update complaint status

---

## Project Structure

```
HostelMS/
├── HostelMS/                   # Project configuration
│   ├── settings.py            # Environment-based settings
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI application
│   └── __init__.py
│
├── hostel/                     # Hostel management app
│   ├── management/
│   │   └── commands/
│   │       └── create_sample_data.py  # Sample data generator
│   ├── decorators.py          # Custom auth decorators
│   ├── db_utils.py            # Oracle procedure wrappers
│   ├── models.py              # Database models
│   ├── views.py               # Business logic
│   ├── forms.py               # Form definitions
│   ├── urls.py                # App URL patterns
│   ├── admin.py               # Django admin config
│   └── apps.py
│
├── user/                       # User management app
│   ├── models.py              # User, Student, Admin models
│   ├── views.py               # Authentication views
│   ├── forms.py               # User forms
│   ├── urls.py                # User URL patterns
│   ├── admin.py
│   └── apps.py
│
├── database/                   # Database scripts
│   ├── oracle_procedures.sql  # 11 stored procedures
│   ├── indexes.sql            # Performance indexes
│   └── README.md              # Oracle setup guide
│
├── templates/                  # HTML templates
│   ├── base.html              # Master template
│   ├── homepage.html          # Landing page
│   ├── hostel/
│   │   ├── admin_dashboard.html
│   │   ├── student_dashboard.html
│   │   ├── complaints.html
│   │   ├── applications.html
│   │   ├── lodge_complaint.html
│   │   └── room_application.html
│   └── user/
│       ├── login.html
│       └── signup.html
│
├── static/                     # Static assets
│   ├── css/
│   │   └── custom.css         # Professional styling
│   ├── js/                    # JavaScript files
│   └── background-image.jpg   # UI background
│
├── logs/                       # Application logs
│   └── hostel.log             # Activity logging
│
├── .env                        # Environment variables (gitignored)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management
└── README.md                  # This file
```

---

## Database Design

### Models

#### User (Custom User Model)
- Extends Django's AbstractUser
- Fields: `username`, `email`, `is_student`, `is_admin`
- Supports role-based authentication

#### Student
- ForeignKey to User (OneToOne relationship)
- Fields: `student_id`, `name`, `email`, `semester`, `application_status`
- ManyToMany with Room (through residents)

#### Admin
- ForeignKey to User (OneToOne relationship)
- Fields: `admin_id`, `name`, `email`
- Manages hostels

#### Hostel
- Fields: `name`, `address`, `type` (Boys/Girls)
- ForeignKey to Admin
- Contains multiple wings

#### Wing
- Fields: `name`
- ForeignKey to Hostel
- Contains multiple floors

#### Floor
- Fields: `number`
- ForeignKey to Wing
- Contains multiple rooms

#### Room
- Fields: `number`, `room_type` (AC/Non-AC), `occupancy` (Single/Double/Triple)
- ForeignKey to Floor
- ManyToMany with Student (residents)

#### Application
- Fields: `room_type`, `occupancy`, `status` (Boolean)
- ForeignKey to Student (applicant)
- Tracks room applications

#### Complaint
- Fields: `description`, `status` (Pending/In Progress/Resolved)
- ForeignKey to Student
- Complaint tracking system

### Entity Relationship Diagram

```
User (1) ──→ (1) Student/Admin
Admin (1) ──→ (*) Hostel
Hostel (1) ──→ (*) Wing
Wing (1) ──→ (*) Floor
Floor (1) ──→ (*) Room
Room (*) ←──→ (*) Student
Student (1) ──→ (*) Application
Student (1) ──→ (*) Complaint
```

---

## Security Features

### Authentication & Authorization

1. **Custom Decorators**
   ```python
   @student_required
   def student_dashboard(request):
       # Only accessible by students

   @admin_required
   def admin_dashboard(request):
       # Only accessible by admins
   ```

2. **Role-Based Access Control**
   - Students cannot access admin views
   - Admins cannot access student-specific views
   - Authorization checks on every protected view

3. **Password Security**
   - Django's built-in password hashing (PBKDF2)
   - Password validation requirements
   - Secure password reset functionality

### Data Protection

1. **Environment Variables**
   - Secret keys stored in `.env`
   - Database credentials protected
   - No hardcoded secrets

2. **CSRF Protection**
   - Django's CSRF middleware enabled
   - CSRF tokens on all forms
   - Cookie security settings

3. **SQL Injection Prevention**
   - Django ORM parameterized queries
   - No raw SQL without sanitization
   - Input validation on all forms

4. **XSS Protection**
   - Django template auto-escaping
   - Sanitized user inputs
   - Content Security Policy headers

### Logging & Monitoring

```python
# All actions logged
logger.info(f'Student {student_id} submitted application')
logger.error(f'Error fetching complaints: {str(e)}')
logger.warning(f'Unauthorized access attempt')
```

---

## API Endpoints

### User Authentication

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET/POST | `/login` | User login | Public |
| GET/POST | `/signup` | User registration | Public |
| GET | `/logout` | User logout | Authenticated |
| GET | `/` | Homepage with role redirection | Authenticated |

### Student Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/student/dashboard/` | Student dashboard | Student |
| GET/POST | `/apply_room/` | Submit room application | Student |
| GET/POST | `/lodge_complaint/` | Lodge complaint | Student |
| GET | `/download_voucher/` | Download fee voucher | Student |

### Admin Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/admin/dashboard/` | Admin dashboard with analytics | Admin |
| GET | `/applications/` | View all applications | Admin |
| GET | `/complaints/` | View all complaints | Admin |

### Django Admin

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/admin/` | Django admin interface | Superuser |

---

## Testing

### Manual Testing

1. **Run System Check**
   ```bash
   python manage.py check
   ```

2. **Create Test Data**
   ```bash
   python manage.py create_sample_data
   ```

3. **Test Workflows**
   - Student registration and login
   - Room application submission
   - Complaint lodging
   - Admin dashboard access
   - Application management


### Running Tests

```bash
# Create sample data for testing
python manage.py create_sample_data

# Start server and test manually
python manage.py runserver

# Access test URLs
# Student: http://localhost:8000/login (john/student123)
# Admin: http://localhost:8000/login (admin/admin123)
```

---



## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide for Python
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting PR

---


## Acknowledgments

- Django Documentation - https://docs.djangoproject.com
- Bootstrap Framework - https://getbootstrap.com
- Chart.js Library - https://www.chartjs.org
- Font Awesome Icons - https://fontawesome.com
- Oracle Database Documentation

---


## Skills Demonstrated

### Backend Development
✅ Django framework mastery
✅ RESTful architecture
✅ Database design and optimization
✅ Oracle PL/SQL programming
✅ Security implementation
✅ Error handling and logging
✅ Custom middleware/decorators

### Frontend Development
✅ Responsive web design
✅ Bootstrap framework
✅ JavaScript/jQuery
✅ Chart.js data visualization
✅ CSS animations
✅ User experience design

### Database Management
✅ Oracle database administration
✅ Stored procedures
✅ Performance optimization
✅ Index design
✅ Django ORM

### Software Engineering
✅ Clean code principles
✅ Separation of concerns
✅ Environment configuration
✅ Documentation
✅ Git version control

---


