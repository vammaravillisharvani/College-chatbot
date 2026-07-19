"""
=====================================================================
 College Enquiry Chatbot - app.py
=====================================================================
 Main Flask backend file.

 What this file does:
 1. Starts a Flask web server.
 2. Loads FAQ data (60 questions + keywords + answers) from
    data/faqs.json.
 3. Defines routes for the Home page, the Chatbot page, and the
    chat API endpoint.
 4. Implements case-insensitive keyword matching to find the best
    matching answer for whatever the user types.

 Written in a beginner-friendly style with comments explaining every
 important section, so it's easy to read, modify, and explain.
=====================================================================
"""

# ---------------------------------------------------------------
# STEP 1: Import required libraries
# ---------------------------------------------------------------
from flask import Flask, render_template, request, jsonify   # Flask core tools
import json                                                   # To read faqs.json
import os                                                     # To build safe file paths
from datetime import datetime                                 # To timestamp chat messages

# ---------------------------------------------------------------
# STEP 2: Create the Flask application object
# ---------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------
# STEP 3: Build a safe, absolute path to data/faqs.json
# ---------------------------------------------------------------
# Normally, os.path.dirname(os.path.abspath(__file__)) is enough to
# find the project folder no matter where "python app.py" is run
# from. BUT some environments (for example the Pydroid3 app on
# Android) run your code from a temporary internal file, so
# __file__ does NOT point at your real project folder in those
# cases. To handle that, we check a few likely locations in order
# and use whichever one actually contains faqs.json.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_WORKING_DIR = os.getcwd()

CANDIDATE_BASE_DIRS = [
    SCRIPT_DIR,                                    # normal case: folder app.py lives in
    CURRENT_WORKING_DIR,                            # folder the terminal was in when you ran "python app.py"
    os.path.join(CURRENT_WORKING_DIR, "College_Chatbot"),  # in case cwd is one level above the project
]


def find_faq_file_path():
    """
    Looks for data/faqs.json in each candidate base folder, in order,
    and returns the first path that actually exists. If none of them
    work, it returns the original expected path so the error message
    still tells you where it looked.
    """
    for base_dir in CANDIDATE_BASE_DIRS:
        candidate_path = os.path.join(base_dir, "data", "faqs.json")
        if os.path.isfile(candidate_path):
            return candidate_path
    # Nothing found -> return the "expected" path so the error is informative
    return os.path.join(SCRIPT_DIR, "data", "faqs.json")


FAQ_FILE_PATH = find_faq_file_path()


def load_faq_data():
    """
    Reads data/faqs.json and returns it as a Python dictionary.
    If the file is missing or contains invalid JSON, we print a
    clear error message (including every folder we checked) and
    return a safe empty structure so the server does not crash.
    """
    try:
        with open(FAQ_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] faqs.json not found. Looked in:")
        for base_dir in CANDIDATE_BASE_DIRS:
            print(f"        - {os.path.join(base_dir, 'data', 'faqs.json')}")
        print("        Make sure the 'data' folder with faqs.json sits right next to app.py,")
        print("        and that you opened/ran app.py directly from inside that project folder")
        print("        (in Pydroid3: use the folder icon to browse to and open app.py in place,")
        print("        rather than pasting code into a new blank file).")
        return {"college_name": "College", "faqs": [], "suggested_questions": [],
                "fallback_answer": "Sorry, I don't have information about that. Please contact the college office."}
    except json.JSONDecodeError as error:
        print(f"[ERROR] faqs.json contains invalid JSON: {error}")
        return {"college_name": "College", "faqs": [], "suggested_questions": [],
                "fallback_answer": "Sorry, I don't have information about that. Please contact the college office."}


# Load the FAQ knowledge base into memory ONCE when the server starts.
# This keeps every chat request fast, since the file is not re-read
# every time a user sends a message.
faq_data = load_faq_data()


# ---------------------------------------------------------------
# STEP 4: Chatbot "brain" -> Case-Insensitive Keyword Matching
# ---------------------------------------------------------------
def get_bot_response(user_message):
    """
    Finds the best FAQ answer for the user's message.

    HOW IT WORKS:
    1. Convert the user's message to lowercase so the search
       IGNORES uppercase/lowercase differences
       (e.g. "FEES", "Fees", and "fees" are all treated the same).
    2. Loop through every FAQ entry and count how many of its
       keywords appear inside the user's (lowercased) message.
    3. The FAQ with the highest keyword match count wins and its
       answer is returned.
    4. If NOTHING matches, return the exact fallback message
       required by the project spec.
    """
    if not user_message or not user_message.strip():
        return "Please type a question so I can help you."

    # Normalize the user's message: lowercase + trim extra spaces.
    # This single line is what makes the search case-insensitive.
    normalized_message = user_message.lower().strip()

    best_match_answer = None
    highest_score = 0

    for faq_entry in faq_data.get("faqs", []):
        match_count = 0

        # Compare against every keyword (also lowercased) for this FAQ
        for keyword in faq_entry.get("keywords", []):
            if keyword.lower() in normalized_message:
                match_count += 1

        # Keep track of the FAQ with the most matching keywords so far
        if match_count > highest_score:
            highest_score = match_count
            best_match_answer = faq_entry["answer"]

    # If we found at least one matching keyword, return that answer
    if best_match_answer is not None:
        return best_match_answer

    # No match found -> return the required fallback message
    return faq_data.get(
        "fallback_answer",
        "Sorry, I don't have information about that. Please contact the college office."
    )


# ---------------------------------------------------------------
# STEP 5: Flask Routes
# ---------------------------------------------------------------

@app.route("/")
def home():
    """Route: "/" -> renders the Home page."""
    return render_template("index.html", college_name=faq_data.get("college_name", "College"))


@app.route("/chatbot")
def chatbot_page():
    """Route: "/chatbot" -> renders the Chat page with suggested questions."""
    return render_template(
        "chatbot.html",
        college_name=faq_data.get("college_name", "College"),
        suggested_questions=faq_data.get("suggested_questions", [])
    )


@app.route("/chat", methods=["POST"])
def chat():
    """
    Route: "/chat" (POST only)
    The JavaScript front-end calls this endpoint every time the user
    sends a message.

    Expects JSON:  { "message": "What is the fee structure?" }
    Returns JSON:  { "reply": "...", "timestamp": "10:45 AM" }
    """
    # silent=True prevents a crash if the request body is empty/invalid
    request_data = request.get_json(silent=True) or {}
    user_message = request_data.get("message", "")

    bot_reply = get_bot_response(user_message)
    current_timestamp = datetime.now().strftime("%I:%M %p")

    return jsonify({
        "reply": bot_reply,
        "timestamp": current_timestamp
    })


# ---------------------------------------------------------------
# STEP 6: Run the Flask development server
# ---------------------------------------------------------------
if __name__ == "__main__":
    # debug=True gives helpful error pages and auto-reloads on save.
    # Set debug=False before deploying to a production server.
    app.run(debug=True, host="0.0.0.0", port=5000)
