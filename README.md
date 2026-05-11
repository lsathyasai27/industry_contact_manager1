
# Industry Level User Authenticated Contact Manager

A polished Django contact management app with user authentication, contact portfolios, tags, notes, CSV import/export, and API endpoints.

## Features

- User-specific contacts with login, registration, and profile access
- Contact portfolio cards with company, job title, category, and favorite status
- Tags and history notes for every contact
- Search across name, company, email, address, and tags
- Import and export contacts via CSV
- Simple JSON API endpoints for contacts
- Admin site support for contacts, tags, and notes
- Basic unit tests for search and API behavior

## Setup

```bash
pip install django
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the app at:
http://127.0.0.1:8000/login/

## CSV import format

Use headers:

`name,company,job_title,phone,email,address,birthday,category,favorite,tags`
