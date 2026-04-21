import os
import json
import base64
import requests
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
from groq import Groq
from knowledge_base import get_context, get_quick_response
from flask_cors import CORS

# Load environment variables
load_dotenv(override=True)

app = Flask(__name__)
CORS(app)

# Initialize Groq Client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# 🔐 Admin Panel Settings
ADMIN_PASSWORD = "svacadmin2025"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO") # Format: "user/repo"

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

    # Get the current file SHA if it exists (required for updates)
    res = requests.get(url, headers=headers)
    sha = res.json().get('sha') if res.status_code == 200 else None

    # Encode content
    if is_binary:
        encoded_content = base64.b64encode(content).decode('utf-8')
    else:
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    payload = {
        "message": message,
        "content": encoded_content,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    put_res = requests.put(url, headers=headers, json=payload)
    return put_res.status_code in [200, 201]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    quick = get_quick_response(user_message)
    if quick:
        return jsonify({"response": quick})

    try:
        system_prompt = f"""
You are SVAI Bot, the official AI chatbot of **S.V. Arts College (Autonomous), Tirupati**.
Your job is to give accurate, fast, and helpful answers to students, staff, and visitors.

## RESPONSE RULES:
1. ALWAYS search the knowledge base below first before answering.
2. Keep answers SHORT (1-4 lines) and DIRECT.
3. If info is NOT in the knowledge base, say: "I currently don't have that data. Try asking about: faculty contacts, fees, schedules, rules, or scholarships."

## KNOWLEDGE BASE:
{get_context()}
"""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            temperature=0.3,
        )
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})

    except Exception as e:
        print(f"[app.py] Groq API error: {e}")
        return jsonify({ "response": "⚠️ I'm having trouble connecting right now. Please try again" }), 200


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

@app.route('/admin/update_json', methods=['POST'])
def update_json_data():
    file_path = 'sv_arts_college_COMPLETE.json'
    try:
        new_data = request.json
        content = json.dumps(new_data, indent=2)
        
        # 1. Update local file (Optional - will fail on Vercel)
        try:
            with open(os.path.join(os.getcwd(), file_path), 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"[LOCAL JSON] Skipping local write (Read-only filesystem): {e}")
        
        # 2. Update GitHub (Permanent)
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
            
            # 1. Attempt to save local (Optional - will fail on Vercel)
            try:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                file_content = file.read()
                with open(save_path, 'wb') as f:
                    f.write(file_content)
            except Exception as e:
                print(f"[LOCAL SAVE] Skipping local write (Read-only filesystem): {e}")
                # We still have the file_content, so we can proceed to GitHub
                file.seek(0) # Reset file pointer
                file_content = file.read()
            
            # 2. Push to GitHub (This is the Permanent Save)
            success = push_to_github(save_rel_path, file_content, f"Admin: Uploaded {final_filename}", is_binary=True)
            
            if not success:
                return jsonify({"error": "GitHub push failed. Please check GITHUB_TOKEN and GITHUB_REPO."}), 500
                
            return jsonify({"status": "success", "file": final_filename}), 200
        return jsonify({"error": "Missing semester or file"}), 400
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)