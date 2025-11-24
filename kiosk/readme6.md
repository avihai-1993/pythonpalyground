Yes, but you need to make sure a few things are done correctly to support **Hebrew characters (UTF-8)** in your CSV files. By default, Python’s `csv` module reads files in the system default encoding, which may **break non-ASCII characters** like Hebrew.

Here’s how to make it safe:

---

### ✅ **CSV Reader Supporting Hebrew**

```python
import csv

def process_csv(file):
    # file is a file-like object from NiceGUI upload
    content = file.read().decode('utf-8')  # decode as UTF-8
    reader = csv.DictReader(content.splitlines())
    
    for row in reader:
        kiosk_name = row['kiosk_name']  # Hebrew works fine
        kiosk_description = row.get('kiosk_description', '')
        url = row['url']
        interval = int(row.get('interval_seconds', 10))
        position = int(row.get('position', 0))
        # save to DB
```

---

### 🔹 Notes:

1. Make sure your **CSV files are saved in UTF-8** (most modern editors like Excel, VSCode, or Google Sheets support this).
2. `file.read().decode('utf-8')` ensures Python correctly interprets Hebrew characters.
3. You can test with a sample CSV:

```csv
kiosk_name,kiosk_description,url,interval_seconds,position
מסך קבלה,קיר קבלה,http://example.com,10,0
מסך חדר ישיבות,חדר 1,http://example.org,7,1
```

4. This will store Hebrew names and descriptions correctly in SQLite.

---

If you want, I can **update your current CSV upload code** in `admin_ui.py` to fully support Hebrew, handle multiple files, and **prevent duplicates** automatically.

Do you want me to do that?
