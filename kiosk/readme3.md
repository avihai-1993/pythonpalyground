Perfect! Let’s integrate **login and authentication** into your NiceGUI Kiosk Admin system. I’ll design it with:

✅ Persistent user accounts in SQLite
✅ Password hashing with **bcrypt**
✅ Admin-only access for kiosk management
✅ Session-based login (with NiceGUI)
✅ Optional: logout functionality

---

# 🏗️ Updated Architecture

```
kiosk_app/
│
├── app.py               # Main entry, runs NiceGUI and mounts pages
├── db.py                # SQLAlchemy models & database setup
├── auth.py              # Authentication utilities
├── admin_ui.py          # Admin interface
├── kiosk_player.py      # Fullscreen kiosk player
├── migrations/          # Alembic migration folder
├── requirements.txt
└── static/              # Optional CSS/JS
```

---

# 🗄️ **Database Models (db.py)**

Add a **User** table:

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///kiosk_app.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_admin = Column(Integer, default=1)  # 1=admin, 0=normal user

class Kiosk(Base):
    __tablename__ = "kiosks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    urls = relationship("KioskURL", back_populates="kiosk", cascade="all, delete-orphan", order_by="KioskURL.position")

class KioskURL(Base):
    __tablename__ = "kiosk_urls"
    id = Column(Integer, primary_key=True, index=True)
    kiosk_id = Column(Integer, ForeignKey("kiosks.id"))
    url = Column(String)
    interval_seconds = Column(Integer, default=10)
    position = Column(Integer, default=0)
    kiosk = relationship("Kiosk", back_populates="urls")

def init_db():
    Base.metadata.create_all(bind=engine)
```

---

# 🔐 **Authentication Utilities (auth.py)**

```python
from db import SessionLocal, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(username: str, password: str, is_admin=1):
    session = SessionLocal()
    hashed = pwd_context.hash(password)
    user = User(username=username, password_hash=hashed, is_admin=is_admin)
    session.add(user)
    session.commit()
    session.close()

def verify_user(username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    if user and pwd_context.verify(password, user.password_hash):
        return user
    return None
```

---

# 🖥️ **Login Page (app.py)**

```python
from nicegui import ui
from auth import verify_user
from admin_ui import admin_pages
from kiosk_player import run_kiosk

# Simple session dictionary
sessions = {}

@ui.page('/')
def login_page():
    username_input = ui.input(label='Username')
    password_input = ui.input(label='Password', password=True)

    def do_login():
        user = verify_user(username_input.value, password_input.value)
        if user:
            sessions['user'] = user.username
            ui.notify(f'Welcome {user.username}!', color='green')
            # redirect to admin
            ui.open('/admin/kiosks')
        else:
            ui.notify('Invalid username or password', color='red')

    ui.button('Login', on_click=do_login)
```

---

# 🛡️ **Protect Admin Pages**

Wrap admin routes in a **login check**:

```python
def require_login(page_func):
    def wrapper(*args, **kwargs):
        if 'user' not in sessions:
            ui.open('/')  # redirect to login
        else:
            return page_func(*args, **kwargs)
    return wrapper

# Example usage in admin_ui.py
@ui.page('/admin/kiosks')
@require_login
def admin_kiosks_page():
    admin_pages()
```

---

# ✅ **Optional: Logout**

```python
@ui.page('/logout')
def logout():
    sessions.pop('user', None)
    ui.notify('Logged out', color='blue')
    ui.open('/')
```

---

# ⚡ **Next Steps / Enhancements**

1. **Persistent sessions** (cookies instead of in-memory dict)
2. **Multiple user roles** (view-only, admin)
3. **Login timeout / session expiration**
4. **Password reset / creation page**
5. **Two-factor authentication** (optional)

---

I can now generate a **full working NiceGUI Kiosk Admin app with authentication**, including:

* Login page
* Admin-only access
* Kiosk CRUD
* URL CRUD
* Fullscreen kiosk player with fade rotation

Do you want me to generate that complete working code next?
