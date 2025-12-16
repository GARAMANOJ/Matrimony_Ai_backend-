# 💍 AI Matrimony Backend

A backend service for an **AI-powered Matrimony Application** built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.  
This project handles user authentication, profiles, preferences, interests, and match logic.

---

## 🚀 Tech Stack

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async)
- **Authentication:** JWT (OAuth2)
- **Password Hashing:** bcrypt, passlib
- **Server:** Uvicorn
- **Language:** Python 3.11

---

## 📂 Project Structure

```text
app/
├── api/
│   └── routes/
│       ├── auth.py
│       ├── profile.py
│       ├── preference.py
│       ├── interest.py
│       └── match.py
├── core/
│   ├── config.py
│   └── database.py
├── models/
│   ├── user.py
│   ├── profile.py
│   ├── preference.py
│   ├── interest.py
│   └── match.py
├── schemas/
├── main.py
└── deps.py
✨ Features

🔐 User Authentication (JWT)

👤 User Profile Management

❤️ Partner Preferences

🎯 Interests & Matching

🤖 AI-based Match Logic (Planned)

🧪 Development Notes

Async SQLAlchemy used for better performance

Modular structure for scalability

Docker support coming soon

👨‍💻 Author

Manoj Gara
GitHub: https://github.com/GARAMANOJ
