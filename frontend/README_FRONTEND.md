# SheRise Flutter Frontend

## Run

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

For Chrome/Web, keep backend running at `http://localhost:8000`.

For Android emulator, the app uses `http://10.0.2.2:8000` by default.
For a physical Android phone, run the backend on `0.0.0.0` and pass your PC's LAN IP:

```bash
flutter run --dart-define=API_BASE_URL=http://<your-pc-ip>:8000
```

Demo login:
- demo@sherise.com
- 123456

To override API URL:

```bash
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```
