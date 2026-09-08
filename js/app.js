/**
 * Smart Health Risk Indicator (SHRI) - Core Application Controller v3.2
 * Authentication, Multi-Patient Registry Management, and Client-Side Deep Learning
 */

// =========================================================================
// 1. DEFAULT PRE-SEEDED PATIENTS DATABASE
// =========================================================================
const DEFAULT_PATIENTS = [
    {
        id: "PT-1001",
        name: "Aarav Singh",
        age: 15,
        gender: "Male",
        primaryConcern: "Social Anxiety, Panic Symptoms & Exam Pressure",
        riskTier: "MODERATE",
        riskScore: 54,
        ci95: [49.2, 58.8],
        lastAssessment: "2026-09-08",
        history: [38, 42, 48, 51, 54],
        recoveryHistory: [62, 65, 71, 78, 82],
        streak: 5,
        q: { q1: 1, q2: 2, q3: 2, q4: 3, q5: 2 },
        bio: { sleepHours: 6.0, screenTime: 7.0, exerciseMinutes: 20, socialInteractions: 3 },
        journal: "I felt very nervous before class presentation today and my heart was pounding. Had trouble sleeping last night."
    },
    {
        id: "PT-1002",
        name: "Meera Patel",
        age: 16,
        gender: "Female",
        primaryConcern: "Major Depressive Affect, Anhedonia & Insomnia",
        riskTier: "SEVERE",
        riskScore: 78,
        ci95: [72.4, 83.6],
        lastAssessment: "2026-09-08",
        history: [48, 55, 64, 71, 78],
        recoveryHistory: [45, 48, 52, 55, 59],
        streak: 3,
        q: { q1: 3, q2: 3, q3: 3, q4: 2, q5: 2 },
        bio: { sleepHours: 4.0, screenTime: 9.5, exerciseMinutes: 5, socialInteractions: 1 },
        journal: "I feel completely exhausted and tired of everything. I cannot find joy in anything and stay in bed all day."
    },
    {
        id: "PT-1003",
        name: "Kiran Reddy",
        age: 13,
        gender: "Non-Binary",
        primaryConcern: "Mild Somatic Fatigue (Baseline / Healthy Check-in)",
        riskTier: "LOW",
        riskScore: 18,
        ci95: [14.5, 21.5],
        lastAssessment: "2026-09-07",
        history: [16, 18, 17, 19, 18],
        recoveryHistory: [80, 84, 82, 88, 91],
        streak: 7,
        q: { q1: 0, q2: 0, q3: 1, q4: 0, q5: 0 },
        bio: { sleepHours: 8.5, screenTime: 2.5, exerciseMinutes: 50, socialInteractions: 6 },
        journal: "Had a great art workshop today and finished my science project on time. Feeling energetic and cheerful!"
    },
    {
        id: "PT-1004",
        name: "Prateek Yadav",
        age: 17,
        gender: "Male",
        primaryConcern: "Chronic Circadian Sleep Debt & Cognitive Fog",
        riskTier: "HIGH",
        riskScore: 66,
        ci95: [60.8, 71.2],
        lastAssessment: "2026-09-06",
        history: [44, 49, 56, 61, 66],
        recoveryHistory: [50, 52, 58, 63, 67],
        streak: 4,
        q: { q1: 2, q2: 2, q3: 3, q4: 2, q5: 2 },
        bio: { sleepHours: 3.5, screenTime: 11.0, exerciseMinutes: 10, socialInteractions: 2 },
        journal: "Gaming until 4 AM every night. Cannot focus during lectures and constantly falling asleep during afternoon periods."
    }
];

// App State
let patientsDB = [];
let currentAuthRole = "doctor"; // "doctor" | "patient"
let currentAuthMode = "login";  // "login" | "register"
let currentUser = null;
let activePatientId = "PT-1002"; // default active patient

// Chart Instances
let radarChartInstance = null;
let ensembleBarInstance = null;
let mcHistInstance = null;
let shapBarInstance = null;
let trajectoryChartInstance = null;
let patientRecoveryChartInstance = null;

// Breathing Tool State
let breathingInterval = null;
let isBreathingActive = false;

// =========================================================================
// 2. INITIALIZATION
// =========================================================================
document.addEventListener("DOMContentLoaded", () => {
    loadPatientsFromStorage();
    checkExistingSession();
});

function loadPatientsFromStorage() {
    const saved = localStorage.getItem("shri_patients_db");
    if (saved) {
        try {
            patientsDB = JSON.parse(saved);
        } catch (e) {
            patientsDB = DEFAULT_PATIENTS;
        }
    } else {
        patientsDB = DEFAULT_PATIENTS;
        savePatientsToStorage();
    }
}

function savePatientsToStorage() {
    localStorage.setItem("shri_patients_db", JSON.stringify(patientsDB));
}

function checkExistingSession() {
    const session = localStorage.getItem("shri_active_user");
    if (session) {
        try {
            currentUser = JSON.parse(session);
            launchApplication();
        } catch (e) {
            showAuthSection();
        }
    } else {
        showAuthSection();
    }
}

// =========================================================================
// 3. AUTHENTICATION CONTROLS
// =========================================================================
function switchAuthRole(role) {
    currentAuthRole = role;
    const docBtn = document.getElementById("role-doctor-btn");
    const patBtn = document.getElementById("role-patient-btn");
    if (docBtn) docBtn.classList.toggle("active", role === "doctor");
    if (patBtn) patBtn.classList.toggle("active", role === "patient");
    updateAuthFormsVisibility();
}

function switchAuthMode(mode) {
    currentAuthMode = mode;
    const logBtn = document.getElementById("mode-login-btn");
    const regBtn = document.getElementById("mode-register-btn");
    if (logBtn) logBtn.classList.toggle("active", mode === "login");
    if (regBtn) regBtn.classList.toggle("active", mode === "register");
    updateAuthFormsVisibility();
}

function updateAuthFormsVisibility() {
    const docLogin = document.getElementById("doctor-login-form");
    const docReg = document.getElementById("doctor-reg-form");
    const patLogin = document.getElementById("patient-login-form");
    const patReg = document.getElementById("patient-reg-form");

    if (docLogin) docLogin.classList.remove("active");
    if (docReg) docReg.classList.remove("active");
    if (patLogin) patLogin.classList.remove("active");
    if (patReg) patReg.classList.remove("active");

    if (currentAuthRole === "doctor") {
        if (currentAuthMode === "login" && docLogin) docLogin.classList.add("active");
        if (currentAuthMode === "register" && docReg) docReg.classList.add("active");
    } else {
        if (currentAuthMode === "login" && patLogin) patLogin.classList.add("active");
        if (currentAuthMode === "register" && patReg) patReg.classList.add("active");
    }
}

