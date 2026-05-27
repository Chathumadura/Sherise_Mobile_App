# SheRise Flutter Frontend

## Run

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

For Chrome/Web, keep backend running at `http://localhost:8000`.

Demo login:
- demo@sherise.com
- 123456

To override API URL:

```bash
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```
