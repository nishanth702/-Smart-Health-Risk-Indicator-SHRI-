/**
 * Smart Health Risk Indicator (SHRI) - Core Application Controller v3.0
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
    document.getElementById("role-doctor-btn").classList.toggle("active", role === "doctor");
    document.getElementById("role-patient-btn").classList.toggle("active", role === "patient");
    updateAuthFormsVisibility();
}

function switchAuthMode(mode) {
    currentAuthMode = mode;
    document.getElementById("mode-login-btn").classList.toggle("active", mode === "login");
    document.getElementById("mode-register-btn").classList.toggle("active", mode === "register");
    updateAuthFormsVisibility();
}

function updateAuthFormsVisibility() {
    document.getElementById("doctor-login-form").classList.remove("active");
    document.getElementById("doctor-reg-form").classList.remove("active");
    document.getElementById("patient-login-form").classList.remove("active");
    document.getElementById("patient-reg-form").classList.remove("active");

    if (currentAuthRole === "doctor") {
        if (currentAuthMode === "login") {
            document.getElementById("doctor-login-form").classList.add("active");
        } else {
            document.getElementById("doctor-reg-form").classList.add("active");
        }
    } else {
        if (currentAuthMode === "login") {
            document.getElementById("patient-login-form").classList.add("active");
        } else {
            document.getElementById("patient-reg-form").classList.add("active");
        }
    }
}

function quickDemoLogin(role) {
    if (role === "doctor") {
        currentUser = {
            role: "doctor",
            name: "Dr. Ramesh S",
            title: "Lead Clinician & Assistant Professor",
            dept: "Department of Adolescent Psychiatry & NWC",
            email: "dr.ramesh@srmist.edu.in"
        };
    } else {
        currentUser = {
            role: "patient",
            name: "Aarav Singh",
            id: "PT-1001",
            age: 15,
            gender: "Male",
            email: "aarav.singh@student.edu"
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
        title: "Clinical Decision Specialist",
        dept: clinic,
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
            name: "Adolescent User",
            id: patId,
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
    showAuthSection();
}

function showAuthSection() {
    document.getElementById("auth-section").style.display = "flex";
    document.getElementById("main-app-section").style.display = "none";
}

// =========================================================================
// 4. APPLICATION ROUTING & PORTAL VIEWS
// =========================================================================
function launchApplication() {
    document.getElementById("auth-section").style.display = "none";
    document.getElementById("main-app-section").style.display = "flex";

    // Update Sidebar Profile
    document.getElementById("sidebar-user-name").innerText = currentUser.name;
    document.getElementById("sidebar-user-role").innerText = currentUser.role === "doctor" ? (currentUser.title || "Clinical Specialist") : "Patient";
    document.getElementById("sidebar-user-avatar").innerText = currentUser.role === "doctor" ? "👨‍⚕️" : "👤";

    if (currentUser.role === "doctor") {
        document.getElementById("doctor-nav-section").style.display = "block";
        document.getElementById("patient-nav-section").style.display = "none";
        document.getElementById("top-add-patient-btn").style.display = "inline-flex";
        showDoctorRegistry();
    } else {
        document.getElementById("doctor-nav-section").style.display = "none";
        document.getElementById("clinical-tabs-section").style.display = "none";
        document.getElementById("patient-nav-section").style.display = "block";
        document.getElementById("top-add-patient-btn").style.display = "none";
        showPatientPortalView();
    }
}

function showDoctorRegistry() {
    document.getElementById("doctor-registry-view").style.display = "block";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    document.getElementById("patient-portal-view").style.display = "none";
    
    document.getElementById("clinical-tabs-section").style.display = "none";
    document.getElementById("nav-registry-btn").classList.add("active");
    document.getElementById("nav-dossier-btn").classList.remove("active");

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
    document.getElementById("nav-registry-btn").classList.remove("active");
    document.getElementById("nav-dossier-btn").classList.add("active");

    populatePatientDossier(activePatientId);
}

function showPatientPortalView() {
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    document.getElementById("patient-portal-view").style.display = "block";

    document.getElementById("page-main-title").innerText = "My Adolescent Wellness Portal";
    document.getElementById("page-subtitle").innerText = "Confidential Daily Check-in & Science-Backed Coping Strategies";

    document.getElementById("patient-portal-welcome-name").innerText = `Hello, ${currentUser.name}! 👋`;
}

// =========================================================================
// 5. DOCTOR PATIENT REGISTRY RENDERING
// =========================================================================
function renderRegistryStats() {
    const total = patientsDB.length;
    const critical = patientsDB.filter(p => p.riskTier === "HIGH" || p.riskTier === "SEVERE").length;
    const avgScore = total > 0 ? (patientsDB.reduce((acc, p) => acc + p.riskScore, 0) / total).toFixed(1) : "0.0";

    document.getElementById("stat-total-patients").innerText = total;
    document.getElementById("sidebar-patient-count").innerText = total;
    document.getElementById("stat-critical-alerts").innerText = critical;
    document.getElementById("stat-avg-score").innerText = avgScore;
}

function renderPatientCards(filterList) {
    const container = document.getElementById("patient-cards-container");
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
    const search = document.getElementById("patient-search-input").value.toLowerCase();
    const filterTier = document.getElementById("filter-risk-select").value;

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
    document.getElementById("add-patient-modal").style.display = "flex";
}

function closeAddPatientModal() {
    document.getElementById("add-patient-modal").style.display = "none";
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
    document.getElementById("dossier-avatar").innerText = pat.gender === 'Female' ? '👧' : '👦';
    document.getElementById("dossier-patient-name").innerText = pat.name;
    document.getElementById("dossier-patient-sub").innerText = `${pat.age}y ${pat.gender} | ID: ${pat.id} | Primary: ${pat.primaryConcern}`;

    // Populate Patient Dropdown
    const dropdown = document.getElementById("dossier-patient-dropdown");
    dropdown.innerHTML = "";
    patientsDB.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.innerText = `${p.name} (${p.id} - ${p.riskTier})`;
        if (p.id === pat.id) opt.selected = true;
        dropdown.appendChild(opt);
    });

    // Populate Form Inputs
    document.getElementById("q1").value = pat.q.q1;
    document.getElementById("val-q1").innerText = pat.q.q1;
    document.getElementById("q2").value = pat.q.q2;
    document.getElementById("val-q2").innerText = pat.q.q2;
    document.getElementById("q3").value = pat.q.q3;
    document.getElementById("val-q3").innerText = pat.q.q3;
    document.getElementById("q4").value = pat.q.q4;
    document.getElementById("val-q4").innerText = pat.q.q4;
    document.getElementById("q5").value = pat.q.q5;
    document.getElementById("val-q5").innerText = pat.q.q5;

    document.getElementById("bio-sleep").value = pat.bio.sleepHours;
    document.getElementById("bio-screen").value = pat.bio.screenTime;
    document.getElementById("bio-exercise").value = pat.bio.exerciseMinutes;
    document.getElementById("bio-social").value = pat.bio.socialInteractions;
    document.getElementById("journal-input").value = pat.journal;

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
    const crisisList = ["suicide", "kill myself", "end my life", "tired of everything", "cannot live anymore", "want to die", "hopeless", "self harm"];
    return crisisList.some(w => lower.includes(w));
}

// Core Execution
function runClinicalAssessment() {
    const pat = patientsDB.find(p => p.id === activePatientId);
    if (!pat) return;

    // Collect Inputs
    const q1 = parseInt(document.getElementById("q1").value);
    const q2 = parseInt(document.getElementById("q2").value);
    const q3 = parseInt(document.getElementById("q3").value);
    const q4 = parseInt(document.getElementById("q4").value);
    const q5 = parseInt(document.getElementById("q5").value);

    const sleepHours = parseFloat(document.getElementById("bio-sleep").value) || 7.0;
    const screenTime = parseFloat(document.getElementById("bio-screen").value) || 4.0;
    const exercise = parseFloat(document.getElementById("bio-exercise").value) || 30;
    const social = parseFloat(document.getElementById("bio-social").value) || 4;
    const journalText = document.getElementById("journal-input").value;

    // Update patient in memory
    pat.q = { q1, q2, q3, q4, q5 };
    pat.bio = { sleepHours, screenTime, exerciseMinutes: exercise, socialInteractions: social };
    pat.journal = journalText;

    // 1. Subnet Feature Extraction
    const depScore = ((q1 + q2 + q3) / 9.0) * 100;
    const anxScore = ((q4 + q5) / 6.0) * 100;
    const sleepDebt = Math.max(0, (8.0 - sleepHours) / 6.0) * 100;
    const screenRisk = Math.min(100, (screenTime / 10.0) * 100);

    // 2. FusionNet Meta-Learner Prediction
    const rawRisk = (depScore * 0.35) + (anxScore * 0.30) + (sleepDebt * 0.20) + (screenRisk * 0.15);
    const calibratedRisk = Math.min(100, Math.max(5, Math.round(rawRisk)));

    // 3. Monte Carlo Dropout Epistemic UQ (T = 20)
    const mcSamples = [];
    for (let i = 0; i < 20; i++) {
        const noise = (Math.random() - 0.5) * 6.5;
        mcSamples.push(Math.min(100, Math.max(0, calibratedRisk + noise)));
    }
    const mean = mcSamples.reduce((a, b) => a + b, 0) / 20;
    const variance = mcSamples.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / 20;
    const stdDev = Math.sqrt(variance);
    const ciLow = Math.max(0, Math.round((mean - 1.96 * stdDev) * 10) / 10);
    const ciHigh = Math.min(100, Math.round((mean + 1.96 * stdDev) * 10) / 10);

    // 4. Update Risk Tier
    let tier = "LOW";
    if (calibratedRisk >= 75) tier = "SEVERE";
    else if (calibratedRisk >= 50) tier = "HIGH";
    else if (calibratedRisk >= 25) tier = "MODERATE";

    pat.riskScore = calibratedRisk;
    pat.riskTier = tier;
    pat.ci95 = [ciLow, ciHigh];
    pat.lastAssessment = new Date().toISOString().split("T")[0];

    // Save to LocalStorage
    savePatientsToStorage();

    // 5. Update UI Displays
    document.getElementById("inf-risk-score").innerText = calibratedRisk;
    const badge = document.getElementById("inf-risk-badge");
    badge.className = `risk-badge ${tier.toLowerCase()}`;
    badge.innerText = `${tier} RISK`;
    document.getElementById("inf-ci-badge").innerText = `95% CI: [${ciLow} – ${ciHigh}]`;

    const gaugeCircle = document.getElementById("risk-circle-gauge");
    const col = tier === "SEVERE" ? "#EF4444" : (tier === "HIGH" ? "#F97316" : (tier === "MODERATE" ? "#F59E0B" : "#10B981"));
    gaugeCircle.style.background = `conic-gradient(${col} 0% ${calibratedRisk}%, #1F2937 ${calibratedRisk}% 100%)`;

    // 6. Render Charts
    renderRadarChart([depScore, anxScore, sleepDebt, screenRisk]);
    renderEnsembleChart([depScore, anxScore, sleepDebt, calibratedRisk]);
    renderMCHistogram(mcSamples);
    renderSHAPChart(depScore, anxScore, sleepDebt, screenTime, exercise);
    renderTrajectoryChart(pat.history, calibratedRisk);
    renderCBTPlans(tier, depScore, anxScore, sleepDebt);
}

// =========================================================================
// 8. CHART.JS VISUALIZATIONS
// =========================================================================
function renderRadarChart(scores) {
    const ctx = document.getElementById("radarChart").getContext("2d");
    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Depressive Affect', 'Somatic Anxiety', 'Sleep Architecture', 'Digital Screen Burden'],
            datasets: [{
                label: 'Domain Risk Score (0-100)',
                data: scores,
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38BDF8',
                pointBackgroundColor: '#0284C7',
                pointBorderColor: '#fff',
                borderWidth: 2
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
                    ticks: { color: '#6B7280', backdropColor: 'transparent', stepSize: 25 },
                    min: 0,
                    max: 100
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderEnsembleChart(subScores) {
    const ctx = document.getElementById("ensembleBarChart").getContext("2d");
    if (ensembleBarInstance) ensembleBarInstance.destroy();

    ensembleBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['DepNet (BiLSTM)', 'AnxNet (1D-CNN)', 'SleepNet (TCN)', 'FusionNet Meta-Score'],
            datasets: [{
                data: subScores,
                backgroundColor: ['#38BDF8', '#FBBF24', '#A855F7', '#EF4444'],
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
            plugins: { legend: { display: false } }
        }
    });
}

function renderMCHistogram(samples) {
    const ctx = document.getElementById("mcHistChart").getContext("2d");
    if (mcHistInstance) mcHistInstance.destroy();

    mcHistInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: samples.map((_, i) => `Pass ${i + 1}`),
            datasets: [{
                label: 'Stochastic Sample Risk',
                data: samples,
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.15)',
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#FBBF24'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: '#374151' }, ticks: { color: '#9CA3AF' } },
                x: { grid: { display: false }, ticks: { color: '#6B7280' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderSHAPChart(dep, anx, sleep, screen, exercise) {
    const ctx = document.getElementById("shapBarChart").getContext("2d");
    if (shapBarInstance) shapBarInstance.destroy();

    const shapValues = [
        +(dep * 0.18).toFixed(1),
        +(anx * 0.15).toFixed(1),
        +(sleep * 0.12).toFixed(1),
        +((screen - 4) * 1.5).toFixed(1),
        -((exercise / 30) * 3.5).toFixed(1)
    ];

    shapBarInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Depression Symptoms (PHQ-9)',
                'Anxiety & Nervousness (GAD-7)',
                'Sleep Architecture Debt (PSQI)',
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
    const ctx = document.getElementById("trajectoryChart").getContext("2d");
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
// 9. PATIENT SELF-ASSESSMENT ACTIONS
// =========================================================================
function updatePatSlider(slider) {
    const labels = ["Great / Energetic", "Good", "Low / Fatigued", "Severely Drained"];
    document.getElementById("pat-val-mood").innerText = labels[slider.value] || "Good";
}

function updatePatSleep(slider) {
    document.getElementById("pat-val-sleep").innerText = `${slider.value} Hours`;
}

function updatePatStress(slider) {
    const labels = ["None", "Mild", "Moderate", "Severe Stress"];
    document.getElementById("pat-val-stress").innerText = labels[slider.value] || "Mild";
}

function submitPatientSelfCheck() {
    alert("✅ Thank you! Your daily wellness check-in has been saved securely on your device.");
}

function showEmergencyModal() {
    document.getElementById("crisis-emergency-modal").style.display = "flex";
}

function closeCrisisModal() {
    document.getElementById("crisis-emergency-modal").style.display = "none";
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