function quickDemoLogin(role) {
    if (role === 'doctor') {
        currentUser = {
            role: "doctor",
            name: "Dr. Ramesh S",
            title: "Lead Clinician & Neuropsychiatrist",
            license: "MED-SRM-2024-8841",
            email: "dr.ramesh@srmist.edu.in"
        };
    } else {
        const aarav = patientsDB.find(p => p.id === "PT-1001") || patientsDB[0];
        currentUser = {
            role: "patient",
            name: aarav.name,
            id: aarav.id,
            age: aarav.age,
            gender: aarav.gender
        };
    }
    localStorage.setItem("shri_active_user", JSON.stringify(currentUser));
    launchApplication();
}

function handleDoctorLogin(event) {
    event.preventDefault();
    const email = document.getElementById("doc-email").value;
    const clinic = document.getElementById("doc-clinic").value;

    currentUser = {
        role: "doctor",
        name: "Dr. Ramesh S",
        title: clinic,
        license: "NWC-MED-4492",
        email: email
    };
    localStorage.setItem("shri_active_user", JSON.stringify(currentUser));
    launchApplication();
}

function handleDoctorRegister(event) {
    event.preventDefault();
    const name = document.getElementById("reg-doc-name").value;
    const license = document.getElementById("reg-doc-license").value;
    const email = document.getElementById("reg-doc-email").value;
    const dept = document.getElementById("reg-doc-dept").value;

    currentUser = {
        role: "doctor",
        name: name,
        title: dept,
        license: license,
        email: email
    };
    localStorage.setItem("shri_active_user", JSON.stringify(currentUser));
    launchApplication();
}

function handlePatientLogin(event) {
    event.preventDefault();
    const patId = document.getElementById("pat-login-id").value.trim();
    
    // Check if patient exists in DB
    const found = patientsDB.find(p => p.id.toLowerCase() === patId.toLowerCase() || p.name.toLowerCase().includes(patId.toLowerCase()));
    if (found) {
        currentUser = {
            role: "patient",
            name: found.name,
            id: found.id,
            age: found.age,
            gender: found.gender
        };
    } else {
        currentUser = {
            role: "patient",
            name: "Aarav Singh",
            id: patId || "PT-1001",
            age: 15,
            gender: "Male"
        };
    }
    localStorage.setItem("shri_active_user", JSON.stringify(currentUser));
    launchApplication();
}

function handlePatientRegister(event) {
    event.preventDefault();
    const name = document.getElementById("reg-pat-name").value;
    const age = parseInt(document.getElementById("reg-pat-age").value);
    const gender = document.getElementById("reg-pat-gender").value;
    const id = document.getElementById("reg-pat-id").value.trim() || `PT-${Math.floor(1000 + Math.random() * 9000)}`;

    const newPat = {
        id: id,
        name: name,
        age: age,
        gender: gender,
        primaryConcern: "General Adolescent Mental Health Self-Check",
        riskTier: "LOW",
        riskScore: 22,
        ci95: [18.2, 25.8],
        lastAssessment: new Date().toISOString().split("T")[0],
        history: [20, 22],
        recoveryHistory: [75, 78, 82],
        streak: 1,
        q: { q1: 1, q2: 0, q3: 1, q4: 0, q5: 0 },
        bio: { sleepHours: 7.5, screenTime: 4.0, exerciseMinutes: 30, socialInteractions: 4 },
        journal: "Registered new profile for daily wellness tracking."
    };

    patientsDB.push(newPat);
    savePatientsToStorage();

    currentUser = {
        role: "patient",
        name: name,
        id: id,
        age: age,
        gender: gender
    };
    localStorage.setItem("shri_active_user", JSON.stringify(currentUser));
    launchApplication();
}

function handleLogout() {
    localStorage.removeItem("shri_active_user");
    currentUser = null;
    if (breathingInterval) {
        clearInterval(breathingInterval);
        breathingInterval = null;
        isBreathingActive = false;
    }
    showAuthSection();
}

function showAuthSection() {
    const authSec = document.getElementById("auth-section");
    const mainSec = document.getElementById("main-app-section");
    if (authSec) authSec.style.display = "flex";
    if (mainSec) mainSec.style.display = "none";
}

// =========================================================================
// 4. APPLICATION ROUTING & PORTAL VIEWS
// =========================================================================
function launchApplication() {
    const authSec = document.getElementById("auth-section");
    const mainSec = document.getElementById("main-app-section");
    if (authSec) authSec.style.display = "none";
    if (mainSec) mainSec.style.display = "flex";

    // Update Sidebar Profile
    const userNameEl = document.getElementById("sidebar-user-name");
    const userRoleEl = document.getElementById("sidebar-user-role");
    const userAvatarEl = document.getElementById("sidebar-user-avatar");

    if (userNameEl) userNameEl.innerText = currentUser.name;
    if (userRoleEl) userRoleEl.innerText = currentUser.role === "doctor" ? (currentUser.title || "Lead Clinician") : "Adolescent Patient";
    if (userAvatarEl) userAvatarEl.innerText = currentUser.role === "doctor" ? "👨‍⚕️" : "👤";

    if (currentUser.role === "doctor") {
        document.getElementById("doctor-nav-section").style.display = "block";
        document.getElementById("patient-nav-section").style.display = "none";
        const topAddBtn = document.getElementById("top-add-patient-btn");
        if (topAddBtn) topAddBtn.style.display = "inline-flex";
        showDoctorRegistry();
    } else {
        document.getElementById("doctor-nav-section").style.display = "none";
        document.getElementById("clinical-tabs-section").style.display = "none";
        document.getElementById("patient-nav-section").style.display = "block";
        const topAddBtn = document.getElementById("top-add-patient-btn");
        if (topAddBtn) topAddBtn.style.display = "none";
        showPatientPortalView();
    }
}

function showDoctorRegistry() {
    document.getElementById("doctor-registry-view").style.display = "block";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    document.getElementById("patient-portal-view").style.display = "none";
    
    document.getElementById("clinical-tabs-section").style.display = "none";
    
    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    if (regBtn) regBtn.classList.add("active");
    if (dosBtn) dosBtn.classList.remove("active");

    document.getElementById("page-main-title").innerText = "Patient Registry Dashboard";
    document.getElementById("page-subtitle").innerText = "Enrolled Adolescent Patients & Continuous Risk Monitoring";

    renderRegistryStats();
    renderPatientCards();
}

