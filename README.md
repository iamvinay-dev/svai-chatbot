# SVA Bot - SVAC College Chatbot

A premium, AI-powered chatbot for **Sri Venkateswara Arts College (SVAC)**, Tirupati. Built with Flask, Groq API (Llama 3.3), and modern web technologies.

## 🚀 Features
- **AI-Powered Responses**: Uses Groq (Llama 3) to answer queries about college admissions, courses, and rules.
- **Premium UI**: Modern, responsive design with smooth animations and a traditional academic aesthetic.
- **Managed by TTD**: Reflects the values and structure of TTD management.
- **Knowledge Base**: Integrated offline knowledge about SVAC for accurate assistance.

## 🛠️ Technology Stack
- **Backend**: Python (Flask)
- **AI Model**: Llama 3.3 via Groq API
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Styling**: Modern CSS with Glassmorphism and Outfit/Inter fonts.

## 📂 Project Structure
```text
svac_chatbot/
├── app.py                    # Main Flask backend
├── requirements.txt          # Python dependencies
├── knowledge_base.py         # College data & rules
├── static/
│   ├── css/
│   │   └── style.css        # Beautiful animations & styling
│   ├── js/
│   │   └── script.js        # Chat functionality
│   ├── images/
│   │   ├── college-logo.png # Generated college logo
│   │   ├── campus-1.jpg     # Generated campus image
│   └── favicon.ico
├── templates/
│   └── index.html           # Main webpage with chat UI
├── .env                     # Store your GROQ_API_KEY securely
└── README.md                # Documentation
```

## ⚙️ Setup Instructions
1. **Clone/Download** the repository.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key**:
   - Open `.env` and replace `your_groq_api_key_here` with your actual Groq API key.
4. **Run the App**:
   ```bash
   python app.py
   ```
5. **Access the Chatbot**:
   - Open `http://127.0.0.1:5000` in your browser.

## 📄 License
This project is for educational purposes. SVAC and TTD are trademarks of their respective entities.
