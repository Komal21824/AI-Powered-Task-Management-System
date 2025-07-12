from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import pandas as pd
import os
import datetime
import pickle
import sqlite3
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load ML models
task_model = pickle.load(open('task_classifier.pkl', 'rb'))
priority_model = pickle.load(open('priority_classifier.pkl', 'rb'))

# Paths
HISTORY_FILE = 'history/task_history.csv'
DB_FILE = 'users.db'

# Ensure files/folders
os.makedirs('history', exist_ok=True)
if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=['Date', 'Task', 'Category', 'Priority', 'DueDate', 'Status']).to_csv(HISTORY_FILE, index=False)

# DB Setup
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
init_db()

class User(UserMixin):
    def __init__(self, id_, username):
        self.id = id_
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE id=?", (user_id,))
        row = c.fetchone()
        return User(row[0], row[1]) if row else None

@app.route('/')
@login_required
def home():
    df = pd.read_csv(HISTORY_FILE)

    # Filters
    category_filter = request.args.get('category', '')
    priority_filter = request.args.get('priority', '')
    if category_filter:
        df = df[df['Category'].str.contains(category_filter)]
    if priority_filter:
        df = df[df['Priority'] == priority_filter]

    category_counts = df['Category'].value_counts().to_dict()
    priority_counts = df['Priority'].value_counts().to_dict()
    categories = pd.read_csv(HISTORY_FILE)['Category'].dropna().unique()
    priorities = pd.read_csv(HISTORY_FILE)['Priority'].dropna().unique()

    return render_template('index.html',
        tasks=df.to_dict(orient='records'),
        category_data=category_counts,
        priority_data=priority_counts,
        categories=categories,
        priorities=priorities,
        current_category=category_filter,
        current_priority=priority_filter
    )

@app.route('/submit', methods=['POST'])
@login_required
def submit_task():
    task = request.form['task']
    due_date = request.form['due_date']
    priority = request.form['priority']
    category = ', '.join(request.form.getlist('category'))
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.read_csv(HISTORY_FILE)
    df = pd.concat([df, pd.DataFrame([{
        'Date': date,
        'Task': task,
        'Category': category,
        'Priority': priority,
        'DueDate': due_date,
        'Status': 'Pending'
    }])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

    return redirect(url_for('home'))

@app.route('/update_status/<int:task_index>/<string:new_status>')
@login_required
def update_status(task_index, new_status):
    df = pd.read_csv(HISTORY_FILE)
    if 0 <= task_index < len(df):
        df.at[task_index, 'Status'] = new_status
        df.to_csv(HISTORY_FILE, index=False)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
            row = c.fetchone()
            if row and row[2] == password:
                login_user(User(row[0], row[1]))
                return redirect(url_for('home'))
            flash("Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash("Registration successful. Please login.")
                return redirect(url_for('login'))
            except:
                flash("Username already exists.")
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/export/csv')
@login_required
def export_csv():
    return send_file(HISTORY_FILE, as_attachment=True)

@app.route('/export/pdf')
@login_required
def export_pdf():
    df = pd.read_csv(HISTORY_FILE)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Task Report", ln=True, align='C')
    pdf.ln(10)

    for col in ['Date', 'Task', 'Category', 'Priority', 'DueDate', 'Status']:
        pdf.cell(32, 10, col, border=1, align='C')
    pdf.ln()

    for _, row in df.iterrows():
        pdf.cell(32, 10, str(row['Date'])[:16], border=1)
        pdf.cell(32, 10, row['Task'][:10], border=1)
        pdf.cell(32, 10, row['Category'][:10], border=1)
        pdf.cell(32, 10, row['Priority'], border=1)
        pdf.cell(32, 10, row['DueDate'], border=1)
        pdf.cell(32, 10, row['Status'], border=1)
        pdf.ln()

    output_path = 'history/task_report.pdf'
    pdf.output(output_path)
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
