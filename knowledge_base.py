import json
import os

# ─────────────────────────────────────────────
# KEYWORD MAPS  (keyword → answer string)
# These fire BEFORE the LLM, keeping cost zero.
# ─────────────────────────────────────────────

KEYWORD_MAP = {
    # ── GREETINGS ──────────────────────────────────────────────────────────
    "hi": "👋 Hello! Welcome to **SV Arts College** chatbot. Ask me anything about faculty, fees, schedule, rules, departments, or contacts!",
    "hello": "👋 Hello! I'm **SVAI Bot**. How can I help you today?",
    "hey": "👋 Hey there! Ask me anything about S.V. Arts College.",
    "good morning": "🌞 Good Morning! How can I assist you today?",
    "good afternoon": "🌤️ Good Afternoon! What would you like to know?",
    "good evening": "🌙 Good Evening! Ask me anything about S.V. Arts College.",
    "thanks": "😊 You're welcome! Feel free to ask more questions.",
    "thank you": "😊 Happy to help! Is there anything else you need?",
    "bye": "👋 Goodbye! Have a great day!",

    # ── COLLEGE BASICS ──────────────────────────────────────────────────────
    "college name": "🏫 **Sri Venkateswara Arts College (Autonomous)** — popularly known as **S.V. Arts College**, Tirupati.",
    "full name": "🏫 Full name: **Sri Venkateswara Arts College (Autonomous)**, Tirupati, Andhra Pradesh.",
    "short name": "📌 Short name: **S.V. Arts College**.",
    "sv arts": "🏫 **S.V. Arts College** (Sri Venkateswara Arts College, Autonomous) is located in Tirupati, A.P. Managed by TTD. Principal: Prof. N. Venugopal Reddy (📞 9000489182).",
    "svac": "🏫 SVAC = **S.V. Arts College (Autonomous)**, Tirupati. Managed by Tirumala Tirupati Devasthanams (TTD).",
    "about college": "🏛️ **S.V. Arts College** was founded in **1945**, managed by TTD. NAAC A+ (3.28 CGPA). Current strength: 3,084 students. 22 labs, 88,000 library volumes, 3 hostel blocks. Principal: Prof. N. Venugopal Reddy.",
    "history": "📜 **College History**: Founded 1943 (resolved), established **1945**. Initial affiliation: Madras University. SVU affiliation: 1954. Current building occupied: 12-10-1967. Founder Principal: Prof. K. Rami Reddy.",
    "founded": "📅 S.V. Arts College was **founded in 1945** on the suggestion of Sri V. Raghunatha Reddy, Former Chairman of TTD.",
    "established": "📅 The college was **established in 1945** and affiliated to Madras University initially, then S.V. University in 1954.",
    "motto": "🕉️ College motto: **Om Namo Venkatesaya**",
    "managed by": "🏢 Managed by **Tirumala Tirupati Devasthanams (TTD)**, Tirupati.",
    "ttd": "🏢 **TTD** = Tirumala Tirupati Devasthanams. S.V. Arts College is managed and funded by TTD.",
    "location": "📍 **S.V. Arts College**, Tirupati, Andhra Pradesh, India.",
    "address": "📍 S.V. Arts College (Autonomous), Tirupati, Andhra Pradesh, India. Managed by TTD.",
    "where is": "📍 S.V. Arts College is located in **Tirupati, Andhra Pradesh**, India.",
    "timings": "🕒 **College Timings**: 09:30 AM to 04:15 PM (Monday–Saturday).",
    "college time": "🕒 College works from **9:30 AM to 4:15 PM**, Monday to Saturday.",
    "working hours": "🕒 College hours: **9:30 AM – 4:15 PM**, Monday to Saturday.",
    "website": "🌐 Websites: **www.tirumala.org** and **www.tirupati.org** | Email: webmaster@tirumala.org",
    "email": "📧 Email: **webmaster@tirumala.org**",
    "accreditation": "🏆 **NAAC A+ Grade** (2022) with CGPA **3.28** on a 4-point scale.",
    "naac": "🏆 **NAAC A+ Grade** accredited in 2022 with CGPA 3.28. Autonomous status conferred: 08-12-2023.",
    "autonomous": "✅ Autonomous status conferred on **08-12-2023**, implemented from academic year **2024-2025**.",
    "student strength": "👥 Current student strength: **3,084 students**.",
    "laboratories": "🔬 The college has **22 well-equipped laboratories**.",
    "library": "📚 **Library**: Open 9:30 AM – 5:00 PM. Contains **88,000 volumes**. Issues books on Mon, Wed, Fri. Returns on Tue, Thu, Sat.",
    "library volumes": "📚 The library has **88,000+ volumes** and 200+ journals.",
    "hostel": "🏠 **College Hostel**: 3 blocks. Warden: Dr. P. Lokanadha Mandadi (📞 9441075059). Principal-in-charge: Prof. N. Venugopal Reddy.",
    "hostel blocks": "🏠 The college hostel has **3 blocks**.",
    "gymnasium": "🏋️ College has a **14-stage Gymnasium** for students.",
    "magazine": "📰 College Magazine is published **once per academic year** to develop creative talents.",

    # ── PRINCIPAL ──────────────────────────────────────────────────────────
    "principal": "👨‍🏫 **Principal**: Prof. N. Venugopal Reddy\n📋 Qualifications: M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths)\n📞 Contact: **9000489182**",
    "venugopal reddy": "👨‍🏫 **Prof. N. Venugopal Reddy** is the current Principal. Qualifications: M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths). 📞 9000489182",
    "principal contact": "📞 Principal's contact: **9000489182** (Prof. N. Venugopal Reddy)",
    "principal phone": "📞 Principal Prof. N. Venugopal Reddy: **9000489182**",
    "head of college": "👨‍🏫 Head of College: **Prof. N. Venugopal Reddy** (Principal) — 📞 9000489182",

    # ── MANAGEMENT ──────────────────────────────────────────────────────────
    "management": "🏢 **TTD Management**:\n1. Sri M. Ravichandra (I.A.S.) – Executive Officer\n2. Sri V. Veerabrahamam (I.A.S.) – Joint EO\n3. Sri O. Balaji (F.C.A.) – FA & CAO\n4. Sri T. Venkatasuneelu – Educational Officer\n5. Dr. N. Venugopal Reddy – Principal",
    "executive officer": "👤 **Executive Officer, TTD**: Sri M. Ravichandra (I.A.S.)",
    "joint executive officer": "👤 **Joint Executive Officer, TTD**: Sri V. Veerabrahamam (I.A.S.)",
    "educational officer": "👤 **Devasthanams Educational Officer**: Sri T. Venkatasuneelu",
    "governing body": "🏛️ **Governing Body** (2024-25) headed by **Sri B.R. Naidu** (TTD Board Chairman). 14 members including TTD officials, faculty HoDs, and external members.",
    "chairman": "🏛️ **Governing Body Chairman**: Sri B.R. Naidu (TTD Board Chairman). Student Union Chairman: **Shaik Asifa** (B.Sc Biotechnology).",
    "board chairman": "🏛️ **TTD Board Chairman**: Sri B.R. Naidu",

    # ── FACULTY – DEPARTMENTS ───────────────────────────────────────────────
    "departments": "📚 **Departments**: Biotechnology, Botany, Chemistry, Commerce, Computer Science, Dairy Science, Economics, Electronics, English, Environmental Science, Hindi, History, Mathematics, Microbiology, Physics, Political Science, Psychology, Sanskrit, Statistics, Telugu, Zoology, Library Science, Physical Education.",

    "biotechnology": "🧬 **Biotechnology Dept**:\n1. Dr. A. Sarangapani – Professor & Head (📞 9441481579)\n2. Dr. P. Mohan – C. Lecturer (📞 8985176265)",
    "biotech": "🧬 **Biotechnology Dept**: Head – Dr. A. Sarangapani (📞 9441481579)",
    "biotech hod": "🧬 **HoD Biotechnology**: Dr. A. Sarangapani — 📞 9441481579",

    "botany": "🌿 **Botany Dept**:\n1. Smt. A. Surekha – Assoc. Prof. & Head (📞 9966262642)\n2. Dr. M. Sudhakar – C. Lecturer (📞 8897038200)",
    "botany hod": "🌿 **HoD Botany**: Smt. A. Surekha — 📞 9966262642",

    "chemistry": "⚗️ **Chemistry Dept** (Head: Prof. P.V. Chalapathi 📞 9985349313):\n1. Prof. P.V. Chalapathi – Prof. & Head\n2. Prof. K. Siva Kumar – Professor (📞 9290080843)\n3. Dr. A. Sarangapani – Assoc. Prof. (📞 9441481579)\n4. Dr. A. Uma Maheswari – Lecturer (📞 9063934514)\n5. Dr. K. Jamuna (📞 9966222714)\n6. Dr. R. Kishore Kumar (📞 8106545107)\n7. Sri D. Prabhakar (📞 7097906377)\n8. Dr. K. Purushotham Naidu (📞 9491152201)\n9. Dr. K. Sankara Reddy (📞 9603633263)",
    "chemistry hod": "⚗️ **HoD Chemistry**: Prof. P.V. Chalapathi — 📞 9985349313",
    "chalapathi": "⚗️ **Prof. P.V. Chalapathi** – Professor & Head, Chemistry Dept. Also in-charge for Microbiology & Environmental Science. 📞 9985349313",

    "commerce": "💰 **Commerce Dept** (Head: Prof. Y. Mallikarjun Rao 📞 9848533623):\n1. Prof. Y. Mallikarjun Rao – Prof. & Head\n2. Prof. S. Usha – Professor (📞 9848870033)\n3. Dr. B. Nageswar Naik – Lecturer (📞 8499855674)\n4. Dr. G. Venkata Ratnam – Lecturer on Deputation (📞 8179332728)\n5. Dr. K. Hema Sundar Raju (📞 9247851024)\n6. Dr. D. Lakshmi Narayana Raju (📞 9502729867)\n7. Dr. D. Raja (📞 9441645670)\n8. Dr. M. Ravi Prasad (📞 9701463463)",
    "commerce hod": "💰 **HoD Commerce**: Prof. Y. Mallikarjun Rao — 📞 9848533623",
    "mallikarjun rao": "💰 **Prof. Y. Mallikarjun Rao** – HoD Commerce. 📞 9848533623. Also: Alumni Association Exec Secretary, IIC NIRF Coordinator, Timetable Committee Co-ordinator.",

    "computer science": "💻 **Computer Science Dept** (Head i/c: Prof. K. Kameswara Rao 📞 9550559568):\n1. Prof. K. Kameswara Rao – Prof. & HoD i/c\n2. Sri K.N.V.V.S.S.S. Chakravarthy (📞 9505123979)\n3. Sri V. Chennakesavulu Reddy (📞 9494744008)\n4. Dr. P. Jyotsna (📞 9704835308)\n5. Sri G. Jayachandra Naidu (📞 9397366874)\n6. Smt. C. Kiranmayi (📞 9866182367)\n7. Smt. G. Pallavi (📞 9908049739)\n8. Sri V. Kamalanadhan (📞 9701602609)\n9. Sri A. Sukesh Reddy (📞 9885884228)\n10. Sri D. Suresh Babu (📞 9666748484)\n11. Smt. N. Sudha Rani – Jr. Computer Operator (📞 8106798250)",
    "cs": "💻 **Computer Science**: Head i/c – Prof. K. Kameswara Rao (📞 9550559568)",
    "computer science hod": "💻 **HoD i/c Computer Science**: Prof. K. Kameswara Rao — 📞 9550559568",
    "bca": "💻 **B.C.A. Honours (Science)**: Strength 50, Fee ₹11,045/-. Managed under Computer Science Dept.",

    "dairy science": "🥛 **Dairy Science Dept**: Dr. K. Uma Rani – Professor & Head. 📞 9963299969",
    "dairy science hod": "🥛 **HoD Dairy Science**: Dr. K. Uma Rani — 📞 9963299969",
    "uma rani": "🥛 **Dr. K. Uma Rani** – Prof. & Head, Dairy Science. Also Psychology Dept. 📞 9963299969. Student Counselling Coordinator, IIC Convener.",

    "economics": "📊 **Economics Dept**:\n1. Dr. M. Kiran Kumar Raju – Prof. & Head (📞 9963640650)\n2. Dr. A. Seshadri – C. Lecturer (📞 7981600052)",
    "economics hod": "📊 **HoD Economics**: Dr. M. Kiran Kumar Raju — 📞 9963640650",
    "kiran kumar": "📊 **Dr. M. Kiran Kumar Raju** – HoD Economics. 📞 9963640650. Also: Associate Red Cross, Nodal Officer Internship, IIC Internship Coordinator.",

    "electronics": "⚡ **Electronics Dept**:\n1. Sri C. Ratna Rao – Sr. Lec. & Head (📞 8790835429)\n2. Smt. K. Mahitha Delhi Rani (📞 9703602704)\n3. Dr. D. Sri Silpa (📞 9533952909)\n4. Smt. K. Swapna (📞 9885496536)\n5. Sri Y. Hari – Tech. Asst. (📞 9849983229)",
    "electronics hod": "⚡ **HoD Electronics**: Sri C. Ratna Rao — 📞 8790835429",
    "ratna rao": "⚡ **Sri C. Ratna Rao** – HoD Electronics & Governing Body Member. 📞 8790835429. Academic Cell Coordinator, Science Club, Website Committee.",

    "english": "📖 **English Dept**:\n1. Dr. S. Markandeyan – Sr. Lec. & Head (📞 9441495414)\n2. Sri C. Muneendran – Sr. Lecturer (📞 9441492596)\n3. Smt. B. Sreedevi – C. Lecturer (📞 9291373659)",
    "english hod": "📖 **HoD English**: Dr. S. Markandeyan — 📞 9441495414",
    "markandeyan": "📖 **Dr. S. Markandeyan** – HoD English, Calendar Committee Co-ordinator, SC/ST Committee Member. 📞 9441495414",

    "environmental science": "🌍 **Environmental Science Dept**:\n1. Prof. P.V. Chalapathi – Prof. & Head i/c (📞 9985349313)\n2. Dr. P. Nagaraju – C. Lecturer (📞 9989871850)\n3. Dr. P. Sreevani – C. Lecturer (📞 9848699956)",

    "hindi": "🗣️ **Hindi Dept**: Smt. T. Thriveni – Assoc. Prof. & Head. 📞 6300586591",
    "hindi hod": "🗣️ **HoD Hindi**: Smt. T. Thriveni — 📞 6300586591",

    "history": "🏺 **History Dept**:\n1. Prof. G. Kishan – Prof. & Head (📞 8919672096)\n2. T. Jayaramaiah – Sr. Lecturer (📞 9703078308)\n3. E. Madhusudan Rao – Lecturer (📞 9441776545)",
    "history hod": "🏺 **HoD History**: Prof. G. Kishan — 📞 8919672096",
    "kishan": "🏺 **Prof. G. Kishan** – HoD History. 📞 8919672096. Calendar Committee Editor, Career Guidance Cell, SC/ST Committee Coordinator, IIC Member.",

    "mathematics": "📐 **Mathematics Dept**:\n1. Prof. P. Baskarudu – Prof. & Head (📞 9490108326, on deputation to SVU Vedic University)\n2. Smt. P. Vijaya Sree – Head & Sr. Lec. (📞 9949631991)\n3. Sri E. Rama Krishna Reddy – Sr. Lec. (📞 9963844499)\n4. Capt. V. Ramesh – Sr. Lec. (📞 9492855008)\n5. Dr. B. Govindarajulu – C. Lec. (📞 9247446451)\n6. Smt. B. Sasi Kala – C. Lec. (📞 8919236821)",
    "maths": "📐 **Mathematics Dept**: Head – Prof. P. Baskarudu (on deputation). Acting Head: Smt. P. Vijaya Sree (📞 9949631991)",
    "mathematics hod": "📐 **HoD Mathematics**: Prof. P. Baskarudu (📞 9490108326) — currently on deputation. Acting: Smt. P. Vijaya Sree (📞 9949631991)",
    "capt ramesh": "📐 **Capt. V. Ramesh** – Sr. Lec. Mathematics. 📞 9492855008. NCC ANO, Discipline Committee Coordinator, Examination Dy. Controller.",
    "vijaya sree": "📐 **Smt. P. Vijaya Sree** – Head & Sr. Lec., Mathematics. 📞 9949631991. IIC Innovation Activity Coordinator, IQAC Member.",

    "microbiology": "🦠 **Microbiology Dept**:\n1. Prof. P.V. Chalapathi – Prof. & Head i/c (📞 9985349313)\n2. Dr. J. Hima Bindu – C. Lec. (📞 9885455977)\n3. Dr. P. Sandhya Priya – C. Lec. (📞 9346760577)",
    "microbiology hod": "🦠 **HoD Microbiology (i/c)**: Prof. P.V. Chalapathi — 📞 9985349313",
    "hima bindu": "🦠 **Dr. J. Hima Bindu** – C. Lec. Microbiology. 📞 9885455977",

    "physics": "🔭 **Physics Dept** (Head: Sri C. Subramanyam 📞 9948164776):\n1. Sri C. Subramanyam – Assoc. Prof. & Head\n2. Prof. Y. Dasaradhudu – Professor (📞 9440054764)\n3. Prof. K. Kameswara Rao – Professor (📞 9550559568)\n4. Prof. R. Ravi Kumar – Professor (📞 9440472062)\n5. Prof. A.V. Chandra Sekhar – Professor (📞 9441010555)\n6. Dr. P. Giri Prakash (📞 9290898291)\n7. Sri G.A.N. Sreenivasa Rao (📞 9951121655)\n8. Dr. V.H.H. Surendra Babu (📞 9515082379)",
    "physics hod": "🔭 **HoD Physics**: Sri C. Subramanyam — 📞 9948164776",
    "subramanyam": "🔭 **Sri C. Subramanyam** – Assoc. Prof. & Head, Physics. 📞 9948164776. Maths & Science Association VP.",
    "dasaradhudu": "🔭 **Prof. Y. Dasaradhudu** – Professor, Physics. 📞 9440054764. Research guidance available.",
    "chandra sekhar": "🔭 **Prof. A.V. Chandra Sekhar** – Professor, Physics. 📞 9441010555. Research Cell Coordinator, Planning Committee Research Coordinator.",

    "political science": "🗳️ **Political Science Dept**:\n1. Sri T. Sreenath – Sr. Lec. & Head (📞 9441642634)\n2. Sri N. Suresh Kumar – Lecturer (📞 9441606794)\n3. Dr. K. Narasimhulu – C. Lec. (📞 9985038780)",
    "political science hod": "🗳️ **HoD Political Science**: Sri T. Sreenath — 📞 9441642634",

    "psychology": "🧠 **Psychology Dept**:\n1. Dr. K. Uma Rani – Prof. & Head (📞 9963299969)\n2. Dr. N.N. Sudha Rani – C. Lec. (📞 9440247894)\n🔬 Research Guidance: Dr. K. Uma Rani (📞 8985136140)",
    "psychology hod": "🧠 **HoD Psychology**: Dr. K. Uma Rani — 📞 9963299969",

    "sanskrit": "📜 **Sanskrit Dept**: Currently **Vacant**.",

    "statistics": "📈 **Statistics Dept**:\n1. Prof. M. Pedda Reddeppa Reddy – Prof. & Head (📞 9885625554)\n2. Dr. N. Ramesh Kumar – C. Lec. (📞 9885234903)",
    "statistics hod": "📈 **HoD Statistics**: Prof. M. Pedda Reddeppa Reddy — 📞 9885625554",

    "telugu": "🔤 **Telugu Dept** (Head: Prof. N. Bheemanna 📞 9949060771):\n1. Prof. N. Bheemanna – Prof. & Head\n2. Dr. P. Lokanadha Mandadi – Sr. Lec. (📞 9441075059)\n3. Sri G. Venkateswarlu – Sr. Lec. (📞 7207552712)\n4. Dr. M. Prasada Rao – Asst. Prof. (📞 9440467046)\n5. Dr. B. Tejovani – C. Lec. (📞 8096117693)\n6. Dr. A. Munaswamy Achari – C. Lec. (📞 9492067294)\n🔬 Research Guidance: Prof. N. Bheemanna",
    "telugu hod": "🔤 **HoD Telugu**: Prof. N. Bheemanna — 📞 9949060771",
    "bheemanna": "🔤 **Prof. N. Bheemanna** – HoD Telugu. 📞 9949060771. Language Association VP. Debate Club, Language Lab, Public Relations Committee.",

    "zoology": "🦎 **Zoology Dept**:\n1. Prof. M. Vani – Prof. & Head (📞 9885002295)\n2. Dr. P.S. Poornima – C. Lec. (📞 9182088973)\n3. B. Bhanu Prakash Reddy – C. Lec. (📞 9959988499)\n4. Dr. P. Annaiah – C. Lec. (📞 9849202212)",
    "zoology hod": "🦎 **HoD Zoology**: Prof. M. Vani — 📞 9885002295",
    "vani": "🦎 **Prof. M. Vani** – HoD Zoology. 📞 9885002295. Health Centre Coordinator, Value Education Cell, Planning Committee Member.",

    "library science": "📚 **Library Science Dept**: Currently **Vacant**.",
    "physical education": "🏃 **Physical Education Dept**:\n1. Sri P. Kumar – HoD & Physical Director (📞 9052216777, on deputation to SGSAC)\n2. Dr. S. Mustaq Ahmed (📞 9052216777)",
    "physical director": "🏃 **Physical Director**: Sri P. Kumar (📞 9052216777, on deputation). Dr. S. Mustaq Ahmed also handles duties (📞 9052216777).",
    "mustaq ahmed": "🏃 **Dr. S. Mustaq Ahmed** – Physical Education. 📞 9052216777. Games & Sports Convener, Anti-Ragging Committee, Discipline Committee.",

    # ── PROGRAMMES / COURSES ────────────────────────────────────────────────
    "courses": "📚 **Programmes Offered** (Year 1, 2025-26):\n**B.A.**: Political Science, History, Special English, Special Telugu, Economics\n**B.Com**: Computer Applications, General\n**B.Sc**: CS, Aquaculture, Maths, Data Science, Statistics, Psychology, Physics, Microbiology, Biotechnology, Electronics, Botany, Zoology, Chemistry, AI, Quantum Technologies\n**B.B.A.** & **B.C.A.**\nTotal Strength: 1,417",
    "programmes": "📚 College offers **B.A., B.Com., B.Sc., B.B.A., B.C.A.** Honours programs. 25 programmes available in Year 1.",
    "ba": "🎓 **B.A. Honours** programs: Political Science (60 seats), History (60), Special English (30), Special Telugu (40), Economics (100). Fee: ₹5,400/-",
    "bcom": "🎓 **B.Com Honours**: Computer Applications (180 seats, ₹10,845/-), General (180 seats, ₹5,400/-)",
    "bsc": "🎓 **B.Sc. Honours**: CS, Aquaculture, Maths, Data Science, Statistics, Psychology, Physics, Microbiology, Biotechnology, Electronics, Botany, Zoology, Chemistry, AI, Quantum Tech. Fees: ₹5,600 – ₹11,045/-",
    "bba": "🎓 **B.B.A. Honours**: 60 seats per section (2 sections), Fee: ₹10,845/-",
    "artificial intelligence": "🤖 **B.Sc. Honours (Artificial Intelligence)**: 30 seats, Fee: ₹11,045/-, Medium: English",
    "ai course": "🤖 **B.Sc. Honours (AI)**: 30 seats, ₹11,045/-. New course offered from 2025-26.",
    "quantum": "⚛️ **B.Sc. Honours (Quantum Technologies)**: 50 seats, Fee: ₹11,045/-. New course.",
    "data science": "📊 **B.Sc. Honours (Data Science)**: 50 seats, Fee: ₹11,045/-, Medium: English.",
    "aquaculture": "🐟 **B.Sc. Honours (Aquaculture)**: 30 seats, Fee: ₹11,045/-",
    "total strength": "👥 **Total Sanctioned Strength** (all programmes): **1,417 seats**.",

    # ── FEES ─────────────────────────────────────────────────────────────────
    "fee": "💸 **Fee Structure**:\n- B.A. / B.Com (G) / B.Sc (basic): ₹5,400/-\n- B.Sc (Physics, Maths, Statistics, Psychology, Electronics, Botany, Zoology, Chemistry): ₹5,600/-\n- B.Com (CA) / B.B.A.: ₹10,845/-\n- B.Sc (CS, Aquaculture, Data Sci, Microbio, Biotech, AI, Quantum, BCA): ₹11,045/-",
    "fees": "💸 **Fee Structure**:\n- B.A. / B.Com General: ₹5,400/-\n- B.Sc (basic sciences): ₹5,600/-\n- B.Com CA / BBA: ₹10,845/-\n- B.Sc (CS, Biotech, AI etc.): ₹11,045/-\nYear 1 fees paid at admission. Year 2 at III Semester start. Year 3 at V Semester start.",
    "fee payment": "💸 **Fee Payment**:\n- Year 1: At time of Admissions\n- Year 2: At beginning of III Semester\n- Year 3: At beginning of V Semester\nName removed from rolls if fees not paid.",
    "bcom ca fee": "💸 **B.Com (Computer Applications) Fee**: ₹10,845/-",
    "bsc fee": "💸 **B.Sc. Fees**: Basic sciences ₹5,600/-. CS, Biotech, AI, Data Science: ₹11,045/-",
    "ba fee": "💸 **B.A. Fee**: ₹5,400/- for all B.A. programmes.",

    # ── SCHOLARSHIPS ─────────────────────────────────────────────────────────
    "scholarship": "🎓 **12 Scholarship Categories** (75% attendance required):\n1. Govt. of India (SC/ST)\n2. State Social Welfare – SC/ST\n3. State Social Welfare – BC\n4. State Social Welfare – EBC\n5. National Merit Scholarship\n6. State Special Merit\n7. State General Merit\n8. Teachers' Children\n9. Ex-Servicemen Children\n10. Physically Challenged\n11. Sports Talent\n12. Poor Boys Scholarship",
    "scholarships": "🎓 College offers **12 types of scholarships**. Minimum **75% attendance** required. Categories include SC/ST, BC, EBC, Merit, Sports, Ex-servicemen, Physically Challenged, and more.",
    "sc st scholarship": "🎓 **SC/ST Scholarship**: Govt. of India Social Welfare Scholarship + State Social Welfare Scholarship. Parents' income up to ₹1,00,000/- per annum.",
    "merit scholarship": "🎓 **National Merit Scholarship**: Minimum 50% average marks. Parents' income up to ₹1,00,000/- per annum.",
    "sports scholarship": "🎓 **Sports Talent Scholarship**: Obtain details from college office.",
    "scholarship attendance": "⚠️ **Minimum 75% attendance** is mandatory to receive any scholarship.",

    # ── ACADEMIC SCHEDULE ────────────────────────────────────────────────────
    "academic schedule": "📅 **Academic Schedule 2025-26**:\n- Odd Semesters (I/III/V): Classes from 18-09-2025, Dasara 28-09 to 05-10, Exams 09-02-2026 to 13-02-2026\n- Even Sem (Conventional): Classes from 16-06-2025, Exams 22-10-2025\n- BBA/BCA Sem I: Classes from 07-06-2025, Exams 04-12-2025\n- Autonomous II/IV Sem: Classes from 10-11-2025, Exams 03-04-2026",
    "semester": "📅 **Semester Info**: 2 semesters per year. Odd sem starts 18-09-2025. Autonomous II/IV sem starts 10-11-2025.",
    "exam date": "📝 **Exam Dates 2025-26**:\n- Odd Sem Theory: 09-02-2026 to 13-02-2026\n- Odd Sem Practicals: 14-02-2026 to 18-02-2026\n- Even Sem (Conventional): 22-10-2025\n- BBA/BCA Sem I: 04-12-2025\n- Autonomous II/IV: 03-04-2026",
    "exam": "📝 **Exam Schedule**: Odd Sem Theory 09-02-2026 to 13-02-2026. Practicals 14-02-2026 to 18-02-2026.",
    "exams": "📝 **Exams**: Odd Sem 09-02-2026 to 13-02-2026. Internal exams held at end of each semester.",
    "class start": "🏫 **Classes Start**: Odd Sem – 18-09-2025 (Monday). Even Sem – 16-06-2025. BBA/BCA – 07-06-2025. Autonomous II/IV – 10-11-2025.",
    "commencement": "🏫 **Commencement of Classes** (Odd Sem): **18-09-2025** (Monday). Applicable to all UG courses including BBA & BCA.",

    # ── HOLIDAYS ─────────────────────────────────────────────────────────────
    "holiday": "📅 **Major Holidays 2025-26**:\n- Dasara: 28-09-2025 to 05-10-2025\n- Sankranthi (Pongal): 10-01-2026 to 18-01-2026\n- Independence Day: 15 Aug 2025\n- Republic Day: 26 Jan 2026\n- Gandhi Jayanthi: 02 Oct 2025\n- Vinayaka Chavithi, Maha Sivaratri, Ugadhi — as per calendar",
    "holidays": "📅 **Holidays**: Dasara (28 Sep – 5 Oct), Sankranthi (10–18 Jan 2026), Independence Day, Republic Day, Gandhi Jayanthi and others as per college calendar.",
    "dasara": "🎉 **Dasara Holidays**: 28-09-2025 to 05-10-2025 (Odd Sem). BBA/BCA: 06-10-2025 to 13-10-2025.",
    "pongal": "🎉 **Pongal/Sankranthi Holidays**: 10-01-2026 to 18-01-2026.",
    "sankranthi": "🎉 **Sankranthi Holidays**: 10-01-2026 to 18-01-2026.",
    "independence day": "🇮🇳 **Independence Day**: 15 August 2025 – Holiday.",
    "republic day": "🇮🇳 **Republic Day**: 26 January 2026 – Holiday.",
    "gandhi jayanthi": "🎗️ **Gandhi Jayanthi**: 2 October 2025 – Holiday.",
    "sivaratri": "🕉️ **Maha Sivaratri**: In February 2026 – Holiday (as per calendar).",
    "ugadhi": "🎊 **Ugadhi**: In March 2026 – Holiday (as per calendar).",

    # ── ATTENDANCE ────────────────────────────────────────────────────────────
    "attendance": "📋 **Attendance Rules**:\n- Minimum **75%** attendance required for promotion.\n- **50%** minimum for condonation (fee: ₹500/-)\n- 5 periods per day, 1 hour each.\n- Absence without leave = 2 days absent.\n- Absent 3+ days without leave → name removed from rolls.",
    "75 percent": "⚠️ **75% attendance** is mandatory for promotion to next class and to appear for exams.",
    "condonation": "⚠️ **Condonation**: Students with 50% attendance can apply with **₹500/- fee**. Submit to Controller of Examinations before exams. NOT eligible to study higher courses.",
    "attendance shortage": "⚠️ **Attendance Shortage**: Condonation available at 50% with ₹500/- fee. Below 50% — must repeat year. Not eligible for higher studies.",
    "late": "⏰ Students coming **late to class** are liable to be fined.",
    "medical certificate": "🏥 **Medical Certificate** is required for absence due to illness.",
    "leave": "📝 Leave must be applied **before** going on leave. Late cancellation must be reported to Principal immediately on return.",

    # ── DISCIPLINE & RULES ────────────────────────────────────────────────────
    "discipline": "📏 **Rules of Discipline**:\n- No public demonstrations or political agitations.\n- Students must wear **identity card** always.\n- Rise when teacher enters class.\n- No leaving class without permission.\n- Internal exams at end of each semester.",
    "rules": "📏 **Key Rules**: 75% attendance. Wear uniform and ID card. No ragging. No mobile in class. Respect teachers. No political activities.",
    "conduct": "📏 Students must rise when teacher enters, not leave class without permission, maintain proper conduct inside and outside college premises.",
    "identity card": "🪪 **Identity Card** must be worn at all times and is **compulsory** during University Semester Examinations.",
    "id card": "🪪 College **identity card** must always be worn. Compulsory at University Semester Examinations.",

    # ── DRESS CODE ────────────────────────────────────────────────────────────
    "uniform": "👔 **Uniform**:\n- 👦 Boys: **Sky Blue shirt + Navy Blue pant**\n- 👧 Girls: **Blue salwar kameez, Navy Blue bottom + Sky Blue top**",
    "dress code": "👔 **Dress Code**:\n- Boys: Sky Blue shirt & Navy Blue pant\n- Girls: Blue salwar kameez, Navy Blue bottom & sky blue top",
    "dress": "👔 Boys: Sky Blue shirt + Navy Blue pant. Girls: Blue salwar kameez, Navy Blue bottom, sky blue top.",

    # ── RAGGING ───────────────────────────────────────────────────────────────
    "ragging": "🚫 **RAGGING IS STRICTLY PROHIBITED — IT IS A CRIME!**\nPunishment: Imprisonment 6 months OR Fine ₹5,000 OR Both + Dismissal.\nEmergency contacts:\n📞 Dy. SP: 9440796702 (0877-2289001)\n📞 Dy. SP: 9440796703 (0877-2289041)\n📞 SP: 9440796747\n📞 Inspector: 9491074524",
    "anti ragging": "🚫 **Anti-Ragging**: Strictly prohibited. Committee headed by Principal (📞 9000489182). Report to Inspector: **9491074524**.",
    "ragging complaint": "🚫 **Ragging Complaint**: Call Inspector of Police: **9491074524** or Dy. SP: **9440796702**. Ragging = crime + dismissal from college.",

    # ── MOBILE/CELL PHONE ─────────────────────────────────────────────────────
    "mobile": "📵 **Mobile Phone Rules**:\n- Using mobile inside college: ₹1,000/- fine\n- Obscene content/messaging: ₹2,000/-\n- Cyberbullying/stalking (5+ persons): ₹10,000/-\n- Criminal use (10+ persons): ₹50,000 to ₹2,50,000 or imprisonment",
    "cell phone": "📵 Mobile phones are restricted. Fine for use inside college: **₹1,000/-**. Stricter penalties for misuse.",
    "phone": "📵 Mobile phone use inside college is **fined ₹1,000/-**. Stricter penalties for cyberbullying or harassment.",

    # ── LIBRARY RULES ─────────────────────────────────────────────────────────
    "library rules": "📚 **Library Rules**:\n- Hours: 9:30 AM – 5:00 PM\n- Issue: Mon/Wed/Fri | Return: Tue/Thu/Sat\n- Loan period: 15 days\n- Overdue fine: ₹1/- per day\n- Staff: 20 books | Students: 2 books\n- Reference books cannot be borrowed\n- No sub-lending",
    "library timing": "📚 **Library Timing**: 9:30 AM to 5:00 PM on all working days.",
    "library fine": "📚 **Library Overdue Fine**: ₹1/- per day. Lost ticket fee: ₹5/-. Lost book must be replaced or cost paid.",
    "library books": "📚 Students allowed **2 tickets** (books). Staff: 20 tickets. Research scholars: 5 extra.",

    # ── HOSTEL ────────────────────────────────────────────────────────────────
    "hostel warden": "🏠 **Hostel Warden**: Dr. P. Lokanadha Mandadi (Sr. Lec. Telugu) — 📞 9441075059",
    "warden": "🏠 **Warden**: Dr. P. Lokanadha Mandadi — 📞 9441075059\n**Deputy Wardens**: Dr. M. Prasada Rao (📞 9440467046), G. Venkateswarlu (📞 7207552712), Dr. B. Nageswar Naik (📞 8499855674)",
    "hostel contact": "🏠 Hostel Warden: Dr. P. Lokanadha Mandadi — 📞 **9441075059**",

    # ── NCC / NSS ─────────────────────────────────────────────────────────────
    "ncc": "🎖️ **NCC Officers**:\n1. Capt. V. Ramesh – ANO, 29(A) Bn. (📞 9492855008)\n2. Dr. K. Purushotham Naidu – ANO, 2(A) R&V Regt. (📞 9491152201)\n3. Dr. A. Umamaheswari – ANO, 11(A) Air Sqn.",
    "nss": "🌟 **NSS Programme Officers**:\n1. Dr. M.P. Reddeppa Reddy (Prof. & HoD Statistics)\n2. Sri E. Madhusudhana Rao (Lec. History — 📞 9441776545)",

    # ── STUDENTS UNION ────────────────────────────────────────────────────────
    "student union": "🎓 **Students Union 2025-26**:\n- President: Prof. N. Venugopal Reddy (Principal)\n- Vice President: Prof. Y. Mallikarjun Rao (HoD Commerce)\n- Chairman: **Shaik Asifa** (B.Sc Biotechnology)\n- Secretary: **P. Lasya Priya** (B.Com CA)",
    "student president": "🎓 **Student Union President**: Prof. N. Venugopal Reddy (Principal)",
    "student chairman": "🎓 **Student Union Chairman**: **Shaik Asifa** (B.Sc Biotechnology)",
    "student secretary": "🎓 **Student Union Secretary**: **P. Lasya Priya** (B.Com Computer Application)",
    "shaik asifa": "🎓 **Shaik Asifa** – Student Union **Chairman** 2025-26. B.Sc Biotechnology student.",
    "lasya priya": "🎓 **P. Lasya Priya** – Student Union **Secretary** 2025-26. B.Com Computer Application student.",
    "arts association": "🎭 **Arts Association**: VP – Prof. G. Kishan (HoD History). Secretary – SR. Balaji (III B.A. Political Science). Joint Sec – K. Thulasi Saksha.",
    "commerce association": "💰 **Commerce Association**: VP – Prof. S. Usha. Secretary – P. Kavya Yadhav (III BCA). Joint Sec – V. Sai Satwik (III B.Com).",
    "games association": "🏃 **Games & Sports Association**: VP – Dr. S. Mustaq Ahmed. Secretary – Mr. Sura Sura Hari (📞 6301857080). Joint Sec – Ms. R. Revathi (📞 8074401764).",
    "language association": "🗣️ **Language Association**: VP – Prof. N. Bheemanna (HoD Telugu). Secretary – A. Priyanka (III B.Sc Statistics).",
    "cultural association": "🎭 **Cultural Association**: VPs – Prof. M. Kiran Kumar Raju & Smt. P. Vijayasree. Boys Sec – Mr. S. Hasan Vali (📞 9989591712). Girls Sec – Ms. Prabhavathi.",
    "maths science association": "🔬 **Maths & Science Association**: VP – Sri C. Subramanyam (HoD Physics). Secretary – A. Pavitra Saram (III B.Sc Psychology).",

    # ── COMMITTEES ───────────────────────────────────────────────────────────
    "iqac": "📋 **IQAC (Internal Quality Assurance Cell)**: Chairperson – Prof. N. Venugopal Reddy (Principal). Co-ordinator – Prof. Y. Mallikarjun Rao (📞 9848533623).",
    "examination cell": "📝 **Examination Cell (Autonomous)**:\n- Controller of Exams: Prof. P.V. Chalapathi (📞 9985349313)\n- Dy. Controller: Prof. K. Kameswara Rao (📞 9550559568)\n- Dy. Controller: Capt. V. Ramesh (📞 9492855008)",
    "controller of examinations": "📝 **Controller of Examinations**: Prof. P.V. Chalapathi — 📞 9985349313",
    "grievance": "📣 **Grievance Redressal Cell**: Convener – Sri E. Ramakrishna Reddy (📞 9963844499). Members: Dr. N.N. Sudha Rani (📞 9440247894), Dr. P. Sreevani (📞 9848699956).",
    "grievance redressal": "📣 **Grievance Redressal**: Contact Sri E. Ramakrishna Reddy — 📞 **9963844499**",
    "anti drug": "🚫 **Anti-Drug Committee**: Chairperson – Principal (📞 9000489182). Members include Prof. K. Sivakumar, Prof. R. Ravi Kumar, Dr. J. Hima Bindu.",
    "women empowerment": "👩 **Women Empowerment & Protection Cell**: Coordinator – Dr. K. Uma Rani (📞 9963299969). Members: Dr. D. Sri Silpa, Smt. K. Swapna, Dr. N.N. Sudha Rani.",
    "sexual harassment": "👩 **Sexual Harassment Committee**: Coordinator – Dr. K. Uma Rani (📞 9963299969). Report to: 📞 9963299969",
    "iic": "💡 **IIC (Institutional Innovation Council)**:\n- President: Dr. N. Venugopal Reddy (📞 9000489182)\n- Convener: Dr. K. Uma Rani (📞 9963299969)\n- VP: Dr. K. Kameswara Rao (📞 9934787766)",
    "skill development": "🎓 **Skill Development & Placement Cell**: Coordinator – Dr. S. Markandeyan (📞 9441495414). Skill Development Centre active from 2016-17.",
    "placement": "🎓 **Placement Cell**: Coordinator – Dr. S. Markandeyan (📞 9441495414).",
    "research cell": "🔬 **Research Cell**: Coordinator – Prof. A.V. Chandra Sekhar (📞 9441010555). Research guidance available in Chemistry, Physics, Telugu, Psychology, Zoology.",
    "career guidance": "🎯 **Career Guidance & Competitive Cell**: Coordinator – Prof. G. Kishan (📞 8919672096). Helps students prepare for competitive exams.",
    "science club": "🔬 **Science Club**: Coordinator – Sri C. Ratna Rao (📞 8790835429).",
    "debate club": "🗣️ **Debate Club**: Coordinator – Prof. N. Bheemanna (📞 9949060771).",
    "red ribbon": "🎀 **Red Ribbon Club**: Coordinator – Prof. P.V. Chalapathi (📞 9985349313).",
    "red cross": "🏥 **Associate Red Cross**: Coordinator – Dr. M. Kiran Kumar Raju (HoD Economics).",
    "youth red cross": "🏥 **Youth Red Cross**: Members include Dr. M. Kiran Kumar Raju (📞 9963640650), Sri T. Jayaramaiah (📞 9703078308).",
    "cie": "💡 **Centre for Innovation Incubation & Entrepreneurship (CIE)**: Coordinator – Prof. R. Ravi Kumar (📞 9440472062).",
    "consumer club": "🛒 **Consumer Club Commerce Association**: Coordinator – Prof. Y. Mallikarjun Rao (📞 9848533623).",
    "poor students": "💝 **Poor Students Aid Fund**: Coordinator – Dr. A. Sarangapani (📞 9441481579). Members include Dr. R. Kishore Kumar, Sri K. Hemasundar Raju.",
    "sramadanam": "🌿 **Swacha Bharath Committee (Sramadanam)**: Coordinator – Prof. M. Pedda Reddeppa Reddy (📞 9885625554).",
    "value education": "📖 **Value Education Cell**: Coordinator – Prof. M. Vani (📞 9885002295).",
    "sports day": "🏅 **Sports Day Committee**: Prof. Y. Dasaradhudu (📞 9440054764), Dr. S. Mustaq Ahmed (📞 8985136140).",
    "website committee": "🌐 **Website Committee**: Coordinator – Sri C. Ratna Rao (📞 8790835429).",
    "timetable committee": "📅 **Timetable Committee**: Coordinator – Prof. Y. Mallikarjun Rao (📞 9848533623).",

    # ── IGNOU / OPEN UNIVERSITY ───────────────────────────────────────────────
    "ignou": "🎓 **IGNOU Centre Coordinator**: Prof. P. Bhaskarudu (HoD Mathematics) — 📞 9490108326",
    "open university": "🎓 **Dr. B.R. Ambedkar Open University Coordinator**: Prof. Y. Mallikarjun Rao (HoD Commerce) — 📞 9848533623",
    "distance education": "🎓 IGNOU Centre & Dr. B.R. Ambedkar Open University both operate at S.V. Arts College. Contact: Prof. P. Bhaskarudu (IGNOU) or Prof. Y. Mallikarjun Rao (BRAOU).",

    # ── SRIVARI SEVA ──────────────────────────────────────────────────────────
    "srivari seva": "🙏 **Srivari Seva**: Compulsory programme introduced by TTD. 50 students daily serve pilgrims at Tirumala — guiding, Q-line control, Nitya Annadanam service.",
    "tirumala seva": "🙏 **Srivari Seva** at Tirumala: Daily Sevas include Suprabhatham, Thomala Seva (Tue/Wed/Thu), Archana, Kalyanotsavam, and more. All prasadams include 1 Small Laddu (4 for Poorabhishekam).",

    # ── NON-TEACHING STAFF ────────────────────────────────────────────────────
    "superintendent": "👤 **Superintendent**: S. Lalitha — 📞 9490370445",
    "non teaching": "👤 **Non-Teaching Staff** (21 members):\n- Superintendent: S. Lalitha (📞 9490370445)\n- Sr. Assistant: K. Usha Shree (📞 9902928446)\n- Jr. Assistant: R. Rajani (📞 6281656465)\n- Computer Operator: N. Sudharani (📞 8106798250)\n- Museum Keeper: M. Jaya Prakash Raju (📞 9966390807)\nAnd 16 more support staff.",
    "staff": "👤 College has **21 non-teaching staff** members including Superintendent, Assistants, Shroffs, and Office Subordinates.",

    # ── ALUMNI ────────────────────────────────────────────────────────────────
    "alumni": "🌟 **Notable Alumni**:\n- Sri N. Chandra Babu Naidu (CM of A.P.)\n- Late S.P. Bala Subramanyam (Singer)\n- B. Karunakar Reddy (Former MLA)\n- Chevireddy Bhaskar Reddy (Former MLA)\n- A. Mohan (Former MLA)\n- Parasa Ratnam (Former MLA)\n- Phalguna Kumar (CA)",
    "famous alumni": "🌟 **Famous Alumni**: CM N. Chandra Babu Naidu, Singer S.P. Balasubramanyam, Multiple Former MLAs.",
    "alumni association": "🤝 **Alumni Association** (since 1970). Enrollment fee: ₹50/-. President: Principal. Contact: Dr. S. Azmal Basha (HoD Psychology).",
    "sp balasubramanyam": "🎵 **Late S.P. Bala Subramanyam** – legendary singer – is a proud alumni of S.V. Arts College.",
    "chandrababu naidu": "🏛️ **Sri N. Chandra Babu Naidu** – Chief Minister of Andhra Pradesh – is an alumni of S.V. Arts College.",

    # ── SUCCESSIVE PRINCIPALS ─────────────────────────────────────────────────
    "successive principals": "👔 S.V. Arts College has had **37 successive principals** since its founding. First: Prof. P.R. Krishna Swamy. Current: Prof. N. Venugopal Reddy (since Feb 2024).",
    "first principal": "👔 **First Principal**: Prof. P.R. Krishna Swamy (M.A., L.T.) — around 1950.",
    "founder principal": "👔 **Founder Principal**: Prof. K. Rami Reddy.",

    # ── VISION & MISSION ──────────────────────────────────────────────────────
    "vision": "🎯 **Vision**: 1. Transform mediocre students into socially responsible citizens. 2. Extend the bounds of knowledge through multidisciplinary curriculum.",
    "mission": "🎯 **Mission**: 1. Inculcate spiritual and moral values. 2. Build competent, committed professionals. 3. Empower students to fulfil academic and professional passions.",

    # ── EXAM MALPRACTICE ──────────────────────────────────────────────────────
    "malpractice": "⚠️ **Exam Malpractice Punishments**: Cheating/copying → paper cancelled + debarred 2 exams. Impersonation → 3-year debarment. Assault on invigilator → debarred 4 exams. Result cancellation for various violations.",
    "cheating": "⚠️ **Cheating in Exams**: Paper cancelled, result cancelled, debarred from next 2 examinations. Impersonation leads to **3-year debarment**.",
    "malpractice committee": "⚠️ Cases not covered by standard malpractice rules are decided by the **Malpractice Committee**.",

    # ── TELEPHONE NUMBERS ─────────────────────────────────────────────────────
    "telephone": "📞 **Important Numbers**:\n- SV Arts College: 2264602\n- TTD PBX (Tirupati): 0877-2231777\n- SVU Registrar: 2289545\n- SVU Controller of Exams: 2289547\n- SVU Police Station: 2289009",
    "phone numbers": "📞 **Key Contacts**:\n- SV Arts College: 2264602\n- TTD PBX Tirupati: 0877-2231777\n- TTD PBX Tirumala: 0877-2277777\n- SVU Registrar: 2289545\n- Ragging Helpline: 9491074524",
    "svims": "🏥 **SVIMS**: 2287777",
    "svu": "🎓 **S.V. University (SVU)**:\n- Registrar: 2289545\n- Joint Registrar: 2289418\n- Controller of Exams: 2289547\n- CE (UG): 2289398\n- Academic: 2289320",
    "tirupati numbers": "📞 **Tirupati TTD Numbers**: TTD PBX 0877-2231777, JEO: 2264977/2264160, PRO: 2264392, DEO: 2264522",
    "tirumala numbers": "📞 **Tirumala Numbers**: TTD PBX 0877-2277777, JEO: 2263766, Arjitha Seva: 2263277, Srivari Seva: 2263679",

    # ── MENTOR SYSTEM ─────────────────────────────────────────────────────────
    "mentor": "👥 **Mentor System**: Each class is assigned a mentor who supervises academic progress and acts as a local guardian. Mentors list is available for all 3 years.",
    "mentors": "👥 **Mentors (2025-26)**: Available for all Years 1, 2, and 3 across all departments. Each class has a dedicated mentor.",
    "mentor year 1": "👥 **Year 1 Mentors** (sample):\n- History: Sri E. Madhusudhana Rao (📞 9441776545)\n- CS-1 & CS-2: Sri K.N.V.V.S.S. Chakravarthy (📞 9505123979)\n- Physics: Dr. Y. Dasaradhudu\n- Maths: Capt. V. Ramesh (📞 9492855008)",

    # ── NATIONAL / INTERNATIONAL DAYS ────────────────────────────────────────
    "teachers day": "🎉 **Teachers Day**: September 5 — celebrated at S.V. Arts College.",
    "independence day date": "🇮🇳 **Independence Day**: 15 August 2025 (Saturday) — Holiday.",
    "republic day date": "🇮🇳 **Republic Day**: 26 January 2026 (Monday) — Holiday.",
    "gandhi jayanthi date": "🎗️ **Gandhi Jayanthi**: 2 October 2025 (Thursday) — Holiday.",
    "ambedkar jayanthi": "🎗️ **Dr. B.R. Ambedkar Jayanthi**: 14 April — celebrated at college.",
    "women day": "👩 **International Women's Day**: March 8 — observed at college.",
    "science day": "🔬 **National Science Day**: February 28 — celebrated at S.V. Arts College.",
    "world aids day": "🎀 **World AIDS Day**: December 1.",
    "nss day": "🌟 **NSS Day**: September 24.",
    "ozone day": "🌍 **World Ozone Day**: September 16.",

    # ── CONTACT ALL ───────────────────────────────────────────────────────────
    "contact": "📞 **Key Contacts**:\n- Principal: 9000489182\n- Superintendent: 9490370445\n- Hostel Warden: 9441075059\n- College Phone: 2264602\n- Anti-Ragging: 9491074524\n- Grievance: 9963844499",
    "emergency": "🚨 **Emergency Contacts**:\n- Principal: 9000489182\n- Anti-Ragging / Inspector: 9491074524\n- Dy. SP: 9440796702\n- Grievance Redressal: 9963844499",
    "helpline": "📞 **Helplines**:\n- Ragging: 9491074524\n- Women's Cell: 9963299969\n- Grievance: 9963844499\n- Principal: 9000489182",
}


