## TaskIQ

**Your Smart Assistant for Smarter Task Management**

TaskIQ is an AI-powered task management system that intelligently classifies your tasks by category and priority. It features a modern dark-themed UI, visual analytics, login system, and smart productivity tools designed to streamline your workflow.

## Features

- 🧠 Smart auto-tagging using ML for task type and priority
- 📅 Due date picker to schedule tasks
- 📊 Interactive dashboard with Pie & Bar charts
- 🔍 Search bar and filters
- 🔐 Secure login and registration system
- 🧩 Project boards and task filters
- 📁 Export tasks to CSV or PDF
- 📱 Fully responsive and mobile-friendly design
- ✉️ *(Coming Soon)* Email reminders for task deadlines

##  Tech Stack

- **Backend**: Python, Flask, Scikit-learn (for ML)
- **Frontend**: HTML, CSS (Dark Theme), JavaScript, Chart.js
- **Authentication**: Flask-Login
- **Exporting**: CSV/PDF with Python tools


##  Project Structure
TaskIQ/
├── app.py
├── train_model.py
├── static/
│ ├── style.css
│ └── chart.js
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── dashboard.html
│ ├── login.html
│ └── register.html
├── models/
│ ├── task_classifier.pkl
│ └── priority_classifier.pkl
├── dataset/
   └── large_task_dataset.csv
