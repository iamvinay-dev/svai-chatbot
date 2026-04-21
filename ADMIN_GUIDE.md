# SVAI Bot Admin Panel Guide 🔐

The Admin Panel allows you to manage the institutional data, college rules, and time tables directly through the browser.

## 📍 Accessing the Panel
1.  Start the server locally or visit your deployed URL.
2.  Go to: `/admin` (e.g., `http://127.0.0.1:5000/admin`)
3.  **Password**: `svacadmin2025` (You can change this in `app.py`)

## 🚀 Managed Features

### 1. Institutional Knowledge
- **Edit JSON**: You can modify the `sv_arts_college_COMPLETE.json` file directly via the dashboard.
- **Update Sections**: Add or remove departments, links, and text.
- **Save Changes**: Clicking "Save" will overwrite the JSON file locally.

### 2. Time Table Management
- **Upload Schedules**: Upload new `.html` files for any semester.
- **Permanent Access**: Once uploaded, the bot's "Time Tables" tab will find them.

## ⚠️ Permanent Changes Note
To make your changes permanent on the live website:
1.  Run the bot **locally** on your computer.
2.  Log in to the `/admin` panel and make your changes.
3.  **Git Push** the updated files to GitHub. Vercel will then redeploy with your new data.
