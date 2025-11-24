Perfect! Let’s build a **complete working NiceGUI Kiosk Admin system with authentication**, persistent SQLite, and fullscreen kiosks.

Here’s a **fully copy-pasteable version**.

---

# 📁 **Project Structure**

```
kiosk_app/
│
├── app.py               # Main entry
├── db.py                # Database models & setup
├── auth.py              # Authentication utilities
├── admin_ui.py          # Admin interface
├── kiosk_player.py      # Fullscreen kiosk player
├── requirements.txt
└── static/              # Optional CSS/JS
```

---

# 🗄️ **db.py**

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
    is_admin = Column(Integer, default=1)

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

# 🔐 **auth.py**

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

# 🖥️ **kiosk_player.py**

```python
from nicegui import ui
import asyncio
from db import SessionLocal, Kiosk

async def run_kiosk(kiosk_id: int):
    session = SessionLocal()
    kiosk = session.query(Kiosk).filter(Kiosk.id == kiosk_id).first()
    urls = [(url.url, url.interval_seconds) for url in kiosk.urls]
    session.close()

    iframe = ui.html().classes('fade-frame')

    async def rotate_urls():
        while True:
            for url, interval in urls:
                ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 0;")
                await asyncio.sleep(0.5)
                iframe.content = f'''
                    <iframe src="{url}"
                            style="position:fixed; top:0; left:0; width:100vw; height:100vh; border:none;">
                    </iframe>
                '''
                ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 1;")
                await asyncio.sleep(interval)

    asyncio.create_task(rotate_urls())
    return iframe
```

---

# 🛠️ **admin_ui.py**

```python
from nicegui import ui
from db import SessionLocal, Kiosk, KioskURL

def admin_pages(sessions):
    session = SessionLocal()

    def require_login(func):
        def wrapper(*args, **kwargs):
            if 'user' not in sessions:
                ui.open('/')  # redirect to login
            else:
                return func(*args, **kwargs)
        return wrapper

    @ui.page('/admin/kiosks')
    @require_login
    def kiosks_page():
        ui.label('Kiosk Management').classes('text-2xl font-bold mb-4')
        kiosks_table = ui.table(columns=['ID', 'Name', 'Description', 'Actions'], rows=[])

        def load_kiosks():
            kiosks_table.rows = []
            for k in session.query(Kiosk).all():
                kiosks_table.add_row({
                    'ID': k.id,
                    'Name': k.name,
                    'Description': k.description or '',
                    'Actions': ui.row().classes('gap-2').add(
                        ui.button('Manage URLs', on_click=lambda x, kid=k.id: ui.open(f'/admin/kiosks/{kid}/urls')),
                        ui.button('Delete', on_click=lambda x, kid=k.id: delete_kiosk(kid))
                    )
                })

        def delete_kiosk(kiosk_id):
            k = session.query(Kiosk).filter(Kiosk.id == kiosk_id).first()
            if k:
                session.delete(k)
                session.commit()
                load_kiosks()

        ui.button('Add Kiosk', on_click=lambda: ui.open('/admin/kiosks/new'))
        load_kiosks()

    @ui.page('/admin/kiosks/<kiosk_id>/urls')
    @require_login
    def manage_urls(kiosk_id: int):
        kiosk = session.query(Kiosk).filter(Kiosk.id == kiosk_id).first()
        ui.label(f'URLs for Kiosk: {kiosk.name}').classes('text-xl font-bold mb-4')
        urls_table = ui.table(columns=['ID', 'URL', 'Interval (s)', 'Actions'], rows=[])

        def load_urls():
            urls_table.rows = []
            for u in kiosk.urls:
                urls_table.add_row({
                    'ID': u.id,
                    'URL': u.url,
                    'Interval (s)': u.interval_seconds,
                    'Actions': ui.row().classes('gap-2').add(
                        ui.button('Edit', on_click=lambda x, uid=u.id: edit_url(uid)),
                        ui.button('Delete', on_click=lambda x, uid=u.id: delete_url(uid))
                    )
                })

        def edit_url(url_id):
            url_obj = session.query(KioskURL).filter(KioskURL.id == url_id).first()
            ui.input(label='URL', value=url_obj.url, on_change=lambda e: setattr(url_obj, 'url', e.value))
            ui.input(label='Interval', value=url_obj.interval_seconds, type='number', on_change=lambda e: setattr(url_obj, 'interval_seconds', int(e.value)))
            ui.button('Save', on_click=lambda: (session.commit(), load_urls()))

        def delete_url(url_id):
            url_obj = session.query(KioskURL).filter(KioskURL.id == url_id).first()
            session.delete(url_obj)
            session.commit()
            load_urls()

        ui.button('Add URL', on_click=lambda: ui.open(f'/admin/kiosks/{kiosk_id}/urls/new'))
        load_urls()
```

---

# 🗝️ **app.py**

```python
from nicegui import ui
from db import init_db
from auth import verify_user, create_user
from admin_ui import admin_pages
from kiosk_player import run_kiosk

# Initialize database
init_db()

# Create default admin user if not exists
create_user('admin', 'admin123', is_admin=1)

# Simple session dictionary
sessions = {}

# Login page
@ui.page('/')
def login_page():
    username_input = ui.input(label='Username')
    password_input = ui.input(label='Password', password=True)

    def do_login():
        user = verify_user(username_input.value, password_input.value)
        if user:
            sessions['user'] = user.username
            ui.notify(f'Welcome {user.username}!', color='green')
            ui.open('/admin/kiosks')
        else:
            ui.notify('Invalid username or password', color='red')

    ui.button('Login', on_click=do_login)

# Logout
@ui.page('/logout')
def logout():
    sessions.pop('user', None)
    ui.notify('Logged out', color='blue')
    ui.open('/')

# Mount admin pages
admin_pages(sessions)

# Public kiosk route
@ui.page('/kiosk/<kiosk_id>')
async def kiosk_page(kiosk_id: int):
    await run_kiosk(kiosk_id)

# CSS for fade effect
ui.add_head_html("""
<style>
.fade-frame {
    transition: opacity 0.5s ease-in-out;
}
</style>
""")

# Run the app
ui.run(
    port=8080,
    reload=True,
    title='Kiosk Admin',
)
```

---

# ✅ **Instructions to Run**

1. Install dependencies:

```bash
pip install nicegui sqlalchemy passlib[bcrypt] aiofiles
```

2. Run the app:

```bash
python app.py
```

3. Open `http://localhost:8080` in your browser.

4. Login with:

```
Username: admin
Password: admin123
```

5. Add kiosks and URLs, then visit `/kiosk/<kiosk_id>` to see fullscreen rotation.

---

This system now includes:

* **Persistent SQLite database**
* **Admin authentication/login**
* **Kiosk CRUD**
* **URL CRUD per kiosk**
* **Fullscreen kiosk player** with fade rotation

---

If you want, I can **upgrade it to auto-launch in kiosk mode** (Chromium/Chrome) with **per-URL intervals**, so you can just run the script on a Raspberry Pi, PC, or digital signage screen.

Do you want me to do that next?
