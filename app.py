from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered."
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password_input):
            session['email'] = email
            return redirect('/dashboard')  # Replace with circular generator page
        else:
            return "Invalid email or password."
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return render_template('dashboard.html', email=session['email'])
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
from fpdf import FPDF
import os
from flask import send_file

@app.route('/create_circular', methods=['GET', 'POST'])
def create_circular():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = request.form['date']

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Circular", ln=True, align='C')

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"Title: {title}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, f"Date: {date}\n\n{content}")

        filename = f"circular_{session['email'].split('@')[0]}.pdf"
        filepath = os.path.join("generated", filename)
        os.makedirs("generated", exist_ok=True)
        pdf.output(filepath)

        return send_file(filepath, as_attachment=True)

    return'''
<!DOCTYPE html>
<html>
<head>
    <title>Create Circular</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .circular-form {
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
        }
        .circular-form h2 {
            margin-bottom: 20px;
            text-align: center;
            color: #333;
        }
        .circular-form label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
        }
        .circular-form input[type="text"],
        .circular-form input[type="date"],
        .circular-form textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 14px;
        }
        .circular-form input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }
        .circular-form input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="circular-form">
        <h2>Create a Circular</h2>
        <form method="post">
            <label for="title">Title:</label>
            <input type="text" name="title" required>

            <label for="date">Date:</label>
            <input type="date" name="date" required>

            <label for="content">Content:</label>
            <textarea name="content" rows="8" required></textarea>

            <input type="submit" value="Generate Circular">
        </form>
    </div>
</body>
</html>
'''



if __name__ == '__main__':
    app.run(debug=True)
