document.addEventListener("DOMContentLoaded", () => {

    // Carousel
    const slides = document.querySelectorAll(".slide");
    const dots   = document.querySelectorAll(".dot");
    let current = 0, timer;

    function goToSlide(n) {
        slides.forEach(s => s.classList.remove("active"));
        dots.forEach(d => d.classList.remove("active"));
        current = (n + slides.length) % slides.length;
        slides[current].classList.add("active");
        dots[current].classList.add("active");
        lucide.createIcons();
    }

    document.getElementById("next-btn")?.addEventListener("click", () => { goToSlide(current + 1); resetTimer(); });
    document.getElementById("prev-btn")?.addEventListener("click", () => { goToSlide(current - 1); resetTimer(); });
    dots.forEach(d => d.addEventListener("click", () => { goToSlide(+d.dataset.slide); resetTimer(); }));

    function startTimer() { timer = setInterval(() => goToSlide(current + 1), 5000); }
    function resetTimer() { clearInterval(timer); startTimer(); }
    if (slides.length) startTimer();

    // Search on Enter
    const input = document.getElementById("search-input");
    input?.addEventListener("keydown", e => { if (e.key === "Enter") searchSchemes(); });

    // Suggestions dropdown
    const dropdown = document.getElementById("suggestions-dropdown");
    input?.addEventListener("focus", () => { if (!input.value.trim()) dropdown?.classList.add("open"); });
    input?.addEventListener("input", () => {
        const clearBtn = document.getElementById("clear-btn");
        if (input.value.trim()) {
            dropdown?.classList.remove("open");
            if (clearBtn) clearBtn.style.display = "flex";
        } else {
            dropdown?.classList.add("open");
            if (clearBtn) clearBtn.style.display = "none";
        }
    });
    document.addEventListener("click", e => {
        if (!e.target.closest(".search-wrapper")) dropdown?.classList.remove("open");
    });

    // Clear button
    document.getElementById("clear-btn")?.addEventListener("click", () => {
        if (input) { input.value = ""; input.focus(); }
        document.getElementById("clear-btn").style.display = "none";
        dropdown?.classList.add("open");
    });

    // Close results button
    document.getElementById("close-results-btn")?.addEventListener("click", () => {
        const sec = document.getElementById("results-section");
        sec?.classList.remove("visible");
        if (input) { input.value = ""; }
        document.getElementById("clear-btn").style.display = "none";
    });

    // Theme Toggle
    const themeBtn  = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    let dark = localStorage.getItem("dark") === "true";
    if (dark) applyDark();

    themeBtn?.addEventListener("click", () => {
        dark = !dark;
        localStorage.setItem("dark", dark);
        dark ? applyDark() : removeDark();
    });

    function applyDark() {
        document.body.classList.add("dark-mode");
        themeIcon?.setAttribute("data-lucide", "moon");
        lucide.createIcons();
    }
    function removeDark() {
        document.body.classList.remove("dark-mode");
        themeIcon?.setAttribute("data-lucide", "sun");
        lucide.createIcons();
    }

    // Mobile Menu
    document.getElementById("mobile-menu-btn")?.addEventListener("click", () => {
        document.getElementById("nav-links")?.classList.toggle("open");
    });

    // Navbar scroll effect
    window.addEventListener("scroll", () => {
        const navbar = document.getElementById("navbar");
        if (navbar) navbar.style.boxShadow = window.scrollY > 10 ? "0 2px 20px rgba(0,0,0,0.1)" : "0 1px 0 var(--border)";

        const backBtn = document.getElementById("back-to-top");
        if (backBtn) {
            window.scrollY > 400 ? backBtn.classList.add("visible") : backBtn.classList.remove("visible");
        }
    });

    // Back to Top
    document.getElementById("back-to-top")?.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});


