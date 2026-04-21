@echo off
echo.
echo 🚀 Starting SVAI Bot Local Server...
echo.

:: Check for .env file
if not exist .env (
    echo ⚠️  No .env file found! 
    echo Please create a .env file and add your GROQ_API_KEY like this:
    echo GROQ_API_KEY=your_api_key_here
    pause
    exit /b
)

:: Install dependencies
echo 📦 Checking dependencies...
pip install -r requirements.txt

:: Run the app
echo.
echo ✅ Server starting at http://127.0.0.1:5000
echo.
python app.py
pause
