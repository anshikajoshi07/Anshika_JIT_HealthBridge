# HealthBridge - Healthcare Management System

This is a Django-based healthcare management application.

## Project Structure

```
healthcare/
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── healthcare/              # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __init__.py
├── health/                  # Health app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   └── __init__.py
├── templates/               # Project templates
│   ├── base.html
│   └── health/
│       └── index.html
├── static/                  # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
└── media/                   # User-uploaded files
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application:
   - Home: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## Apps

### Health
Main app for health-related features including health records management.