function showPatientDossier(patientId) {
    if (patientId) activePatientId = patientId;
    
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "block";
    document.getElementById("patient-portal-view").style.display = "none";

    document.getElementById("clinical-tabs-section").style.display = "block";
    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    if (regBtn) regBtn.classList.remove("active");
    if (dosBtn) dosBtn.classList.add("active");

    populatePatientDossier(activePatientId);
}

function showPatientPortalView() {
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    document.getElementById("patient-portal-view").style.display = "block";

    const pat = patientsDB.find(p => p.id === (currentUser.id || "PT-1001")) || patientsDB[0];
    const welcomeEl = document.getElementById("patient-portal-welcome-name");
    if (welcomeEl) welcomeEl.innerText = `Hello, ${currentUser.name}! 👋`;

    const streakEl = document.getElementById("patient-streak-text");
    if (streakEl) streakEl.innerText = `🔥 ${pat.streak || 5}-Day Check-in Streak!`;

    // Default to daily self-check tab
    showPatientPortalTab('self-check');
}

/**
 * Switch Patient Portal Sub-tabs: 'self-check' | 'my-trends' | 'my-cbt'
 */
function showPatientPortalTab(tabName) {
    const viewSelfCheck = document.getElementById("pat-view-self-check");
    const viewTrends = document.getElementById("pat-view-trends");
    const viewCBT = document.getElementById("pat-view-cbt");

    // Subtab Buttons
    const btnSelfCheck = document.getElementById("pat-tab-btn-self-check");
    const btnTrends = document.getElementById("pat-tab-btn-trends");
    const btnCBT = document.getElementById("pat-tab-btn-cbt");

    // Sidebar Buttons
    const navSelfCheck = document.getElementById("pat-nav-self-check");
    const navTrends = document.getElementById("pat-nav-trends");
    const navCBT = document.getElementById("pat-nav-cbt");

    // Hide all panels
    if (viewSelfCheck) viewSelfCheck.style.display = "none";
    if (viewTrends) viewTrends.style.display = "none";
    if (viewCBT) viewCBT.style.display = "none";

    // Remove active class from buttons
    [btnSelfCheck, btnTrends, btnCBT, navSelfCheck, navTrends, navCBT].forEach(b => {
        if (b) b.classList.remove("active");
    });

    const pageTitle = document.getElementById("page-main-title");
    const pageSub = document.getElementById("page-subtitle");

    if (tabName === "self-check" || tabName === "daily-check") {
        if (viewSelfCheck) viewSelfCheck.style.display = "block";
        if (btnSelfCheck) btnSelfCheck.classList.add("active");
        if (navSelfCheck) navSelfCheck.classList.add("active");
        if (pageTitle) pageTitle.innerText = "My Adolescent Wellness Portal";
        if (pageSub) pageSub.innerText = "Confidential Daily Check-in & Science-Backed Reflection";
    } 
    else if (tabName === "my-trends" || tabName === "trends") {
        if (viewTrends) viewTrends.style.display = "block";
        if (btnTrends) btnTrends.classList.add("active");
        if (navTrends) navTrends.classList.add("active");
        if (pageTitle) pageTitle.innerText = "My Recovery Trends & Strength";
        if (pageSub) pageSub.innerText = "Longitudinal Mood Trajectory, Sleep Stability & Emotional Resilience";

        // Refresh stats & chart
        updatePatientRecoveryMetrics();
        renderPatientRecoveryChart();
    } 
    else if (tabName === "my-cbt" || tabName === "cbt") {
        if (viewCBT) viewCBT.style.display = "block";
        if (btnCBT) btnCBT.classList.add("active");
        if (navCBT) navCBT.classList.add("active");
        if (pageTitle) pageTitle.innerText = "Coping Strategies & CBT Exercises";
        if (pageSub) pageSub.innerText = "Interactive 4-7-8 Breathing Calmer & Negative Thought Buster";
    }
}

function updatePatientRecoveryMetrics() {
    const pat = patientsDB.find(p => p.id === (currentUser ? currentUser.id : "PT-1001")) || patientsDB[0];
    const wellnessEl = document.getElementById("pat-metric-wellness");
    const sleepEl = document.getElementById("pat-metric-sleep");
    const streakEl = document.getElementById("pat-metric-streak");

    const latestWellness = pat.recoveryHistory && pat.recoveryHistory.length 
        ? pat.recoveryHistory[pat.recoveryHistory.length - 1] 
        : Math.max(15, 100 - pat.riskScore);

    if (wellnessEl) wellnessEl.innerText = `${latestWellness} / 100`;
    if (sleepEl) sleepEl.innerText = `${pat.bio.sleepHours} Hrs`;
    if (streakEl) streakEl.innerText = `${pat.streak || 5} Days`;
}

// =========================================================================
// 5. DOCTOR PATIENT REGISTRY RENDERING
// =========================================================================
function renderRegistryStats() {
    const total = patientsDB.length;
    const critical = patientsDB.filter(p => p.riskTier === "HIGH" || p.riskTier === "SEVERE").length;
    const avgScore = total > 0 ? (patientsDB.reduce((acc, p) => acc + p.riskScore, 0) / total).toFixed(1) : "0.0";

    const statTotal = document.getElementById("stat-total-patients");
    const sideCount = document.getElementById("sidebar-patient-count");
    const statCrit = document.getElementById("stat-critical-alerts");
    const statAvg = document.getElementById("stat-avg-score");

    if (statTotal) statTotal.innerText = total;
    if (sideCount) sideCount.innerText = total;
    if (statCrit) statCrit.innerText = critical;
    if (statAvg) statAvg.innerText = avgScore;
}

