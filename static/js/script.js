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

    // Timetable Modal Logic
    const timetableTab = document.getElementById('timetableTab');
    const timetableModal = document.getElementById('timetableModal');
    const closeTimetableModal = document.getElementById('closeTimetableModal');
    const backFromTimetable = document.getElementById('backFromTimetable');

    // 🟢 WhatsApp Modal Logic
    const whatsappTab = document.getElementById('whatsappTab');
    const whatsappModal = document.getElementById('whatsappModal');
    const closeWhatsappModal = document.getElementById('closeWhatsappModal');

    if (whatsappTab) {
        whatsappTab.addEventListener('click', () => {
            closeMenu();
            whatsappModal.style.display = 'block';
            fetchWhatsAppGroups();
        });
    }

    if (closeWhatsappModal) {
        closeWhatsappModal.addEventListener('click', () => whatsappModal.style.display = 'none');
    }

    if (timetableTab) {
        timetableTab.addEventListener('click', () => {
            closeMenu(); // Auto-close on mobile
            timetableModal.style.display = 'block';
        });
    }

    if (closeTimetableModal) {
        closeTimetableModal.addEventListener('click', () => {
            timetableModal.style.display = 'none';
        });
    }

    if (backFromTimetable) {
        backFromTimetable.addEventListener('click', () => {
            timetableModal.style.display = 'none';
        });
    }

    // Schedule state
    let currentSem = 1;
    let currentType = 'academic';

    window.changeScheduleType = function(type) {
        currentType = type;
        document.querySelectorAll('.type-btn').forEach(btn => {
            btn.classList.toggle('active', btn.innerText.toLowerCase().includes(type) || (type === 'final' && btn.innerText.includes('End')));
        });
        fetchSchedule();
    };

    window.loadSchedule = function(semNum, element) {
        currentSem = semNum;
        
        // UI Feedback
        document.querySelectorAll('.semester-card').forEach(card => card.classList.remove('active'));
        if (element) element.classList.add('active');
        
        // Show type selector
        document.getElementById('scheduleTypes').style.display = 'flex';
        
        fetchSchedule();
    };

    async function fetchSchedule() {
        const displayArea = document.getElementById('scheduleDisplay');
        if (!displayArea) return;

        const sem = currentSem;
        const type = currentType;
        const baseName = `sem${sem}_${type}`;

        displayArea.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--primary);"><i class="fa-solid fa-spinner fa-spin"></i> Loading...</div>';

        try {
            // 1. Try HTML
            const hRes = await fetch(`/static/timetable/${baseName}.html`);
            if (hRes.ok) {
                displayArea.innerHTML = await hRes.text();
                return;
            }

            // 2. Try Word (DOC/DOCX)
            const docRes = await fetch(`/static/timetable/${baseName}.doc`);
            const docxRes = await fetch(`/static/timetable/${baseName}.docx`);
            const ext = docxRes.ok ? 'docx' : 'doc';
            const hasDoc = docRes.ok || docxRes.ok;

            if (hasDoc) {
                displayArea.innerHTML = `
                    <div style="text-align:center; padding: 30px; border: 2px solid #eee; border-radius: 12px;">
                        <i class="fa-solid fa-file-word" style="font-size: 3.5rem; color: #2b579a; margin-bottom: 15px;"></i>
                        <p><strong>Semester ${sem} - ${type.toUpperCase()} Schedule</strong> is available!</p>
                        <a href="/static/timetable/${baseName}.${ext}" download class="back-btn" style="display:inline-block; margin-top:15px; background: #2b579a;">
                            <i class="fa-solid fa-download"></i> Download Word File
                        </a>
                    </div>`;
            } else {
                displayArea.innerHTML = `
                    <div style="text-align:center; padding: 40px; color: #7f8c8d;">
                        <i class="fa-solid fa-calendar-xmark" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                        <p>No ${type} schedule found for Semester ${sem}.</p>
                        <p style="font-size: 0.8rem; margin-top: 10px;">Please check other categories or the full handbook.</p>
                    </div>`;
            }

            // Scroll to display
            displayArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (err) {
            displayArea.innerHTML = '<p style="text-align:center; color: red;">Connection error.</p>';
        }
    }

    async function fetchWhatsAppGroups() {
        const waContainer = document.getElementById('whatsappContainer');
        if (!waContainer) return;
        
        try {
            const res = await fetch('/admin/get_json');
            if (res.ok) {
                const data = await res.json();
                if (data.whatsapp_groups && data.whatsapp_groups.length > 0) {
                    waContainer.innerHTML = data.whatsapp_groups.map(g => `
                        <a href="${g.link}" target="_blank" style="text-decoration:none; color:inherit;">
                            <div style="background: #f0f7f4; border: 1px solid #c8e6c9; padding: 18px; border-radius: 16px; display: flex; align-items: center; justify-content: space-between; gap: 15px; transition: 0.3s; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);" onmouseover="this.style.background='#e8f5e9'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='#f0f7f4'; this.style.transform='translateY(0)'">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <i class="fa-brands fa-whatsapp" style="color: #25D366; font-size: 1.8rem;"></i>
                                    <div>
                                        <h4 style="margin:0; font-size: 1.05rem; color: #2c3e50;">${g.name}</h4>
                                        <p style="margin:0; font-size: 0.8rem; color: #7f8c8d;">Official Community Group</p>
                                    </div>
                                </div>
                                <i class="fa-solid fa-chevron-right" style="color: #bdc3c7; font-size: 0.8rem;"></i>
                            </div>
                        </a>
                    `).join('');
                } else {
                    waContainer.innerHTML = '<div style="text-align:center; padding:30px; color:#999;"><i class="fa-solid fa-circle-info" style="font-size:2rem; margin-bottom:10px; opacity:0.5;"></i><p>No official groups added yet.</p></div>';
                }
            }
        } catch (e) {
            waContainer.innerHTML = '<div style="color:red; text-align:center;">Failed to load links. Please try again.</div>';
        }
    }

    // Modal Global Click
    window.addEventListener('click', (e) => {
        if (e.target == coursesModal) coursesModal.style.display = 'none';
        if (e.target == timetableModal) timetableModal.style.display = 'none';
        if (e.target == whatsappModal) whatsappModal.style.display = 'none';
    });
});
