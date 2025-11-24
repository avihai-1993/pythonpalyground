
Perfect! Let’s upgrade the system step by step. Here’s what we’ll do:

1. **Auto-launch kiosks in Chromium/Chrome in fullscreen/kiosk mode**
2. **Admin CSV upload** to add multiple kiosks & URLs at once
3. **Dockerfile** based on Python 3.11
4. **Docker Compose** to run the app

---

# 1️⃣ **Auto-launch kiosk in fullscreen**

We can use **NiceGUI’s `browser` parameter** to launch Chromium in kiosk mode:

```python
ui.run(
    port=8080,
    reload=True,
    title='Kiosk Admin',
    browser='chromium-browser --kiosk --start-fullscreen --noerrdialogs --incognito --disable-infobars --disable-session-crashed-bubble --overscroll-history-navigation=0 http://localhost:8080'
)
```

* On Windows: replace `chromium-browser` with `chrome`
* On macOS: replace with `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome`

---

# 2️⃣ **CSV Upload Logic**

We’ll allow the admin to **upload multiple CSV files**. Each CSV can contain:

```
kiosk_name,kiosk_description,url,interval_seconds,position
```

### Add this in `admin_ui.py`:

```python
import csv
from nicegui import ui
from db import SessionLocal, Kiosk, KioskURL

def csv_upload_page():
    session = SessionLocal()

    def process_csv(file):
        reader = csv.DictReader(file)
        for row in reader:
            # Get or create kiosk
            kiosk = session.query(Kiosk).filter(Kiosk.name == row['kiosk_name']).first()
            if not kiosk:
                kiosk = Kiosk(name=row['kiosk_name'], description=row.get('kiosk_description', ''))
                session.add(kiosk)
                session.commit()
            # Add URL
            url_entry = KioskURL(
                kiosk_id=kiosk.id,
                url=row['url'],
                interval_seconds=int(row.get('interval_seconds', 10)),
                position=int(row.get('position', 0))
            )
            session.add(url_entry)
        session.commit()
        ui.notify("CSV processed successfully", color='green')

    with ui.page('/admin/csv-upload'):
        ui.label("Upload CSV files to add kiosks and URLs").classes('text-xl font-bold mb-4')
        ui.upload(on_upload=process_csv, multiple=True)
```

* `multiple=True` allows **multiple CSVs at once**
* Each CSV can add new kiosks or append URLs to existing kiosks

---

# 3️⃣ **Dockerfile**

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "app.py"]
```

---

# 4️⃣ **Docker Compose**

```yaml
version: '3.9'

services:
  kiosk_app:
    build: .
    container_name: kiosk_app
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/kiosk_app.db  # persist SQLite DB
    environment:
      - PYTHONUNBUFFERED=1
    stdin_open: true
    tty: true
```

---

# 5️⃣ **requirements.txt**

```
nicegui
sqlalchemy
passlib[bcrypt]
aiofiles
```

---

# ✅ **Next Steps / Notes**

* You can now deploy this system in Docker.
* Admin can upload **multiple CSVs**, each with multiple kiosks & URLs.
* The kiosk player still rotates URLs with fade transitions.
* If you want, I can **add the logic to automatically launch a specified kiosk on container start** in fullscreen mode, so it behaves like a **digital signage screen**.

Do you want me to do that next?
