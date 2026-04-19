document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const closeSidebar = document.getElementById('closeSidebar');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.add('active');
        });
    }

    const closeMenu = () => {
        sidebar.classList.remove('active');
    };

    if (closeSidebar) {
        closeSidebar.addEventListener('click', closeMenu);
    }
    const chatContainer = document.getElementById('chatContainer');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // Modal Elements
    const coursesTab = document.getElementById('coursesTab');
    const coursesModal = document.getElementById('coursesModal');
    const closeModal = document.querySelector('.close-modal');
    const backBtn = document.querySelector('.back-btn');
    const coursesTableBody = document.getElementById('coursesTableBody');

    const programmesData = [
        {name: "B.A. Honours (Political Science)", seats: 60, fee: "5,400"},
        {name: "B.A. Honours (History)", seats: 60, fee: "5,400"},
        {name: "B.A. Honours (Special English)", seats: 30, fee: "5,400"},
        {name: "B.A. Honours (Special Telugu)", seats: 40, fee: "5,400"},
        {name: "B.A. Honours (Economics)", seats: 100, fee: "5,400"},
        {name: "B.Com Honours (C.A.)", seats: 180, fee: "10,845"},
        {name: "B.Com Honours (General)", seats: 180, fee: "5,400"},
        {name: "B.Sc. Honours (Computer Science)", seats: 80, fee: "11,045"},
        {name: "B.Sc. Honours (Aquaculture)", seats: 30, fee: "11,045"},
        {name: "B.Sc. Honours (Mathematics)", seats: 74, fee: "5,600"},
        {name: "B.Sc. Honours (Data Science)", seats: 50, fee: "11,045"},
        {name: "B.Sc. Honours (Statistics)", seats: 50, fee: "5,600"},
        {name: "B.Sc. Honours (Psychology)", seats: 35, fee: "5,600"},
        {name: "B.Sc. Honours (Physics)", seats: 50, fee: "5,600"},
        {name: "B.Sc. Honours (Microbiology)", seats: 60, fee: "11,045"},
        {name: "B.Sc. Honours (Biotechnology)", seats: 30, fee: "11,045"},
        {name: "B.Sc. Honours (Electronics)", seats: 48, fee: "5,600"},
        {name: "B.Sc. Honours (Botany)", seats: 80, fee: "5,600"},
        {name: "B.Sc. Honours (Zoology)", seats: 100, fee: "5,600"},
        {name: "B.Sc. Honours (Chemistry)", seats: 80, fee: "5,600"},
        {name: "B.Sc. Honours (Artificial Intelligence)", seats: 30, fee: "11,045"},
        {name: "B.Sc. Honours (Quantum Technologies)", seats: 50, fee: "11,045"},
        {name: "B.B.A. Honours", seats: 60, fee: "10,845"},
        {name: "B.C.A. Honours (Science)", seats: 50, fee: "11,045"}
    ];

    function populateCourses() {
        coursesTableBody.innerHTML = '';
        programmesData.forEach(p => {
            const row = `<tr>
                <td>${p.name}</td>
                <td>${p.seats}</td>
                <td>${p.fee}</td>
            </tr>`;
            coursesTableBody.innerHTML += row;
        });
    }

    coursesTab.addEventListener('click', () => {
        closeMenu(); // Auto-close on mobile
        populateCourses();
        coursesModal.style.display = 'block';
    });

    closeModal.addEventListener('click', () => {
        coursesModal.style.display = 'none';
    });

    backBtn.addEventListener('click', () => {
        coursesModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target == coursesModal) {
            coursesModal.style.display = 'none';
        }
    });

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const now = new Date();
        const timeString = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');

        // Basic formatting for bold text and new lines
        let formattedMessage = message;
        if (!isUser) {
            formattedMessage = message
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>');
        }

        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${formattedMessage}</p>
                <span class="time">${isUser ? 'You' : 'SVAI Bot'} • ${timeString}</span>
            </div>
        `;

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        userInput.value = '';
        addMessage(message, true);

        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message', 'loading-msg');
        loadingDiv.innerHTML = `<div class="message-content"><p>Thinking...</p></div>`;
        chatContainer.appendChild(loadingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            chatContainer.removeChild(loadingDiv);

            if (data.response) {
                addMessage(data.response, false);
            } else {
                addMessage("I'm sorry, I encountered an error. Please ensure your `GROQ_API_KEY` is correctly set in the .env file.", false);
            }
        } catch (error) {
            console.error('Error:', error);
            chatContainer.removeChild(loadingDiv);
            addMessage("Unable to connect to the server. Please check if the Flask app is running.", false);
        }
    }

    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });

    // Time Table Logic
    const timetableTab = document.getElementById('timetableTab');
    const timetableModal = document.getElementById('timetableModal');
    const closeTimetable = document.getElementById('closeTimetable');
    const backFromTimetable = document.getElementById('backFromTimetable');

    if (timetableTab) {
        timetableTab.addEventListener('click', () => {
            closeMenu(); // Auto-close on mobile
            timetableModal.style.display = 'block';
        });
    }

    if (closeTimetable) {
        closeTimetable.addEventListener('click', () => {
            timetableModal.style.display = 'none';
        });
    }

    if (backFromTimetable) {
        backFromTimetable.addEventListener('click', () => {
            timetableModal.style.display = 'none';
        });
    }

    window.loadSchedule = async function(semNum) {
        const displayArea = document.getElementById('scheduleDisplay');
        if (!displayArea) return;

        // Visual feedback for selected card
        document.querySelectorAll('.semester-card').forEach(card => card.classList.remove('active'));
        event.currentTarget.classList.add('active');

        try {
            displayArea.innerHTML = '<div style="text-align:center; padding: 40px;"><i class="fa-solid fa-spinner fa-spin"></i> Finding Timetable...</div>';
            
            const response = await fetch(`/static/timetable/sem${semNum}.html`);
            if (response.ok) {
                const html = await response.text();
                // Remove weird diamond characters gracefully
                const cleanHtml = html.replace(/[^\x20-\x7E\s\u00A0-\u00FF]/g, "");
                displayArea.innerHTML = cleanHtml;
                
                // Ensure it scrolls into view
                displayArea.style.display = 'block';
                setTimeout(() => {
                    displayArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            } else {
                displayArea.innerHTML = `
                    <div style="text-align:center; padding: 30px; color: #7f8c8d;">
                        <i class="fa-solid fa-file-circle-exclamation" style="font-size: 3rem; margin-bottom: 15px;"></i>
                        <p><strong>Timetable for Semester ${semNum} is not uploaded yet.</strong></p>
                        <p style="font-size: 0.8rem;">Please check back later or contact the HOD.</p>
                    </div>`;
            }
        } catch (err) {
            displayArea.innerHTML = '<p style="text-align:center; padding:20px;">Connection error. Please try again.</p>';
        }
    };
});
