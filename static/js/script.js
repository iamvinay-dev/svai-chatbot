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
                addMessage("⚠️ I'm having trouble connecting right now. Please try again", false);
            }
        } catch (error) {
            console.error('Error:', error);
            chatContainer.removeChild(loadingDiv);
            addMessage("⚠️ I'm having trouble connecting right now. Please try again", false);
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

    window.loadSchedule = async function(semNum, element) {
        const displayArea = document.getElementById('scheduleDisplay');
        if (!displayArea) return;

        // Visual feedback for selected card
        document.querySelectorAll('.semester-card').forEach(card => card.classList.remove('active'));
        if (element) {
            element.classList.add('active');
        }

        try {
            displayArea.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--primary);"><i class="fa-solid fa-spinner fa-spin"></i> Checking for updates...</div>';
            
            // Try HTML first
            const htmlRes = await fetch(`/static/timetable/sem${semNum}.html`);
            if (htmlRes.ok) {
                const html = await htmlRes.text();
                displayArea.innerHTML = html;
                return;
            }

            // Fallback for Word Documents
            const docRes = await fetch(`/static/timetable/sem${semNum}.doc`);
            const docxRes = await fetch(`/static/timetable/sem${semNum}.docx`);
            const exists = docRes.ok || docxRes.ok;
            const ext = docxRes.ok ? 'docx' : 'doc';

            if (exists) {
                displayArea.innerHTML = `
                    <div style="text-align:center; padding: 30px; color: #2c3e50; background: #fff; border-radius: 12px; border: 2px solid #eee;">
                        <i class="fa-solid fa-file-word" style="font-size: 3rem; margin-bottom: 15px; color: #2b579a;"></i>
                        <p><strong>Semester ${semNum} schedule is available as a Word document.</strong></p>
                        <a href="/static/timetable/sem${semNum}.${ext}" download class="btn-primary" style="display:inline-block; margin-top:15px; padding:10px 25px; border-radius:30px; text-decoration:none;">
                            <i class="fa-solid fa-download"></i> Download Sem ${semNum} Schedule
                        </a>
                    </div>`;
            } else {
                displayArea.innerHTML = `
                    <div style="text-align:center; padding: 30px; color: #7f8c8d; background: #f8f9fa; border-radius: 12px; margin: 10px;">
                        <i class="fa-solid fa-file-circle-exclamation" style="font-size: 3rem; margin-bottom: 15px; color: #e67e22;"></i>
                        <p><strong>Semester ${semNum} detailed schedule is under update.</strong></p>
                        <p style="font-size: 0.85rem; margin-bottom: 20px;">Please check back in a few days.</p>
                        <a href="/college_data.pdf" target="_blank" style="display:inline-block; padding: 12px 20px; background: var(--primary); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
                           <i class="fa-solid fa-file-pdf"></i> Download College Handbook (80MB)
                        </a>
                    </div>`;
            }

            // Scroll to view
            displayArea.style.display = 'block';
            setTimeout(() => {
                displayArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);

        } catch (err) {
            displayArea.innerHTML = '<p style="text-align:center; padding:20px; color: red;">Connection error. Please try again.</p>';
        }
    };
});