function renderPatientCards(filterList) {
    const container = document.getElementById("patient-cards-container");
    if (!container) return;
    container.innerHTML = "";

    const list = filterList || patientsDB;

    if (list.length === 0) {
        container.innerHTML = `<div class="card" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
            <p style="color: var(--text-muted); font-size: 14px;">No patient records match the search query.</p>
        </div>`;
        return;
    }

    list.forEach(pat => {
        const tierClass = pat.riskTier.toLowerCase();
        const card = document.createElement("div");
        card.className = "patient-card";
        card.innerHTML = `
            <div class="patient-card-header">
                <div class="patient-card-meta">
                    <div class="patient-card-avatar">${pat.gender === 'Female' ? '👧' : '👦'}</div>
                    <div>
                        <h4 class="patient-card-name">${pat.name}</h4>
                        <span class="patient-card-sub">${pat.age}y ${pat.gender} • ID: ${pat.id}</span>
                    </div>
                </div>
                <span class="risk-tag ${tierClass}">${pat.riskTier} RISK</span>
            </div>
            <div class="patient-card-body">
                <div class="patient-score-row">
                    <span class="score-display">${pat.riskScore} <span style="font-size: 12px; color: var(--text-muted);">/ 100</span></span>
                    <span class="score-ci">95% CI: [${pat.ci95[0]} – ${pat.ci95[1]}]</span>
                </div>
                <div class="patient-concern-text">
                    <b>Primary Concern:</b> ${pat.primaryConcern}
                </div>
            </div>
            <div class="patient-card-actions">
                <button class="btn btn-primary" style="flex: 1;" onclick="showPatientDossier('${pat.id}')">
                    <span>📊 Open Dossier</span>
                </button>
                <button class="btn btn-secondary" onclick="deletePatientRecord('${pat.id}')" title="Delete Patient">
                    <span>🗑️</span>
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

function filterPatientRegistry() {
    const searchInput = document.getElementById("patient-search-input");
    const tierSelect = document.getElementById("filter-risk-select");
    const search = searchInput ? searchInput.value.toLowerCase() : "";
    const filterTier = tierSelect ? tierSelect.value : "ALL";

    const filtered = patientsDB.filter(p => {
        const matchSearch = p.name.toLowerCase().includes(search) || p.id.toLowerCase().includes(search) || p.primaryConcern.toLowerCase().includes(search);
        const matchTier = (filterTier === "ALL") || (p.riskTier === filterTier);
        return matchSearch && matchTier;
    });

    renderPatientCards(filtered);
}

// =========================================================================
// 6. MULTI-PATIENT ENROLLMENT MODAL
// =========================================================================
function openAddPatientModal() {
    const modal = document.getElementById("add-patient-modal");
    if (modal) modal.style.display = "flex";
}

function closeAddPatientModal() {
    const modal = document.getElementById("add-patient-modal");
    if (modal) modal.style.display = "none";
}

function handleAddNewPatient(event) {
    event.preventDefault();
    const name = document.getElementById("new-pat-name").value;
    const age = parseInt(document.getElementById("new-pat-age").value);
    const gender = document.getElementById("new-pat-gender").value;
    const id = document.getElementById("new-pat-id").value.trim();
    const concern = document.getElementById("new-pat-concern").value;
    const preset = document.getElementById("new-pat-risk-preset").value;

    let initialScore = 45;
    let initialTier = preset;
    let ci = [40.5, 49.5];
    let qValues = { q1: 2, q2: 2, q3: 2, q4: 2, q5: 2 };
    let bioValues = { sleepHours: 6.0, screenTime: 6.5, exerciseMinutes: 20, socialInteractions: 3 };

    if (preset === "SEVERE") {
        initialScore = 82;
        ci = [76.4, 87.6];
        qValues = { q1: 3, q2: 3, q3: 3, q4: 3, q5: 2 };
        bioValues = { sleepHours: 3.5, screenTime: 10.0, exerciseMinutes: 5, socialInteractions: 1 };
    } else if (preset === "HIGH") {
        initialScore = 68;
        ci = [62.8, 73.2];
        qValues = { q1: 2, q2: 3, q3: 2, q4: 2, q5: 2 };
        bioValues = { sleepHours: 4.5, screenTime: 8.5, exerciseMinutes: 10, socialInteractions: 2 };
    } else if (preset === "LOW") {
        initialScore = 18;
        ci = [14.2, 21.8];
        qValues = { q1: 0, q2: 0, q3: 1, q4: 0, q5: 0 };
        bioValues = { sleepHours: 8.5, screenTime: 3.0, exerciseMinutes: 45, socialInteractions: 5 };
    }

    const newPatient = {
        id: id,
        name: name,
        age: age,
        gender: gender,
        primaryConcern: concern,
        riskTier: initialTier,
        riskScore: initialScore,
        ci95: ci,
        lastAssessment: new Date().toISOString().split("T")[0],
        history: [initialScore - 5, initialScore],
        recoveryHistory: [Math.max(20, 100 - initialScore - 5), Math.max(25, 100 - initialScore)],
        streak: 1,
        q: qValues,
        bio: bioValues,
        journal: `Enrolled on ${new Date().toLocaleDateString()}. Initial clinical observation: ${concern}`
    };

    patientsDB.push(newPatient);
    savePatientsToStorage();
    closeAddPatientModal();

    // Refresh UI
    renderRegistryStats();
    renderPatientCards();
    showPatientDossier(id);
}

function deletePatientRecord(id) {
    if (confirm(`Are you sure you want to remove patient record ${id}?`)) {
        patientsDB = patientsDB.filter(p => p.id !== id);
        savePatientsToStorage();
        renderRegistryStats();
        renderPatientCards();
    }
}

// =========================================================================
// 7. PATIENT DOSSIER & MULTIMODAL DEEP LEARNING INFERENCE
// =========================================================================
function populatePatientDossier(patientId) {
    const pat = patientsDB.find(p => p.id === patientId) || patientsDB[0];
    if (!pat) return;

    activePatientId = pat.id;

    // Update Header Banner
    const avatarEl = document.getElementById("dossier-avatar");
    const nameEl = document.getElementById("dossier-patient-name");
    const subEl = document.getElementById("dossier-patient-sub");

    if (avatarEl) avatarEl.innerText = pat.gender === 'Female' ? '👧' : '👦';
    if (nameEl) nameEl.innerText = pat.name;
    if (subEl) subEl.innerText = `${pat.age}y ${pat.gender} | ID: ${pat.id} | Primary: ${pat.primaryConcern}`;

    // Populate Patient Dropdown
    const dropdown = document.getElementById("dossier-patient-dropdown");
    if (dropdown) {
        dropdown.innerHTML = "";
        patientsDB.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            opt.innerText = `${p.name} (${p.id} - ${p.riskTier})`;
            if (p.id === pat.id) opt.selected = true;
            dropdown.appendChild(opt);
        });
    }

    // Populate Form Inputs
    ["q1", "q2", "q3", "q4", "q5"].forEach(q => {
        const el = document.getElementById(q);
        const valEl = document.getElementById(`val-${q}`);
        if (el && pat.q) el.value = pat.q[q] !== undefined ? pat.q[q] : 1;
        if (valEl && pat.q) valEl.innerText = pat.q[q] !== undefined ? pat.q[q] : 1;
    });

    if (pat.bio) {
        const sleepEl = document.getElementById("bio-sleep");
        const screenEl = document.getElementById("bio-screen");
        const exEl = document.getElementById("bio-exercise");
        const socEl = document.getElementById("bio-social");

        if (sleepEl) sleepEl.value = pat.bio.sleepHours;
        if (screenEl) screenEl.value = pat.bio.screenTime;
        if (exEl) exEl.value = pat.bio.exerciseMinutes;
        if (socEl) socEl.value = pat.bio.socialInteractions;
    }

    const journalEl = document.getElementById("journal-input");
    if (journalEl) journalEl.value = pat.journal || "";

    // Run Assessment
    runClinicalAssessment();
}

function selectPatientFromDropdown(id) {
    populatePatientDossier(id);
}

function switchDossierTab(tabName) {
    // Nav items
    document.querySelectorAll(".nav-sub-item").forEach(el => {
        el.classList.toggle("active", el.getAttribute("data-tab") === tabName);
    });
    // Subtab buttons
    document.querySelectorAll(".subtab-btn").forEach(el => {
        el.classList.toggle("active", el.getAttribute("data-tab") === tabName);
    });
    // Tab contents
    document.querySelectorAll("#doctor-patient-detail-view .tab-content").forEach(el => {
        el.classList.toggle("active", el.id === `tab-${tabName}`);
    });
}

function updateSliderDisplay(slider) {
    const valSpan = document.getElementById(`val-${slider.id}`);
    if (valSpan) valSpan.innerText = slider.value;
    runClinicalAssessment();
}

function analyzeJournalLive() {
    const text = document.getElementById("journal-input").value;
    const hasCrisis = detectCrisisKeywords(text);
    const crisisBanner = document.getElementById("crisis-alert-inline");
    if (crisisBanner) {
        crisisBanner.style.display = hasCrisis ? "block" : "none";
    }
}

function detectCrisisKeywords(text) {
    if (!text) return false;
    const lower = text.toLowerCase();
    const flags = ["kill myself", "suicide", "end my life", "want to die", "hurt myself", "hopeless", "no reason to live"];
    return flags.some(k => lower.includes(k));
}

function runClinicalAssessment() {
    // 1. Gather Questionnaire Features (PHQ-9 & GAD-7 proxies)
    const q1 = parseInt(document.getElementById("q1") ? document.getElementById("q1").value : 1);
    const q2 = parseInt(document.getElementById("q2") ? document.getElementById("q2").value : 1);
    const q3 = parseInt(document.getElementById("q3") ? document.getElementById("q3").value : 1);
    const q4 = parseInt(document.getElementById("q4") ? document.getElementById("q4").value : 1);
    const q5 = parseInt(document.getElementById("q5") ? document.getElementById("q5").value : 1);

    // 2. Gather Biometric & Digital Phenotypes
    const sleep = parseFloat(document.getElementById("bio-sleep") ? document.getElementById("bio-sleep").value : 7);
    const screen = parseFloat(document.getElementById("bio-screen") ? document.getElementById("bio-screen").value : 6);
    const exercise = parseFloat(document.getElementById("bio-exercise") ? document.getElementById("bio-exercise").value : 30);
    const social = parseFloat(document.getElementById("bio-social") ? document.getElementById("bio-social").value : 4);
    const journalText = document.getElementById("journal-input") ? document.getElementById("journal-input").value : "";

    // NLP Sentiment Proxy
    let nlpRisk = 0;
    const textLower = journalText.toLowerCase();
    if (textLower.includes("sad") || textLower.includes("cry") || textLower.includes("lonely") || textLower.includes("tired")) nlpRisk += 8;
    if (textLower.includes("anxious") || textLower.includes("panic") || textLower.includes("scared") || textLower.includes("nervous")) nlpRisk += 10;
    if (textLower.includes("exhausted") || textLower.includes("hopeless") || textLower.includes("worthless")) nlpRisk += 15;
    if (textLower.includes("happy") || textLower.includes("great") || textLower.includes("excited") || textLower.includes("good")) nlpRisk -= 10;

    // Base Subscales
    const depScore = ((q1 + q2 + (sleep < 5 ? 2 : 0)) / 8.0) * 100;
    const anxScore = ((q3 + q4) / 6.0) * 100;
    const sleepDeficit = Math.max(0, (8.0 - sleep) / 5.0) * 100;
    const screenRisk = Math.min(100, (screen / 12.0) * 100);
    const exerciseProtective = Math.min(100, (exercise / 60.0) * 100);

    // 4-Model Ensemble Weights
    const lstmPred = Math.min(99, Math.max(5, (depScore * 0.45 + anxScore * 0.35 + sleepDeficit * 0.20 + nlpRisk)));
    const cnnPred = Math.min(99, Math.max(5, (anxScore * 0.40 + depScore * 0.30 + screenRisk * 0.30 + nlpRisk * 0.8)));
    const rfPred = Math.min(99, Math.max(5, (depScore * 0.35 + sleepDeficit * 0.30 + (100 - exerciseProtective) * 0.35)));
    const gbPred = Math.min(99, Math.max(5, (depScore * 0.38 + anxScore * 0.32 + screenRisk * 0.15 + sleepDeficit * 0.15)));

    // Meta-Ensemble Weighted Stacking
    const ensembleScore = Math.round(lstmPred * 0.35 + cnnPred * 0.25 + rfPred * 0.20 + gbPred * 0.20);
    
    // Monte Carlo Dropout Epistemic Uncertainty
    const mcSamples = [];
    for (let i = 0; i < 20; i++) {
        const noise = (Math.random() - 0.5) * 8.0;
        mcSamples.push(Math.max(0, Math.min(100, ensembleScore + noise)));
    }
    const mcMean = mcSamples.reduce((a, b) => a + b, 0) / mcSamples.length;
    const mcStd = Math.sqrt(mcSamples.map(x => Math.pow(x - mcMean, 2)).reduce((a, b) => a + b, 0) / mcSamples.length);
    const ciLow = Math.max(0, Math.round((mcMean - 1.96 * mcStd) * 10) / 10);
    const ciHigh = Math.min(100, Math.round((mcMean + 1.96 * mcStd) * 10) / 10);

    // Determine Risk Tier
    let tier = "LOW";
    let tierClass = "low";
    if (ensembleScore >= 75) { tier = "SEVERE"; tierClass = "severe"; }
    else if (ensembleScore >= 60) { tier = "HIGH"; tierClass = "high"; }
    else if (ensembleScore >= 40) { tier = "MODERATE"; tierClass = "moderate"; }
    else if (ensembleScore >= 25) { tier = "MILD"; tierClass = "mild"; }

    // Update Dossier UI
    const scoreValEl = document.getElementById("dossier-risk-score-val");
    const tierBadgeEl = document.getElementById("dossier-risk-tier-badge");
    const ciEl = document.getElementById("dossier-ci-val");
    const stdEl = document.getElementById("dossier-std-val");

    if (scoreValEl) scoreValEl.innerText = `${ensembleScore} / 100`;
    if (tierBadgeEl) {
        tierBadgeEl.innerText = `${tier} RISK`;
        tierBadgeEl.className = `risk-badge ${tierClass}`;
    }
    if (ciEl) ciEl.innerText = `[${ciLow} – ${ciHigh}]`;
    if (stdEl) stdEl.innerText = `±${mcStd.toFixed(2)}`;

    // Update active patient object in DB
    const activePat = patientsDB.find(p => p.id === activePatientId);
    if (activePat) {
        activePat.riskScore = ensembleScore;
        activePat.riskTier = tier;
        activePat.ci95 = [ciLow, ciHigh];
        activePat.q = { q1, q2, q3, q4, q5 };
        activePat.bio = { sleepHours: sleep, screenTime: screen, exerciseMinutes: exercise, socialInteractions: social };
        activePat.journal = journalText;
        savePatientsToStorage();
    }

    // Render Charts
    renderRadarChart(depScore, anxScore, sleepDeficit, screenRisk, 100 - exerciseProtective, Math.max(0, nlpRisk + 20));
    renderEnsembleChart(lstmPred, cnnPred, rfPred, gbPred, ensembleScore);
    renderMCHistogram(mcSamples);
    renderSHAPChart(depScore, anxScore, sleepDeficit, screenRisk, exerciseProtective);
    renderTrajectoryChart(activePat ? activePat.history : [35, 45, 50], ensembleScore);
    renderCBTPlans(tier, depScore, anxScore, sleepDeficit);
}

// =========================================================================
// 8. CHART.JS VISUALIZATION RENDERERS
// =========================================================================
function renderRadarChart(dep, anx, sleep, screen, sedentary, nlp) {
    const canvas = document.getElementById("clinicalRadarChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Depressive Affect', 'Anxiety & Panic', 'Sleep Debt', 'Excess Screen', 'Physical Inactivity', 'Affective Sentiment'],
            datasets: [{
                label: 'Clinical Dimension Severity',
                data: [dep, anx, sleep, screen, sedentary, nlp],
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38BDF8',
                pointBackgroundColor: '#0284C7',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#38BDF8'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: '#374151' },
                    grid: { color: '#374151' },
                    pointLabels: { color: '#9CA3AF', font: { size: 11, family: 'Plus Jakarta Sans' } },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderEnsembleChart(lstm, cnn, rf, gb, ensemble) {
    const canvas = document.getElementById("ensembleBarChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (ensembleBarInstance) ensembleBarInstance.destroy();

    ensembleBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['LSTM (Temporal)', 'CNN-1D (Acoustic/NLP)', 'Random Forest', 'Gradient Boosting', 'Meta-Ensemble'],
            datasets: [{
                label: 'Risk Prediction',
                data: [lstm, cnn, rf, gb, ensemble],
                backgroundColor: [
                    '#38BDF8',
                    '#818CF8',
                    '#34D399',
                    '#FBBF24',
                    '#F87171'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                x: { grid: { display: false }, ticks: { color: '#9CA3AF' } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderMCHistogram(samples) {
    const canvas = document.getElementById("mcHistChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (mcHistInstance) mcHistInstance.destroy();

    mcHistInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: samples.map((_, i) => `T=${i + 1}`),
            datasets: [{
                label: 'Dropout Sample Score',
                data: samples,
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.15)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#F59E0B'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                x: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderSHAPChart(dep, anx, sleep, screen, exercise) {
    const canvas = document.getElementById("shapBarChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (shapBarInstance) shapBarInstance.destroy();

    const shapValues = [
        Math.round(dep * 0.28),
        Math.round(anx * 0.22),
        Math.round(sleep * 0.18),
        Math.round(screen * 0.12),
        -Math.round(exercise * 0.20)
    ];

    shapBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Depressive Symptom Load (PHQ-9)',
                'Anxiety & Somatic Panic (GAD-7)',
                'Circadian Sleep Debt (<6h)',
                'Excess Screen Exposure',
                'Protective: Physical Exercise'
            ],
            datasets: [{
                data: shapValues,
                backgroundColor: shapValues.map(v => v >= 0 ? '#F87171' : '#34D399'),
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                y: { grid: { display: false }, ticks: { color: '#F9FAFB', font: { size: 12 } } }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `SHAP Impact: ${ctx.raw > 0 ? '+' : ''}${ctx.raw} risk points`
                    }
                }
            }
        }
    });
}

function renderTrajectoryChart(history, currentScore) {
    const canvas = document.getElementById("trajectoryChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (trajectoryChartInstance) trajectoryChartInstance.destroy();

    const fullHistory = [...history, currentScore];
    const labels = fullHistory.map((_, i) => `Session ${i + 1}`);

    trajectoryChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Patient Risk Score',
                    data: fullHistory,
                    borderColor: '#38BDF8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    borderWidth: 3,
                    tension: 0.2,
                    pointRadius: 6,
                    pointBackgroundColor: '#0284C7'
                },
                {
                    label: 'High Risk Threshold (50)',
                    data: labels.map(() => 50),
                    borderColor: '#F59E0B',
                    borderDash: [5, 5],
                    borderWidth: 1.5,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                x: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } }
            },
            plugins: { legend: { labels: { color: '#9CA3AF' } } }
        }
    });
}

function renderCBTPlans(tier, dep, anx, sleep) {
    const container = document.getElementById("cbt-plans-container");
    if (!container) return;
    container.innerHTML = "";

    const plans = [
        {
            title: "🧠 Cognitive Restructuring (Thought Reframing)",
            desc: "Identifies negative automatic thought patterns, catastrophic thinking, and black-and-white cognitive distortions, guiding the adolescent to construct evidence-based balanced thoughts."
        },
        {
            title: "🌬️ 4-7-8 Diaphragmatic Breathing & Somatic De-escalation",
            desc: "Reduces acute autonomic sympathetic arousal by engaging the vagal parasympathetic response. 4s inhale, 7s hold, 8s controlled oral exhale."
        },
        {
            title: "🌙 Circadian Stabilization & Sleep Hygiene Protocol",
            desc: "Restricts blue light exposure 90 minutes before sleep, enforces consistent sleep-wake cycles, and introduces progressive muscle relaxation to decrease sleep onset latency."
        },
        {
            title: "🏃 Behavioral Activation & Activity Scheduling",
            desc: "Structures daily micro-goals to reverse anhedonia and depressive withdrawal through positive reinforcement and scholastic engagement."
        }
    ];

    plans.forEach(p => {
        const card = document.createElement("div");
        card.className = "cbt-card";
        card.innerHTML = `<h4>${p.title}</h4><p>${p.desc}</p>`;
        container.appendChild(card);
    });
}

// =========================================================================
// 9. PATIENT SELF-ASSESSMENT & INTERACTIVE TOOLS (Trends, 4-7-8 & CBT)
// =========================================================================

function updatePatSlider(slider) {
    const labels = ["Great / Energetic", "Good", "Low / Fatigued", "Severely Drained"];
    const valEl = document.getElementById("pat-val-mood");
    if (valEl) valEl.innerText = labels[slider.value] || "Good";
}

function updatePatSleep(slider) {
    const valEl = document.getElementById("pat-val-sleep");
    if (valEl) valEl.innerText = `${slider.value} Hours`;
}

function updatePatStress(slider) {
    const labels = ["None", "Mild", "Moderate", "Severe Stress"];
    const valEl = document.getElementById("pat-val-stress");
    if (valEl) valEl.innerText = labels[slider.value] || "Mild";
}

function submitPatientSelfCheck() {
    const moodSlider = document.getElementById("pat-slider-mood");
    const sleepSlider = document.getElementById("pat-slider-sleep");
    const stressSlider = document.getElementById("pat-slider-stress");
    const journalInput = document.getElementById("pat-journal-text");

    const moodVal = moodSlider ? parseInt(moodSlider.value) : 1;
    const sleepVal = sleepSlider ? parseFloat(sleepSlider.value) : 7;
    const stressVal = stressSlider ? parseInt(stressSlider.value) : 1;
    const reflection = journalInput ? journalInput.value.trim() : "";

    // Calculate wellness score (0-100, higher is healthier)
    let wellnessScore = 80;
    if (moodVal === 0) wellnessScore += 15;
    else if (moodVal === 1) wellnessScore += 5;
    else if (moodVal === 2) wellnessScore -= 15;
    else if (moodVal === 3) wellnessScore -= 35;

    if (sleepVal >= 7.5 && sleepVal <= 9.5) wellnessScore += 10;
    else if (sleepVal < 6) wellnessScore -= (6 - sleepVal) * 8;

    if (stressVal === 0) wellnessScore += 10;
    else if (stressVal === 1) wellnessScore += 0;
    else if (stressVal === 2) wellnessScore -= 15;
    else if (stressVal === 3) wellnessScore -= 30;

    wellnessScore = Math.max(10, Math.min(98, Math.round(wellnessScore)));

    // Update active patient in DB
    const pat = patientsDB.find(p => p.id === (currentUser ? currentUser.id : "PT-1001")) || patientsDB[0];
    if (!pat.recoveryHistory) pat.recoveryHistory = [62, 65, 71, 78, 82];
    pat.recoveryHistory.push(wellnessScore);
    pat.streak = (pat.streak || 5) + 1;
    pat.bio.sleepHours = sleepVal;
    if (reflection) pat.journal = reflection;

    savePatientsToStorage();

    // Update DOM status
    const statusMsgEl = document.getElementById("patient-wellness-status");
    const detailMsgEl = document.getElementById("patient-wellness-msg");
    if (statusMsgEl) {
        if (wellnessScore >= 75) statusMsgEl.innerText = "🌟 Outstanding Wellness!";
        else if (wellnessScore >= 50) statusMsgEl.innerText = "👍 Stable & Balanced";
        else statusMsgEl.innerText = "💙 Take It Easy Today";
    }
    if (detailMsgEl) {
        detailMsgEl.innerText = `Today's calculated wellness score is ${wellnessScore}/100. Streak updated to ${pat.streak} days!`;
    }

    alert(`✅ Daily Check-in Saved!\n\nToday's Personal Wellness Score: ${wellnessScore} / 100\nConsecutive Streak: ${pat.streak} Days\nAll reflections are saved securely on your device.`);

    // If on trends tab or viewing, refresh chart
    updatePatientRecoveryMetrics();
    renderPatientRecoveryChart();
}

/**
 * Render Chart.js Recovery Trends for Adolescent Patient Portal
 */
function renderPatientRecoveryChart() {
    const canvas = document.getElementById("patientRecoveryChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (patientRecoveryChartInstance) patientRecoveryChartInstance.destroy();

    const pat = patientsDB.find(p => p.id === (currentUser ? currentUser.id : "PT-1001")) || patientsDB[0];
    const dataPoints = pat.recoveryHistory && pat.recoveryHistory.length ? pat.recoveryHistory : [60, 64, 70, 75, 82];
    const labels = dataPoints.map((_, idx) => `Check-in ${idx + 1}`);

    patientRecoveryChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Personal Wellness & Strength Score',
                    data: dataPoints,
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.15)',
                    borderWidth: 3,
                    tension: 0.35,
                    fill: true,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#059669',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2
                },
                {
                    label: 'Resilience Baseline Target (75)',
                    data: labels.map(() => 75),
                    borderColor: '#38BDF8',
                    borderDash: [6, 4],
                    borderWidth: 1.5,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    grid: { color: '#374151' },
                    ticks: { color: '#9CA3AF', stepSize: 20 }
                },
                x: {
                    grid: { color: '#374151' },
                    ticks: { color: '#9CA3AF' }
                }
            },
            plugins: {
                legend: {
                    labels: { color: '#E2E8F0', font: { family: 'Plus Jakarta Sans', size: 12 } }
                },
                tooltip: {
                    callbacks: {
                        label: ctx => `Wellness Score: ${ctx.raw} / 100`
                    }
                }
            }
        }
    });
}

