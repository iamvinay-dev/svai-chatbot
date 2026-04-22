import json
import os
import re
import unicodedata

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 0 — TEXT NORMALIZATION & ALIASES
# ══════════════════════════════════════════════════════════════════════════════

def normalize(text: str) -> str:
    text = text.lower().strip()
    # Remove accents/diacritics
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    # Remove non-alphanumeric chars
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Map common typos or phrases to primary keywords
ALIAS_MAP = {
    "commities": "all committees",
    "commities list": "all committees",
    "comities": "all committees",
    "hods": "all hod",
    "hod names": "all hod",
    "maters": "all mentors",
    "menters": "all mentors",
    "mentors list": "all mentors",
    "pricnipal": "principal",
    "principle": "principal",
    "college history": "history",
    "naac grade": "naac",
    "fee structure": "fees",
    "tution fee": "fees",
    "rules and regulations": "rules",
    "anti-ragging": "ragging",
    "bullying": "ragging",
}

def apply_aliases(msg: str) -> str:
    for alias, canonical in ALIAS_MAP.items():
        if alias in msg:
            msg = msg.replace(alias, canonical)
    return msg

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — KEYWORD MAP
# ══════════════════════════════════════════════════════════════════════════════

KEYWORD_MAP = {
    "hi": "👋 Hello! Welcome to **SV Arts College** chatbot. Ask me about faculty, fees, schedules, or rules!",
    "hello": "👋 Hello! I'm **SVAI Bot**. How can I help you today?",
    "thanks": "😊 You're welcome! Feel free to ask more questions.",
    "thank you": "😊 Happy to help!",
    
    "college name": "🏫 **Sri Venkateswara Arts College (Autonomous)**, Tirupati.",
    "sv arts": "🏫 **S.V. Arts College** (Autonomous) is located in Tirupati, A.P. Managed by TTD.",
    "about college": "🏛️ **S.V. Arts College**: Founded in 1945 by TTD. It is an Autonomous institution with a NAAC A+ Grade (CGPA 3.28).",
    "history": "📜 **College History**: Foundational resolution in 1943, opened in 1945. Founder Principal: K. Rami Reddy. Current building occupied on 12-10-1967.",
    "motto": "🕉️ College motto: **Om Namo Venkatesaya**",
    "managed by": "🏢 Managed by **Tirumala Tirupati Devasthanams (TTD)**.",
    "timings": "🕒 **College Timings**: 09:30 AM to 04:15 PM (Monday–Saturday).",
    "website": "🌐 Websites: **www.tirumala.org** and **www.tirupati.org**",
    "naac": "🏆 **NAAC A+ Grade** (2022) with CGPA **3.28**.",
    "autonomous": "✅ Autonomous status conferred on **08-12-2023**, implemented from **2024-2025**.",
    "hostel": "🏠 **Hostel**: 3 blocks. Warden: Dr. P. Lokanadha Mandadi (📞 9441075059).",
    "ragging": "🚫 **RAGGING IS PROHIBITED**: Punishment includes 6 months prison or ₹5,000 fine + dismissal. Call Inspector: 9491074524.",
    "mobile": "📵 **Mobiles**: Fine of ₹1,000 for use inside college. Stricter penalties for misuse.",
    "fees": "💸 **Fees**: B.A./B.Com(G) ₹5,400. B.Sc(Basic) ₹5,600. B.Com(CA)/BBA ₹10,845. B.Sc(CS/AI/Biotech) ₹11,045.",
    "rules": "📏 **Rules**: 75% attendance mandatory. Uniform: Sky Blue/Navy Blue. ID card compulsory.",
    "attendance": "📋 **Attendance**: Minimum 75% required. Condonation at 50% with ₹500 fee.",
}

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — DATA LOADERS & SPECIAL QUERIES
# ══════════════════════════════════════════════════════════════════════════════

def get_json_data():
    search_paths = [
        os.path.join(os.path.dirname(__file__), 'college_data.json'),
        os.path.join(os.path.dirname(__file__), 'sv_arts_college_COMPLETE.json'),
        'college_data.json'
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: continue
    return None

def handle_special_queries(msg: str) -> str | None:
    data = get_json_data()
    if not data: return None

    # Principal lookup
    if "principal" in msg:
        ordinals = ["first", "second", "third", "fourth", "fifth"]
        for i, word in enumerate(ordinals):
            if word in msg:
                succ = data.get('successive_principals', [])
                if len(succ) > i:
                    p = succ[i]
                    return f"👔 **{word.capitalize()} Principal**: {p['name']} ({p.get('period', 'N/A')})"
        
        years = re.findall(r'\d{4}', msg)
        if years:
            yr = years[0]
            for p in data.get('successive_principals', []):
                if yr in p.get('period', ''):
                    return f"👔 **Principal in {yr}**: {p['name']} ({p['period']})"

    # All HODs
    if "all hod" in msg:
        res = "👨‍🏫 **Heads of Departments:**\n"
        depts = data.get('faculty_members', {}).get('departments', {})
        for d, info in depts.items():
            faculty = info if isinstance(info, list) else info.get('faculty', [])
            for m in faculty:
                if "head" in m.get('designation', '').lower():
                    res += f"• {d.replace('_',' ').title()}: **{m['name']}**\n"
        return res

    # Committees
    if "all committees" in msg:
        coms = data.get('committees_2025_2026', [])
        res = f"🏢 **Committees ({len(coms)} Total):**\n"
        for i, c in enumerate(coms[:15]): # Limit to first 15 for chat brevity
            res += f"{i+1}. {c['name']}\n"
        res += "...and others. Ask for specific committees like 'Anti-Ragging members'."
        return res

    return None

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — PUBLIC API
# ══════════════════════════════════════════════════════════════════════════════

def get_quick_response(user_message: str) -> str | None:
    msg = normalize(user_message)
    msg = apply_aliases(msg)
    
    # 1. Try special structured queries
    special = handle_special_queries(msg)
    if special: return special
    
    # 2. Try simple keyword map
    for key, val in KEYWORD_MAP.items():
        if key in msg:
            return val
    return None

def get_smart_offline_response(user_message: str) -> str | None:
    # This acts as a pattern-based second layer
    msg = normalize(user_message)
    if "fee" in msg and ("how much" in msg or "what is" in msg):
        return KEYWORD_MAP["fees"]
    if "where" in msg and "college" in msg:
        return KEYWORD_MAP["sv arts"]
    return None

def get_context() -> str:
    # System prompt generator for LLM
    data = get_json_data()
    if not data: return "SV Arts College official bot."
    
    # Simplified summary for LLM context
    context = f"Official Bot for S.V. Arts College (Autonomous), Tirupati.\n"
    context += f"Principal: Prof. N. Venugopal Reddy (9000489182).\n"
    context += f"Accreditation: NAAC A+.\n"
    # (Add more as needed or keep it dynamic)
    return context
