import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
from knowledge_base import get_context
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
    user_message = request.json.get('message', '').lower()
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # 🎓 STUDENT UNION & MANAGEMENT
    if any(k in user_message for k in ["shaik asifa", "chairman"]) and "student" in user_message:
        return jsonify({"response": "🎓 **Student Union Chairman**: Shaik Asifa (B.Sc Biotechnology)."})

    if any(k in user_message for k in ["lasya priya", "secretary"]) and "student" in user_message:
        return jsonify({"response": "📜 **Student Union Secretary**: P. Lasya Priya (B.Com CA)."})

    if "principal" in user_message:
        return jsonify({"response": "👨‍🏫 **Principal**: **Prof. N. Venugopal Reddy**, M.Sc, M.Phil, Ph.D. Contact: **9000489182**."})

    # 🏢 DEPARTMENTS & FACULTY
    if "computer science" in user_message:
        return jsonify({"response": "💻 **Computer Science Dept**: Headed by **Prof. K. Kameswara Rao**. Faculty includes Sri Chakravarthy, Dr. Jyotsna, and others. They offer Data Science, AI, and CS Honours."})

    if "commerce" in user_message:
        return jsonify({"response": "💰 **Commerce Dept**: Headed by **Prof. Y. Mallikarjun Rao**. Faculty includes Prof. S. Usha and Dr. B. Nageswar Naik."})

    if "physics" in user_message:
        return jsonify({"response": "🔭 **Physics Dept**: Headed by **Sri C. Subramanyam**. Notable faculty: Prof. Y. Dasaradhudu and Prof. K. Kameswara Rao."})

    # 🗓️ SCHEDULE & RULES
    if any(k in user_message for k in ["holiday", "break", "vacation"]):
        return jsonify({"response": "📅 **Upcoming Holidays**: \n- **Dasara**: 28-09-2025 to 05-10-2025\n- **Sankranthi**: 10-01-2026 to 18-01-2026"})

    if any(k in user_message for k in ["timing", "time", "clock"]):
        return jsonify({"response": "🕒 **College Timings**: 09:30 AM to 04:15 PM (Monday - Saturday)"})
    
    if any(k in user_message for k in ["uniform", "dress", "dress code"]):
        return jsonify({"response": "👔 **Uniform Rules**: \n- **Boys**: Sky Blue shirt & Navy Blue pant.\n- **Girls**: Blue salwar kameez with Navy Blue bottom & sky blue top."})

    if any(k in user_message for k in ["ragging", "complaint", "anti-ragging"]):
        return jsonify({"response": "🚫 **Anti-Ragging**: Ragging is strictly prohibited. For complaints, contact the Inspector at **9491074524**."})

    if "library" in user_message:
        return jsonify({"response": "📚 **Library**: Open 09:30 AM to 05:00 PM. Features 88,000+ volumes and 200+ journals."})

    # 🌟 NOTABLE ALUMNI
    if "alumni" in user_message or "famous" in user_message:
        return jsonify({"response": "🌟 **Notable Alumni**: \n- **Sri N. Chandra Babu Naidu** (Chief Minister of A.P.)\n- **Late S.P. Balasubramanyam** (Great Singer)\n- **B. Karunakar Reddy** (Former M.L.A.)"})

    # 📍 LOCATION
    if any(k in user_message for k in ["location", "address", "where is"]):
        return jsonify({"response": "📍 **Location**: S.V. Arts College is located in Tirupati, near the main road. Managed by TTD."})

    # 💰 FEES & SCHOLARSHIPS
    if "fee" in user_message:
        return jsonify({"response": "💸 **Fees (Approx.)**: \n- BA: ₹5,400\n- B.Com CA: ₹10,845\n- B.Sc: ₹5,600 - ₹11,045\n(Check official portal for exact details)"})

    if "scholarship" in user_message:
        return jsonify({"response": "🎓 **Scholarships**: 9 categories available including Govt Social Welfare (SC/ST/BC), Merit Scholarships, and Sports Talent."})

    try:
        system_prompt = f"""
        You are SVAI Bot, a smart college assistant chatbot designed to handle thousands of students efficiently while minimizing API cost.
        Your primary goal is to give accurate, fast, and short responses while avoiding unnecessary AI generation.

        ---
        ## 🧠 DECISION SYSTEM (FOLLOW STRICTLY)
        Before answering any question, you MUST internally follow this order:

        ### 1. RULE-BASED RESPONSE (FIRST PRIORITY)
        If the user input is simple or contains common keywords, respond instantly using short predefined answers.
        Examples:
        - "hi", "hello" → "Hello! How can I help you?"
        - "fees" → "Fees can be paid at the admin office or online portal."
        - "timings" → "College runs from 9:00 AM to 4:00 PM."
        - "location" → "The college is located near the main road."
        Keep responses very short (1 line).

        ---
        ### 2. FAQ MEMORY MATCH (SECOND PRIORITY)
        If the question is similar to a known FAQ, respond using stored answers from the Context below.
        Even if the wording is different, identify the closest meaning.

        ---
        ### 3. AI RESPONSE (LAST PRIORITY)
        Only generate a full AI response if the question is not covered in rules or FAQ.

        ---
        ## ⚡ RESPONSE STYLE RULES
        - ALWAYS try your best to find the answer in the Context Data below.
        - Keep answers SHORT and DIRECT (1–3 lines).
        - If you find the information, give a BOLD and clear answer.

        ---
        ## 🚫 COST CONTROL & ACCURACY
        - If the information is ABSOLUTELY NOT there, do NOT make it up.
        - Instead, respond: "I don't have that specific information yet. **Try asking about:** Faculty numbers, College Timings, Uniform rules, or Admission fees."

        ---
        ## 🎯 PERSONALITY
        - Be a helpful, smart, and fast College Assistant.
        - Use emojis to look modern and professional.
        - If a student asks for a specific faculty member's number, give it from the context.
        - If they ask about exam dates or schedules, refer to the "Academic Schedule" section.

        ---
        ## 🧩 INSTITUTIONAL KNOWLEDGE (FULL HANDBOOK DATA)
        You have access to the complete 86-page college handbook in JSON format. Use this to answer deeply about any department, rules, or history.
        
        {get_context()}
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
            stream=False
        )
        
        bot_response = completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "I'm having trouble connecting. Please try again later."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
