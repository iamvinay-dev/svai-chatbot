import os
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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # ─────────────────────────────────────────────────────────────────────────
    # PRIORITY 1 — KEYWORD / RULE-BASED (zero cost, instant)
    # ─────────────────────────────────────────────────────────────────────────
    quick = get_quick_response(user_message)
    if quick:
        return jsonify({"response": quick})

    # ─────────────────────────────────────────────────────────────────────────
    # PRIORITY 2 — LEGACY INLINE RULES (kept for backward compatibility)
    # ─────────────────────────────────────────────────────────────────────────
    msg_lower = user_message.lower()

    if any(k in msg_lower for k in ["shaik asifa", "chairman"]) and "student" in msg_lower:
        return jsonify({"response": "🎓 **Student Union Chairman**: Shaik Asifa (B.Sc Biotechnology)."})

    if any(k in msg_lower for k in ["lasya priya", "secretary"]) and "student" in msg_lower:
        return jsonify({"response": "📜 **Student Union Secretary**: P. Lasya Priya (B.Com CA)."})

    if "principal" in msg_lower:
        return jsonify({"response": "👨‍🏫 **Principal**: **Prof. N. Venugopal Reddy**, M.Sc, M.Phil, Ph.D. Contact: **9000489182**."})

    # ─────────────────────────────────────────────────────────────────────────
    # PRIORITY 3 — AI RESPONSE (LLM fallback)
    # ─────────────────────────────────────────────────────────────────────────
    try:
        system_prompt = f"""
You are SVAI Bot, the official AI chatbot of **S.V. Arts College (Autonomous), Tirupati**.
Your job is to give accurate, fast, and helpful answers to students, staff, and visitors.

## RESPONSE RULES:
1. ALWAYS search the knowledge base below first before answering.
2. Keep answers SHORT (1-4 lines) and DIRECT.
3. Use **bold** for important names, numbers, and dates.
4. Use emojis to make responses friendly and professional.
5. If info is NOT in the knowledge base, say: "I currently don't have that data. Try asking about: faculty contacts, fees, schedules, rules, or scholarships."
6. NEVER make up phone numbers, names, or dates.
7. For phone numbers, always prefix with 📞.

## PERSONALITY:
- Smart, friendly college assistant
- Helpful to students, parents, and staff
- Professional but approachable

## KNOWLEDGE BASE:
{get_context()}
"""
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama3-8b-8192",
            max_tokens=300,
            temperature=0.3,
        )
        response = chat_completion.choices[0].message.content
        return jsonify({"response": response})

    except Exception as e:
        print(f"[app.py] Groq API error: {e}")
        return jsonify({
            "response": "⚠️ I'm having trouble connecting right now. Please try again"
        }), 200


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

if __name__ == '__main__':
    app.run(debug=True, port=5000)