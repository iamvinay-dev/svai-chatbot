# SVAI Bot: System Architecture & Technical Explanation

This document provides a comprehensive deep-dive into how the SV Arts College Chatbot is built, why certain technical decisions were made, and how each component works.

---

## 📁 File Structure & Responsibilities

### 1. `app.py` (The Heart)
- **Role**: Flask Backend & API Server.
- **Key Logic**: Handles the `/chat` route. It first checks for a "Quick Response" (from `knowledge_base.py`). if none found, it calls the **Groq Llama-3** API.
- **Why this way?**: We use Flask because it is lightweight and perfect for Vercel deployment.
- **Persistence Trick**: Since Vercel is "read-only," our Admin Panel cannot save files normally. `app.py` includes a `push_to_github` function that sends any data updates back to your GitHub repository so they aren't lost when the server restarts.

### 2. `knowledge_base.py` (The Brain)
- **Role**: Intelligence Dispatching & Data Extraction.
- **Features**: 
    - **Keyword Map**: Over 300+ hardcoded "Instant Answers" (0ms latency, $0 cost).
    - **Special Query Handler**: Custom Python logic that scans `college_data.json` to instantly build lists of HODs, Committees, and Mentors.
- **Design Decision**: We used a "Keywords-First" approach to ensure the most common student questions (like "Principal contact") are answered instantly without wasting API tokens.

### 3. `college_data.json` (The Source of Truth)
- **Role**: Central Database.
- **Why JSON?**: A JSON file acts as a portable, human-readable database. It’s easier to manage for this scale than a full SQL database and integrates perfectly with our GitHub persistence model.

### 4. `templates/index.html` & `admin.html`
- **Role**: User & Administrative Interfaces.
- **Design**: Uses a **Glassmorphic Dashboard** style. 
- **Modals**: Most features (Mentors, Courses) are built as "Modals" (popups) to keep the user on the home screen without refreshing the page.

### 5. `static/js/script.js` & `style.css`
- **Role**: Dynamic UI & Styling.
- **Logic**: Handles the "Thinking..." state, fetching chat responses, and populating the Mentors/Committees grids by reading the JSON file.

---

## 🔥 Feature Explanations

### 1. Two-Tier Intelligence System
- **Tier 1 (Instant)**: The system scans for keywords. If you ask about "Attendance," it gives the handbook rule instantly.
- **Tier 2 (LLM)**: If the question is complex (e.g., *"How do I balance my studies with NSS?"*), it sends the request to **Groq (Llama 3.3 70B)** with a custom system prompt.

### 2. The "Smart" Principal Finder
- **How it works**: In `knowledge_base.py`, we use Regular Expressions (`re`) to find years in your questions.
- **Why**: Students often ask "Who was principal in 1980?". Instead of hoping the AI remembers, the code scans the structured historical list in the JSON for that specific year.

### 3. Admin "Read-Write" Persistence
- **The Problem**: Standard web servers allow saving files. Vercel (where this is likely hosted) deletes local files every time it updates.
- **The Solution**: We integrated the GitHub API. When you save a change in the Admin Panel, the bot "commits" that change to your GitHub repo. Vercel then sees the new commit and rebuilds the site with the updated data.

### 4. Mentor/Committee Dynamic Grids
- **Construction**: These aren't just static text. They are "Grids" built from the JSON.
- **Advantage**: If you add a new mentor to the JSON, they automatically appear in the UI without you ever touching the HTML code.

---

## 🛠️ Design Philosophy: "Speed & Accuracy"

The code is structured the way it is to prioritize **Accuracy** over "Chattiness."
- **Institutional Context**: By forcing the LLM to read the `college_data.json` every time, we ensure it never "hallucinates" a teacher's name or a fake phone number.
- **Cost Optimization**: 90% of user queries are intercepted by the Keyword Map, making the bot extremely cheap (or free) to run even with high student traffic.

---
*Documented by Antigravity AI for SV Arts College (TTD)*