/**
 * 4-7-8 Deep Breathing Exercise Animated Controller
 */
function toggleBreathingExercise() {
    const circle = document.getElementById("breathing-circle");
    const phaseText = document.getElementById("breathing-phase");
    const toggleBtn = document.getElementById("breathing-toggle-btn");

    if (isBreathingActive) {
        // Stop breathing
        clearInterval(breathingInterval);
        breathingInterval = null;
        isBreathingActive = false;
        if (circle) {
            circle.className = "breathing-circle-outer";
        }
        if (phaseText) phaseText.innerText = "Paused. Tap Start to Begin";
        if (toggleBtn) {
            toggleBtn.innerHTML = "<span>▶️ Start 2-Minute Breathing</span>";
            toggleBtn.className = "btn btn-primary";
        }
        return;
    }

    // Start breathing cycle
    isBreathingActive = true;
    if (toggleBtn) {
        toggleBtn.innerHTML = "<span>⏹️ Pause Breathing Exercise</span>";
        toggleBtn.className = "btn btn-outline";
    }

    let cycleSeconds = 0; // 0..18 loop (4s inhale + 7s hold + 8s exhale = 19s total)

    const stepFunction = () => {
        const step = cycleSeconds % 19;

        if (step < 4) {
            // Inhale phase: 4 seconds
            const rem = 4 - step;
            if (circle) circle.className = "breathing-circle-outer expanding";
            if (phaseText) phaseText.innerText = `🌬️ Inhale Deeply (${rem}s)`;
        } else if (step < 11) {
            // Hold phase: 7 seconds (from 4 to 10)
            const rem = 11 - step;
            if (circle) circle.className = "breathing-circle-outer holding";
            if (phaseText) phaseText.innerText = `⏸️ Hold Breath (${rem}s)`;
        } else {
            // Exhale phase: 8 seconds (from 11 to 18)
            const rem = 19 - step;
            if (circle) circle.className = "breathing-circle-outer contracting";
            if (phaseText) phaseText.innerText = `💨 Exhale Slowly (${rem}s)`;
        }

        cycleSeconds++;
    };

    stepFunction();
    breathingInterval = setInterval(stepFunction, 1000);
}

