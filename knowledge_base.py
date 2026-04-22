"""
knowledge_base.py  —  SVAI Bot  |  S.V. Arts College (Autonomous), Tirupati
=============================================================================
OFFLINE-FIRST ARCHITECTURE
───────────────────────────
Layer 1  get_quick_response()   → Keyword + structured JSON queries  (OFFLINE)
Layer 2  get_smart_offline_response() → Pattern-based smart replies   (OFFLINE)
Layer 3  (in app.py)            → Groq LLM API if key present        (ONLINE)
Layer 4  (in app.py)            → Generic helpful fallback            (OFFLINE)

The bot works 100% without any API key — Layers 1 & 2 handle ~95% of questions.
"""

import json
import os
import re
import unicodedata

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 0 — TEXT NORMALIZATION
# ══════════════════════════════════════════════════════════════════════════════

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — ALIAS MAP  (typo / alternate phrasing → canonical keyword)
# ══════════════════════════════════════════════════════════════════════════════

ALIAS_MAP: dict[str, str] = {
    # Principal / Principle typos
    "pricniple": "principal", "pricnipal": "principal", "princpal": "principal",
    "principel": "principal", "prinicpal": "principal", "pricipal": "principal",
    "prinicple": "principal", "prncipal": "principal", "princible": "principal",
    "first principle": "first principal", "second principle": "second principal",
    "third principle": "third principal", "fourth principle": "fourth principal",
    "fifth principle": "fifth principal", "1st principle": "first principal",
    "2nd principle": "second principal", "3rd principle": "third principal",
    "1st principal": "first principal", "2nd principal": "second principal",
    "3rd principal": "third principal",
    "principles of college": "vision mission", "college principles": "vision mission",
    "college principle": "vision mission", "svac principles": "vision mission",
    "all principles": "vision mission", "what are the principles": "vision mission",
    "tell me principles": "vision mission",

    # HOD typos
    "hods": "all hod", "all hods": "all hod", "list hods": "all hod",
    "list of hod": "all hod", "list of hods": "all hod",
    "who are hods": "all hod", "show hods": "all hod", "show me hods": "all hod",
    "hod names": "all hod", "heads of department": "all hod",
    "head of departments": "all hod", "department heads": "all hod",
    "all heads of departments": "all hod",

    # Committee typos
    "commities": "all committees", "comitees": "all committees",
    "committess": "all committees", "commitees": "all committees",
    "all commities": "all committees", "all comitees": "all committees",
    "list of commities": "all committees", "list of commitees": "all committees",
    "committee names": "all committees", "what are the commitees": "all committees",
    "how many comitees": "how many committees", "how many committess": "how many committees",
    "how many commities": "how many committees",
    "how many committees are there": "how many committees",
    "total committees": "how many committees", "number of committees": "how many committees",

    # Mentor typos
    "maters": "all mentors", "menters": "all mentors", "all mators": "all mentors",
    "mentor names": "all mentors", "list mentors": "all mentors",
    "show mentors": "all mentors", "who are mentors": "all mentors",
    "list of mentors": "all mentors", "mentor list": "all mentors",

    # Fee typos
    "fees structure": "fees", "fee structure": "fees", "tution fee": "fees",
    "tuition fee": "fees", "tution fees": "fees", "tuition fees": "fees",
    "college fees": "fees", "course fees": "fees", "how much fee": "fees",
    "what is the fee": "fees", "what are the fees": "fees",
    "sem fee": "fees", "semester fee": "fees",

    # Rules typos
    "colege rules": "rules", "collge rules": "rules", "college rule": "rules",
    "all rules": "rules", "what are rules": "rules",
    "attendence": "attendance", "attendnce": "attendance", "atendance": "attendance",
    "attendence rules": "attendance", "attendnce rules": "attendance",

    # Department typos
    "biotechnolgy": "biotechnology", "bio tech": "biotechnology",
    "bio technology": "biotechnology", "zoologgy": "zoology", "zoolgy": "zoology",
    "microbiolgy": "microbiology", "micro biology": "microbiology",
    "enviromental science": "environmental science",
    "politcal science": "political science", "pol science": "political science",
    "poly science": "political science", "comerce": "commerce",
    "computr science": "computer science", "comp sci": "computer science",
    "comp science": "computer science", "maths department": "mathematics",
    "math department": "mathematics", "mathematic": "mathematics",
    "physcis": "physics", "pyshics": "physics", "chemisty": "chemistry",
    "chemistty": "chemistry", "statics": "statistics", "statistcs": "statistics",
    "econmics": "economics", "econimics": "economics",
    "psycology": "psychology", "psycholgy": "psychology",

    # College basics typos
    "svac": "sv arts", "sv college": "sv arts", "sv arts college": "sv arts",
    "tirupathi college": "sv arts", "tirupati arts college": "sv arts",
    "about svac": "about college", "about sv arts": "about college",
    "college info": "about college", "college history": "history",
    "when was college founded": "founded", "year of establishment": "established",
    "naac grade": "naac", "autonomous status": "autonomous",
    "college website": "website", "college email": "email",
    "college timing": "timings", "college hours": "timings",
    "college contact": "contact",

    # Principal basics
    "who is principal": "current principal", "who is the principal": "current principal",
    "principal name": "current principal", "principal number": "principal contact",
    "principal phone number": "principal phone", "contact principal": "principal contact",
    "venugopal": "venugopal reddy",

    # Facilities
    "gym": "gymnasium", "hostle": "hostel", "hostle warden": "hostel warden",
    "hostel info": "hostel", "hostel information": "hostel",
    "library info": "library", "books": "library books",
    "how many books": "library volumes", "volumes": "library volumes",

    # Scholarships
    "scholrship": "scholarships", "scolarship": "scholarships",
    "scholarship types": "scholarship", "types of scholarship": "scholarship",
    "financial aid": "scholarships",

    # Specific committees
    "iqac committee": "iqac", "exam cell": "examination cell",
    "exam committee": "examination cell", "examinaton cell": "examination cell",
    "anti ragging committee": "anti ragging", "women cell": "women empowerment",
    "womens cell": "women empowerment", "sexual harrasment": "sexual harassment",
    "grivenace": "grievance", "greivance": "grievance",
    "greivance cell": "grievance redressal", "innovation council": "iic",
    "skill developement": "skill development", "palcement cell": "placement",
    "reseach cell": "research cell", "carrer guidance": "career guidance",
    "anti-drug": "anti drug", "timetable committe": "timetable committee",
    "time table committee": "timetable committee",
    "website committe": "website committee", "poor student fund": "poor students",
    "srivariseva": "srivari seva", "srivari service": "srivari seva",

    # NCC / NSS / Union
    "union chairman": "student chairman", "union secretary": "student secretary",
    "union president": "student president",

    # Exams
    "exam dates": "exam date", "examination dates": "exam date",
    "when is exam": "exam date", "exam schedule": "exam date",
    "academic calander": "academic schedule", "academic calender": "academic schedule",
    "when do classes start": "class start", "when classes start": "class start",
    "malpratice": "malpractice", "cheating exam": "cheating",
    "exam malpractice": "malpractice", "copying in exam": "cheating",

    # Ragging / Rules
    "raggging": "ragging", "report ragging": "ragging complaint",
    "ragging helpline": "helpline", "bullying": "ragging",
    "cell phone rules": "mobile", "mobile rules": "mobile",
    "mobile phone": "mobile", "phone rules": "mobile",
    "dress rules": "dress code", "uniform rules": "uniform",
    "what to wear": "uniform", "college uniform": "uniform",

    # Alumni
    "famous students": "alumni", "notable students": "alumni",
    "old students": "alumni", "sp balu": "sp balasubramanyam",
    "chandrababu": "chandrababu naidu",

    # Misc
    "tell me everything": "about college", "all info": "about college",
    "ignou center": "ignou", "distance learining": "distance education",
    "sramadaan": "sramadanam", "swach bharat": "sramadanam",
    "superintendent contact": "superintendent",
    "non teaching staff": "non teaching", "support staff": "non teaching",
    "telephone numbers": "telephone", "important numbers": "phone numbers",
    "emergency number": "emergency", "helpline number": "helpline",
    "incubation center": "cie", "entrepreneurship": "cie",
    "all fees": "fees", "complete fee": "fees", "full fee": "fees",
}

def apply_aliases(msg: str) -> str:
    for alias in sorted(ALIAS_MAP.keys(), key=len, reverse=True):
        if alias in msg:
            msg = msg.replace(alias, ALIAS_MAP[alias])
    return msg

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — KEYWORD MAP
# ══════════════════════════════════════════════════════════════════════════════