// Search Function
async function searchSchemes() {
    const input    = document.getElementById("search-input");
    const btn      = document.getElementById("search-btn");
    const query    = input?.value.trim() ?? "";

    if (!query) {
        if (input) { input.focus(); input.style.outline = "2px solid #EF4444"; }
        setTimeout(() => { if (input) input.style.outline = ""; }, 1500);
        showToast("Please enter a search query first");
        return;
    }

    // Close suggestions
    document.getElementById("suggestions-dropdown")?.classList.remove("open");

    const resultsSection   = document.getElementById("results-section");
    const resultsContainer = document.getElementById("results-container");
    const resultsTitle     = document.getElementById("results-title");
    const intentBadge      = document.getElementById("intent-badge");
    const queryDisplay     = document.getElementById("search-query-display");

    // Loading state
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner" style="width:16px;height:16px;border-width:2px;display:inline-block;vertical-align:middle;"></span> Searching...`;

    resultsSection.classList.add("visible");
    resultsContainer.innerHTML = `
        <div class="loading-state" style="grid-column:1/-1;">
            <div class="spinner"></div>
            <p>Finding the best schemes for you…</p>
        </div>`;
    intentBadge.style.display = "none";
    resultsTitle.textContent = "Searching…";
    if (queryDisplay) queryDisplay.textContent = `Results for: "${query}"`;

    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });

    try {
        const res = await fetch("/api/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        if (!res.ok) throw new Error(`Server error: ${res.status}`);
        const data = await res.json();
        renderResults(data, query);

    } catch (err) {
        resultsTitle.textContent = "Could not connect to server";
        resultsContainer.innerHTML = `
            <div class="no-results" style="grid-column:1/-1;">
                <h3>Server not reachable</h3>
                <p>Make sure the Flask API is running on <strong>http://localhost:5000</strong></p>
                <p style="margin-top:0.5rem;font-size:0.82rem;color:#94A3B8;">Error: ${err.message}</p>
            </div>`;
        showToast("Could not connect to Flask server");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> <span>Search</span>`;
    }
}


// Render Results
function renderResults(data, query) {
    const resultsContainer = document.getElementById("results-container");
    const resultsTitle     = document.getElementById("results-title");
    const intentBadge      = document.getElementById("intent-badge");
    const results          = data.results || [];
    const intent           = data.intent  || "";

    resultsTitle.textContent = results.length > 0 ? `${results.length} Schemes Found` : "No Schemes Found";

    if (intent && intent !== "general") {
        intentBadge.textContent = `Category: ${intent.replace(/_/g, " ")}`;
        intentBadge.style.display = "inline-flex";
    } else {
        intentBadge.style.display = "none";
    }

    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results" style="grid-column:1/-1;">
                <h3>No schemes found for "${escapeHtml(query)}"</h3>
                <p>Try keywords like "scholarship", "farmer loan", "health insurance", or "mahila scheme"</p>
            </div>`;
        showToast("No results found — try different keywords");
        lucide.createIcons();
        return;
    }

    resultsContainer.innerHTML = results.map((scheme, i) => {
        const score = Math.round((scheme.score || 0) * 100);
        const name  = scheme.scheme_name || "Unknown Scheme";
        const cat   = scheme.category    || "General";
        const desc  = scheme.description || "No description available.";
        const delay = i * 0.07;

        return `
        <div class="result-card" style="animation-delay:${delay}s;">
            <div class="result-card-header">
                <h3>${escapeHtml(name)}</h3>
                <span class="result-score">${score}% match</span>
            </div>
            <span class="result-category">
                <i data-lucide="tag" style="width:11px;height:11px;margin-right:4px;"></i>
                ${escapeHtml(cat)}
            </span>
            <p class="result-desc">${escapeHtml(desc)}</p>
            <a href="#" class="result-link" onclick="event.preventDefault(); showToast('Opening official portal…')">
                View Details
                <i data-lucide="arrow-right" style="width:14px;height:14px;"></i>
            </a>
        </div>`;
    }).join("");

    lucide.createIcons();
    showToast(`${results.length} schemes found for your query!`);
}


// Quick Search from category / carousel buttons
function quickSearch(query) {
    const input = document.getElementById("search-input");
    if (input) { input.value = query; document.getElementById("clear-btn").style.display = "flex"; }
    window.scrollTo({ top: 0, behavior: "smooth" });
    setTimeout(searchSchemes, 400);
}


// Toast Notification
function showToast(msg, duration = 3000) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), duration);
}


// Escape HTML
function escapeHtml(str) {
    const d = document.createElement("div");
    d.textContent = str;
    return d.innerHTML;
}


// Sign In Modal
function openSignIn() {
    document.getElementById("modal-overlay")?.classList.add("open");
    document.getElementById("signin-modal")?.classList.add("open");
    setTimeout(() => document.getElementById("signin-user")?.focus(), 300);
}

function closeSignIn() {
    document.getElementById("modal-overlay")?.classList.remove("open");
    document.getElementById("signin-modal")?.classList.remove("open");
}

function handleSignIn() {
    const user = document.getElementById("signin-user")?.value.trim();
    const pass = document.getElementById("signin-pass")?.value.trim();
    if (!user || !pass) {
        showToast("Please enter your credentials");
        return;
    }
    showToast("Sign In feature coming soon!");
    closeSignIn();
}

