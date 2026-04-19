# 🚀 SVAI Bot: Easy Step-by-Step Launch Guide

Follow these 4 simple steps to get your bot onto the official college website!

---

## Step 1: Put your code on GitHub 📦
Think of GitHub as a "Storage Box" on the internet that holds your code.
1. Create a free account at [GitHub.com](https://github.com).
2. Click **New** to create a "Repository" named `svac_bot`.
3. Upload **ALL** the files from your folder on your laptop into this GitHub box.

---

## Step 2: Make it Live on Render.com 🌐
This turns your code into a real website.
1. Sign up at [Render.com](https://render.com) using your GitHub account.
2. Click **New +** -> **Web Service**.
3. Select your `svac_bot` from the list.
4. **Environment Settings**: Find the "Environment Variables" button and add:
   - **Key**: `GROQ_API_KEY`
   - **Value**: (Paste your secret key here)
5. Click **Create Web Service**. 
6. Render will give you a link like: `https://svac-bot.onrender.com`. **Save this link!**

---

## Step 3: Your College Website Widget 🤖
Copy this code. You will need it for the college website.
**NOTE**: Replace `https://svac-bot.onrender.com` with your real link from Step 2.

```html
<!-- SVAI Bot Widget Code -->
<div id="chatbot-container">
    <button onclick="toggleChat()" id="bot-bubble" style="position:fixed; bottom:20px; right:20px; background:#1a237e; color:white; border-radius:50%; width:60px; height:60px; border:none; cursor:pointer; font-size:24px; box-shadow:0 4px 10px rgba(0,0,0,0.3); z-index:9999;">
        🤖
    </button>
    <div id="bot-window" style="display:none; position:fixed; bottom:90px; right:20px; width:380px; height:600px; background:white; border-radius:15px; box-shadow:0 5px 30px rgba(0,0,0,0.2); z-index:9999; overflow:hidden;">
        <iframe src="https://svac-bot.onrender.com" style="width:100%; height:100%; border:none;"></iframe>
    </div>
</div>

<script>
function toggleChat() {
    var win = document.getElementById('bot-window');
    win.style.display = (win.style.display === 'none') ? 'block' : 'none';
}
</script>
```

---

## Step 4: Final Integration 🏛️
1. Go to the college website's code (or give it to the manager).
2. Open the main file (usually `index.html`).
3. Paste the code from **Step 3** at the very bottom, right before the `</body>` tag.
4. Save and Publish!

**Your SVAI Bot is now live on svac.edu.in!**