KEYWORD_MAP: dict[str, str] = {

    # GREETINGS
    "hi": "👋 Hello! Welcome to **SV Arts College** chatbot. Ask me anything about faculty, fees, schedule, rules, departments, or contacts!",
    "hello": "👋 Hello! I'm **SVAI Bot**. How can I help you today?",
    "hey": "👋 Hey there! Ask me anything about S.V. Arts College.",
    "hlo": "👋 Hello! I'm **SVAI Bot**. How can I help you today?",
    "good morning": "🌞 Good Morning! How can I assist you today?",
    "good afternoon": "🌤️ Good Afternoon! What would you like to know?",
    "good evening": "🌙 Good Evening! Ask me anything about S.V. Arts College.",
    "thanks": "😊 You're welcome! Feel free to ask more questions.",
    "thank you": "😊 Happy to help! Is there anything else you need?",
    "bye": "👋 Goodbye! Have a great day!",

    # COLLEGE BASICS
    "college name": "🏫 **Sri Venkateswara Arts College (Autonomous)** — popularly known as **S.V. Arts College**, Tirupati.",
    "full name": "🏫 Full name: **Sri Venkateswara Arts College (Autonomous)**, Tirupati, Andhra Pradesh.",
    "sv arts": "🏫 **S.V. Arts College** (Sri Venkateswara Arts College, Autonomous) is located in Tirupati, A.P. Managed by TTD. Principal: Prof. N. Venugopal Reddy (📞 9000489182).",
    "about college": "🏛️ **S.V. Arts College**: Founded 1945 | Managed by TTD | NAAC A+ (CGPA 3.28) | Autonomous from 2024-25 | 3,084 students | 22 Labs | 88,000 library volumes | 23 departments.",
    "history": "📜 Founded in **1945** with 80 students. Founder Principal: Prof. K. Rami Reddy. Affiliated: Madras University → S.V. University (1954). Current building: 12-10-1967.",
    "founded": "📅 College was resolved in 1943 and officially opened in **1945** with Prof. K. Rami Reddy as the founder principal.",
    "established": "📅 Established in **1945**. Current three-storeyed building occupied on **October 12, 1967**.",
    "motto": "🕉️ College motto: **Om Namo Venkatesaya**",
    "managed by": "🏢 Managed by **Tirumala Tirupati Devasthanams (TTD)**, Tirupati.",
    "ttd": "🏢 **TTD** = Tirumala Tirupati Devasthanams. S.V. Arts College is managed and funded by TTD.",
    "location": "📍 **S.V. Arts College**, Tirupati, Andhra Pradesh, India.",
    "address": "📍 S.V. Arts College (Autonomous), Tirupati, Andhra Pradesh, India. Managed by TTD.",
    "timings": "🕒 **College Timings**: 09:30 AM to 04:15 PM (Monday–Saturday).",
    "working hours": "🕒 College hours: **9:30 AM – 4:15 PM**, Monday to Saturday.",
    "website": "🌐 Websites: **www.tirumala.org** and **www.tirupati.org** | Email: webmaster@tirumala.org",
    "email": "📧 Email: **webmaster@tirumala.org**",
    "accreditation": "🏆 **NAAC A+ Grade** (2022) with CGPA **3.28** on a 4-point scale.",
    "naac": "🏆 **NAAC A+ Grade** accredited in 2022 with CGPA 3.28. Autonomous status conferred: 08-12-2023.",
    "autonomous": "✅ Autonomous status conferred on **08-12-2023**, implemented from academic year **2024-2025**.",
    "student strength": "👥 Current student strength: **3,084 students**.",
    "laboratories": "🔬 The college has **22 well-equipped laboratories**.",
    "library": "📚 **Library**: Open 9:30 AM – 5:00 PM. Contains **88,000+ volumes**. Issues books: Mon/Wed/Fri. Returns: Tue/Thu/Sat.",
    "library volumes": "📚 The library has **88,000+ volumes** and 200+ journals.",
    "hostel": "🏠 **Hostel**: 3 blocks. Warden: Dr. P. Lokanadha Mandadi (📞 9441075059). Principal-in-charge: Prof. N. Venugopal Reddy.",
    "gymnasium": "🏋️ College has a **14-stage Gymnasium** for students.",
    "magazine": "📰 College Magazine published **once per academic year** to develop creative talents.",

    # VISION / MISSION
    "vision mission": "✨ **S.V. Arts College — Vision, Mission & Principles**\n\n🕉️ **Motto:** Om Namo Venkatesaya\n\n🎯 **Vision:**\n  1. Transform mediocre students into socially responsible citizens.\n  2. Extend the bounds of knowledge through multidisciplinary curriculum.\n\n🚀 **Mission:**\n  1. Inculcate spiritual and moral values.\n  2. Build competent, committed professionals.\n  3. Empower students to fulfil academic and professional passions.\n\n📜 **Pledge:** We, the members of S.V. Arts College, pledge to educate ourselves and contribute to the nation's progress.",
    "vision": "🎯 **Vision**: 1) Transform mediocre students into socially responsible citizens. 2) Extend the bounds of knowledge through multidisciplinary curriculum.",
    "mission": "🚀 **Mission**: 1) Inculcate spiritual and moral values. 2) Build competent, committed professionals. 3) Empower students academically and professionally.",
    "pledge": "📜 **College Pledge**: We, the members of S.V. Arts College, pledge to educate ourselves and contribute to the nation's progress.",

    # PRINCIPAL
    "current principal": "👨‍🏫 **Current Principal**: Prof. N. Venugopal Reddy (since 1 Feb 2024). Qualifications: M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths). 📞 **9000489182**",
    "founder principal": "👔 **Founder Principal**: Sri K. Rami Reddy, M.A., M.Sc., L.T. (1945–1950).",
    "first principal": "👔 **1st Principal**: Sri K. Rami Reddy, M.A., M.Sc., L.T. — Period: 1945–1950.",
    "second principal": "👔 **2nd Principal**: Sri P.R. Krishna Swamy — Period: 1950–1952.",
    "third principal": "👔 **3rd Principal**: Sri N. Palani Swamy — Period: 1952–1954.",
    "fourth principal": "👔 **4th Principal**: Sri N. Rama Rao — Period: 1954–1955.",
    "fifth principal": "👔 **5th Principal**: Sri P.V. Seshagiri Rao — Period: 1955–1957.",
    "sixth principal": "👔 **6th Principal**: Sri S. Nagaiah — Period: 1957–1959.",
    "seventh principal": "👔 **7th Principal**: Sri B. Raghava Baliga — Period: 1959–1960.",
    "eighth principal": "👔 **8th Principal**: Sri Y.V. Ramana — Period: 1960–1961.",
    "venugopal reddy": "👨‍🏫 **Prof. N. Venugopal Reddy** – Current Principal. M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths). 📞 9000489182",
    "principal contact": "📞 Principal Prof. N. Venugopal Reddy: **9000489182**",
    "principal phone": "📞 Principal's phone: **9000489182**",
    "head of college": "👨‍🏫 Head of College: **Prof. N. Venugopal Reddy** (Principal) — 📞 9000489182",
    "successive principals": "👔 **43 Successive Principals (1945–Present)**:\n1. Sri K. Rami Reddy (1945-50)\n2. Sri P.R. Krishna Swamy (1950-52)\n3. Sri N. Palani Swamy (1952-54)\n4. Sri N. Rama Rao (1954-55)\n5. Sri P.V. Seshagiri Rao (1955-57)\n6. Sri S. Nagaiah (1957-59)\n7. Sri B. Raghava Baliga (1959-60)\n8. Sri Y.V. Ramana (1960-61)\n9. Sri S. Nagaiah (1961-62)\n10. Sri N. Rama Rao (1962-63)\n11. Sri S. Nagaiah (1963-70)\n12. Prof. B. Ramasubba Reddy (1970-87)\n13. Dr. K. Appaswamy Pillai (1987-92)\n14. Dr. G. Sathyanarayana Rao (1992-95)\n15. Prof. D. Balakrishna Rao (1995-97)\n… (28 more) …\n43. **Prof. N. Venugopal Reddy** (Feb 2024–Present)\n\n💡 Ask 'who was principal in [year]' for a specific year.",

    # MANAGEMENT
    "management": "🏢 **TTD Management**:\n1. Sri M. Ravichandra (I.A.S.) – Executive Officer\n2. Sri V. Veerabrahamam (I.A.S.) – Joint EO\n3. Sri O. Balaji (F.C.A.) – FA & CAO\n4. Sri T. Venkatasuneelu – Educational Officer\n5. Dr. N. Venugopal Reddy – Principal",
    "executive officer": "👤 **Executive Officer, TTD**: Sri M. Ravichandra (I.A.S.)",
    "governing body": "🏛️ **Governing Body (2024-25)**: Chairman – **Sri B.R. Naidu** (TTD Board Chairman). 14 members total.",
    "chairman": "🏛️ **Governing Body Chairman**: Sri B.R. Naidu. Student Union Chairman: **Shaik Asifa** (B.Sc Biotechnology).",

    # DEPARTMENTS
    "departments": "📚 **23 Departments**: Biotechnology, Botany, Chemistry, Commerce, Computer Science, Dairy Science, Economics, Electronics, English, Environmental Science, Hindi, History, Mathematics, Microbiology, Physics, Political Science, Psychology, Sanskrit, Statistics, Telugu, Zoology, Library Science, Physical Education.",

    # ALL HODs
    "all hod": "👨‍🏫 **All Heads of Departments — 2025-26:**\n• Biotechnology: Dr. A. Sarangapani (📞 9441481579)\n• Botany: Smt. A. Surekha (📞 9966262642)\n• Chemistry: Prof. P.V. Chalapathi (📞 9985349313)\n• Commerce: Prof. Y. Mallikarjun Rao (📞 9848533623)\n• Computer Science: Prof. K. Kameswara Rao i/c (📞 9550559568)\n• Dairy Science: Dr. K. Uma Rani (📞 9963299969)\n• Economics: Dr. M. Kiran Kumar Raju (📞 9963640650)\n• Electronics: Sri C. Ratna Rao (📞 8790835429)\n• English: Dr. S. Markandeyan (📞 9441495414)\n• Environmental Science: Prof. P.V. Chalapathi i/c (📞 9985349313)\n• Hindi: Smt. T. Thriveni (📞 6300586591)\n• History: Prof. G. Kishan (📞 8919672096)\n• Mathematics: Acting – Smt. P. Vijaya Sree (📞 9949631991)\n• Microbiology: Prof. P.V. Chalapathi i/c (📞 9985349313)\n• Physics: Sri C. Subramanyam (📞 9948164776)\n• Political Science: Sri T. Sreenath (📞 9441642634)\n• Psychology: Dr. K. Uma Rani (📞 9963299969)\n• Sanskrit: Vacant\n• Statistics: Prof. M. Pedda Reddeppa Reddy (📞 9885625554)\n• Telugu: Prof. N. Bheemanna (📞 9949060771)\n• Zoology: Prof. M. Vani (📞 9885002295)\n• Library Science: Vacant\n• Physical Education: Dr. S. Mustaq Ahmed (📞 9052216777)",

    # INDIVIDUAL DEPARTMENTS
    "biotechnology": "🧬 **Biotechnology**: Head – Dr. A. Sarangapani (📞 9441481579) | Dr. P. Mohan – C. Lec. (📞 8985176265)",
    "biotech hod": "🧬 **HoD Biotechnology**: Dr. A. Sarangapani — 📞 9441481579",
    "botany": "🌿 **Botany**: Head – Smt. A. Surekha (📞 9966262642) | Dr. M. Sudhakar – C. Lec. (📞 8897038200)",
    "botany hod": "🌿 **HoD Botany**: Smt. A. Surekha — 📞 9966262642",
    "chemistry": "⚗️ **Chemistry Dept** (Head: Prof. P.V. Chalapathi 📞 9985349313):\n1. Prof. P.V. Chalapathi – Prof. & Head\n2. Prof. K. Siva Kumar (📞 9290080843)\n3. Dr. A. Sarangapani (📞 9441481579)\n4. Dr. A. Uma Maheswari (📞 9063934514)\n5. Dr. K. Jamuna (📞 9966222714)\n6. Dr. R. Kishore Kumar (📞 8106545107)\n7. Sri D. Prabhakar (📞 7097906377)\n8. Dr. K. Purushotham Naidu (📞 9491152201)\n9. Dr. K. Sankara Reddy (📞 9603633263)",
    "chemistry hod": "⚗️ **HoD Chemistry**: Prof. P.V. Chalapathi — 📞 9985349313",
    "commerce": "💰 **Commerce Dept** (Head: Prof. Y. Mallikarjun Rao 📞 9848533623):\n1. Prof. Y. Mallikarjun Rao – Prof. & Head\n2. Prof. S. Usha (📞 9848870033)\n3. Dr. B. Nageswar Naik (📞 8499855674)\n4. Dr. G. Venkata Ratnam (📞 8179332728)\n5. Dr. K. Hema Sundar Raju (📞 9247851024)\n6. Dr. D. Lakshmi Narayana Raju (📞 9502729867)\n7. Dr. D. Raja (📞 9441645670)\n8. Dr. M. Ravi Prasad (📞 9701463463)",
    "commerce hod": "💰 **HoD Commerce**: Prof. Y. Mallikarjun Rao — 📞 9848533623",
    "computer science": "💻 **Computer Science Dept** (Head i/c: Prof. K. Kameswara Rao 📞 9550559568):\n1. Prof. K. Kameswara Rao – Prof. & HoD i/c\n2. Sri K.N.V.V.S.S.S. Chakravarthy (📞 9505123979)\n3. Sri V. Chennakesavulu Reddy (📞 9494744008)\n4. Dr. P. Jyotsna (📞 9704835308)\n5. Sri G. Jayachandra Naidu (📞 9397366874)\n6. Smt. C. Kiranmayi (📞 9866182367)\n7. Smt. G. Pallavi (📞 9908049739)\n8. Sri V. Kamalanadhan (📞 9701602609)\n9. Sri A. Sukesh Reddy (📞 9885884228)\n10. Sri D. Suresh Babu (📞 9666748484)",
    "computer science hod": "💻 **HoD CS**: Prof. K. Kameswara Rao — 📞 9550559568",
    "dairy science": "🥛 **Dairy Science**: Head – Dr. K. Uma Rani (📞 9963299969)",
    "economics": "📊 **Economics**: Head – Dr. M. Kiran Kumar Raju (📞 9963640650) | Dr. A. Seshadri – C. Lec. (📞 7981600052)",
    "economics hod": "📊 **HoD Economics**: Dr. M. Kiran Kumar Raju — 📞 9963640650",
    "electronics": "⚡ **Electronics Dept** (Head: Sri C. Ratna Rao 📞 8790835429):\n1. Sri C. Ratna Rao – Sr. Lec. & Head\n2. Smt. K. Mahitha Delhi Rani (📞 9703602704)\n3. Dr. D. Sri Silpa (📞 9533952909)\n4. Smt. K. Swapna (📞 9885496536)\n5. Sri Y. Hari – Tech. Asst. (📞 9849983229)",
    "electronics hod": "⚡ **HoD Electronics**: Sri C. Ratna Rao — 📞 8790835429",
    "english": "📖 **English Dept** (Head: Dr. S. Markandeyan 📞 9441495414):\n1. Dr. S. Markandeyan – Sr. Lec. & Head\n2. Sri C. Muneendran (📞 9441492596)\n3. Smt. B. Sreedevi (📞 9291373659)",
    "english hod": "📖 **HoD English**: Dr. S. Markandeyan — 📞 9441495414",
    "environmental science": "🌍 **Environmental Science** (Head i/c: Prof. P.V. Chalapathi 📞 9985349313):\n1. Dr. P. Nagaraju (📞 9989871850)\n2. Dr. P. Sreevani (📞 9848699956)",
    "hindi": "🗣️ **Hindi**: Head – Smt. T. Thriveni (📞 6300586591)",
    "hindi hod": "🗣️ **HoD Hindi**: Smt. T. Thriveni — 📞 6300586591",
    "history": "🏺 **History Dept** (Head: Prof. G. Kishan 📞 8919672096):\n1. Prof. G. Kishan – Prof. & Head\n2. T. Jayaramaiah – Sr. Lec. (📞 9703078308)\n3. E. Madhusudan Rao – Lec. (📞 9441776545)",
    "history hod": "🏺 **HoD History**: Prof. G. Kishan — 📞 8919672096",
    "mathematics": "📐 **Mathematics Dept** (Acting Head: Smt. P. Vijaya Sree 📞 9949631991):\n1. Prof. P. Baskarudu – Head (on deputation, 📞 9490108326)\n2. Smt. P. Vijaya Sree – Acting Head & Sr. Lec. (📞 9949631991)\n3. Sri E. Rama Krishna Reddy (📞 9963844499)\n4. Capt. V. Ramesh (📞 9492855008)\n5. Dr. B. Govindarajulu (📞 9247446451)\n6. Smt. B. Sasi Kala (📞 8919236821)",
    "mathematics hod": "📐 **HoD Mathematics**: Prof. P. Baskarudu (on deputation). Acting: Smt. P. Vijaya Sree (📞 9949631991)",
    "maths": "📐 **Maths Dept**: Acting Head – Smt. P. Vijaya Sree (📞 9949631991). 6 faculty members.",
    "microbiology": "🦠 **Microbiology** (Head i/c: Prof. P.V. Chalapathi 📞 9985349313):\n1. Dr. J. Hima Bindu (📞 9885455977)\n2. Dr. P. Sandhya Priya (📞 9346760577)",
    "microbiology hod": "🦠 **HoD Microbiology**: Prof. P.V. Chalapathi i/c — 📞 9985349313",
    "physics": "🔭 **Physics Dept** (Head: Sri C. Subramanyam 📞 9948164776):\n1. Sri C. Subramanyam – Assoc. Prof. & Head\n2. Prof. Y. Dasaradhudu (📞 9440054764)\n3. Prof. K. Kameswara Rao (📞 9550559568)\n4. Prof. R. Ravi Kumar (📞 9440472062)\n5. Prof. A.V. Chandra Sekhar (📞 9441010555)\n6. Dr. P. Giri Prakash (📞 9290898291)\n7. Sri G.A.N. Sreenivasa Rao (📞 9951121655)\n8. Dr. V.H.H. Surendra Babu (📞 9515082379)",
    "physics hod": "🔭 **HoD Physics**: Sri C. Subramanyam — 📞 9948164776",
    "political science": "🗳️ **Political Science Dept** (Head: Sri T. Sreenath 📞 9441642634):\n1. Sri T. Sreenath – Sr. Lec. & Head\n2. Sri N. Suresh Kumar (📞 9441606794)\n3. Dr. K. Narasimhulu (📞 9985038780)",
    "political science hod": "🗳️ **HoD Political Science**: Sri T. Sreenath — 📞 9441642634",
    "psychology": "🧠 **Psychology Dept** (Head: Dr. K. Uma Rani 📞 9963299969):\n1. Dr. K. Uma Rani – Prof. & Head\n2. Dr. N.N. Sudha Rani (📞 9440247894)",
    "psychology hod": "🧠 **HoD Psychology**: Dr. K. Uma Rani — 📞 9963299969",
    "sanskrit": "📜 **Sanskrit Dept**: Currently **Vacant**.",
    "statistics": "📈 **Statistics Dept** (Head: Prof. M. Pedda Reddeppa Reddy 📞 9885625554):\n1. Prof. M. Pedda Reddeppa Reddy\n2. Dr. N. Ramesh Kumar (📞 9885234903)",
    "statistics hod": "📈 **HoD Statistics**: Prof. M. Pedda Reddeppa Reddy — 📞 9885625554",
    "telugu": "🔤 **Telugu Dept** (Head: Prof. N. Bheemanna 📞 9949060771):\n1. Prof. N. Bheemanna – Prof. & Head\n2. Dr. P. Lokanadha Mandadi (📞 9441075059)\n3. Sri G. Venkateswarlu (📞 7207552712)\n4. Dr. M. Prasada Rao (📞 9440467046)\n5. Dr. B. Tejovani (📞 8096117693)\n6. Dr. A. Munaswamy Achari (📞 9492067294)",
    "telugu hod": "🔤 **HoD Telugu**: Prof. N. Bheemanna — 📞 9949060771",
    "zoology": "🦎 **Zoology Dept** (Head: Prof. M. Vani 📞 9885002295):\n1. Prof. M. Vani – Prof. & Head\n2. Dr. P.S. Poornima (📞 9182088973)\n3. B. Bhanu Prakash Reddy (📞 9959988499)\n4. Dr. P. Annaiah (📞 9849202212)",
    "zoology hod": "🦎 **HoD Zoology**: Prof. M. Vani — 📞 9885002295",
    "physical education": "🏃 **Physical Education**: Sri P. Kumar (on deputation); Dr. S. Mustaq Ahmed (📞 9052216777)",

    # PROGRAMMES / FEES
    "courses": "📚 **Programmes (2025-26)**: B.A. (5 streams), B.Com (2), B.Sc (15 streams incl. AI, Quantum Tech, Data Science), B.B.A., B.C.A. Total: 25 programmes, 1,417 seats.",
    "programmes": "📚 College offers **B.A., B.Com., B.Sc., B.B.A., B.C.A.** Honours programs. 25 programmes. Total strength: 1,417 seats.",
    "fees": "💸 **Fee Structure 2025-26:**\n• B.A. (all) / B.Com General: ₹5,400/-\n• B.Sc (Physics, Maths, Stats, Psychology, Electronics, Botany, Zoology, Chemistry): ₹5,600/-\n• B.Com CA / B.B.A.: ₹10,845/-\n• B.Sc (CS, Aquaculture, Data Science, Microbiology, Biotech, AI, Quantum) / BCA: ₹11,045/-\n\n📅 Year 1 fee at Admission | Year 2 at III Sem | Year 3 at V Sem\n⚠️ Non-payment = name removed from rolls.",
    "fee": "💸 **Fees**: B.A./B.Com General ₹5,400/- | B.Sc basic ₹5,600/- | B.Com CA/BBA ₹10,845/- | B.Sc CS/AI/Biotech ₹11,045/-",
    "ba": "🎓 **B.A. Honours**: Political Science (60), History (60), Special English (30), Special Telugu (40), Economics (100). Fee: ₹5,400/-",
    "bcom": "🎓 **B.Com Honours**: CA (180 seats, ₹10,845/-) | General (180 seats, ₹5,400/-)",
    "bsc": "🎓 **B.Sc. Honours**: 15 streams including CS, AI, Quantum Tech, Data Science, Biotechnology, Chemistry, Physics, and more. Fees: ₹5,600–₹11,045/-",
    "bba": "🎓 **B.B.A. Honours**: 60 seats/section × 2 sections. Fee: ₹10,845/-",
    "bca": "🎓 **B.C.A. Honours**: 50 seats. Fee: ₹11,045/-",
    "artificial intelligence": "🤖 **B.Sc. AI (Honours)**: 30 seats | Fee: ₹11,045/- | New from 2025-26",
    "quantum": "⚛️ **B.Sc. Quantum Technologies (Honours)**: 50 seats | Fee: ₹11,045/- | New course",
    "data science": "📊 **B.Sc. Data Science (Honours)**: 50 seats | Fee: ₹11,045/-",
    "aquaculture": "🐟 **B.Sc. Aquaculture (Honours)**: 30 seats | Fee: ₹11,045/-",

    # SCHOLARSHIPS
    "scholarship": "🎓 **12 Scholarship Types** (75% attendance required):\n1. Govt. of India (SC/ST) — income ≤ ₹1L/yr\n2. State Social Welfare – SC/ST\n3. State Social Welfare – BC\n4. State Social Welfare – EBC\n5. National Merit — min 50% marks\n6. State Special Merit\n7. State General Merit\n8. Teachers' Children\n9. Ex-Servicemen Children\n10. Physically Challenged\n11. Sports Talent — contact college office\n12. Poor Boys Scholarship",
    "scholarships": "🎓 College offers **12 types of scholarships**. Minimum **75% attendance** required. Includes SC/ST, BC, EBC, Merit, Sports, Ex-servicemen, Physically Challenged scholarships.",

    # ACADEMIC SCHEDULE
    "academic schedule": "📅 **Academic Schedule 2025-26:**\n• Odd Sems (I/III/V): Classes 18-09-2025, Dasara 28-09 to 05-10, Exams 09-02-2026 to 13-02-2026\n• Even Sem (Conventional): Classes 16-06-2025, Exams 22-10-2025\n• BBA/BCA Sem I: Classes 07-06-2025, Exams 04-12-2025\n• Autonomous II/IV Sem: Classes 10-11-2025, Exams 03-04-2026",
    "exam date": "📝 **Exam Dates 2025-26:**\n• Odd Sem Theory: 09-02-2026 to 13-02-2026\n• Odd Sem Practicals: 14-02-2026 to 18-02-2026\n• Even Sem (Conventional): 22-10-2025\n• BBA/BCA Sem I: 04-12-2025\n• Autonomous II/IV: 03-04-2026",
    "exams": "📝 Odd Sem Theory: **09 Feb – 13 Feb 2026**. Practicals: 14 Feb – 18 Feb 2026.",
    "class start": "🏫 Classes Start: Odd Sem 18-09-2025 | Even Sem 16-06-2025 | BBA/BCA 07-06-2025 | Autonomous II/IV 10-11-2025.",
    "holidays": "📅 **Holidays 2025-26**: Dasara (28 Sep–5 Oct) | Sankranthi (10–18 Jan 2026) | Independence Day (15 Aug) | Republic Day (26 Jan) | Gandhi Jayanthi (2 Oct)",
    "dasara": "🎉 **Dasara Holidays**: 28-09-2025 to 05-10-2025 (Odd Sem).",
    "sankranthi": "🎉 **Sankranthi Holidays**: 10-01-2026 to 18-01-2026.",

    # ATTENDANCE
    "attendance": "📋 **Attendance Rules:**\n• Minimum **75%** required for promotion\n• **50%** minimum for condonation (fee: ₹500/-)\n• 5 periods/day, 1 hour each\n• Absent 3+ days without leave → name removed from rolls\n• Medical certificate required for illness absence",
    "condonation": "⚠️ **Condonation**: 50%–74% attendance → apply with ₹500/- fee. Below 50% → repeat year. Condonation students NOT eligible for higher studies.",

    # DISCIPLINE & RULES
    "rules": "📏 **College Rules:**\n✅ 75% attendance mandatory\n✅ Wear uniform (Sky Blue shirt + Navy Blue pant for boys)\n✅ ID card always\n🚫 No ragging (criminal offence)\n🚫 No mobile in class (₹1,000 fine)\n🚫 No political activities\n🚫 No smoking/drugs on campus\n✅ Rise when teacher enters\n✅ No leaving class without permission",
    "discipline": "📏 **Discipline Rules**: No public demonstrations. Wear ID card always. Rise when teacher enters. No leaving class without permission. No political agitations on campus.",
    "uniform": "👔 **Uniform:**\n• Boys: Sky Blue shirt + Navy Blue pant\n• Girls: Blue salwar kameez (Navy Blue bottom + Sky Blue top)",
    "dress code": "👔 Boys: Sky Blue shirt & Navy Blue pant | Girls: Blue salwar kameez (Navy Blue bottom, Sky Blue top)",
    "identity card": "🪪 **Identity Card** must be worn at all times. Compulsory during University Semester Examinations.",

    # RAGGING
    "ragging": "🚫 **RAGGING — STRICTLY PROHIBITED. IT IS A CRIME!**\nPunishment: 6 months imprisonment OR ₹5,000 fine OR Both + Dismissal.\n📞 Inspector: 9491074524 | Dy. SP: 9440796702 | SP: 9440796747",
    "anti ragging": "🚫 **Anti-Ragging**: Headed by Principal (📞 9000489182). Report to Inspector: **9491074524**.",

    # MOBILE
    "mobile": "📵 **Mobile Rules:**\n• Use inside college: ₹1,000 fine\n• Obscene content/messaging: ₹2,000\n• Cyberbullying (5+ persons): ₹10,000\n• Criminal use (10+ persons): ₹50,000–₹2,50,000 or imprisonment",

    # LIBRARY
    "library rules": "📚 **Library Rules:**\n• Hours: 9:30 AM – 5:00 PM\n• Issue: Mon/Wed/Fri | Return: Tue/Thu/Sat\n• Loan period: 15 days | Overdue fine: ₹1/day\n• Students: 2 books | Staff: 20 books",

    # HOSTEL
    "hostel warden": "🏠 **Hostel Warden**: Dr. P. Lokanadha Mandadi — 📞 9441075059",
    "warden": "🏠 **Warden**: Dr. P. Lokanadha Mandadi (📞 9441075059)\n**Deputy Wardens**: Dr. M. Prasada Rao (📞 9440467046), G. Venkateswarlu (📞 7207552712), Dr. B. Nageswar Naik (📞 8499855674)",

    # NCC / NSS
    "ncc": "🎖️ **NCC Officers:**\n1. Capt. V. Ramesh – ANO, 29(A) Bn. (📞 9492855008)\n2. Dr. K. Purushotham Naidu – ANO, 2(A) R&V Regt. (📞 9491152201)\n3. Dr. A. Umamaheswari – ANO, 11(A) Air Sqn.",
    "nss": "🌟 **NSS Programme Officers:**\n1. Dr. M.P. Reddeppa Reddy (Prof. & HoD Statistics)\n2. Sri E. Madhusudhana Rao (📞 9441776545)",

    # STUDENT UNION
    "student union": "🎓 **Students Union 2025-26:**\n• President: Prof. N. Venugopal Reddy (Principal)\n• Vice President: Prof. Y. Mallikarjun Rao\n• Chairman: **Shaik Asifa** (B.Sc Biotechnology)\n• Secretary: **P. Lasya Priya** (B.Com CA)",
    "student chairman": "🎓 **Student Union Chairman**: **Shaik Asifa** (B.Sc Biotechnology)",
    "student secretary": "🎓 **Student Union Secretary**: **P. Lasya Priya** (B.Com Computer Application)",
    "student president": "🎓 **Student Union President**: Prof. N. Venugopal Reddy (Principal)",

    # ASSOCIATIONS
    "arts association": "🎭 **Arts Association**: VP – Prof. G. Kishan | Sec – SR. Balaji (III B.A. Pol. Sci.) | Joint Sec – K. Thulasi Saksha.",
    "commerce association": "💰 **Commerce Association**: VP – Prof. S. Usha | Sec – P. Kavya Yadhav (III BCA) | Joint Sec – V. Sai Satwik.",
    "games association": "🏃 **Games & Sports**: VP – Dr. S. Mustaq Ahmed | Sec – Sura Hari (📞 6301857080) | Joint Sec – R. Revathi (📞 8074401764).",
    "maths science association": "🔬 **Maths & Science Association**: VP – Sri C. Subramanyam (HoD Physics) | Sec – A. Pavitra Saram (III B.Sc Psychology).",

    # COMMITTEES
    "how many committees": "🏢 S.V. Arts College has **52 officially constituted committees** for 2025-2026. Ask 'list of committees' to see all names.",
    "committees": "🏢 S.V. Arts College has **52 committees** for 2025-26. Ask 'list of committees' for all names, or 'who is in [committee name]' for members.",
    "iqac": "📋 **IQAC**: Chairperson – Prof. N. Venugopal Reddy (Principal). Co-ordinator – Prof. Y. Mallikarjun Rao (📞 9848533623).",
    "examination cell": "📝 **Examination Cell:**\n• Controller: Prof. P.V. Chalapathi (📞 9985349313)\n• Dy. Controller: Prof. K. Kameswara Rao (📞 9550559568)\n• Dy. Controller: Capt. V. Ramesh (📞 9492855008)",
    "grievance": "📣 **Grievance Redressal**: Convener – Sri E. Ramakrishna Reddy (📞 9963844499).",
    "grievance redressal": "📣 **Grievance**: Contact Sri E. Ramakrishna Reddy — 📞 **9963844499**",
    "anti drug": "🚫 **Anti-Drug Committee**: Chairperson – Principal (📞 9000489182).",
    "women empowerment": "👩 **Women Empowerment & Protection Cell**: Coordinator – Dr. K. Uma Rani (📞 9963299969).",
    "sexual harassment": "👩 **Sexual Harassment Committee**: Coordinator – Dr. K. Uma Rani — 📞 9963299969",
    "iic": "💡 **IIC (Institutional Innovation Council):** President – Dr. N. Venugopal Reddy | Convener – Dr. K. Uma Rani (📞 9963299969) | VP – Dr. K. Kameswara Rao",
    "skill development": "🎓 **Skill Development & Placement**: Coordinator – Dr. S. Markandeyan (📞 9441495414).",
    "placement": "🎓 **Placement Cell**: Coordinator – Dr. S. Markandeyan (📞 9441495414).",
    "research cell": "🔬 **Research Cell**: Coordinator – Prof. A.V. Chandra Sekhar (📞 9441010555).",
    "career guidance": "🎯 **Career Guidance**: Coordinator – Prof. G. Kishan (📞 8919672096).",
    "science club": "🔬 **Science Club**: Coordinator – Sri C. Ratna Rao (📞 8790835429).",
    "debate club": "🗣️ **Debate Club**: Coordinator – Prof. N. Bheemanna (📞 9949060771).",
    "red ribbon": "🎀 **Red Ribbon Club**: Coordinator – Prof. P.V. Chalapathi (📞 9985349313).",
    "cie": "💡 **CIE (Innovation Incubation & Entrepreneurship)**: Coordinator – Prof. R. Ravi Kumar (📞 9440472062).",
    "poor students": "💝 **Poor Students Aid Fund**: Coordinator – Dr. A. Sarangapani (📞 9441481579).",
    "sramadanam": "🌿 **Swacha Bharath / Sramadanam**: Coordinator – Prof. M. Pedda Reddeppa Reddy (📞 9885625554).",
    "value education": "📖 **Value Education Cell**: Coordinator – Prof. M. Vani (📞 9885002295).",
    "website committee": "🌐 **Website Committee**: Coordinator – Sri C. Ratna Rao (📞 8790835429).",
    "timetable committee": "📅 **Timetable Committee**: Coordinator – Prof. Y. Mallikarjun Rao (📞 9848533623).",

    # MENTOR
    "mentor": "👥 **Mentor System**: Each class has a dedicated mentor who supervises academic progress. Ask 'all mentors' or 'year 1 mentors' etc.",
    "all mentors": "👥 **Mentors 2025-26**: Available for Year 1, 2, and 3. Each class has a dedicated mentor. Ask 'year 1 mentors', 'year 2 mentors', or 'year 3 mentors' for the specific list.",

    # MALPRACTICE
    "malpractice": "⚠️ **Exam Malpractice Penalties:**\n1. Copying/Cheating → Paper cancelled + 2-exam debarment\n2. Impersonation → 3-year debarment\n3. Assault on invigilator → 4-exam debarment\n4. Mob assistance → All papers cancelled + 2-exam debarment\nOther cases → Malpractice Committee",
    "cheating": "⚠️ **Cheating**: Paper cancelled + result cancelled + **2-exam debarment**. Impersonation = **3-year debarment**.",

    # CONTACTS
    "contact": "📞 **Key Contacts:**\n• Principal: 9000489182\n• Superintendent: 9490370445\n• Hostel Warden: 9441075059\n• College Phone: 2264602\n• Anti-Ragging: 9491074524\n• Grievance: 9963844499\n• Women's Cell: 9963299969",
    "emergency": "🚨 **Emergency:** Principal: 9000489182 | Anti-Ragging Inspector: 9491074524 | Dy. SP: 9440796702 | Grievance: 9963844499",
    "helpline": "📞 Ragging: 9491074524 | Women's Cell: 9963299969 | Grievance: 9963844499 | Principal: 9000489182",
    "telephone": "📞 SV Arts College: 2264602 | TTD PBX Tirupati: 0877-2231777 | SVU Registrar: 2289545",

    # ALUMNI
    "alumni": "🌟 **Notable Alumni:**\n• N. Chandra Babu Naidu (CM of A.P.)\n• Late S.P. Bala Subramanyam (Legendary Singer)\n• B. Karunakar Reddy (Former MLA)\n• Chevireddy Bhaskar Reddy (Former MLA)\n• A. Mohan, Parasa Ratnam (Former MLAs)\n• Phalguna Kumar (CA)",
    "sp balasubramanyam": "🎵 **Late S.P. Bala Subramanyam** – legendary playback singer – is a proud alumni of S.V. Arts College.",
    "chandrababu naidu": "🏛️ **Sri N. Chandra Babu Naidu** – Chief Minister of Andhra Pradesh – is an alumni of S.V. Arts College.",

    # SPECIAL PROGRAMS
    "srivari seva": "🙏 **Srivari Seva**: Compulsory TTD programme. 50 students daily serve pilgrims at Tirumala — guiding, Q-line control, Nitya Annadanam service.",
    "ignou": "🎓 **IGNOU Centre Coordinator**: Prof. P. Bhaskarudu — 📞 9490108326",
    "open university": "🎓 **Dr. B.R. Ambedkar Open University Coordinator**: Prof. Y. Mallikarjun Rao — 📞 9848533623",

    # NON-TEACHING STAFF
    "superintendent": "👤 **Superintendent**: S. Lalitha — 📞 9490370445",
    "non teaching": "👤 **Non-Teaching Staff (21 members):** Superintendent: S. Lalitha (📞 9490370445) | Sr. Asst: K. Usha Shree (📞 9902928446) | Jr. Asst: R. Rajani (📞 6281656465) | Computer Operator: N. Sudharani (📞 8106798250) + 17 more.",

    # DAYS
    "teachers day": "🎉 **Teachers Day**: September 5 — celebrated at S.V. Arts College.",
    "women day": "👩 **International Women's Day**: March 8 — observed at college.",
    "science day": "🔬 **National Science Day**: February 28 — celebrated at S.V. Arts College.",
}


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — JSON DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════

