# SheRise Backend - FastAPI + SQLite

## Run

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000/docs

If you run the Flutter app on a physical Android device, use your PC's LAN IP as the API base URL, for example `http://192.168.1.10:8000`.

## Demo Login

- Email: demo@sherise.com
- Password: 123456

## Main Endpoints

- POST `/auth/register`
- POST `/auth/login`
- GET/PUT `/profile`
- POST/DELETE `/profile/photo`
- CRUD `/emergency-contacts`
- POST/GET/resolve `/sos`
- CRUD `/posts`
- CRUD `/mentors`
- CRUD `/courses`
- CRUD `/complaints`
- GET `/complaints/legal-rights`
