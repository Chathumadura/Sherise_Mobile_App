# SheRise Real-World Full System - Final UI Version

This project is a **Flutter + FastAPI + SQLite** full-system starter for **SheRise**.
It was updated to match the **final UI direction** you provided, including:

- Splash screen
- Login screen
- Create account screen
- Home dashboard
- Safety & Emergency module UI
- Safety tips page
- Career & Skills course UI
- Profile page with profile picture add / update / delete
- Community and Legal CRUD screens

---

## Tech Stack

### Frontend
- Flutter
- HTTP
- Shared Preferences
- Image Picker

### Backend
- FastAPI
- SQLAlchemy ORM
- SQLite
- JWT Authentication
- Multipart upload for profile picture

---

## Main Features

### 1. Authentication & Profile
- Register
- Login
- Token-based session handling
- View profile
- Update profile
- Add profile picture
- Update profile picture
- Delete profile picture

### 2. Safety & Emergency
- Add emergency contact
- Update emergency contact
- Delete emergency contact
- Set primary contact
- Trigger SOS alert
- Safety tips page
- Important emergency numbers section

### 3. Career & Skills
- Search courses
- My Courses / All Courses filtering
- Add course
- Update course
- Delete course
- Course progress tracking
- Course image URL support
- Instructor / duration / category fields

### 4. Community
- Create community posts
- Update posts
- Delete posts
- Mentor management
- Add / update / delete mentors

### 5. Legal Help
- View legal rights
- Create complaint
- Update complaint
- Delete complaint

---

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload
```

Open Swagger docs:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

For Android emulator:

- Default API base URL: `http://10.0.2.2:8000`

For Chrome/Web:

- Default API base URL: `http://localhost:8000`

You can also override the API URL:

```bash
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```

---

## Demo Login

```text
Email: demo@sherise.com
Password: 123456
```

---

## Notes

- Profile images are stored in `backend/app/static/uploads/profile_pics`
- If you want to move to production, replace the secret key in `backend/app/security.py`
- This project is structured as a **real-world academic system starter**, so you can further extend notifications, real GPS location sharing, password reset, and enroll/payment features later.
