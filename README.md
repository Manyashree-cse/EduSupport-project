# EduSupport - Student Support & Ticket Management System

A Flask + MySQL + Bootstrap prototype for managing student administrative support requests.

## Features

- Student registration/login
- Role-based access: Student, Staff, Admin
- Ticket creation and tracking
- Categories and priorities
- Assignment to staff
- Status workflow
- Comments
- Activity/audit history
- Ticket ageing
- SLA calculation and breach indication
- Admin dashboard
- Staff dashboard

## Setup

### 1. Create database

```sql
CREATE DATABASE edusupport;
```

### 2. Configure MySQL

Edit `config.py` and replace `YOUR_PASSWORD`.

### 3. Create environment

```bash
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run

```bash
python app.py
```

Open:

http://127.0.0.1:5000

## Demo roles

Registration creates students.

To create an admin/staff user, first register a student, then change the role in MySQL:

```sql
UPDATE users SET role='admin' WHERE email='your-email@example.com';
```

After logging out and back in, the user will have admin access.

Admin can create staff accounts from the dashboard.

## Ticket workflow

OPEN -> ASSIGNED -> IN_PROGRESS -> PENDING -> RESOLVED -> CLOSED

Students can close a ticket only after it is RESOLVED.
