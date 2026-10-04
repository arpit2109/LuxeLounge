# LuxeLounge

A hospitality booking application with a React frontend and Django REST backend for rooms, reservations, user accounts, and 3D room content.

## Technologies

React 19, Create React App, Python, Django, Django REST Framework, and Simple JWT.

## Setup and run

Run the backend:

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
python -m pip install django djangorestframework djangorestframework-simplejwt
python manage.py migrate
python manage.py runserver
```

Run the frontend in a second terminal:

```bash
cd frontend
npm install
npm start
```

The backend has no requirements file in this checkout. Install any additional packages required by local settings separately, and keep credentials in environment variables.


## Django secret key

Set DJANGO_SECRET_KEY in the environment before starting the backend. Generate a local key with python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())". The settings fallback is for local development only; configure your own key for deployments.