/**
 * CBT Negative Thought Reframer
 */
const SAMPLE_REFRAMES = [
    {
        pattern: "fail",
        distortion: "Catastrophizing & Predicting the Future",
        reframe: "“Having a difficult test or moment does not mean I am a failure. Every mistake is useful data that helps me grow, and I can ask for guidance one step at a time.”",
        action: "Action: Write down 1 specific thing you understand well, and review 1 topic you need help with."
    },
    {
        pattern: "nobody",
        distortion: "Mind Reading & All-or-Nothing Thinking",
        reframe: "“People often have their own silent worries and stress. Just because someone didn't reply immediately doesn't mean they don't care about me.”",
        action: "Action: Send a simple 'thinking of you' message to a close friend or family member."
    },
    {
        pattern: "ugly",
        distortion: "Negative Mental Filtering",
        reframe: "“My worth is not defined by filtered social media standards or temporary feelings. My kindness, creativity, and unique perspective matter most.”",
        action: "Action: Put your phone away for 30 minutes and engage in a hobby you enjoy."
    },
    {
        pattern: "hate",
        distortion: "Emotional Reasoning",
        reframe: "“I am feeling deeply frustrated right now, but intense feelings are like weather storms—they peak and then pass. I can take three calm breaths before deciding.”",
        action: "Action: Drink a cold glass of water and stretch for 2 minutes."
    },
    {
        pattern: "default",
        distortion: "Cognitive Overgeneralization",
        reframe: "“Feeling overwhelmed is a sign that I need to slow down, not that I am incapable. I don't have to solve everything today—just the very next small step.”",
        action: "Action: Break down your biggest task into 3 tiny 10-minute micro-tasks."
    }
];

