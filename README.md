Circular Generator Web App

A Flask-based web application that allows authenticated users to create and download professional circulars in PDF format. Useful for schools, colleges, departments, and organizations to quickly generate official notices.

Features

- User Signup & Login with session handling
- Secure password storage using hashing
- Dashboard view with user-specific content
- Form to generate circulars with title, date, and content
- Auto-generation of PDF with proper formatting
- Signature section for "HOD of the Department"
- Downloadable circulars
- Minimal and clean user interface

Technologies Used

- Python 3
- Flask
- SQLite
- FPDF (for PDF generation)
- HTML & CSS (with Roboto font)
- Jinja2 templating


circular-generator-app/
│
├── templates/
│ ├── login.html
│ ├── signup.html
│ ├── dashboard.html
│
├── static/
│ └── (optional for styles/images)
│
├── generated/
│ └── circular_username.pdf
│
├── app.py
├── users.db
└── README.md
