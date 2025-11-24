Perfect! We’ll go with **persistent SQLite with migrations**. Here’s the **full plan and code structure** for your NiceGUI Kiosk Admin system.

We’ll use **SQLAlchemy** for database ORM and **Alembic** for migrations (optional but recommended).

---

# 🏗️ **Project Structure**

```
kiosk_app/
│
├── app.py               # Main entry, starts NiceGUI and mounts admin & kiosks
├── db.py                # SQLAlchemy models & database setup
├── admin_ui.py          # Admin interface (Kiosk & URL management)
├── kiosk_player.py      # Fullscreen kiosk player logic
├── migrations/          # Alembic migration folder
├── requirements.txt
└── static/              # Optional: CSS/JS files
```

---

# 🗄️ **Database Models (db.py)**

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///kiosk_app.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

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

# 🖥️ **Kiosk Player (kiosk_player.py)**

```python
from nicegui import ui
import asyncio
from db import SessionLocal, Kiosk, KioskURL

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

# 🛠️ **Admin Interface (admin_ui.py)**

```python
from nicegui import ui
from db import SessionLocal, Kiosk, KioskURL

def admin_pages():
    session = SessionLocal()

    with ui.page('/admin/kiosks'):
        ui.label('Kiosk Management').classes('text-2xl font-bold mb-4')
        kiosks_table = ui.table(
            columns=['ID', 'Name', 'Description', 'Actions'],
            rows=[],
            row_key='id',
        )

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

    # URL Management page per kiosk
    @ui.page('/admin/kiosks/<kiosk_id>/urls')
    def manage_urls(kiosk_id: int):
        kiosk = session.query(Kiosk).filter(Kiosk.id == kiosk_id).first()
        ui.label(f'URLs for Kiosk: {kiosk.name}').classes('text-xl font-bold mb-4')
        urls_table = ui.table(
            columns=['ID', 'URL', 'Interval (s)', 'Actions'],
            rows=[]
        )

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

# ⚡ **Main Application (app.py)**

```python
from nicegui import ui
from db import init_db
import admin_ui
from kiosk_player import run_kiosk

init_db()  # create tables

# mount admin pages
admin_ui.admin_pages()

# public kiosk route
@ui.page('/kiosk/<kiosk_id>')
async def kiosk_page(kiosk_id: int):
    await run_kiosk(kiosk_id)

ui.run(
    port=8080,
    reload=True,
    title='Kiosk Admin',
    dark=False,
)
```

---

# ✅ **Next Steps / Optional Features**

1. **Alembic migration setup** (for versioning)
2. **Authentication for admin**
3. **Drag-and-drop URL ordering**
4. **Test URLs directly in iframe from admin**
5. **Live refresh without page reload**

---

I can now generate a **fully working, copy-pasteable single project** with:

* Admin interface
* Persistent SQLite DB
* Fullscreen kiosk mode
* URL rotation with fade
* Add/edit/delete kiosks and URLs

Do you want me to do that next?