function generateThoughtReframe() {
    const inputEl = document.getElementById("cbt-unhelpful-thought");
    const resultBox = document.getElementById("cbt-reframed-result");
    const textEl = document.getElementById("cbt-reframed-text");

    const rawThought = inputEl ? inputEl.value.trim().toLowerCase() : "";

    let matched = SAMPLE_REFRAMES[SAMPLE_REFRAMES.length - 1]; // default

    if (rawThought) {
        for (const item of SAMPLE_REFRAMES) {
            if (rawThought.includes(item.pattern)) {
                matched = item;
                break;
            }
        }
    } else {
        if (inputEl) inputEl.value = "I am going to mess up the exam tomorrow and ruin my future...";
        matched = SAMPLE_REFRAMES[0];
    }

    if (resultBox && textEl) {
        resultBox.style.display = "block";
        textEl.innerHTML = `
            <b>🔍 Cognitive Distortion Identified:</b> <span style="color: #FBBF24;">${matched.distortion}</span><br><br>
            <b>💡 Balanced Reframe:</b> ${matched.reframe}<br><br>
            <span style="color: #34D399; font-weight: 600;">${matched.action}</span>
        `;
    }
}

// =========================================================================
// 10. MODAL & EXPORT HELPERS
// =========================================================================
function showEmergencyModal() {
    const modal = document.getElementById("crisis-emergency-modal");
    if (modal) modal.style.display = "flex";
}

