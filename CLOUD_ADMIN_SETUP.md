# 🚀 SVAI Bot Cloud Admin Setup (Permanent Changes)

To make changes through the Admin Panel **PERMANENT** on the live website (without running locally), follow these steps:

## 1. Create a GitHub Token
1.  Go to [GitHub Settings > Tokens](https://github.com/settings/tokens).
2.  Click **"Generate new token (classic)"**.
3.  Name it `SVAI_ADMIN` and check the **repo** box.
4.  Copy the token (you will only see it once).

## 2. Add the Token to Vercel
1.  Go to your [Vercel Dashboard](https://vercel.com).
2.  Open your **svai-chatbot** project.
3.  Go to **Settings > Environment Variables**.
4.  Add a new variable:
    *   **Name**: `GITHUB_TOKEN`
    *   **Value**: (Paste your token here)
5.  Add another variable:
    *   **Name**: `GITHUB_REPO`
    *   **Value**: `iamvinay-dev/svai-chatbot`
6.  **Redeploy** your site.

## 3. How to Upload Documents (.doc/.docx)
1.  Log into your `/admin` panel.
2.  Go to the **Time Tables** tab.
3.  The panel now accepts `.doc` and `.docx` files.
4.  After you click **Upload**, the bot will "commit" the file directly to your GitHub.
5.  **Wait 1-2 minutes**: Vercel will automatically redeploy the site with your new file.

---

## ✅ Why this works?
By linking your GitHub account, the Admin Panel now acts as a professional CMS. Every time you save a rule or upload a timetable, it updates your source code permanently.
