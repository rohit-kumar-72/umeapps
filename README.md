# Django Project
![umeapps onrender com_api](https://github.com/user-attachments/assets/2c8bc3f7-c7e7-4d20-bb3d-e25d046c36f3)

A Django-based web API hosted on Render.

## 🌐 Live URL

👉 [https://umeapps.onrender.com/api](https://umeapps.onrender.com/api)

## 🚀 Features

- Django REST API
- PostgreSQL database
- Gemini API integration
- Deploy-ready on Render

## 📆 Repository

[GitHub - rohit-kumar-72/umeapps](https://github.com/rohit-kumar-72/umeapps)

## 🛆 Requirements

- Python 3.11
- PostgreSQL database

## 🔧 Environment Variables

Make sure to set the following environment variables:

| Variable   | Description                  |
|------------|------------------------------|
| `DB_URL`   | Your PostgreSQL database URL |
| `API_KEY`  | Gemini API key               |

## 🛠️ Installation

```bash
git clone https://github.com/rohit-kumar-72/umeapps.git
cd umeapps
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Run Migrations & Server

```bash
python manage.py migrate
python manage.py runserver
```

## 📂 Static Files

To collect static files for production:

```bash
python manage.py collectstatic --noinput
```