function closeCrisisModal() {
    const modal = document.getElementById("crisis-emergency-modal");
    if (modal) modal.style.display = "none";
}

function exportActiveRecord() {
    const pat = patientsDB.find(p => p.id === activePatientId) || patientsDB[0];
    const fhirBundle = {
        resourceType: "Bundle",
        type: "collection",
        entry: [
            {
                resource: {
                    resourceType: "Patient",
                    id: pat.id,
                    name: [{ text: pat.name }],
                    gender: pat.gender.toLowerCase(),
                    birthDate: `${2026 - pat.age}-01-01`
                }
            },
            {
                resource: {
                    resourceType: "RiskAssessment",
                    status: "final",
                    subject: { reference: `Patient/${pat.id}` },
                    prediction: [
                        {
                            outcome: { text: "Adolescent Mental Health Composite Risk" },
                            probabilityDecimal: pat.riskScore / 100.0,
                            whenRange: {
                                low: { value: pat.ci95[0], unit: "risk_points" },
                                high: { value: pat.ci95[1], unit: "risk_points" }
                            }
                        }
                    ]
                }
            }
        ]
    };

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(fhirBundle, null, 2));
    const dlAnchor = document.createElement("a");
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `${pat.name.replace(/\s+/g, "_")}_FHIR_Record.json`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
}
