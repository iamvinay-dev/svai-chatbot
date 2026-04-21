// Global Knowledge Cache for Performance
let knowledgeCache = null;
let lastCacheTime = 0;
const CACHE_TTL = 300000; // 5 minutes

async function getKnowledgeData() {
    const now = Date.now();
    if (knowledgeCache && (now - lastCacheTime < CACHE_TTL)) {
        return knowledgeCache;
    }
    try {
        const res = await fetch('/admin/get_json');
        if (res.ok) {
            knowledgeCache = await res.json();
            lastCacheTime = now;
            return knowledgeCache;
        }
    } catch (e) {
        console.error("Cache fetch failed:", e);
    }
    return knowledgeCache; // Return stale cache if fetch fails
}

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

    // 🟢 Mentors Modal Logic
    const mentorsTab = document.getElementById('mentorsTab');
    const mentorsModal = document.getElementById('mentorsModal');
    const closeMentorsModal = document.getElementById('closeMentorsModal');

    const committeesTab = document.getElementById('committeesTab');
    const committeesModal = document.getElementById('committeesModal');
    const closeCommitteesModal = document.getElementById('closeCommitteesModal');

    if (committeesTab) {
        committeesTab.addEventListener('click', () => {
            closeMenu();
            committeesModal.style.display = 'block';
            loadCommittees();
        });
    }

    if (closeCommitteesModal) {
        closeCommitteesModal.addEventListener('click', () => committeesModal.style.display = 'none');
    }

    if (mentorsTab) {
        mentorsTab.addEventListener('click', () => {
            closeMenu();
            mentorsModal.style.display = 'block';
            fetchMentors('1st_year');
        });
    }

    if (closeMentorsModal) {
        closeMentorsModal.addEventListener('click', () => mentorsModal.style.display = 'none');
    }

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
            closeMenu();
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
            const hRes = await fetch(`/static/timetable/${baseName}.html`);
            if (hRes.ok) {
                displayArea.innerHTML = await hRes.text();
                return;
            }

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

            displayArea.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (err) {
            displayArea.innerHTML = '<p style="text-align:center; color: red;">Connection error.</p>';
        }
    }

    async function fetchWhatsAppGroups() {
        const waContainer = document.getElementById('whatsappContainer');
        if (!waContainer) return;
        
        try {
            const data = await getKnowledgeData();
            if (data && data.whatsapp_groups && data.whatsapp_groups.length > 0) {
                const fragment = document.createDocumentFragment();
                data.whatsapp_groups.forEach(g => {
                    const div = document.createElement('div');
                    div.innerHTML = `
                        <a href="${g.link}" target="_blank" style="text-decoration:none; color:inherit;">
                            <div class="whatsapp-card-item">
                                <div style="display: flex; align-items: center; gap: 15px;">
                                    <i class="fa-brands fa-whatsapp" style="color: #25D366; font-size: 1.8rem;"></i>
                                    <div>
                                        <h4 style="margin:0; font-size: 1.05rem; color: #2c3e50;">${g.name}</h4>
                                        <p style="margin:0; font-size: 0.8rem; color: #7f8c8d;">Official Community Group</p>
                                    </div>
                                </div>
                                <i class="fa-solid fa-chevron-right" style="color: #bdc3c7; font-size: 0.8rem;"></i>
                            </div>
                        </a>`;
                    fragment.appendChild(div.firstElementChild);
                });
                waContainer.innerHTML = '';
                waContainer.appendChild(fragment);
            } else {
                waContainer.innerHTML = '<div style="text-align:center; padding:30px; color:#999;"><p>No official groups added yet.</p></div>';
            }
        } catch (e) {
            waContainer.innerHTML = '<div style="color:red; text-align:center;">Failed to load links.</div>';
        }
    }

    // Modal Global Click
    window.addEventListener('click', (e) => {
        if (e.target == coursesModal) coursesModal.style.display = 'none';
        if (e.target == timetableModal) timetableModal.style.display = 'none';
        if (e.target == whatsappModal) whatsappModal.style.display = 'none';
        if (e.target == mentorsModal) mentorsModal.style.display = 'none';
        if (e.target == committeesModal) committeesModal.style.display = 'none';
    });
});