def match_keywords(user_message: str) -> str | None:
    """
    Returns a pre-defined answer if any keyword matches, else None.
    Checks longer phrases first for better accuracy.
    """
    msg = user_message.lower().strip()
    # Sort by length descending so multi-word phrases are checked first
    sorted_keys = sorted(KEYWORD_MAP.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in msg:
            return KEYWORD_MAP[key]
    return None


def get_context() -> str:
    """
    Returns a rich, structured context string from the JSON file.
    Used as the system prompt for the LLM fallback.
    """
    json_path = os.path.join(os.path.dirname(__file__), 'college_data.json')

    base = """
=== SVAI BOT — FULL KNOWLEDGE BASE: S.V. ARTS COLLEGE (AUTONOMOUS), TIRUPATI ===

COLLEGE BASICS:
- Full Name: Sri Venkateswara Arts College (Autonomous)
- Short Name: S.V. Arts College
- Managed by: Tirumala Tirupati Devasthanams (TTD)
- Location: Tirupati, Andhra Pradesh, India
- Affiliated University: S.V. University (S.V.U.), Tirupati
- Accreditation: NAAC A+ Grade (2022), CGPA 3.28 on 4-point scale
- Autonomous Status Conferred: 08-12-2023 (Implemented from 2024-25)
- Founded: 1945 | Founder Principal: Prof. K. Rami Reddy
- Initial Affiliation: Madras University → S.V. University (1954)
- Current Building Occupied: 12-10-1967
- Student Strength: 3,084 | Laboratories: 22 | Library: 88,000 volumes
- Hostel Blocks: 3 | Gymnasium Stages: 14
- College Timings: 09:30 AM to 04:15 PM
- Websites: www.tirumala.org, www.tirupati.org
- Email: webmaster@tirumala.org
- Motto: Om Namo Venkatesaya

PRINCIPAL:
- Prof. N. Venugopal Reddy | M.Sc(Physics), M.Phil., Ph.D., M.Sc.(Maths) | Phone: 9000489182

MANAGEMENT (TTD Officials):
1. Sri M. Ravichandra (I.A.S.) – Executive Officer
2. Sri V. Veerabrahamam (I.A.S.) – Joint Executive Officer
3. Sri O. Balaji (F.C.A.) – FA & CAO
4. Sri T. Venkatasuneelu – Devasthanams Educational Officer
5. Dr. N. Venugopal Reddy – Principal

GOVERNING BODY (2024-25) — Chairman: Sri B.R. Naidu (TTD Board Chairman), 14 members total.

STUDENT UNION (2025-26):
- President: Prof. N. Venugopal Reddy | VP: Prof. Y. Mallikarjun Rao
- Chairman: Shaik Asifa (B.Sc Biotechnology)
- Secretary: P. Lasya Priya (B.Com Computer Application)
"""

    if not os.path.exists(json_path):
        return base

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # ── Academic Schedule ──────────────────────────────────────────
        sch = data.get('academic_schedule_2025_2026', {})
        odd = sch.get('odd_semesters_I_III_V', {})
        even = sch.get('even_semesters_II_IV_VI_conventional', {})
        bba = sch.get('semester_I_BBA_BCA', {})
        auto = sch.get('autonomous_II_IV_semester', {})
        base += f\"\"\"
ACADEMIC SCHEDULE 2025-26:
Odd Semesters (I/III/V — All UG incl. BBA/BCA):
  - Classes: {odd.get('commencement_of_classes')}
  - Dasara: {odd.get('dasara_holidays')}
  - Instructions Close: {odd.get('closure_of_instructions')}
  - Theory Exams: {odd.get('sem_end_exams_theory')}
  - Practical Exams: {odd.get('sem_end_exams_practicals')}

Even Semesters (Conventional):
  - Classes: {even.get('commencement_of_classes')}
  - Dasara: {even.get('dasara_holidays')}
  - End Exams: {even.get('end_examinations')}

BBA/BCA Semester I:
  - Classes: {bba.get('commencement_of_classes')}
  - End Exams: {bba.get('end_examinations')}

Autonomous II/IV Semester:
  - Classes: {auto.get('commencement_of_classes')}
  - Sankranthi Holidays: {auto.get('sankranthi_holidays')}
  - End Exams: {auto.get('end_examinations')}
\"\"\"

        # ── Programmes & Fees ──────────────────────────────────────────
        prog = data.get('programmes_of_study', {})
        yr1 = prog.get('year_1_2025_26', [])
        base += \"\\nPROGRAMMES (Year 1, 2025-26) & FEES:\\n\"
        for p in yr1:
            base += f\"  {p['sno']}. {p['program']} | Strength: {p['strength']} | Fee: ₹{p['fee_rs']}/-\\n\"
        base += f\"Total Sanctioned Strength: {prog.get('total_sanctioned_strength', 1417)}\\n\"

        fee_reg = prog.get('fee_regulations', {})
        base += f\"\"\"
FEE PAYMENT:
  - Year 1: {fee_reg.get('year_1_payment')}
  - Year 2: {fee_reg.get('year_2_payment')}
  - Year 3: {fee_reg.get('year_3_payment')}
  Note: {fee_reg.get('removal_from_rolls')}
\"\"\"

        # ── Scholarships ───────────────────────────────────────────────
        schol = data.get('scholarships', {})
        base += f\"\\nSCHOLARSHIPS (Attendance req: {schol.get('attendance_requirement')}):\\n\"
        for s in schol.get('list', []):
            base += f\"  {s['sno']}. {s['name']} — {s['eligibility']}\\n\"

        # ── Faculty Departments ────────────────────────────────────────
        base += \"\\nDEPARTMENTS & FACULTY:\\n\"
        depts = data.get('faculty_members', {}).get('departments', {})
        for dept, members in depts.items():
            base += f\"\\n[{dept.upper().replace('_',' ')}]\\n\"
            if isinstance(members, list):
                for m in members:
                    if m.get('name') != 'Vacant':
                        base += f\"  - {m.get('name')} | {m.get('designation','')} | {m.get('qualifications','')} | 📞 {m.get('phone','')}\\n\"
            elif isinstance(members, dict):
                # Handle research_guidance
                rg = members.get('research_guidance', [])
                if rg:
                    base += \"  Research Guidance: \" + \", \".join([r if isinstance(r, str) else r.get('name','') for r in rg]) + \"\\n\"
                for m in members.get('faculty', []):
                    if m.get('name') != 'Vacant':
                        base += f\"  - {m.get('name')} | {m.get('designation','')} | {m.get('qualifications','')} | 📞 {m.get('phone','')}\\n\"

        # ── Non-Teaching Staff ─────────────────────────────────────────
        base += \"\\nNON-TEACHING STAFF:\\n\"
        for s in data.get('non_teaching_staff', []):
            base += f\"  {s['sno']}. {s['name']} | {s['designation']} | 📞 {s['phone']}\\n\"

        # ── Rules ──────────────────────────────────────────────────────
        att = data.get('rules_of_attendance', {})
        base += f\"\"\"
ATTENDANCE RULES:
  - Minimum for promotion: {att.get('minimum_for_promotion')}
  - Condonation minimum: {att.get('condonation_minimum')} (Fee: {att.get('condonation_fee')})
  - Periods per day: {att.get('periods_per_day')} (each {att.get('period_duration')})
  - Benefit of attendance for: {', '.join(att.get('benefit_of_attendance_for', []))}
  - Key rules: {' | '.join(att.get('rules', [])[:4])}
\"\"\"

        dis = data.get('rules_of_discipline', {})
        base += f\"\"\"
DISCIPLINE:
  - Dress code — Boys: {dis.get('dress_code', {}).get('boys')}
  - Dress code — Girls: {dis.get('dress_code', {}).get('girls')}
  - Identity card: {dis.get('identity_card')}
  - Prohibited: {', '.join(dis.get('prohibited', []))}
\"\"\"

        rag = data.get('ragging_policy', {})
        base += f\"\"\"
RAGGING POLICY:
  - Status: {rag.get('status')}
  - Punishment: {rag.get('punishment')}
  - Contacts: {', '.join([f\\\"{c['designation']}: {c['cell']}\\\" for c in rag.get('contacts', [])])}
\"\"\"

        cell = data.get('cell_phone_rules', {})
        base += \"\\nCELL PHONE RULES:\\n\"
        for p in cell.get('penalties', []):
            base += f\"  - {p['offence']}: {p['fine']}\\n\"

        lib = data.get('library_rules', {})
        base += f\"\"\"
LIBRARY:
  - Hours: {lib.get('working_hours')}
  - Issue days: {lib.get('book_issue_days')}
  - Return days: {lib.get('book_return_days')}
  - Loan period: {lib.get('loan_period_days')} days | Fine: {lib.get('overdue_fine')}
  - Quota — Staff: {lib.get('ticket_quota', {}).get('teaching_staff')} | Students: {lib.get('ticket_quota', {}).get('students_all_years')}
\"\"\"

        # ── Hostel ─────────────────────────────────────────────────────
        hos = data.get('hostel_information', {})
        base += f\"\"\"
HOSTEL:
  - Blocks: {hos.get('blocks')}
  - Warden: {hos.get('warden', {}).get('name')} | 📞 {hos.get('warden', {}).get('phone')}
  - Deputy Wardens: {', '.join([f\\\"{d['name']} (📞{d['phone']})\\\" for d in hos.get('deputy_wardens', [])])}
\"\"\"

        # ── Committees (All 52) ────────────────────────────────────────
        base += \"\\nCOMMITTEES (2025-26) — All 52:\\n\"
        for c in data.get('committees_2025_2026', []):
            coordinator = c.get('coordinator', c.get('co_ordinator', {}))
            coord_name = coordinator.get('name', 'N/A') if isinstance(coordinator, dict) else 'N/A'
            coord_phone = coordinator.get('phone', '') if isinstance(coordinator, dict) else ''
            base += f\"  {c['no']}. {c['name']} | Coordinator: {coord_name} | 📞 {coord_phone}\\n\"

        # ── Mentors ────────────────────────────────────────────────────
        base += \"\\nMENTORS 2025-26:\\n\"
        mentors = data.get('mentors_list_2025_2026', {})
        for yr, lst in mentors.items():
            base += f\"  [{yr.upper()}]\\n\"
            for m in lst:
                base += f\"    - {m.get('class','')}: {m.get('mentor','N/A')} | 📞 {m.get('phone','')}\\n\"

        # ── University Exam Norms ──────────────────────────────────────
        base += \"\\nEXAMINATION MALPRACTICE NORMS:\\n\"
        for v in data.get('university_examination_norms', {}).get('violations_and_penalties', []):
            base += f\"  {v['sno']}. {v['violation']} → {', '.join(v['penalties'])}\\n\"

        # ── Arjitha Sevas ──────────────────────────────────────────────
        base += \"\\nARJITHA SEVAS AT TIRUMALA:\\n  Daily Sevas: \"
        sevas = data.get('arjitha_sevas_tirumala', {})
        base += \", \".join([s['name'] for s in sevas.get('daily_sevas', [])]) + \"\\n\"
        base += \"  Annual Sevas: \" + \", \".join([s['name'] for s in sevas.get('annual_periodical_sevas', [])]) + \"\\n\"

        # ── Telephone Numbers ──────────────────────────────────────────
        phones = data.get('important_telephone_numbers', {})
        tirupati = phones.get('tirupati', {})
        tirumala = phones.get('tirumala', {})
        base += \"\\nIMPORTANT TELEPHONE NUMBERS:\\n\"
        base += \"  Tirupati:\\n\"
        for k, v in tirupati.items():
            base += f\"    {k}: {v}\\n\"
        base += \"  Tirumala:\\n\"
        for k, v in tirumala.items():
            base += f\"    {k}: {v}\\n\"

        # ── Notable Alumni ─────────────────────────────────────────────
        base += \"\\nNOTABLE ALUMNI:\\n\"
        for a in data.get('foreword', {}).get('notable_alumni', []):
            base += f\"  - {a['name']} ({a['achievement']})\\n\"

        # ── National/International Days ────────────────────────────────
        base += \"\\nIMPORTANT NATIONAL/INTERNATIONAL DAYS:\\n\"
        for d in data.get('important_national_international_days', []):
            base += f\"  - {d['date']}: {d['significance']}\\n\"

        return base

    except Exception as e:
        print(f\"[knowledge_base] Error reading JSON: {e}\")
        return base


def get_quick_response(user_message: str) -> str | None:
    \"\"\"
    Public API used by app.py before calling the LLM.
    Returns a matched keyword answer or None.
    \"\"\"
    return match_keywords(user_message)
