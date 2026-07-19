# 🎓 College Enquiry Chatbot

A full-stack **College Enquiry Chatbot** web application built with **Flask**
(backend) and **HTML, CSS, JavaScript** (frontend). It answers 60+ common
college questions — admissions, courses, fees, hostel, placements, library,
transport, timings, scholarships, faculty, exams, attendance, and more —
through a modern, responsive chat interface.

---

## 1. Project Structure

```
College_Chatbot/
│── app.py                # Flask backend (routes + chatbot logic)
│── requirements.txt       # Python dependencies
│── README.md               # This file
│── data/
│   └── faqs.json            # 60+ Q&A entries the chatbot searches
│── templates/
│   ├── index.html            # Home page
│   └── chatbot.html          # Chat interface page
│── static/
│   ├── style.css              # All styling (theme, layout, chat bubbles)
│   └── script.js               # Chat logic (send, typing animation, etc.)
```

---

## 2. Requirements

- **Python 3.9 or newer**
- **pip** (comes bundled with Python)
- Internet connection is only needed the first time, to load the Google
  Fonts used for styling — the app itself runs fully offline.

The only Python package required is **Flask** (see `requirements.txt`).

---

## 3. Installation Steps

### Step 1 — Extract the project
Unzip / copy the `College_Chatbot` folder anywhere on your computer.

### Step 2 — Open a terminal inside the project folder
```bash
cd College_Chatbot
```

### Step 3 — (Recommended) Create a virtual environment
A virtual environment keeps this project's packages separate from the rest
of your system.

```bash
python3 -m venv venv
```

Activate it:
```bash
# Windows (Command Prompt / PowerShell):
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```
You'll know it worked because your terminal prompt will show `(venv)` at
the start of the line.

### Step 4 — Install the dependencies
```bash
pip install -r requirements.txt
```
This installs Flask (and its small set of internal dependencies).

---

## 4. How to Run the Project

```bash
python app.py
```

You should see terminal output similar to:
```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

Now open your web browser and visit:
```
http://127.0.0.1:5000/
```

- Click **"Start Chat"** or **"Chat Now"** to open the chatbot page.
- Type a question and press **Enter** (or click the send button).
- Try the suggested question chips for quick examples.

To stop the server: press `CTRL + C` in the terminal.

---

## 5. How the Chatbot Works

1. `app.py` loads all Q&A entries from `data/faqs.json` into memory when
   the server starts.
2. When you send a message, it's sent to the `/chat` route as a POST
   request containing JSON: `{ "message": "your question" }`.
3. The backend converts your message to **lowercase** and compares it
   against each FAQ's list of keywords (also lowercased) — this is what
   makes the search **ignore uppercase/lowercase differences**
   (e.g. "FEES", "Fees", and "fees" all match the same answer).
4. The FAQ with the most matching keywords is selected as the answer.
5. If no keywords match at all, the chatbot replies:
   > "Sorry, I don't have information about that. Please contact the college office."

### Adding a new question
Open `data/faqs.json` and add a new object to the `"faqs"` array, for example:
```json
{
  "id": 61,
  "category": "Fees",
  "keywords": ["exam fee", "examination fee"],
  "question": "Is there a separate examination fee?",
  "answer": "Yes, a nominal examination fee of ₹1000 per semester is charged separately from the tuition fee."
}
```
No code changes are needed — just restart the Flask server.

---

## 6. Troubleshooting Common Errors

### ❌ `ModuleNotFoundError: No module named 'flask'`
**Cause:** Flask isn't installed in the Python environment you're using to
run the app.
**Fix:**
1. Make sure your virtual environment is activated (you should see `(venv)`
   in your terminal prompt). If not, activate it (see Step 3 above).
2. Run:
   ```bash
   pip install -r requirements.txt
   ```
3. If you have multiple Python versions installed, try:
   ```bash
   python3 -m pip install -r requirements.txt
   python3 app.py
   ```

### ❌ `FileNotFoundError` / chatbot always replies with the fallback message / terminal shows "faqs.json not found"
**Cause:** The app can't find `data/faqs.json` — usually because the
`data` folder is missing, misspelled, or you're running `python app.py`
from the wrong directory.
**Fix:**
1. Confirm the folder structure matches exactly:
   `College_Chatbot/data/faqs.json` (the `data` folder must sit right next
   to `app.py`, not inside `templates` or `static`).
2. Always run the app from inside the `College_Chatbot` folder:
   ```bash
   cd College_Chatbot
   python app.py
   ```
3. Check `data/faqs.json` for typos — if the JSON is invalid (e.g. a
   missing comma or bracket), the terminal will print an error like
   `faqs.json contains invalid JSON`. You can validate the file using any
   online JSON validator, or Python:
   ```bash
   python -c "import json; json.load(open('data/faqs.json'))"
   ```
   If this command runs with no output, your JSON is valid.

### ❌ `Address already in use` / `Port 5000 is in use by another program`
**Cause:** Another program (or a previous run of this app) is already
using port 5000.
**Fix:** Either stop the other program, or change the port in `app.py`:
```python
app.run(debug=True, host="0.0.0.0", port=5001)
```
Then visit `http://127.0.0.1:5001/` instead.

### ❌ Page loads but has no styling / looks plain HTML
**Cause:** The browser can't find `style.css`, usually due to a typo in
the file path.
**Fix:** Make sure the file is exactly at `static/style.css` and that
`templates/index.html` / `chatbot.html` reference it with
`{{ url_for('static', filename='style.css') }}` (already set up correctly
in this project — only relevant if you renamed folders).

### ❌ Enter key doesn't send messages / buttons don't respond
**Cause:** `static/script.js` failed to load (check the browser console
with F12 for a red error).
**Fix:** Confirm `static/script.js` exists and hasn't been renamed, and
hard-refresh the page (`Ctrl+Shift+R` / `Cmd+Shift+R`) to clear the cache.

---

## 7. Future Enhancements

- Replace `data/faqs.json` with a MySQL/PostgreSQL database.
- Add an admin panel to manage FAQs without editing JSON directly.
- Add NLP-based matching (e.g. spaCy) for understanding paraphrased questions.
- Add multi-language support.
- Deploy to a cloud host (Render, Railway, PythonAnywhere) for public access.

---

## 8. Credits

Built as a demonstration project for **Greenfield Institute of Technology**
(a placeholder name) — update the college name and contact details in
`data/faqs.json` and the templates to match your real college.