// Close modal on Escape key
document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeSignIn();
});


// Voice Search — Cross Browser (Chrome/Edge/Safari + Firefox)
(function initVoice() {
    const voiceBtn = document.getElementById("voice-btn");
    const micIcon  = document.getElementById("mic-icon");
    const input    = document.getElementById("search-input");
    if (!voiceBtn) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        // ── Primary: Web Speech API (Chrome, Edge, Safari) ──────
        const recognition = new SpeechRecognition();
        recognition.continuous     = false;
        recognition.interimResults = true;
        recognition.lang           = "hi-IN";
        recognition.maxAlternatives = 1;
        let isListening = false;

        voiceBtn.addEventListener("click", () => {
            if (isListening) { recognition.stop(); return; }
            recognition.start();
        });

        recognition.onstart = () => {
            isListening = true;
            voiceBtn.classList.add("recording");
            lucide.createIcons();
            showToast("Listening… Hindi, Hinglish ya English mein boliye");
            if (input) input.placeholder = "Bol rahe hain…";
        };

        recognition.onresult = (event) => {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            if (input) {
                input.value = transcript;
                document.getElementById("clear-btn").style.display = "flex";
            }
            if (event.results[event.results.length - 1].isFinal) {
                showToast(`Captured: "${transcript}"`);
                setTimeout(searchSchemes, 600);
            }
        };

        recognition.onerror = (e) => {
            const msgs = {
                "no-speech"   : "Koi awaaz nahi aayi — dobara try karein",
                "not-allowed" : "Microphone permission denied — browser settings check karein",
                "audio-capture": "Microphone nahi mila"
            };
            showToast(msgs[e.error] || `Voice error: ${e.error}`);
        };

        recognition.onend = () => {
            isListening = false;
            voiceBtn.classList.remove("recording");
            lucide.createIcons();
            if (input) input.placeholder = "e.g. 'main ek garib student hoon, mujhe scholarship chahiye'";
        };

    } else {
        // ── Fallback: MediaRecorder → Flask Backend (Firefox) ───
        if (!navigator.mediaDevices || !window.MediaRecorder) {
            voiceBtn.onclick = () => showToast("Voice not supported in this browser");
            voiceBtn.style.opacity = "0.4";
            return;
        }

        let mediaRecorder, audioChunks = [], isRecording = false;

        voiceBtn.addEventListener("click", async () => {
            if (isRecording) {
                mediaRecorder.stop();
                return;
            }

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioChunks = [];

                // Pick best supported format
                const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
                    ? "audio/webm;codecs=opus"
                    : MediaRecorder.isTypeSupported("audio/ogg;codecs=opus")
                    ? "audio/ogg;codecs=opus"
                    : "audio/webm";

                mediaRecorder = new MediaRecorder(stream, { mimeType });

                mediaRecorder.ondataavailable = e => { if (e.data.size > 0) audioChunks.push(e.data); };

                mediaRecorder.onstart = () => {
                    isRecording = true;
                    voiceBtn.classList.add("recording");
                    lucide.createIcons();
                    showToast("Recording… boliye, phir mic button dobara dabayein");
                    if (input) input.placeholder = "Recording…";
                };

                mediaRecorder.onstop = async () => {
                    isRecording = false;
                    voiceBtn.classList.remove("recording");
                    lucide.createIcons();
                    stream.getTracks().forEach(t => t.stop());
                    if (input) input.placeholder = "Transcribing…";
                    showToast("Processing your voice…");

                    const blob = new Blob(audioChunks, { type: mimeType });
                    const formData = new FormData();
                    formData.append("audio", blob, "voice." + mimeType.split("/")[1].split(";")[0]);

                    try {
                        const res = await fetch("/api/voice", { method: "POST", body: formData });
                        const data = await res.json();
                        if (data.transcript) {
                            if (input) {
                                input.value = data.transcript;
                                document.getElementById("clear-btn").style.display = "flex";
                            }
                            showToast(`Captured: "${data.transcript}"`);
                            setTimeout(searchSchemes, 600);
                        } else {
                            showToast(data.error || "Could not understand — please try again");
                        }
                    } catch (err) {
                        showToast("Voice transcription failed — server error");
                    }

                    if (input) input.placeholder = "e.g. 'main ek garib student hoon, mujhe scholarship chahiye'";
                };

                mediaRecorder.start();

            } catch (err) {
                showToast("Microphone access denied — browser settings check karein");
            }
        });
    }
})();