def get_json_data():
    search_paths = [
        os.path.join(os.path.dirname(__file__), 'sv_arts_college_COMPLETE.json'),
        os.path.join(os.path.dirname(__file__), 'college_data.json'),
        os.path.join(os.getcwd(), 'sv_arts_college_COMPLETE.json'),
        os.path.join(os.getcwd(), 'college_data.json'),
        'sv_arts_college_COMPLETE.json', 'college_data.json',
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                continue
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 4 — STRUCTURED QUERY HANDLER  (JSON-backed)
# ══════════════════════════════════════════════════════════════════════════════

def handle_special_queries(msg: str) -> str | None:

    # Vision / Mission / Principles
    if any(k in msg for k in ["vision mission", "vision and mission", "all principles",
                               "college principles", "svac principles"]):
        return KEYWORD_MAP["vision mission"]

    # Principal ordinal lookup
    if "principal" in msg:
        ordinals = [
            ("first", 0), ("second", 1), ("third", 2), ("fourth", 3),
            ("fifth", 4), ("sixth", 5), ("seventh", 6), ("eighth", 7),
            ("ninth", 8), ("tenth", 9), ("11th", 10), ("12th", 11),
            ("13th", 12), ("14th", 13), ("15th", 14), ("43rd", 42),
        ]
        for word, idx in ordinals:
            if word in msg:
                data = get_json_data()
                if data:
                    successive = data.get('successive_principals', [])
                    if len(successive) > idx:
                        p = successive[idx]
                        return (f"👔 **{word.capitalize()} Principal of SVAC**: "
                                f"{p['name']} ({p.get('qualifications', '')})\n"
                                f"Period: {p.get('period', '')}")
                # Fallback to static keyword map
                key = f"{word} principal"
                if key in KEYWORD_MAP:
                    return KEYWORD_MAP[key]

        # Year-based lookup
        years = re.findall(r'\d{4}', msg)
        if years:
            data = get_json_data()
            year_int = int(years[0])
            if data:
                for p in data.get('successive_principals', []):
                    if str(year_int) in p.get('period', ''):
                        return (f"👔 **Principal in {year_int}**: {p['name']} "
                                f"({p.get('qualifications', '')})\nPeriod: {p.get('period', '')}")
            return f"👔 I couldn't find the specific principal for {year_int}. Ask 'successive principals' for the full list."

    data = get_json_data()
    if not data:
        return None

    # All HoDs from JSON
    if any(k in msg for k in ["all hod", "head of department names", "all heads"]):
        res = "👨‍🏫 **All Heads of Departments — 2025-26:**\n"
        depts = data.get('faculty_members', {}).get('departments', {})
        for dept, info in depts.items():
            faculty = info if isinstance(info, list) else info.get('faculty', [])
            for m in faculty:
                d = m.get('designation', '').lower()
                if "head" in d or "hod" in d:
                    res += f"• {dept.replace('_',' ').title()}: **{m['name']}** (📞 {m.get('phone','N/A')})\n"
        return res

    # List all committees
    if any(k in msg for k in ["all committees", "list of committees", "names of committees"]):
        coms = data.get('committees_2025_2026', [])
        if not coms:
            return KEYWORD_MAP["committees"]
        res = f"🏢 **All {len(coms)} Committees — S.V. Arts College 2025-26:**\n\n"
        for c in coms:
            coord = "N/A"
            for key in ['coordinator', 'co_ordinator']:
                val = c.get(key)
                if val:
                    coord = val.get('name', 'N/A') if isinstance(val, dict) else val
                    break
            if coord == "N/A":
                for m in c.get('members', []):
                    if m.get('role', '').lower() in ['coordinator', 'co-ordinator', 'convener']:
                        coord = m.get('name', 'N/A')
                        break
            res += f"{c.get('no','')}. **{c['name']}** — Coord: {coord}\n"
        res += "\n💡 Ask 'who is in [Committee Name]?' for full member list."
        return res

    # How many committees
    if any(k in msg for k in ["how many committees", "total committees", "number of committees"]):
        count = len(data.get('committees_2025_2026', [])) or 52
        return f"🏢 S.V. Arts College has **{count} officially constituted committees** for 2025-2026."

    # Committee members
    if any(k in msg for k in ["who are in", "who is in", "members of", "members in"]):
        coms = data.get('committees_2025_2026', [])
        best_match, best_len = None, 0
        for c in coms:
            words = [w for w in c['name'].lower().split() if len(w) > 3]
            mc = sum(1 for w in words if w in msg)
            if mc > 0 and mc >= best_len:
                best_len, best_match = mc, c
        if best_match:
            c = best_match
            res = f"👥 **Members of {c['name']}:**\n"
            for m in c.get('members', []):
                res += f"• **{m.get('name','N/A')}** | {m.get('role','Member')} | {m.get('desig', m.get('designation',''))} | 📞 {m.get('phone', m.get('contact','N/A'))}\n"
            return res
        return "📋 Please specify which committee (e.g., 'Who is in Anti-Ragging?'). Ask 'list of committees' to see all."

    # All mentors
    if any(k in msg for k in ["all mentors", "mentor names", "list of mentors", "mentor list"]):
        res = "👥 **College Mentors 2025-26:**\n"
        mentors = data.get('mentors_list_2025_2026', {})
        for year, list_item in mentors.items():
            res += f"\n**[{year.upper()}]**\n"
            for m in list_item:
                res += f"• {m.get('class','')}: **{m.get('mentor','N/A')}** (📞 {m.get('phone','N/A')})\n"
        return res

    # Year-specific mentors
    if "mentor" in msg:
        mentors = data.get('mentors_list_2025_2026', {})
        for label, keys in [("Year 1", ["year_1","year1"]), ("Year 2", ["year_2","year2"]), ("Year 3", ["year_3","year3"])]:
            if any(k in msg for k in [label.lower(), label.lower().replace(" ",""), label.lower()[:6]]):
                for k in keys:
                    yr = mentors.get(k, [])
                    if yr:
                        res = f"👥 **{label} Mentors 2025-26:**\n"
                        for m in yr:
                            res += f"• {m.get('class','')}: **{m.get('mentor','N/A')}** (📞 {m.get('phone','N/A')})\n"
                        return res

    # Full fees from JSON
    if any(k in msg for k in ["all fees", "full fee list", "complete fee"]):
        prog = data.get('programmes_of_study', {})
        yr1 = prog.get('year_1_2025_26', [])
        if yr1:
            res = "💸 **Complete Fee List — All Programmes 2025-26:**\n\n"
            for p in yr1:
                res += f"  {p.get('sno','')}. {p.get('program','')} | {p.get('strength','')} seats | ₹{p.get('fee_rs','N/A')}/-\n"
            fee_reg = prog.get('fee_regulations', {})
            res += f"\n📅 Year 1: {fee_reg.get('year_1_payment','At Admission')} | Year 2: {fee_reg.get('year_2_payment','III Sem')} | Year 3: {fee_reg.get('year_3_payment','V Sem')}\n"
            return res

    return None


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 5 — SMART OFFLINE RESPONSE  (Layer 2 — no JSON needed)
#  Handles natural language questions without exact keyword matches.
#  This is the NEW layer that makes the bot work fully offline.
# ══════════════════════════════════════════════════════════════════════════════

# Department name → keyword in KEYWORD_MAP
DEPT_KEYWORDS = {
    "biotech": "biotechnology", "biology": "biotechnology",
    "botany": "botany", "plant": "botany",
    "chem": "chemistry", "chemistry": "chemistry",
    "commerce": "commerce", "business": "commerce",
    "computer": "computer science", "cs": "computer science",
    "dairy": "dairy science",
    "economics": "economics", "economy": "economics",
    "electronics": "electronics",
    "english": "english",
    "environment": "environmental science", "env sci": "environmental science",
    "hindi": "hindi",
    "history": "history",
    "math": "mathematics", "maths": "mathematics",
    "microbio": "microbiology",
    "physics": "physics",
    "political": "political science", "pol sci": "political science",
    "psych": "psychology",
    "sanskrit": "sanskrit",
    "stat": "statistics",
    "telugu": "telugu",
    "zoo": "zoology",
    "physical edu": "physical education", "sports": "physical education",
}

COMMITTEE_KEYWORDS_OFFLINE = {
    "iqac": "iqac", "quality": "iqac",
    "exam": "examination cell", "examination": "examination cell",
    "ragging": "anti ragging", "anti ragging": "anti ragging",
    "women": "women empowerment", "gender": "women empowerment",
    "iic": "iic", "innovation": "iic",
    "grievance": "grievance redressal",
    "drug": "anti drug",
    "skill": "skill development", "placement": "placement",
    "research": "research cell",
    "career": "career guidance",
    "science club": "science club",
    "debate": "debate club",
    "red ribbon": "red ribbon",
    "cie": "cie", "incubation": "cie",
    "poor": "poor students",
    "sramadam": "sramadanam", "swach": "sramadanam",
    "value": "value education",
    "website": "website committee",
    "timetable": "timetable committee", "time table": "timetable committee",
}


def get_smart_offline_response(user_message: str) -> str | None:
    """
    Pattern-based intelligent offline response handler.
    Covers natural language questions without needing exact keyword hits.
    """
    msg = normalize(user_message)
    msg = apply_aliases(msg)  # apply aliases again on original (pre-alias) text too

    # ── "Who is HoD of [dept]" / "HoD of [dept]" ─────────────────────────
    hod_patterns = [
        r"hod of (\w[\w\s]*)", r"head of (\w[\w\s]*) dep",
        r"who is head of (\w[\w\s]*)", r"who is hod of (\w[\w\s]*)",
        r"(\w[\w\s]*) hod", r"(\w[\w\s]*) head",
        r"(\w[\w\s]*) department head",
    ]
    for pattern in hod_patterns:
        m = re.search(pattern, msg)
        if m:
            dept_word = m.group(1).strip()
            for keyword, map_key in DEPT_KEYWORDS.items():
                if keyword in dept_word or dept_word in keyword:
                    hod_key = f"{map_key} hod"
                    if hod_key in KEYWORD_MAP:
                        return KEYWORD_MAP[hod_key]
                    if map_key in KEYWORD_MAP:
                        return KEYWORD_MAP[map_key]

    # ── "[dept] faculty" / "[dept] teachers" / "[dept] staff" ────────────
    if any(w in msg for w in ["faculty", "teachers", "staff of", "lecturers"]):
        for keyword, map_key in DEPT_KEYWORDS.items():
            if keyword in msg and map_key in KEYWORD_MAP:
                return KEYWORD_MAP[map_key]

    # ── "contact of [dept]" / "phone of [dept]" ──────────────────────────
    if any(w in msg for w in ["contact", "phone", "number", "call"]):
        for keyword, map_key in DEPT_KEYWORDS.items():
            if keyword in msg:
                hod_key = f"{map_key} hod"
                if hod_key in KEYWORD_MAP:
                    return KEYWORD_MAP[hod_key]

    # ── "what is [committee]" / "who runs [committee]" ───────────────────
    if any(w in msg for w in ["who is in", "members of", "who runs", "committee", "cell", "club"]):
        for keyword, map_key in COMMITTEE_KEYWORDS_OFFLINE.items():
            if keyword in msg and map_key in KEYWORD_MAP:
                return KEYWORD_MAP[map_key]

    # ── Fee questions ─────────────────────────────────────────────────────
    if any(w in msg for w in ["fee", "cost", "price", "how much", "charges", "money"]):
        if any(w in msg for w in ["ba", "arts", "b a"]):
            return KEYWORD_MAP["ba"]
        if any(w in msg for w in ["bcom", "b com", "commerce"]):
            return KEYWORD_MAP["bcom"]
        if any(w in msg for w in ["bsc", "b sc", "science"]):
            return KEYWORD_MAP["bsc"]
        if any(w in msg for w in ["bba", "b b a", "business admin"]):
            return KEYWORD_MAP["bba"]
        if any(w in msg for w in ["bca", "b c a", "computer app"]):
            return KEYWORD_MAP["bca"]
        return KEYWORD_MAP["fees"]

    # ── Scholarship questions ─────────────────────────────────────────────
    if any(w in msg for w in ["scholarship", "financial help", "stipend", "aid", "grant"]):
        return KEYWORD_MAP["scholarships"]

    # ── Attendance questions ──────────────────────────────────────────────
    if any(w in msg for w in ["attendance", "percent", "absent", "75", "shortage", "condon"]):
        return KEYWORD_MAP["attendance"]

    # ── Exam questions ────────────────────────────────────────────────────
    if any(w in msg for w in ["exam", "test", "semester end", "practical", "theory"]):
        if any(w in msg for w in ["date", "when", "schedule", "time"]):
            return KEYWORD_MAP["exam date"]
        if any(w in msg for w in ["cheat", "copy", "malprac", "punish"]):
            return KEYWORD_MAP["malpractice"]
        return KEYWORD_MAP["exams"]

    # ── Ragging questions ─────────────────────────────────────────────────
    if any(w in msg for w in ["rag", "bully", "harass", "tease", "eve teas"]):
        return KEYWORD_MAP["ragging"]

    # ── Mobile / phone fine ───────────────────────────────────────────────
    if any(w in msg for w in ["mobile", "cell phone", "smartphone", "phone fine"]):
        return KEYWORD_MAP["mobile"]

    # ── Rules / discipline ────────────────────────────────────────────────
    if any(w in msg for w in ["rule", "disciplin", "conduct", "regulat", "policy"]):
        return KEYWORD_MAP["rules"]

    # ── Dress / uniform ───────────────────────────────────────────────────
    if any(w in msg for w in ["dress", "uniform", "wear", "clothes", "outfit"]):
        return KEYWORD_MAP["uniform"]

    # ── Principal questions ───────────────────────────────────────────────
    if any(w in msg for w in ["principal", "head of college", "hoc", "director"]):
        return KEYWORD_MAP["current principal"]

    # ── Library questions ─────────────────────────────────────────────────
    if any(w in msg for w in ["library", "book", "reading room", "volumes", "lend"]):
        return KEYWORD_MAP["library"]

    # ── Hostel questions ──────────────────────────────────────────────────
    if any(w in msg for w in ["hostel", "dormitory", "warden", "room", "accomod"]):
        return KEYWORD_MAP["hostel"]

    # ── Contact / helpline ────────────────────────────────────────────────
    if any(w in msg for w in ["contact", "number", "helpline", "phone", "call", "reach"]):
        return KEYWORD_MAP["contact"]

    # ── College basics ────────────────────────────────────────────────────
    if any(w in msg for w in ["naac", "accredit", "grade", "ranking"]):
        return KEYWORD_MAP["naac"]
    if any(w in msg for w in ["autonomous", "self govern"]):
        return KEYWORD_MAP["autonomous"]
    if any(w in msg for w in ["establish", "found", "start", "history", "1945", "1943"]):
        return KEYWORD_MAP["history"]

    # ── Specific courses ─────────────────────────────────────────────────
    if "artificial intelligence" in msg or " ai " in msg:
        return KEYWORD_MAP["artificial intelligence"]
    if "quantum" in msg:
        return KEYWORD_MAP["quantum"]
    if "data science" in msg:
        return KEYWORD_MAP["data science"]

    # ── Vision / Mission (catch remaining "principles" variants) ──────────
    if any(w in msg for w in ["vision", "mission", "principle", "motto", "pledge", "objective"]):
        return KEYWORD_MAP["vision mission"]

    # ── Alumni ───────────────────────────────────────────────────────────
    if any(w in msg for w in ["alumni", "famous", "notable", "old student", "singer", "cm", "naidu"]):
        return KEYWORD_MAP["alumni"]

    # ── NCC / NSS ────────────────────────────────────────────────────────
    if "ncc" in msg:
        return KEYWORD_MAP["ncc"]
    if "nss" in msg:
        return KEYWORD_MAP["nss"]

    # ── Associations ─────────────────────────────────────────────────────
    if "association" in msg or "club" in msg:
        if "art" in msg:
            return KEYWORD_MAP["arts association"]
        if "commerce" in msg or "consumer" in msg:
            return KEYWORD_MAP["commerce association"]
        if "game" in msg or "sport" in msg:
            return KEYWORD_MAP["games association"]
        if "science" in msg or "math" in msg:
            return KEYWORD_MAP["maths science association"]

    # ── Student Union ─────────────────────────────────────────────────────
    if "student union" in msg or "union" in msg:
        return KEYWORD_MAP["student union"]

    return None


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 6 — MAIN MATCHING (PUBLIC)
# ══════════════════════════════════════════════════════════════════════════════

def match_keywords(user_message: str) -> str | None:
    msg = normalize(user_message)
    msg = apply_aliases(msg)

    # Structured / JSON-backed queries
    special = handle_special_queries(msg)
    if special:
        return special

    # Keyword map — longest key first
    sorted_keys = sorted(KEYWORD_MAP.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in msg:
            return KEYWORD_MAP[key]

    # Word-level fallback
    words = [w for w in msg.split() if len(w) > 3]
    if len(words) >= 2:
        for key in sorted_keys:
            key_words = [w for w in key.split() if len(w) > 3]
            if key_words and all(w in msg for w in key_words):
                return KEYWORD_MAP[key]

    return None


def get_quick_response(user_message: str) -> str | None:
    """Layer 1: Keyword + structured match. Called first by app.py."""
    return match_keywords(user_message)


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 7 — LLM CONTEXT  (system prompt for Groq fallback)
# ══════════════════════════════════════════════════════════════════════════════

def get_context() -> str:
    json_path = os.path.join(os.path.dirname(__file__), 'sv_arts_college_COMPLETE.json')
    if not os.path.exists(json_path):
        json_path = os.path.join(os.getcwd(), 'sv_arts_college_COMPLETE.json')

    base = """
=== SVAI BOT KNOWLEDGE BASE — S.V. ARTS COLLEGE (AUTONOMOUS), TIRUPATI ===

COLLEGE: Sri Venkateswara Arts College (Autonomous) | SVAC | TTD-managed | Tirupati, A.P.
NAAC: A+ Grade (2022), CGPA 3.28 | Autonomous: from 2024-25 | Founded: 1945
Students: 3,084 | Labs: 22 | Library: 88,000 volumes | Hostel: 3 blocks
Timings: 9:30 AM – 4:15 PM | Motto: Om Namo Venkatesaya
Website: www.tirumala.org | Email: webmaster@tirumala.org

VISION: 1) Transform students into socially responsible citizens. 2) Extend knowledge through multidisciplinary curriculum.
MISSION: 1) Inculcate spiritual/moral values. 2) Build competent professionals. 3) Empower students academically and professionally.

PRINCIPAL: Prof. N. Venugopal Reddy | M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths) | 9000489182

MANAGEMENT: Sri M. Ravichandra (IAS, EO) | Sri V. Veerabrahamam (IAS, Jt EO) | Sri O. Balaji (FCA, FA&CAO) | Sri T. Venkatasuneelu (Edu Officer)

HoDs (2025-26):
Biotechnology: Dr. A. Sarangapani (9441481579) | Botany: Smt. A. Surekha (9966262642)
Chemistry: Prof. P.V. Chalapathi (9985349313) | Commerce: Prof. Y. Mallikarjun Rao (9848533623)
CS: Prof. K. Kameswara Rao i/c (9550559568) | Dairy Science: Dr. K. Uma Rani (9963299969)
Economics: Dr. M. Kiran Kumar Raju (9963640650) | Electronics: Sri C. Ratna Rao (8790835429)
English: Dr. S. Markandeyan (9441495414) | Hindi: Smt. T. Thriveni (6300586591)
History: Prof. G. Kishan (8919672096) | Mathematics (acting): Smt. P. Vijaya Sree (9949631991)
Microbiology: Prof. P.V. Chalapathi i/c | Physics: Sri C. Subramanyam (9948164776)
Political Science: Sri T. Sreenath (9441642634) | Psychology: Dr. K. Uma Rani (9963299969)
Statistics: Prof. M. Pedda Reddeppa Reddy (9885625554) | Telugu: Prof. N. Bheemanna (9949060771)
Zoology: Prof. M. Vani (9885002295) | Physical Edu: Dr. S. Mustaq Ahmed (9052216777)

FEES 2025-26: B.A./B.Com Gen: Rs.5,400 | B.Sc basic: Rs.5,600 | B.Com CA/BBA: Rs.10,845 | B.Sc CS/AI/Biotech/Data Sci: Rs.11,045 | BCA: Rs.11,045

ATTENDANCE: 75% required. Condonation at 50% (Rs.500 fee). Below 50% = repeat year.

DISCIPLINE: Sky Blue shirt + Navy Blue pant (boys). Blue salwar kameez (girls). ID card mandatory. Mobile fine: Rs.1,000. No ragging (6 months prison or Rs.5,000 fine + dismissal).

COMMITTEES: 52 total. Key ones: IQAC (Coord: Prof. Y. Mallikarjun Rao), Examination Cell (Controller: Prof. P.V. Chalapathi 9985349313), Anti-Ragging (Principal 9000489182), Women Empowerment (Dr. K. Uma Rani 9963299969), Grievance (Sri E. Ramakrishna Reddy 9963844499), IIC (Dr. K. Uma Rani convener), Skill Dev/Placement (Dr. S. Markandeyan 9441495414), Research Cell (Prof. A.V. Chandra Sekhar 9441010555), Career Guidance (Prof. G. Kishan 8919672096).

STUDENT UNION: Chairman: Shaik Asifa (BSc Biotech) | Secretary: P. Lasya Priya (BCom CA) | President: Prof. N. Venugopal Reddy

SCHOLARSHIPS (75% attendance): 12 types — SC/ST Govt., State Social Welfare (SC/ST, BC, EBC), National Merit (50% marks), State Special/General Merit, Teachers' Children, Ex-Servicemen, Physically Challenged, Sports Talent, Poor Boys.

EXAM SCHEDULE: Odd Sem Theory 09-02-2026 to 13-02-2026 | Practicals 14-02-2026 | Even Sem 22-10-2025 | BBA/BCA Sem I 04-12-2025 | Autonomous II/IV 03-04-2026

MALPRACTICE: Cheating → 2-exam debarment | Impersonation → 3-year debarment | Assault on invigilator → 4-exam debarment

HOSTEL: Warden: Dr. P. Lokanadha Mandadi (9441075059). 3 blocks.
LIBRARY: 9:30 AM – 5 PM. Issue Mon/Wed/Fri. Return Tue/Thu/Sat. 15-day loan. Fine Rs.1/day. Students 2 books, Staff 20.

SUCCESSIVE PRINCIPALS (43 total): 1. Sri K. Rami Reddy (1945-50) ... 43. Prof. N. Venugopal Reddy (Feb 2024–present)

NOTABLE ALUMNI: N. Chandra Babu Naidu (CM AP), Late S.P. Bala Subramanyam (Singer), several Former MLAs.

KEY CONTACTS: Principal 9000489182 | Superintendent S. Lalitha 9490370445 | Hostel Warden 9441075059 | Anti-Ragging Inspector 9491074524 | Grievance 9963844499 | Women's Cell 9963299969 | College Phone 2264602
"""

    if not os.path.exists(json_path):
        return base

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Append full faculty list
        base += "\n\nFULL FACULTY:\n"
        depts = data.get('faculty_members', {}).get('departments', {})
        for dept, members in depts.items():
            base += f"[{dept.upper().replace('_',' ')}] "
            faculty_list = members if isinstance(members, list) else members.get('faculty', [])
            for m in faculty_list:
                if m.get('name') != 'Vacant':
                    base += f"{m.get('name')} ({m.get('designation','')}, {m.get('phone','')}) | "
            base += "\n"

        # Append committees
        base += "\nALL COMMITTEES:\n"
        for c in data.get('committees_2025_2026', []):
            coord = "N/A"
            for key in ['coordinator', 'co_ordinator']:
                val = c.get(key)
                if val:
                    coord = val.get('name', 'N/A') if isinstance(val, dict) else val
                    break
            base += f"{c.get('no','')}. {c.get('name','')} — Coord: {coord}\n"

        # Append mentors
        base += "\nMENTORS 2025-26:\n"
        for yr, lst in data.get('mentors_list_2025_2026', {}).items():
            base += f"[{yr.upper()}] "
            for m in lst:
                base += f"{m.get('class','')}: {m.get('mentor','N/A')} ({m.get('phone','')}) | "
            base += "\n"

        # Successive principals
        base += "\nSUCCESSIVE PRINCIPALS:\n"
        for p in data.get('successive_principals', []):
            base += f"{p.get('name','')} ({p.get('qualifications','')}) — {p.get('period','')}\n"

        return base

    except Exception as e:
        print(f"[knowledge_base] Error reading JSON: {e}")
        return base
