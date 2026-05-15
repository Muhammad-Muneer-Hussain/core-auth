# Core-Auth
### Advanced Asynchronous Backend Authentication System (Enterprise Core)

---

## 📌 Project Overview
**Core-Auth** is a high-performance asynchronous authentication and authorization backend built using **FastAPI, PostgreSQL, Redis, JWT, and SQLAlchemy**. 

The project follows enterprise backend engineering principles including:
* **Fully asynchronous architecture** (Non-blocking I/O)
* **JWT authentication lifecycle** (Access & Refresh token separation)
* **Redis-based token revocation** (Secure logout)
* **Zero-Trust request validation**
* **Dependency injection** security layer
* **Automated CI quality pipeline** via GitHub Actions
* **Secure password hashing** using bcrypt
* **Async database operations** via SQLAlchemy + asyncpg

> This project was implemented according to the provided enterprise specification document.

---

## 🛠️ Tech Stack

| Purpose | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI |
| **Database** | PostgreSQL |
| **Cache / Blacklist** | Redis |
| **ORM** | SQLAlchemy Async |
| **JWT Authentication** | PyJWT |
| **Password Hashing** | Passlib / bcrypt |
| **Async DB Driver** | asyncpg |
| **Testing** | Pytest |
| **Async Testing** | pytest-asyncio |
| **Linting** | Ruff |
| **Security Auditing** | Bandit |
| **CI Pipeline** | GitHub Actions |

---

## 🚀 Core Features

### ⚡ Asynchronous Architecture
* Fully async FastAPI endpoints.
* Non-blocking PostgreSQL operations.
* Non-blocking Redis operations.
* Async dependency injection & integration testing.

### 🔑 JWT Authentication System
The system implements a dual-token architecture:
1. **Access Token:** Short lifespan, used for protected API access, signed using `ACCESS_SECRET`.
2. **Refresh Token:** Long lifespan, used to rotate sessions, signed using `REFRESH_SECRET`.

### 🛑 Redis Blacklist System
JWT tokens are naturally stateless. To support secure logout and token revocation, Redis is used as an in-memory blacklist layer.
* When users logout, the current token is blacklisted.
* Token remains blocked until expiration.
* Redis **TTL (Time-To-Live)** automatically removes expired blacklist entries.

### 🛡️ Zero-Trust Validation
Every protected request independently validates:
* JWT signature & Token expiry
* Token type enforcement
* Redis blacklist state
* User existence & active status

---

## 🛣️ API Endpoints

### Authentication Routes
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Authenticate user & return tokens |
| `POST` | `/auth/refresh` | Rotate refresh token |
| `POST` | `/auth/logout` | Revoke active token (Blacklist) |

### User Routes
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/users/me` | Get authenticated user profile |

---

## 📋 Response Schemas

### 1. UserRegistrationResponse
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-05-16T10:00:00Z"
}
2. TokenExchangeResponse
{
  "access_token": "JWT_TOKEN",
  "refresh_token": "JWT_TOKEN",
  "token_type": "bearer"
}
3. StandardActionResponse
{
  "detail": "Revocation complete"
}
📂 Project Structure
core-auth/
│
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── auth.py
│   │       └── users.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── redis/
│   │   └── client.py
│   │
│   ├── schemas/
│   │   ├── token.py
│   │   └── user.py
│   │
│   └── main.py
│
├── tests/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── .env
└── README.md

⚙️ Installation & Setup

1. Clone Repository
git clone <repo-url>
cd core-auth

2. Create Virtual Environment

python -m venv venv

3. Activate Virtual Environment
Windows:
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Environment Variables
Create a .env file in the root directory:
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/coreauth
REDIS_URL=redis://localhost:6379

ACCESS_SECRET=your_access_secret
REFRESH_SECRET=your_refresh_secret

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

6. Run Application
uvicorn app.main:app --reload
Swagger Documentation: Open http://127.0.0.1:8000/docs

🔄 Authentication Flow
Register User: POST /auth/registerLogin User: POST /auth/login $\rightarrow$ Returns Access & Refresh Token.
Authorize Swagger: Use the Authorize button in Swagger UI.
Access Protected Route: GET /users/me
Refresh Session: POST /auth/refresh
Logout User: POST /auth/logout

Zero-Trust Validation: Attempting to reuse a blacklisted token returns 401 Unauthorized.

🛡️ Security & Quality Gates
GitHub Actions CI Pipeline
The project includes automated CI verification with the following stages:

Environment spawn

PostgreSQL & Redis startup

Ruff lint validation

Bandit security scanning

Async integration testing

Quality Commands
Run Tests: pytest

Linting Check: ruff check .

Security Audit: bandit -r app

🧑‍💻 Author
Muhammad Muneer Hussain

📄 License
This project is developed for educational, enterprise backend engineering, and portfolio demonstration purposes.

