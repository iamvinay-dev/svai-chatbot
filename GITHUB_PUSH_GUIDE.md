# 🚀 How to Push SVAI Bot to GitHub

Follow these exact steps to upload your project safely and professionally.

---

### Phase 1: Create the Repository on GitHub
1.  Go to [github.com](https://github.com/) and log in.
2.  Click the **"+"** icon in the top right -> **New repository**.
3.  **Repository name**: `svac-ai-bot` (or any name you like).
4.  **Description**: Paste the "Professional Description" provided below.
5.  Keep it **Public**.
6.  **Do NOT** check any boxes (No README, No .gitignore).
7.  Click **Create repository**.

---

### Phase 2: Run these Commands in your Terminal
Open your terminal in VS Code and run these one-by-one:

1.  **Initialize Git:**
    ```bash
    git init
    ```
2.  **Add your files:**
    ```bash
    git add .
    ```
3.  **Create first commit:**
    ```bash
    git commit -m "Initial commit of SVAI Bot"
    ```
4.  **Set to Main branch:**
    ```bash
    git branch -M main
    ```
5.  **Connect to GitHub:** (REPLACE `<your-link>` with the link from the GitHub page)
    ```bash
    git remote add origin <your-link-here>
    ```
6.  **Push to GitHub:**
    ```bash
    git push -u origin main
    ```

---

### 📝 Professional Description (Under 350 Characters):
> SVAI Bot: An AI Digital Assistant for S.V. Arts College (TTD). Features a cost-optimized Llama 3.1 decision system, a full digital handbook of faculty & fees, and a mobile-responsive timetable download portal. Built with Flask & Groq API for high-speed, accurate student assistance.

---

### ⚠️ IMPORTANT: Environment Variables
Since we used `.gitignore`, your `.env` file is NOT on GitHub. When you deploy it to a server (like Render), you must manually go to "Environment Variables" and add:
- `GROQ_API_KEY` = `(Your actual key)`
