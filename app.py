import os
import json
import base64
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from knowledge_base import get_context, get_quick_response, get_smart_offline_response
from flask_cors import CORS

# Load environment variables
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)

# ── Groq client (optional — only used when API key exists) ─────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("[SVAI] Groq API client initialized.")
    except Exception as e:
        print(f"[SVAI] Groq init failed: {e}. Running in offline mode.")
else:
    print("[SVAI] No GROQ_API_KEY found. Running in OFFLINE mode.")

# 🔐 Admin Panel Settings
ADMIN_PASSWORD = "svacadmin2025"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # Format: "user/repo"


def push_to_github(file_path, content, message, is_binary=False):
    """Commits a file directly to GitHub repo to make changes permanent on Vercel."""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("[GITHUB] Missing Token or Repo Config. Skipping cloud commit.")
        return False
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha') if res.status_code == 200 else None
    if is_binary:
        encoded_content = base64.b64encode(content).decode('utf-8')
    else:
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    payload = {"message": message, "content": encoded_content, "branch": "main"}
    if sha:
        payload["sha"] = sha
    put_res = requests.put(url, headers=headers, json=payload)
    return put_res.status_code in [200, 201]


# ══════════════════════════════════════════════════════════════════════════════
#  RESPONSE PIPELINE
#  Layer 1 (Always works — offline): Keyword / structured match
#  Layer 2 (Always works — offline): Smart offline fuzzy response
#  Layer 3 (Needs internet): Groq LLM API call
# ══════════════════════════════════════════════════════════════════════════════

def get_response(user_message: str) -> str:
    """
    3-layer response pipeline.
    Returns a response string no matter what — never crashes.
    """

    # ── LAYER 1: Keyword / Structured Match (Instant, 100% offline) ────────
    quick = get_quick_response(user_message)
    if quick:
        return quick

    # ── LAYER 2: Smart Offline Response (Pattern-based, 100% offline) ──────
    offline = get_smart_offline_response(user_message)
    if offline:
        return offline

    # ── LAYER 3: Groq LLM (Needs internet + API key) ────────────────────────
    if groq_client:
        try:
            system_prompt = f"""You are SVAI Bot, the official AI assistant of S.V. Arts College (Autonomous), Tirupati, Andhra Pradesh.

## YOUR TASK:
Answer questions using ONLY the knowledge base provided below. Be accurate, friendly, and concise (2-6 lines unless listing data).

## CRITICAL RULES:
1. NEVER make up phone numbers, names, or fees — only use what is in the knowledge base.
2. For typos/misspellings, figure out what the user meant and answer correctly.
3. "Principles" of the college = Vision & Mission statements.
4. "First/second principal" = ordinal from successive principals list.
5. HODs = Heads of Departments.
6. There are 52 official committees for 2025-26.
7. If answer is not available, say: "I don't have that specific data. Ask about: faculty contacts, fees, schedules, rules, committees, scholarships, or mentors."

## KNOWLEDGE BASE:
{get_context()}
"""
            completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=800,
                temperature=0.2,
            )
            return completion.choices[0].message.content

        except Exception as e:
            print(f"[app.py] Groq API error: {e}")
            # Fall through to offline fallback message

    # ── FINAL FALLBACK: Helpful offline message ─────────────────────────────
    return (
        "⚠️ I couldn't find a specific answer for that. "
        "Try asking about: **faculty contacts**, **fees**, **exam schedule**, "
        "**attendance rules**, **committees**, **scholarships**, **HoDs**, or **mentors**. "
        "You can also ask: 'list of committees', 'all HoDs', 'chemistry faculty', 'college fees' etc."
    )


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    response = get_response(user_message)
    return jsonify({"response": response})


# 🔍 SEO & File Routes
@app.route('/robots.txt')
def robots():
    return send_from_directory(os.getcwd(), 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.getcwd(), 'sitemap.xml')

@app.route('/college_data.pdf')
def download_handbook():
    return send_from_directory(os.getcwd(), 'college_data.pdf')

# 🔐 Admin Panel Routes
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    if data.get('password') == ADMIN_PASSWORD:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 401

@app.route('/admin/get_json')
def get_json_data():
    file_path = os.path.join(os.getcwd(), 'sv_arts_college_COMPLETE.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({"error": "File not found"}), 404

@app.route('/admin/save_json', methods=['POST'])
def save_json_data():
    file_path = 'sv_arts_college_COMPLETE.json'
    try:
        new_data = request.json
        content = json.dumps(new_data, indent=2)
        try:
            with open(os.path.join(os.getcwd(), file_path), 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"[LOCAL JSON] Skipping local write: {e}")
        success = push_to_github(file_path, content, "Admin: Updated institutional data via dashboard")
        if not success:
            return jsonify({"error": "GitHub push failed. Check your Token configuration."}), 500
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/upload_timetable', methods=['POST'])
def upload_timetable():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        sem = request.form.get('sem')
        type_val = request.form.get('type', 'academic')
        if file and sem:
            filename = file.filename
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            final_filename = f"sem{sem}_{type_val}.{ext}"
            save_rel_path = f"static/timetable/{final_filename}"
            save_path = os.path.join(os.getcwd(), save_rel_path)
            try:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file_content = file.read()
                with open(save_path, 'wb') as f:
                    f.write(file_content)
            except Exception as e:
                print(f"[LOCAL SAVE] Skipping local write: {e}")
                file.seek(0)
                file_content = file.read()
            success = push_to_github(save_rel_path, file_content, f"Admin: Uploaded {final_filename}", is_binary=True)
            if not success:
                return jsonify({"error": "GitHub push failed."}), 500
            return jsonify({"status": "success", "file": final_filename}), 200
        return jsonify({"error": "Missing semester or file"}), 400
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)