let committeesDataStore = {};

async function loadCommittees() {
    const tabContainer = document.getElementById('committeesTabContainer');
    if (!tabContainer) return;

    try {
        const data = await getKnowledgeData();
        if (data && data.committees) {
            committeesDataStore = data.committees;
            const names = Object.keys(committeesDataStore);

            if (names.length > 0) {
                tabContainer.innerHTML = names.map((name, i) => `
                    <button class="year-tab ${i===0 ? 'active' : ''}" onclick="switchCommittee('${name}', this)" style="white-space:nowrap; flex:none;">
                        ${name}
                    </button>
                `).join('');
                switchCommittee(names[0]);
            }
        }
    } catch (e) {
        console.error("Committee load error:", e);
    }
}

function switchCommittee(name, btn = null) {
    if (btn) {
        document.querySelectorAll('#committeesTabContainer .year-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }

    const content = document.getElementById('committeesContent');
    const members = committeesDataStore[name] || [];

    if (members.length > 0) {
        const fragment = document.createDocumentFragment();
        members.forEach(m => {
            const card = document.createElement('div');
            card.className = 'mentor-card';
            card.innerHTML = `
                <div class="mentor-sl" style="color:var(--primary); opacity:0.3;">${m.sl}</div>
                <div class="mentor-info">
                    <h4 style="font-size:1rem;">${m.name}</h4>
                    <p style="color:var(--primary); font-weight:700;">${m.role}</p>
                    <p style="font-size:0.8rem; margin-top:2px;">${m.desig}</p>
                    ${m.contact !== '-' ? `<p style="font-size:0.8rem; color:#4a5568; margin-top:5px;"><i class="fa-solid fa-phone" style="font-size:0.7rem;"></i> ${m.contact}</p>` : ''}
                </div>`;
            fragment.appendChild(card);
        });
        content.innerHTML = '';
        content.appendChild(fragment);
    } else {
        content.innerHTML = '<p style="grid-column:1/-1; text-align:center; padding:40px; color:#aaa;">No members listed.</p>';
    }
}

async function fetchMentors(year = '1st_year') {
    const body = document.getElementById('mentorsTableBody');
    if (!body) return;

    // Show loading if cache is empty
    if (!knowledgeCache) {
        body.innerHTML = '<div style="text-align:center; padding:40px; grid-column: 1/-1;"><i class="fa-solid fa-spinner fa-spin"></i> Initializing Directory...</div>';
    }

    try {
        const data = await getKnowledgeData();
        if (data && data.mentors) {
            // Map '1st_year' to '1st Year' for JSON lookup
            const apiKey = year.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            const mentors = data.mentors[apiKey] || data.mentors[year] || [];
            
            const fragment = document.createDocumentFragment();
            if (mentors.length > 0) {
                mentors.forEach(m => {
                    const card = document.createElement('div');
                    card.className = 'mentor-card';
                    card.innerHTML = `
                        <div class="mentor-sl">${m.sl}</div>
                        <div class="mentor-info">
                            <h4>${m.mentor}</h4>
                            <p>${m.group}</p>
                            ${m.mobile ? `<p style="font-size:0.8rem; color:#4a5568;"><i class="fa-solid fa-phone" style="font-size:0.7rem;"></i> ${m.mobile}</p>` : ''}
                        </div>
                        <i class="fa-solid fa-graduation-cap mentor-badge"></i>`;
                    fragment.appendChild(card);
                });
                body.innerHTML = '';
                body.appendChild(fragment);
            } else {
                body.innerHTML = '<div style="text-align:center; padding:40px; grid-column: 1/-1;">No data found for ' + apiKey + '.</div>';
            }
        }
    } catch (e) {
        console.error("Mentor fetch error:", e);
        body.innerHTML = '<div style="color:red; text-align:center; padding:40px; grid-column: 1/-1;">Failed to load mentor data.</div>';
    }
}

function switchMentorYear(year) {
    // Update tabs UI
    document.querySelectorAll('.year-tab').forEach(btn => {
        btn.classList.remove('active');
        if (btn.innerText.toLowerCase().includes(year.split('_')[0])) {
            btn.classList.add('active');
        }
    });
    fetchMentors(year);
}
