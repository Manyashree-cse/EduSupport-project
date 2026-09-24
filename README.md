# EduSupport - Student Support & Ticket Management System

A Flask + MySQL + Bootstrap prototype for managing student administrative support requests.

## Features

- Student registration and login
- Role-based access: Student, Staff, Admin
- Ticket creation and tracking
- Ticket categories and priorities
- Assignment of tickets to staff
- Ticket status workflow
- Comments and remarks
- Activity/audit history
- Ticket ageing
- SLA calculation and breach indication
- Admin dashboard
- Staff dashboard
- Student dashboard
- Resolution and closure tracking

## Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Password Security:** Werkzeug
- **Database Driver:** PyMySQL
- **Environment Configuration:** python-dotenv

## Project Structure

```text
EduSupport_Full_Project/
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── README.md
├── .env                 # Local only - not committed to GitHub
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── ticket.py
│   ├── comment.py
│   ├── activity.py
│   └── category.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── student.py
│   ├── staff.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── student/
│   ├── staff/
│   └── admin/
│
└── static/
    ├── css/
    └── js/
```

## Setup

### Prerequisites

Make sure the following are installed:

- Python 3.x
- MySQL Server
- MySQL Workbench (optional)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Manyashree-cse/EduSupport-project
cd EduSupport_Full_Project
```

### 2. Create the MySQL database

Open MySQL Workbench or MySQL Command Line and run:

```sql
CREATE DATABASE edusupport;
```

You can verify the database with:

```sql
SHOW DATABASES;
```

### 3. Create and activate virtual environment

Windows:

```bash
python -m venv myenv
myenv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```text
EduSupport_Full_Project/
├── .env
├── app.py
├── config.py
├── extensions.py
└── ...
```

Add:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:YOUR_MYSQL_PASSWORD@localhost/edusupport
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL root password.

Example:

```env
SECRET_KEY=my-development-secret-key
DATABASE_URL=mysql+pymysql://root:MyPassword@localhost/edusupport
```

> **Security:** Do not commit the actual `.env` file to GitHub. It contains sensitive configuration values and should remain local. The `.env` file is included in `.gitignore`.

### 6. Run the application

```bash
python app.py
```

The application will create the required database tables automatically when the database connection is successful.

Open the application:

```text
http://127.0.0.1:5000
```

## User Roles

### Student

Students can:

- Register and log in
- Create support tickets
- Select a category and priority
- View their tickets
- View ticket status
- Add comments
- View ticket activity
- Close resolved tickets

### Staff

Staff can:

- Log in to the staff dashboard
- View assigned tickets
- Update ticket status
- Add comments or remarks
- Process tickets
- Resolve tickets

### Admin

Admins can:

- View all tickets
- Monitor ticket ageing
- Monitor SLA status
- Assign tickets to staff
- Change ticket priority/status
- View activity history
- Create staff accounts
- Monitor overall ticket status

## Demo Roles

### Creating an Admin

Registration creates a student account by default.

After registering, an administrator can be created by updating the user's role in MySQL:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'your-email@example.com';
```

Verify the role:

```sql
SELECT id, name, email, role
FROM users;
```

Log out and log in again to access the Admin Dashboard.

### Creating Staff

After logging in as Admin, use the Admin Dashboard to create staff accounts.

The newly created account can then be used to log in through the normal login page.

## Ticket Workflow

```text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↓
PENDING
  ↓
RESOLVED
  ↓
CLOSED
```

Students can close a ticket only after it has been marked as `RESOLVED`.

## Priority Levels

The system supports:

- **LOW**
- **MEDIUM**
- **HIGH**
- **URGENT**

Priority levels are used to determine the applicable SLA.

## SLA and Ageing

Ticket ageing represents the amount of time elapsed since the ticket was created.

For example:

```text
Age: 5h
SLA: Within SLA
```

If the ticket exceeds its configured SLA:

```text
Age: 30h
SLA: Breached
```

This helps staff and administrators identify tickets that require attention.

## Security

- Passwords are stored using password hashing.
- Role-based access controls restrict functionality based on user role.
- Students can access only their own tickets.
- Staff members can work with tickets assigned to them.
- `.env` is excluded from version control.
- Database credentials are not stored directly in the source code.

## Validation and Edge Cases

The application handles scenarios such as:

- Students attempting to access another student's ticket
- Unauthorized staff/admin pages
- Closing tickets before resolution
- Adding comments to closed tickets
- Ticket assignment
- SLA breach detection
- Ticket ageing calculation
- Invalid login credentials
- Duplicate email registration

## AI Usage Report

AI-assisted development was used during the development of this prototype.

The repository includes an AI usage report documenting:

- AI tool used
- Tasks given to AI
- Useful prompts
- AI-generated code
- Code modified by the developer
- Incorrect AI-generated output
- How errors were identified
- How errors were fixed
- Validation performed after AI-assisted development

## Future Enhancements

Possible future improvements include:

- Email notifications
- Automated SLA escalation
- Ticket search and filtering
- File attachments
- Advanced analytics and reports
- Notification system
- Password reset through email
- CSRF protection
- Production deployment
- API integration
- Automated testing

## License

This project was developed as a prototype for an academic/product engineering assignment.