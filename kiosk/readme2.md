Perfect — here is a **clean, production-ready NiceGUI app** that includes:

✅ **Smooth fade animation** between URLs
✅ **Automatic fullscreen kiosk mode** (Chromium)

You get a rotating dashboard screen that looks like a professional kiosk display.

---

# ✅ **Final Code: NiceGUI + Smooth Fade + Chromium Kiosk Mode**

## 📌 `app.py`

```python
from nicegui import ui
import asyncio

# (URL, interval seconds)
URLS = [
    ("https://example.com", 8),
    ("https://news.ycombinator.com", 10),
    ("https://wikipedia.org", 6),
]

# container for iframe
iframe = ui.html().classes('fade-frame')

async def rotate_urls():
    while True:
        for url, interval in URLS:

            # fade out
            ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 0;")
            await asyncio.sleep(0.5)

            # update iframe HTML
            iframe.content = f'''
                <iframe src="{url}"
                        style="
                            position:fixed;
                            top:0; left:0;
                            width:100vw;
                            height:100vh;
                            border:none;
                        ">
                </iframe>
            '''

            # fade in
            ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 1;")
            await asyncio.sleep(interval)


@ui.page('/')
async def index():
    asyncio.create_task(rotate_urls())


# CSS for smooth fade animation
ui.add_head_html("""
<style>
.fade-frame {
    transition: opacity 0.5s ease-in-out;
}
</style>
""")

# AUTOSTART CHROMIUM IN KIOSK MODE
ui.run(
    port=8080,
    reload=False,
    dark=False,
    title='Kiosk Rotator',
    browser='chromium-browser --kiosk --start-fullscreen --noerrdialogs --incognito --disable-infobars --disable-session-crashed-bubble --overscroll-history-navigation=0 http://localhost:8080'
)
```

---

# 🧩 **How It Works**

### ✔ Fade Animation

Using a CSS class + JavaScript:

```css
transition: opacity 0.5s ease-in-out;
```

Before switching the iframe:

```python
ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 0;")
```

After updating:

```python
ui.run_javascript("document.querySelector('.fade-frame').style.opacity = 1;")
```

### ✔ Chromium Kiosk Mode

NiceGUI spawns Chromium automatically with:

```
--kiosk                      # fullscreen
--start-fullscreen           # force fullscreen
--noerrdialogs               # prevent popups
--incognito
--disable-infobars
--disable-session-crashed-bubble
```

Works on:

* Linux (Raspberry Pi, Ubuntu, Debian)
* Windows with `"chrome"` instead of `"chromium-browser"`
* macOS (small tweak needed)

---

# 📌 Want a Windows or Mac Version Too?

If you tell me your OS, I’ll give you the exact kiosk command:

* Windows → Chrome kiosk
* macOS → Chromium/Chrome kiosk
* Linux → Chromium kiosk (already set)

---

# ⚡ Want to add more features next?

I can add:

✔ Fade + slide animations
✔ Per-URL refresh timers
✔ Show loading spinner between pages
✔ Control panel for adding/editing URLs
✔ Read URLs from YAML file

Just tell me!
