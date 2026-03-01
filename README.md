# 📝 Task Management API

A professional, secure, and fully documented RESTful API built with **Django Rest Framework (DRF)**. This application allows users to manage personal tasks while providing administrative oversight and real-time productivity analytics.

## ✨ Key Features
* **User Ownership**: Strict data isolation—users can only see and manage their own tasks.
* **Admin Dashboard**: Staff users have full visibility and management capabilities across all tasks.
* **Productivity Analytics**: A dedicated `/api/tasks/stats/` endpoint providing completion rates and task counts.
* **Interactive Documentation**: Fully integrated **Swagger UI** and **Redoc** for easy API testing.
* **Advanced Filtering**: Built-in support for searching (title/description), ordering (by date), and status filtering.

---

## 🛠️ Tech Stack
* **Backend**: Django 5.x & Django Rest Framework (DRF)
* **Database**: SQLite (Development)
* **Documentation**: `drf-spectacular` (OpenAPI 3.0)
* **Testing**: Python Unittest / APITestCase

---

## 📥 Installation & Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kanishkaverma26/Task-Management-App.git
   cd Task-Management-App

2. **Create a Virtual Environment**
   ```bash
     python -m venv .venv

3. **Activate on Windows**
   ```bash
    .venv\Scripts\activate
   
4. **Install Dependencies**
   ```bash
    pip install -r requirements.txt
   
5. **Run Migrations & Start Server**
   ```bash
    python manage.py migrate
    python manage.py runserver

Once the server is running, you can access the interactive API Documentation (Swagger UI) at:
http://127.0.0.1:8000/api/docs/
--
### 👤 Administrative Access

To manage the database directly and view all user tasks, you should create a Superuser:

1. **Create the Superuser:**
   ```bash
   python manage.py createsuperuser
Follow the prompts to set a username, email, and password.

2. **Access the Admin Panel:**
Once the server is running, navigate to:
http://127.0.0.1:8000/admin/

Log in with your superuser credentials to manage Users and Tasks directly.
---

## 🧪 Testing
The project includes a modular test suite. To run all tests:
   ```bash
   python manage.py test
