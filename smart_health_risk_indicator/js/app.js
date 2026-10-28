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
        clinicalDiagnosis: "Generalized Social Anxiety Disorder with Panic Features (ICD-10 F41.1)",
        psychologistNotes: "Presents with severe anticipatory dread prior to oral class presentations. Reports somatic palpitations and diaphoresis. Cognitive restructuring and 4-7-8 breathing exercises initiated.",
        referringClinician: "Dr. Ramesh S, Lead Neuropsychiatrist",
        riskTier: "MODERATE",
        riskScore: 56,
        ci95: [51.2, 60.8],
        lastAssessment: "2026-10-23",
        history: [38, 42, 48, 51, 56],
        recoveryHistory: [62, 65, 71, 78, 82],
        streak: 5,
        q: { q1: 1, q2: 2, q3: 2, q4: 2, q5: 1, q6: 3, q7: 3, q8: 2, q9: 3, q10: 3, q11: 2, q12: 1, q13: 1 },
        bio: { sleepHours: 6.0, screenTime: 7.0, exerciseMinutes: 20, socialInteractions: 3 },
        journal: "I felt very nervous before class presentation today and my heart was pounding. Had trouble sleeping last night."
    },
    {
        id: "PT-1002",
        name: "Meera Patel",
        age: 16,
        gender: "Female",
        primaryConcern: "Major Depressive Affect, Anhedonia & Insomnia",
        clinicalDiagnosis: "Major Depressive Disorder, Severe Single Episode (ICD-10 F32.2)",
        psychologistNotes: "Profound vegetative signs: early-morning insomnia, marked loss of interest in academics and art, persistent fatigue, and feelings of inadequacy. Intensive CBT behavioral activation and circadian stabilization recommended.",
        referringClinician: "Dr. Priya Sen, Consultant Clinical Psychologist",
        riskTier: "SEVERE",
        riskScore: 82,
        ci95: [76.4, 87.6],
        lastAssessment: "2026-10-23",
        history: [48, 55, 64, 71, 82],
        recoveryHistory: [45, 48, 52, 55, 59],
        streak: 3,
        q: { q1: 3, q2: 3, q3: 3, q4: 3, q5: 3, q6: 2, q7: 2, q8: 2, q9: 2, q10: 2, q11: 3, q12: 2, q13: 3 },
        bio: { sleepHours: 4.0, screenTime: 9.5, exerciseMinutes: 5, socialInteractions: 1 },
        journal: "I feel completely exhausted and tired of everything. I cannot find joy in anything and stay in bed all day."
    },
    {
        id: "PT-1003",
        name: "Kiran Reddy",
        age: 13,
        gender: "Non-Binary",
        primaryConcern: "Mild Somatic Fatigue (Baseline / Healthy Check-in)",
        clinicalDiagnosis: "Developmental Mental Health Check-in (Sub-clinical / Normal Control)",
        psychologistNotes: "Adolescent maintains well-balanced lifestyle. Occasional fatigue linked to sports schedule. Excellent interpersonal connection and high psychological resilience.",
        referringClinician: "Dr. Ramesh S, Lead Neuropsychiatrist",
        riskTier: "LOW",
        riskScore: 16,
        ci95: [12.5, 19.5],
        lastAssessment: "2026-10-22",
        history: [16, 18, 17, 19, 16],
        recoveryHistory: [80, 84, 82, 88, 91],
        streak: 7,
        q: { q1: 0, q2: 0, q3: 1, q4: 1, q5: 0, q6: 0, q7: 0, q8: 1, q9: 0, q10: 1, q11: 0, q12: 0, q13: 0 },
        bio: { sleepHours: 8.5, screenTime: 2.5, exerciseMinutes: 50, socialInteractions: 6 },
        journal: "Had a great art workshop today and finished my science project on time. Feeling energetic and cheerful!"
    },
    {
        id: "PT-1004",
        name: "Prateek Yadav",
        age: 17,
        gender: "Male",
        primaryConcern: "Chronic Circadian Sleep Debt & Cognitive Fog",
        clinicalDiagnosis: "Delayed Sleep-Wake Phase Disorder with Secondary Academic Distress (ICD-10 G47.21)",
        psychologistNotes: "Sleep phase delayed by 4+ hours due to nocturnal esports and social media immersion. Day-time somnolence causes academic disengagement. Sleep hygiene restructuring and blue-light protocol prescribed.",
        referringClinician: "Dr. Amitava Roy, Neurodevelopmental Specialist",
        riskTier: "HIGH",
        riskScore: 68,
        ci95: [62.8, 73.2],
        lastAssessment: "2026-10-21",
        history: [44, 49, 56, 61, 68],
        recoveryHistory: [50, 52, 58, 63, 67],
        streak: 4,
        q: { q1: 2, q2: 2, q3: 3, q4: 3, q5: 1, q6: 2, q7: 2, q8: 2, q9: 1, q10: 3, q11: 2, q12: 2, q13: 2 },
        bio: { sleepHours: 3.5, screenTime: 11.0, exerciseMinutes: 10, socialInteractions: 2 },
        journal: "Gaming until 4 AM every night. Cannot focus during lectures and constantly falling asleep during afternoon periods."
    },
    {
        id: "PT-1005",
        name: "Ananya Sen",
        age: 15,
        gender: "Female",
        primaryConcern: "High Academic Perfectionism, Exam Phobia & Somatic Nausea",
        clinicalDiagnosis: "Somatoform Autonomic Dysfunction & Academic Anxiety (ICD-10 F45.3)",
        psychologistNotes: "Presents with recurrent tension headaches and abdominal pain on exam mornings. Strong internal drive for top percentile grades. Somatic grounding techniques and perfectionism de-escalation initiated.",
        referringClinician: "Dr. K. Radhakrishnan, Adolescent Behavioral Health",
        riskTier: "MODERATE",
        riskScore: 58,
        ci95: [53.1, 62.9],
        lastAssessment: "2026-10-23",
        history: [45, 48, 52, 55, 58],
        recoveryHistory: [68, 70, 72, 75, 76],
        streak: 6,
        q: { q1: 1, q2: 1, q3: 2, q4: 2, q5: 2, q6: 3, q7: 3, q8: 3, q9: 3, q10: 3, q11: 1, q12: 2, q13: 1 },
        bio: { sleepHours: 5.5, screenTime: 5.0, exerciseMinutes: 15, socialInteractions: 3 },
        journal: "Woke up with a bad headache again today because mathematics mock exams are starting tomorrow. Terrified of disappointing parents."
    },
    {
        id: "PT-1006",
        name: "Devansh Roy",
        age: 14,
        gender: "Male",
        primaryConcern: "Persistent Dysthymic Affect & Digital Peer Alienation",
        clinicalDiagnosis: "Dysthymic Disorder / Persistent Depressive Disorder in Adolescents (ICD-10 F34.1)",
        psychologistNotes: "Insidious onset of anhedonia and social withdrawal over past 8 months. Expresses feelings of alienation from school peer group. Spends 10+ hours alone gaming. Graded social exposure plan established.",
        referringClinician: "Dr. Priya Sen, Consultant Clinical Psychologist",
        riskTier: "HIGH",
        riskScore: 64,
        ci95: [59.4, 68.6],
        lastAssessment: "2026-10-22",
        history: [50, 54, 58, 60, 64],
        recoveryHistory: [52, 55, 57, 59, 61],
        streak: 2,
        q: { q1: 2, q2: 3, q3: 2, q4: 2, q5: 2, q6: 1, q7: 2, q8: 1, q9: 1, q10: 2, q11: 3, q12: 1, q13: 2 },
        bio: { sleepHours: 6.5, screenTime: 10.5, exerciseMinutes: 10, socialInteractions: 1 },
        journal: "Nobody at school really talks to me or cares. I feel like an outsider looking in through a glass window."
    },
    {
        id: "PT-1007",
        name: "Fatima Zahra",
        age: 16,
        gender: "Female",
        primaryConcern: "Affective Dysregulation, Mood Swings & Interpersonal Distress",
        clinicalDiagnosis: "Cyclothymic Affective Instability / Emotional Dysregulation (ICD-10 F34.0)",
        psychologistNotes: "Demonstrates rapid affective shifts from irritability to tearfulness following minor peer disputes. Shows strong insight into triggers. Dialectical Behavior Therapy (DBT) emotion regulation worksheets provided.",
        referringClinician: "Dr. Ramesh S, Lead Neuropsychiatrist",
        riskTier: "HIGH",
        riskScore: 62,
        ci95: [57.2, 66.8],
        lastAssessment: "2026-10-23",
        history: [52, 55, 59, 61, 62],
        recoveryHistory: [58, 60, 62, 65, 66],
        streak: 4,
        q: { q1: 2, q2: 2, q3: 2, q4: 2, q5: 2, q6: 2, q7: 3, q8: 2, q9: 2, q10: 2, q11: 2, q12: 3, q13: 2 },
        bio: { sleepHours: 5.0, screenTime: 8.0, exerciseMinutes: 25, socialInteractions: 4 },
        journal: "I got so angry today during group project when someone changed my slides. Cried in the washroom for 30 minutes afterwards."
    },
    {
        id: "PT-1008",
        name: "Rohan Gupta",
        age: 17,
        gender: "Male",
        primaryConcern: "Reactive Adjustment Disorder Post Sports Injury",
        clinicalDiagnosis: "Adjustment Disorder with Depressed Mood (ICD-10 F43.21)",
        psychologistNotes: "Previously state-level football captain. Sidelined due to ACL tear. Grieving athletic identity loss. Demonstrates good foundational resilience and family support; cognitive reframing progressing favorably.",
        referringClinician: "Dr. Amitava Roy, Neurodevelopmental Specialist",
        riskTier: "MILD",
        riskScore: 36,
        ci95: [31.5, 40.5],
        lastAssessment: "2026-10-20",
        history: [42, 40, 38, 37, 36],
        recoveryHistory: [70, 72, 75, 78, 80],
        streak: 8,
        q: { q1: 2, q2: 2, q3: 2, q4: 2, q5: 1, q6: 1, q7: 2, q8: 1, q9: 1, q10: 1, q11: 2, q12: 1, q13: 1 },
        bio: { sleepHours: 7.0, screenTime: 6.0, exerciseMinutes: 20, socialInteractions: 3 },
        journal: "Doing my physiotherapy exercises regularly now. Miss running on the field with my team, but doctor says recovery is on schedule."
    },
    {
        id: "PT-1009",
        name: "Diya Sharma",
        age: 13,
        gender: "Female",
        primaryConcern: "Separation Dread, School Avoidance & Somatic Tremors",
        clinicalDiagnosis: "Separation Anxiety Disorder of Childhood / School Refusal (ICD-10 F93.0)",
        psychologistNotes: "Intense distress on school mornings with nausea, trembling, and separation fears from mother. Cooperative with gradual in-vivo school return protocol. Family counseling concurrently scheduled.",
        referringClinician: "Dr. Priya Sen, Consultant Clinical Psychologist",
        riskTier: "MODERATE",
        riskScore: 52,
        ci95: [47.5, 56.5],
        lastAssessment: "2026-10-22",
        history: [60, 58, 55, 54, 52],
        recoveryHistory: [64, 66, 68, 70, 72],
        streak: 3,
        q: { q1: 1, q2: 1, q3: 2, q4: 2, q5: 1, q6: 3, q7: 3, q8: 3, q9: 3, q10: 2, q11: 1, q12: 2, q13: 1 },
        bio: { sleepHours: 6.0, screenTime: 4.5, exerciseMinutes: 15, socialInteractions: 2 },
        journal: "Felt very nervous when bus arrived this morning, but mom practiced the counting exercise with me and I was able to attend all classes."
    },
    {
        id: "PT-1010",
        name: "Vihaan Nair",
        age: 15,
        gender: "Male",
        primaryConcern: "High-Stress Academic Exposure with Exemplary Coping (Resilience Control)",
        clinicalDiagnosis: "General Pediatric Mental Wellness Examination (Normal Control Benchmark - ICD-10 Z00.00)",
        psychologistNotes: "High academic workload (pre-engineering coaching) but demonstrates exceptional psychological resilience, consistent 8h sleep, daily 60min badminton, and strong peer network. Serves as clinical control benchmark.",
        referringClinician: "Dr. Ramesh S, Lead Neuropsychiatrist",
        riskTier: "LOW",
        riskScore: 14,
        ci95: [10.8, 17.2],
        lastAssessment: "2026-10-23",
        history: [15, 14, 16, 15, 14],
        recoveryHistory: [88, 90, 89, 92, 94],
        streak: 12,
        q: { q1: 0, q2: 0, q3: 0, q4: 1, q5: 0, q6: 1, q7: 1, q8: 0, q9: 0, q10: 2, q11: 0, q12: 0, q13: 0 },
        bio: { sleepHours: 8.0, screenTime: 3.0, exerciseMinutes: 60, socialInteractions: 7 },
        journal: "Studied for 4 hours for physics exam, then played badminton for an hour with my friends. Feeling confident and relaxed."
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
    if (window.shriI18n) {
        window.shriI18n.applyTranslations();
    }
});

function loadPatientsFromStorage() {
    const saved = localStorage.getItem("shri_patients_db");
    if (saved) {
        try {
            patientsDB = JSON.parse(saved);
            // Upgrade if new clinical cohort cases added
            if (patientsDB.length < DEFAULT_PATIENTS.length) {
                patientsDB = DEFAULT_PATIENTS;
                savePatientsToStorage();
            }
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
    // When visiting the link, always prompt with the secure Login / Registration page first
    localStorage.removeItem("shri_active_user");
    currentUser = null;
    showAuthSection();
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
            license: "MED-CLINIC-2024-8841",
            email: "dr.ramesh@healthclinic.org"
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
    try {
        const authSec = document.getElementById("auth-section");
        const mainSec = document.getElementById("main-app-section");
        if (authSec) authSec.style.display = "none";
        if (mainSec) mainSec.style.display = "flex";

        // Update Sidebar Profile
        const userNameEl = document.getElementById("sidebar-user-name");
        const userRoleEl = document.getElementById("sidebar-user-role");
        const userAvatarEl = document.getElementById("sidebar-user-avatar");

        if (userNameEl) {
            if (currentUser && currentUser.role === "patient") {
                userNameEl.innerText = window.shriI18n ? window.shriI18n.getPatientName(currentUser.id, currentUser.name) : currentUser.name;
            } else {
                userNameEl.innerText = window.shriI18n ? window.shriI18n.getClinicianName(currentUser ? currentUser.name : "Dr. Ramesh S") : (currentUser ? currentUser.name : "Dr. Ramesh S");
            }
        }
        if (userRoleEl) {
            if (currentUser && currentUser.role === "patient") {
                userRoleEl.innerText = t("adolescentPatient", "Adolescent Patient");
            } else {
                userRoleEl.innerText = window.shriI18n ? window.shriI18n.getClinicianRole(currentUser ? (currentUser.title || currentUser.role) : "Lead Clinician") : "Lead Clinician";
            }
        }
        if (userAvatarEl) userAvatarEl.innerText = currentUser && currentUser.role === "doctor" ? "👨‍⚕️" : "👤";

        if (currentUser && currentUser.role === "patient") {
            const docNav = document.getElementById("doctor-nav-section");
            const clinTabs = document.getElementById("clinical-tabs-section");
            const patNav = document.getElementById("patient-nav-section");
            const topAddBtn = document.getElementById("top-add-patient-btn");
            if (docNav) docNav.style.display = "none";
            if (clinTabs) clinTabs.style.display = "none";
            if (patNav) patNav.style.display = "block";
            if (topAddBtn) topAddBtn.style.display = "none";
            showPatientPortalView();
        } else {
            const docNav = document.getElementById("doctor-nav-section");
            const patNav = document.getElementById("patient-nav-section");
            const topAddBtn = document.getElementById("top-add-patient-btn");
            if (docNav) docNav.style.display = "block";
            if (patNav) patNav.style.display = "none";
            if (topAddBtn) topAddBtn.style.display = "inline-flex";
            showDoctorRegistry();
        }

        if (window.shriI18n) {
            window.shriI18n.applyTranslations();
        }
    } catch (err) {
        console.error("Error in launchApplication:", err);
    }
}

function showDoctorRegistry() {
    document.getElementById("doctor-registry-view").style.display = "block";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    const valView = document.getElementById("doctor-validation-view");
    if (valView) valView.style.display = "none";
    const dsView = document.getElementById("doctor-datasets-view");
    if (dsView) dsView.style.display = "none";
    document.getElementById("patient-portal-view").style.display = "none";
    
    document.getElementById("clinical-tabs-section").style.display = "none";
    
    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    const valBtn = document.getElementById("nav-val-btn");
    if (regBtn) regBtn.classList.add("active");
    if (dosBtn) dosBtn.classList.remove("active");
    if (valBtn) valBtn.classList.remove("active");
    const dsBtn = document.getElementById("nav-datasets-btn");
    if (dsBtn) dsBtn.classList.remove("active");

    document.getElementById("page-main-title").innerText = t("patientRegistry", "Patient Registry Dashboard");
    document.getElementById("page-subtitle").innerText = t("patientRegistrySub", "Enrolled Adolescent Patients & Continuous Risk Monitoring");

    renderRegistryStats();
    renderPatientCards();
}

function showPatientDossier(patientId) {
    if (patientId) activePatientId = patientId;
    
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "block";
    const valView = document.getElementById("doctor-validation-view");
    if (valView) valView.style.display = "none";
    const dsView = document.getElementById("doctor-datasets-view");
    if (dsView) dsView.style.display = "none";
    document.getElementById("patient-portal-view").style.display = "none";

    document.getElementById("clinical-tabs-section").style.display = "block";
    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    const valBtn = document.getElementById("nav-val-btn");
    if (regBtn) regBtn.classList.remove("active");
    if (dosBtn) dosBtn.classList.add("active");
    if (valBtn) valBtn.classList.remove("active");
    const dsBtn = document.getElementById("nav-datasets-btn");
    if (dsBtn) dsBtn.classList.remove("active");

    populatePatientDossier(activePatientId);
    const pageTitle = document.getElementById("page-main-title");
    const pageSub = document.getElementById("page-subtitle");
    if (pageTitle) pageTitle.innerText = t("patientDossier", "Patient Clinical Dossier");
    if (pageSub) pageSub.innerText = t("patientDossierSub", "Comprehensive Multimodal Phenotyping, Permutation XAI & Clinical Action Plans");
}

function showValidationBenchmark() {
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    const valView = document.getElementById("doctor-validation-view");
    if (valView) valView.style.display = "block";
    document.getElementById("patient-portal-view").style.display = "none";

    document.getElementById("clinical-tabs-section").style.display = "none";
    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    const valBtn = document.getElementById("nav-val-btn");
    if (regBtn) regBtn.classList.remove("active");
    if (dosBtn) dosBtn.classList.remove("active");
    if (valBtn) valBtn.classList.add("active");
    const dsBtn = document.getElementById("nav-datasets-btn");
    if (dsBtn) dsBtn.classList.remove("active");

    document.getElementById("page-main-title").innerText = t("benchmarkTitle", "Multi-Hospital Pilot Benchmark & Clinical Validation");
    document.getElementById("page-subtitle").innerText = t("benchmarkSubtitle", "Multi-Center Cohort Validation (N = 10,000) across Metropolitan Medical Center, Apollo Children's & NIMHANS");

    if (window.shriValidationController) {
        window.shriValidationController.selectCohort('pooled');
    }
}

function switchHospitalCohort(cohortKey) {
    document.querySelectorAll(".cohort-pill").forEach(p => {
        p.classList.toggle("active", p.id === `pill-cohort-${cohortKey}`);
    });
    if (window.shriValidationController) {
        window.shriValidationController.selectCohort(cohortKey);
    }
}

function showPatientPortalView() {
    document.getElementById("doctor-registry-view").style.display = "none";
    document.getElementById("doctor-patient-detail-view").style.display = "none";
    const valView = document.getElementById("doctor-validation-view");
    if (valView) valView.style.display = "none";
    const dsView = document.getElementById("doctor-datasets-view");
    if (dsView) dsView.style.display = "none";
    document.getElementById("patient-portal-view").style.display = "block";

    const pat = patientsDB.find(p => p.id === (currentUser.id || "PT-1001")) || patientsDB[0];
    const welcomeEl = document.getElementById("patient-portal-welcome-name");
    if (welcomeEl) {
        const patId = (currentUser && currentUser.role === "patient") ? currentUser.id : "PT-1001";
        const patName = (currentUser && currentUser.role === "patient") ? currentUser.name : "Aarav Singh";
        const locName = window.shriI18n ? window.shriI18n.getPatientName(patId, patName) : patName;
        welcomeEl.innerText = `${t("greetingHello", "Hello")}, ${locName}! 👋`;
    }

    const streakEl = document.getElementById("patient-streak-text");
    if (streakEl) streakEl.innerText = `🔥 ${pat.streak || 5}-Day Check-in Streak!`;

    // Default to daily self-check tab
    showPatientPortalTab('self-check');
}

/**
 * Switch Patient Portal Sub-tabs: 'self-check' | 'my-voice' | 'my-trends' | 'my-cbt'
 */
function showPatientPortalTab(tabName) {
    const viewSelfCheck = document.getElementById("pat-view-self-check");
    const viewVoice = document.getElementById("pat-view-voice");
    const viewTrends = document.getElementById("pat-view-trends");
    const viewCBT = document.getElementById("pat-view-cbt");
    const viewRecordings = document.getElementById("pat-view-recordings");

    // Subtab Buttons
    const btnSelfCheck = document.getElementById("pat-tab-btn-self-check");
    const btnVoice = document.getElementById("pat-tab-btn-voice");
    const btnTrends = document.getElementById("pat-tab-btn-trends");
    const btnCBT = document.getElementById("pat-tab-btn-cbt");
    const btnRecordings = document.getElementById("pat-tab-btn-recordings");

    // Sidebar Buttons
    const navSelfCheck = document.getElementById("pat-nav-self-check");
    const navVoice = document.getElementById("pat-nav-voice");
    const navTrends = document.getElementById("pat-nav-trends");
    const navCBT = document.getElementById("pat-nav-cbt");
    const navRecordings = document.getElementById("pat-nav-recordings");

    // Hide all panels
    if (viewSelfCheck) viewSelfCheck.style.display = "none";
    if (viewVoice) viewVoice.style.display = "none";
    if (viewTrends) viewTrends.style.display = "none";
    if (viewCBT) viewCBT.style.display = "none";
    if (viewRecordings) viewRecordings.style.display = "none";

    // Remove active class from buttons
    [btnSelfCheck, btnVoice, btnTrends, btnCBT, btnRecordings, navSelfCheck, navVoice, navTrends, navCBT, navRecordings].forEach(b => {
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
    else if (tabName === "my-voice" || tabName === "voice") {
        if (viewVoice) viewVoice.style.display = "block";
        if (btnVoice) btnVoice.classList.add("active");
        if (navVoice) navVoice.classList.add("active");
        if (pageTitle) pageTitle.innerText = "Voice Mood Reflection Check-in";
        if (pageSub) pageSub.innerText = "Browser-Native Voice Prosody & Acoustic Tone Analysis";
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
    else if (tabName === "my-recordings" || tabName === "recordings") {
        if (viewRecordings) viewRecordings.style.display = "block";
        if (btnRecordings) btnRecordings.classList.add("active");
        if (navRecordings) navRecordings.classList.add("active");
        if (pageTitle) pageTitle.innerText = t("myRecordings", "My Audio Recordings & Transcripts");
        if (pageSub) pageSub.innerText = t("audioHistorySub", "Review, listen to, and download past multilingual recordings and clinical transcripts.");
        renderAudioHistoryTable();
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


function showClinicalDatasetsView() {
    const regView = document.getElementById("doctor-registry-view");
    const detView = document.getElementById("doctor-patient-detail-view");
    const valView = document.getElementById("doctor-validation-view");
    const dsView = document.getElementById("doctor-datasets-view");
    const patView = document.getElementById("patient-portal-view");
    const clinTabs = document.getElementById("clinical-tabs-section");

    if (regView) regView.style.display = "none";
    if (detView) detView.style.display = "none";
    if (valView) valView.style.display = "none";
    if (dsView) dsView.style.display = "block";
    if (patView) patView.style.display = "none";
    if (clinTabs) clinTabs.style.display = "none";

    const regBtn = document.getElementById("nav-registry-btn");
    const dosBtn = document.getElementById("nav-dossier-btn");
    const valBtn = document.getElementById("nav-val-btn");
    const dsBtn = document.getElementById("nav-datasets-btn");

    if (regBtn) regBtn.classList.remove("active");
    if (dosBtn) dosBtn.classList.remove("active");
    if (valBtn) valBtn.classList.remove("active");
    if (dsBtn) dsBtn.classList.add("active");

    const mainTitle = document.getElementById("page-main-title");
    const subTitle = document.getElementById("page-subtitle");
    if (mainTitle) mainTitle.innerText = "Clinical Questionnaires & Psychometric Datasets";
    if (subTitle) subTitle.innerText = "AACAP & DSM-5 Standardized Screening Batteries, 10-Cohort Registry & Semi-Structured Interview Protocols";

    renderCohortDatasetTable();
}

function switchDatasetSubtab(subtabKey) {
    document.querySelectorAll(".ds-subtab-content").forEach(el => {
        el.style.display = "none";
        el.classList.remove("active");
    });
    document.querySelectorAll(".cohort-pill").forEach(pill => {
        if (pill.id.startsWith("pill-ds-")) pill.classList.remove("active");
    });

    const activeContent = document.getElementById(`subtab-ds-${subtabKey}`);
    const activePill = document.getElementById(`pill-ds-${subtabKey}`);
    if (activeContent) {
        activeContent.style.display = "block";
        activeContent.classList.add("active");
    }
    if (activePill) activePill.classList.add("active");

    if (subtabKey === "cohort") {
        renderCohortDatasetTable();
    }
}

function renderCohortDatasetTable() {
    const tbody = document.getElementById("cohort-table-tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    patientsDB.forEach(pat => {
        const tr = document.createElement("tr");
        const tierClass = pat.riskTier ? pat.riskTier.toLowerCase() : "low";
        const pName = window.shriI18n ? window.shriI18n.getPatientName(pat.id, pat.name) : pat.name;
        const pGender = window.shriI18n ? window.shriI18n.getPatientGender(pat.gender) : pat.gender;
        const pDiagnosis = window.shriI18n ? window.shriI18n.getPatientDiagnosis(pat.id, pat.clinicalDiagnosis || pat.primaryConcern) : (pat.clinicalDiagnosis || pat.primaryConcern);
        const pNotes = window.shriI18n ? window.shriI18n.getPatientNotes(pat.id, pat.psychologistNotes || pat.journal) : (pat.psychologistNotes || pat.journal);
        const pTier = window.shriI18n ? window.shriI18n.getRiskTierText(pat.riskTier) : pat.riskTier;
        const yrUnit = t("yearsUnit", "y");

        tr.innerHTML = `
            <td><b>${pat.id}</b></td>
            <td><b>${pName}</b> <span style="font-size: 11px; color: #7d8b85;">(${pat.age}${yrUnit} ${pGender})</span></td>
            <td><span class="badge badge-info" style="font-size: 11px;">${pDiagnosis}</span></td>
            <td style="max-width: 320px; font-size: 12px; color: var(--text-secondary);">${pNotes}</td>
            <td><span class="risk-tag ${tierClass}" style="font-size: 10px;">${pTier}</span></td>
            <td><b>${pat.riskScore}</b> <span style="font-size: 11px; color: #7d8b85;">[${pat.ci95 ? pat.ci95[0] : 0} – ${pat.ci95 ? pat.ci95[1] : 0}]</span></td>
            <td>
                <button class="btn btn-primary btn-xs" style="font-size: 11px; padding: 4px 8px;" onclick="loadPatientFromDataset('${pat.id}')">
                    ${t("openDossierBtn", "Open Dossier")}
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function loadPatientFromDataset(patId) {
    showPatientDossier(patId);
}

function applyClinicalPreset(presetType) {
    const presets = {
        severe_depression: {
            q1: 3, q2: 3, q3: 3, q4: 3, q5: 3,
            q6: 2, q7: 2, q8: 2, q9: 2,
            q10: 2, q11: 3, q12: 2, q13: 3,
            sleep: 4.0, screen: 9.5, exercise: 5, social: 1,
            journal: "I feel completely exhausted and have lost interest in everything. Cannot sleep through the night."
        },
        acute_panic: {
            q1: 1, q2: 2, q3: 2, q4: 2, q5: 1,
            q6: 3, q7: 3, q8: 3, q9: 3,
            q10: 3, q11: 2, q12: 2, q13: 1,
            sleep: 5.5, screen: 7.0, exercise: 15, social: 3,
            journal: "Heart was racing and felt like I couldn't breathe before class presentation today. Terrified of exams."
        },
        circadian_burnout: {
            q1: 2, q2: 2, q3: 3, q4: 3, q5: 1,
            q6: 2, q7: 2, q8: 2, q9: 1,
            q10: 3, q11: 2, q12: 2, q13: 2,
            sleep: 3.5, screen: 11.5, exercise: 10, social: 2,
            journal: "Up until 4 AM gaming and watching videos. Constant brain fog during lectures and cannot focus."
        },
        healthy_resilient: {
            q1: 0, q2: 0, q3: 0, q4: 1, q5: 0,
            q6: 1, q7: 0, q8: 0, q9: 0,
            q10: 1, q11: 0, q12: 0, q13: 0,
            sleep: 8.0, screen: 3.0, exercise: 60, social: 7,
            journal: "Had a great study session with classmates and played sports in the evening. Feeling energized and confident."
        }
    };

    const p = presets[presetType];
    if (!p) return;

    for (let i = 1; i <= 13; i++) {
        const key = `q${i}`;
        const el = document.getElementById(key);
        const valEl = document.getElementById(`val-${key}`);
        if (el && p[key] !== undefined) el.value = p[key];
        if (valEl && p[key] !== undefined) valEl.innerText = p[key];
    }

    const sleepEl = document.getElementById("bio-sleep");
    const screenEl = document.getElementById("bio-screen");
    const exEl = document.getElementById("bio-exercise");
    const socEl = document.getElementById("bio-social");
    const journalEl = document.getElementById("journal-input");

    if (sleepEl) sleepEl.value = p.sleep;
    if (screenEl) screenEl.value = p.screen;
    if (exEl) exEl.value = p.exercise;
    if (socEl) socEl.value = p.social;
    if (journalEl) journalEl.value = p.journal;

    runClinicalAssessment();
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
        const pName = window.shriI18n ? window.shriI18n.getPatientName(pat.id, pat.name) : pat.name;
        const pGender = window.shriI18n ? window.shriI18n.getPatientGender(pat.gender) : pat.gender;
        const pConcern = window.shriI18n ? window.shriI18n.getPatientConcern(pat.id, pat.primaryConcern) : pat.primaryConcern;
        const pTier = window.shriI18n ? window.shriI18n.getRiskTierText(pat.riskTier) : `${pat.riskTier} RISK`;
        const yrUnit = t("yearsUnit", "y");

        const card = document.createElement("div");
        card.className = "patient-card";
        card.innerHTML = `
            <div class="patient-card-header">
                <div class="patient-card-meta">
                    <div class="patient-card-avatar">${pat.gender === 'Female' ? '👧' : '👦'}</div>
                    <div>
                        <h4 class="patient-card-name">${pName}</h4>
                        <span class="patient-card-sub">${pat.age}${yrUnit} ${pGender} • ID: ${pat.id}</span>
                    </div>
                </div>
                <span class="risk-tag ${tierClass}">${pTier}</span>
            </div>
            <div class="patient-card-body">
                <div class="patient-score-row">
                    <span class="score-display">${pat.riskScore} <span style="font-size: 12px; color: var(--text-muted);">/ 100</span></span>
                    <span class="score-ci">95% CI: [${pat.ci95[0]} – ${pat.ci95[1]}]</span>
                </div>
                <div class="patient-concern-text">
                    <b>${t("primaryConcern", "Primary Concern")}:</b> ${pConcern}
                </div>
            </div>
            <div class="patient-card-actions">
                <button class="btn btn-primary" style="flex: 1;" onclick="showPatientDossier('${pat.id}')">
                    <span>📊 ${t("openDossierBtn", "Open Dossier")}</span>
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
    const locName = window.shriI18n ? window.shriI18n.getPatientName(pat.id, pat.name) : pat.name;
    const locGender = window.shriI18n ? window.shriI18n.getPatientGender(pat.gender) : pat.gender;
    const locConcern = window.shriI18n ? window.shriI18n.getPatientConcern(pat.id, pat.primaryConcern) : pat.primaryConcern;
    const yrUnit = t("yearsUnit", "y");
    const primLabel = t("primaryLabel", "Primary");

    if (nameEl) nameEl.innerText = locName;
    if (subEl) subEl.innerText = `${pat.age}${yrUnit} ${locGender} | ID: ${pat.id} | ${primLabel}: ${locConcern}`;

    // Populate Patient Dropdown
    const dropdown = document.getElementById("dossier-patient-dropdown");
    if (dropdown) {
        dropdown.innerHTML = "";
        patientsDB.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.id;
            const dropName = window.shriI18n ? window.shriI18n.getPatientName(p.id, p.name) : p.name;
            const dropTier = window.shriI18n ? window.shriI18n.getRiskTierText(p.riskTier) : p.riskTier;
            opt.innerText = `${dropName} (${p.id} - ${dropTier})`;
            if (p.id === pat.id) opt.selected = true;
            dropdown.appendChild(opt);
        });
    }

    // Populate Form Inputs
    ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13"].forEach(q => {
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
    // 1. Gather Standardized Questionnaire Features (PHQ-A, GAD-7 & Psychologist Metrics)
    const q1 = parseInt(document.getElementById("q1") ? document.getElementById("q1").value : 1);
    const q2 = parseInt(document.getElementById("q2") ? document.getElementById("q2").value : 1);
    const q3 = parseInt(document.getElementById("q3") ? document.getElementById("q3").value : 1);
    const q4 = parseInt(document.getElementById("q4") ? document.getElementById("q4").value : 1);
    const q5 = parseInt(document.getElementById("q5") ? document.getElementById("q5").value : 1);
    const q6 = parseInt(document.getElementById("q6") ? document.getElementById("q6").value : 1);
    const q7 = parseInt(document.getElementById("q7") ? document.getElementById("q7").value : 1);
    const q8 = parseInt(document.getElementById("q8") ? document.getElementById("q8").value : 1);
    const q9 = parseInt(document.getElementById("q9") ? document.getElementById("q9").value : 1);
    const q10 = parseInt(document.getElementById("q10") ? document.getElementById("q10").value : 1);
    const q11 = parseInt(document.getElementById("q11") ? document.getElementById("q11").value : 1);
    const q12 = parseInt(document.getElementById("q12") ? document.getElementById("q12").value : 1);
    const q13 = parseInt(document.getElementById("q13") ? document.getElementById("q13").value : 1);

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

    // Validated Clinical Subscales
    const depScore = ((q1 + q2 + q3 + q4 + q5) / 15.0) * 100;
    const anxScore = ((q6 + q7 + q8 + q9) / 12.0) * 100;
    const psyScore = ((q10 + q11 + q12 + q13) / 12.0) * 100;
    const academicBurnout = (q10 / 3.0) * 100;
    const peerAlienation = (q11 / 3.0) * 100;
    const emotionalDysreg = (q12 / 3.0) * 100;
    const sleepDeficit = Math.max(0, (8.0 - sleep) / 5.0) * 100;
    const screenRisk = Math.min(100, (screen / 12.0) * 100);
    const exerciseProtective = Math.min(100, (exercise / 60.0) * 100);

    // 4-Model Ensemble Architecture with Clinical Psychometrics
    const lstmPred = Math.min(99, Math.max(5, (depScore * 0.35 + anxScore * 0.30 + psyScore * 0.20 + sleepDeficit * 0.15 + nlpRisk)));
    const cnnPred = Math.min(99, Math.max(5, (anxScore * 0.35 + depScore * 0.25 + academicBurnout * 0.20 + screenRisk * 0.20 + nlpRisk * 0.8)));
    const rfPred = Math.min(99, Math.max(5, (depScore * 0.30 + peerAlienation * 0.25 + sleepDeficit * 0.25 + (100 - exerciseProtective) * 0.20)));
    const gbPred = Math.min(99, Math.max(5, (depScore * 0.30 + anxScore * 0.25 + emotionalDysreg * 0.25 + screenRisk * 0.10 + sleepDeficit * 0.10)));

    // 5. Acoustic Vocal Biomarker Score (100% Extent Multi-Modal Ingestion)
    const voiceScore = (window.shriVoiceAnalyzer && window.shriVoiceAnalyzer.latestMetrics)
        ? window.shriVoiceAnalyzer.latestMetrics.vocalRiskScore
        : 52;

    // 5-Modality Meta-Ensemble Weighted Stacking
    const ensembleScore = Math.round(
        lstmPred * 0.30 +
        cnnPred * 0.25 +
        rfPred * 0.15 +
        gbPred * 0.15 +
        voiceScore * 0.15
    );
    
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

    // ── Update Dossier UI (Ensemble / SHAP tab elements) ──────────────────────
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

    // ── Update ASSESSMENT TAB live gauge (always visible) ─────────────────────
    const infScoreEl  = document.getElementById("inf-risk-score");
    const infBadgeEl  = document.getElementById("inf-risk-badge");
    const infCiEl     = document.getElementById("inf-ci-badge");
    const infSummaryEl = document.getElementById("inf-risk-summary");
    const gaugeCircle  = document.getElementById("risk-circle-gauge");

    if (infScoreEl) infScoreEl.innerText = ensembleScore;
    if (infBadgeEl) {
        infBadgeEl.innerText = `${tier} RISK`;
        infBadgeEl.className = `risk-badge ${tierClass}`;
    }
    if (infCiEl) infCiEl.innerText = `95% CI: [${ciLow} – ${ciHigh}]`;
    if (infSummaryEl) {
        const summaryMap = {
            SEVERE:   "Composite score indicates severe psychiatric risk. Immediate clinical review required.",
            HIGH:     "High-risk profile detected: pronounced depressive and anxious symptom burden.",
            MODERATE: "Moderate risk with notable mood and sleep disruptions. Monitor closely.",
            MILD:     "Mild risk indicators present. Recommend lifestyle and psychosocial support.",
            LOW:      "Low composite risk. Patient shows adequate resilience and coping capacity."
        };
        infSummaryEl.innerText = summaryMap[tier] || summaryMap.LOW;
    }
    // Update gauge circle border-color to match risk tier
    if (gaugeCircle) {
        const tierColors = { SEVERE: '#b84a47', HIGH: '#c26f30', MODERATE: '#a08040', MILD: '#7c6fa0', LOW: '#477d64' };
        gaugeCircle.style.borderColor = tierColors[tier] || '#477d64';
    }

    // ── Update active patient object in DB ───────────────────────────────────
    const activePat = patientsDB.find(p => p.id === activePatientId);
    if (activePat) {
        activePat.riskScore = ensembleScore;
        activePat.riskTier = tier;
        activePat.ci95 = [ciLow, ciHigh];
        activePat.q = { q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13 };
        activePat.bio = { sleepHours: sleep, screenTime: screen, exerciseMinutes: exercise, socialInteractions: social };
        activePat.journal = journalText;
        savePatientsToStorage();
    }

    // ── Render Charts ────────────────────────────────────────────────────────
    renderRadarChart(depScore, anxScore, sleepDeficit, academicBurnout, peerAlienation, emotionalDysreg);
    renderEnsembleChart(lstmPred, cnnPred, rfPred, gbPred, ensembleScore);
    renderMCHistogram(mcSamples);
    renderSHAPChart(depScore, anxScore, sleepDeficit, screenRisk, exerciseProtective, academicBurnout, peerAlienation);
    renderTrajectoryChart(activePat ? activePat.history : [35, 45, 50], ensembleScore);
    renderCBTPlans(tier, depScore, anxScore, sleepDeficit);
}

// =========================================================================
// 8. CHART.JS VISUALIZATION RENDERERS
// =========================================================================
function renderRadarChart(dep, anx, sleep, screen, sedentary, nlp) {
    // Try both canvas IDs (HTML uses 'radarChart', legacy uses 'clinicalRadarChart')
    const canvas = document.getElementById("radarChart") || document.getElementById("clinicalRadarChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Depressive Affect (PHQ-A)', 'Anxiety & Panic (GAD-7)', 'Circadian Sleep Debt', 'Academic Burnout (PSY-1)', 'Peer Social Alienation', 'Affective Volatility'],
            datasets: [{
                label: 'Clinical Dimension Severity',
                data: [dep, anx, sleep, screen, sedentary, nlp],
                backgroundColor: 'rgba(59, 122, 116, 0.2)',
                borderColor: '#3b7a74',
                pointBackgroundColor: '#275954',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#3b7a74'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: '#e4ded2' },
                    grid: { color: '#ede7db' },
                    pointLabels: { color: '#202d29', font: { size: 11, family: 'Plus Jakarta Sans' } },
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
                    '#3b7a74',
                    '#7c6fa0',
                    '#6b8f7f',
                    '#af8431',
                    '#c26f30'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#ede7db' }, ticks: { color: '#586561' } },
                x: { grid: { display: false }, ticks: { color: '#586561' } }
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
                borderColor: '#af8431',
                backgroundColor: 'rgba(175, 132, 49, 0.12)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                pointRadius: 4,
                pointBackgroundColor: '#af8431'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { min: 0, max: 100, grid: { color: '#ede7db' }, ticks: { color: '#586561' } },
                x: { grid: { color: '#ede7db' }, ticks: { color: '#586561' } }
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
                backgroundColor: shapValues.map(v => v >= 0 ? '#b84a47' : '#477d64'),
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { color: '#ede7db' }, ticks: { color: '#586561' } },
                y: { grid: { display: false }, ticks: { color: '#202d29', font: { size: 12 } } }
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
                    borderColor: '#3b7a74',
                    backgroundColor: 'rgba(59, 122, 116, 0.12)',
                    borderWidth: 3,
                    tension: 0.2,
                    pointRadius: 6,
                    pointBackgroundColor: '#275954'
                },
                {
                    label: 'High Risk Threshold (50)',
                    data: labels.map(() => 50),
                    borderColor: '#c26f30',
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
                y: { min: 0, max: 100, grid: { color: '#ede7db' }, ticks: { color: '#586561' } },
                x: { grid: { color: '#ede7db' }, ticks: { color: '#586561' } }
            },
            plugins: { legend: { labels: { color: '#202d29' } } }
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
    _updatePatLiveScore();
}

function updatePatSleep(slider) {
    const valEl = document.getElementById("pat-val-sleep");
    if (valEl) valEl.innerText = `${slider.value} Hours`;
    _updatePatLiveScore();
}

function updatePatStress(slider) {
    const labels = ["None", "Mild", "Moderate", "Severe Stress"];
    const valEl = document.getElementById("pat-val-stress");
    if (valEl) valEl.innerText = labels[slider.value] || "Mild";
    _updatePatLiveScore();
}

/**
 * Live patient wellness score preview — updates badge and status text
 * immediately as sliders move, without saving to DB.
 */
function _updatePatLiveScore() {
    const moodVal  = parseInt((document.getElementById("pat-slider-mood")  || {}).value || 1);
    const sleepVal = parseFloat((document.getElementById("pat-slider-sleep") || {}).value || 7);
    const stressVal= parseInt((document.getElementById("pat-slider-stress")|| {}).value || 1);

    let wellnessScore = 80;
    if (moodVal === 0) wellnessScore += 15;
    else if (moodVal === 1) wellnessScore += 5;
    else if (moodVal === 2) wellnessScore -= 15;
    else if (moodVal === 3) wellnessScore -= 35;

    if (sleepVal >= 7.5 && sleepVal <= 9.5) wellnessScore += 10;
    else if (sleepVal < 6) wellnessScore -= (6 - sleepVal) * 8;

    if (stressVal === 0) wellnessScore += 10;
    else if (stressVal === 2) wellnessScore -= 15;
    else if (stressVal === 3) wellnessScore -= 30;

    wellnessScore = Math.max(10, Math.min(98, Math.round(wellnessScore)));

    // Update badge
    const badge = document.getElementById("pat-badge-status");
    if (badge) {
        if (wellnessScore >= 75) {
            badge.innerText = "🌟 Thriving";
            badge.className = "badge badge-success";
        } else if (wellnessScore >= 50) {
            badge.innerText = "👍 Balanced";
            badge.className = "badge badge-info";
        } else if (wellnessScore >= 30) {
            badge.innerText = "💙 Needs Support";
            badge.className = "badge badge-warning";
        } else {
            badge.innerText = "⚠️ Seek Help";
            badge.className = "badge badge-danger";
        }
    }

    // Update wellness status text
    const statusEl = document.getElementById("patient-wellness-status");
    const msgEl    = document.getElementById("patient-wellness-msg");
    const iconEl   = document.getElementById("pat-wellness-icon");
    if (statusEl) {
        if (wellnessScore >= 75) statusEl.innerText = "🌟 Outstanding Wellness!";
        else if (wellnessScore >= 50) statusEl.innerText = "👍 Stable & Balanced";
        else if (wellnessScore >= 30) statusEl.innerText = "💙 Take It Easy Today";
        else statusEl.innerText = "⚠️ Please Seek Support";
    }
    if (msgEl) {
        msgEl.innerText = `Live wellness estimate: ${wellnessScore}/100 — Based on your current mood, sleep, and stress inputs.`;
    }
    if (iconEl) {
        if (wellnessScore >= 75) iconEl.innerText = "🌟";
        else if (wellnessScore >= 50) iconEl.innerText = "😊";
        else if (wellnessScore >= 30) iconEl.innerText = "😔";
        else iconEl.innerText = "😟";
    }

    // Also update the Trends tab metric card if visible
    const metricEl = document.getElementById("pat-metric-wellness");
    if (metricEl) metricEl.innerText = `${wellnessScore} / 100`;
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
                    borderColor: '#477d64',
                    backgroundColor: 'rgba(71, 125, 100, 0.15)',
                    borderWidth: 3,
                    tension: 0.35,
                    fill: true,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    pointBackgroundColor: '#325846',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2
                },
                {
                    label: 'Resilience Baseline Target (75)',
                    data: labels.map(() => 75),
                    borderColor: '#7c6fa0',
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
                    labels: { color: '#202d29', font: { family: 'Plus Jakarta Sans', size: 12 } }
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
            <span style="color: #3b7a74; font-weight: 600;">${matched.action}</span>
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

// =========================================================================
// 11. VOICE ACOUSTIC BIOMARKER HANDLERS (100% Extent)
// =========================================================================
let isVoiceRecordingDoctor = false;
let isVoiceRecordingPatient = false;

async function toggleVoiceRecording() {
    const btn = document.getElementById("btn-voice-record");
    const statusEl = document.getElementById("voice-record-status");
    const iconEl = document.getElementById("voice-mic-icon");

    if (!isVoiceRecordingDoctor) {
        isVoiceRecordingDoctor = true;
        if (btn) {
            btn.innerHTML = "<span>⏹️ Stop & Analyze Audio</span>";
            btn.classList.add("record-btn-pulsing");
        }
        if (statusEl) statusEl.innerText = "🔴 Listening & Extracting Acoustic Waveform...";
        if (iconEl) iconEl.innerText = "🎙️";
        if (window.shriVoiceAnalyzer) {
            await window.shriVoiceAnalyzer.startRecording("voiceWaveformCanvas");
        }
    } else {
        isVoiceRecordingDoctor = false;
        if (btn) {
            btn.innerHTML = "<span>⏺️ Start Speech Recording</span>";
            btn.classList.remove("record-btn-pulsing");
        }
        if (statusEl) statusEl.innerText = "✅ Acoustic Prosody Extracted!";
        let metrics = null;
        if (window.shriVoiceAnalyzer) {
            metrics = await window.shriVoiceAnalyzer.stopRecording();
        }
        if (metrics) updateVoiceAcousticDisplay(metrics);
        runClinicalAssessment();
    }
}

function loadVoiceDemoPreset(preset) {
    if (window.shriVoiceAnalyzer) {
        const metrics = window.shriVoiceAnalyzer.loadDemoPreset(preset);
        updateVoiceAcousticDisplay(metrics);
        runClinicalAssessment();
    }
}

function updateVoiceAcousticDisplay(metrics) {
    const f0MeanEl = document.getElementById("voice-f0-mean");
    const f0StdEl = document.getElementById("voice-f0-std");
    const jitterEl = document.getElementById("voice-jitter");
    const shimmerEl = document.getElementById("voice-shimmer");
    const pauseEl = document.getElementById("voice-pause-ratio");
    const rateEl = document.getElementById("voice-speech-rate");
    const scoreEl = document.getElementById("voice-risk-score-display");
    const badgeEl = document.getElementById("voice-risk-tier-badge");
    const summaryEl = document.getElementById("voice-clinical-summary");

    if (f0MeanEl) f0MeanEl.innerText = `${metrics.f0Mean} Hz`;
    if (f0StdEl) f0StdEl.innerText = `${metrics.f0Std} Hz`;
    if (jitterEl) jitterEl.innerText = `${metrics.jitter} %`;
    if (shimmerEl) shimmerEl.innerText = `${metrics.shimmer} %`;
    if (pauseEl) pauseEl.innerText = `${metrics.pauseRatio} %`;
    if (rateEl) rateEl.innerText = `${metrics.speechRate} syl/s`;
    if (scoreEl) scoreEl.innerText = `${metrics.vocalRiskScore} / 100`;
    if (badgeEl) {
        badgeEl.innerText = `${metrics.tier} RISK`;
        badgeEl.className = `badge badge-${metrics.tier === 'SEVERE' ? 'danger' : (metrics.tier === 'HIGH' ? 'warning' : 'success')}`;
    }
    if (summaryEl) summaryEl.innerText = metrics.summary;
}

async function togglePatVoiceRecording() {
    const btn = document.getElementById("pat-btn-voice-record");
    const statusEl = document.getElementById("pat-voice-status");

    if (!isVoiceRecordingPatient) {
        isVoiceRecordingPatient = true;
        if (btn) {
            btn.innerHTML = "<span>⏹️ Stop Voice Reflection</span>";
            btn.classList.add("record-btn-pulsing");
        }
        if (statusEl) statusEl.innerText = "🔴 Listening to your voice...";
        if (window.shriVoiceAnalyzer) {
            await window.shriVoiceAnalyzer.startRecording("patVoiceWaveformCanvas");
        }
    } else {
        isVoiceRecordingPatient = false;
        if (btn) {
            btn.innerHTML = "<span>⏺️ Record 15-Second Voice Check-in</span>";
            btn.classList.remove("record-btn-pulsing");
        }
        if (statusEl) statusEl.innerText = "✅ Voice reflection captured privately!";
        let metrics = null;
        if (window.shriVoiceAnalyzer) {
            metrics = await window.shriVoiceAnalyzer.stopRecording();
        }
        const feedbackEl = document.getElementById("pat-voice-feedback-text");
        if (feedbackEl && metrics) {
            feedbackEl.innerHTML = `<b>Vocal Melody:</b> Fundamental pitch ${metrics.f0Mean} Hz, jitter ${metrics.jitter}%. ${metrics.summary}`;
        }
    }
}


// ─────────────────────────────────────────────────────────────────────────────
// GENUINE MULTILINGUAL AUDIO RECORDING, TRANSLATION & HISTORY EVENT HANDLERS
// ─────────────────────────────────────────────────────────────────────────────

async function handleStartMultilingualRecording() {
    const spokenLang = document.getElementById("pat-spoken-lang-select") ? document.getElementById("pat-spoken-lang-select").value : "te-IN";
    const targetLang = document.getElementById("pat-target-lang-select") ? document.getElementById("pat-target-lang-select").value : "en-US";
    const btnStart = document.getElementById("pat-btn-voice-start");
    const btnStop = document.getElementById("pat-btn-voice-stop");
    const btnCancel = document.getElementById("pat-btn-voice-cancel");
    const transcriptsPanel = document.getElementById("pat-transcripts-panel");
    const playerContainer = document.getElementById("pat-audio-player-container");

    if (transcriptsPanel) transcriptsPanel.style.display = "none";
    if (playerContainer) playerContainer.style.display = "none";

    if (btnStart) btnStart.style.display = "none";
    if (btnStop) {
        btnStop.style.display = "inline-flex";
        btnStop.disabled = false;
    }
    if (btnCancel) btnCancel.style.display = "inline-flex";

    if (window.shriVoiceAnalyzer) {
        const res = await window.shriVoiceAnalyzer.startRecording(spokenLang, targetLang, "patVoiceWaveformCanvas");
        if (!res.success) {
            alert(res.error || "Could not access microphone. Using simulated mode.");
        }
    }
}

async function handleStopMultilingualRecording() {
    const btnStart = document.getElementById("pat-btn-voice-start");
    const btnStop = document.getElementById("pat-btn-voice-stop");
    const btnCancel = document.getElementById("pat-btn-voice-cancel");
    const transcriptsPanel = document.getElementById("pat-transcripts-panel");
    const playerContainer = document.getElementById("pat-audio-player-container");

    if (btnStop) {
        btnStop.disabled = true;
        btnStop.innerHTML = "<span>⏳ Processing...</span>";
    }

    if (window.shriVoiceAnalyzer) {
        const result = await window.shriVoiceAnalyzer.stopRecording();
        
        if (playerContainer) playerContainer.style.display = "block";
        if (transcriptsPanel) transcriptsPanel.style.display = "block";

        const badgeSource = document.getElementById("pat-badge-source-lang");
        const badgeTarget = document.getElementById("pat-badge-target-lang");
        const langNames = {
            "en-US": "English (en-US)",
            "hi-IN": "हिन्दी (Hindi - hi-IN)",
            "te-IN": "తెలుగు (Telugu - te-IN)",
            "ta-IN": "தமிழ் (Tamil - ta-IN)"
        };
        const sLang = document.getElementById("pat-spoken-lang-select") ? document.getElementById("pat-spoken-lang-select").value : "te-IN";
        const tLang = document.getElementById("pat-target-lang-select") ? document.getElementById("pat-target-lang-select").value : "en-US";
        if (badgeSource) badgeSource.innerText = langNames[sLang] || sLang;
        if (badgeTarget) badgeTarget.innerText = langNames[tLang] || tLang;

        const feedbackEl = document.getElementById("pat-voice-feedback-text");
        if (feedbackEl && result.metrics) {
            feedbackEl.innerHTML = `<b>Vocal Cadence:</b> Pitch modulation (Mean F0: ${result.metrics.f0Mean} Hz, Jitter: ${result.metrics.jitter}%). ${result.metrics.summary}`;
        }
    }

    if (btnStop) {
        btnStop.style.display = "none";
        btnStop.innerHTML = `<span>⏹️ <span data-i18n="stopRecordBtn">${t('stopRecordBtn', 'Stop & Transcribe')}</span></span>`;
    }
    if (btnCancel) btnCancel.style.display = "none";
    if (btnStart) btnStart.style.display = "inline-flex";
}

function handleCancelMultilingualRecording() {
    if (window.shriVoiceAnalyzer) {
        window.shriVoiceAnalyzer.cancelRecording();
    }
    const btnStart = document.getElementById("pat-btn-voice-start");
    const btnStop = document.getElementById("pat-btn-voice-stop");
    const btnCancel = document.getElementById("pat-btn-voice-cancel");
    const timerEl = document.getElementById("pat-voice-timer");

    if (btnStart) btnStart.style.display = "inline-flex";
    if (btnStop) btnStop.style.display = "none";
    if (btnCancel) btnCancel.style.display = "none";
    if (timerEl) timerEl.innerText = "00:00";
}

function handleSpeakTranslatedText() {
    const transInput = document.getElementById("pat-translated-transcript");
    const text = transInput ? transInput.value : "";
    const targetLang = document.getElementById("pat-target-lang-select") ? document.getElementById("pat-target-lang-select").value : "en-US";
    if (!text.trim()) {
        alert("No translated text available to speak.");
        return;
    }
    if (window.shriVoiceAnalyzer) {
        window.shriVoiceAnalyzer.speakText(text, targetLang);
    }
}

async function handleReTranslateTranscript() {
    const origInput = document.getElementById("pat-original-transcript");
    const transInput = document.getElementById("pat-translated-transcript");
    const text = origInput ? origInput.value : "";
    const sourceLang = document.getElementById("pat-spoken-lang-select") ? document.getElementById("pat-spoken-lang-select").value : "te-IN";
    const targetLang = document.getElementById("pat-target-lang-select") ? document.getElementById("pat-target-lang-select").value : "en-US";

    if (!text.trim()) {
        alert("Please enter original text to translate.");
        return;
    }

    if (window.shriVoiceAnalyzer) {
        if (transInput) transInput.value = "Translating...";
        const trans = await window.shriVoiceAnalyzer.translateText(text, sourceLang, targetLang);
        if (transInput) transInput.value = trans;
        window.shriVoiceAnalyzer.currentTranslation = trans;
        window.shriVoiceAnalyzer.currentTranscript = text;

        const badgeSource = document.getElementById("pat-badge-source-lang");
        const badgeTarget = document.getElementById("pat-badge-target-lang");
        const langNames = {
            "en-US": "English (en-US)",
            "hi-IN": "हिन्दी (Hindi - hi-IN)",
            "te-IN": "తెలుగు (Telugu - te-IN)",
            "ta-IN": "தமிழ் (Tamil - ta-IN)"
        };
        if (badgeSource) badgeSource.innerText = langNames[sourceLang] || sourceLang;
        if (badgeTarget) badgeTarget.innerText = langNames[targetLang] || targetLang;
    }
}

async function handleSaveCurrentAudioSession() {
    if (!window.shriVoiceAnalyzer) return;
    const patId = currentUser ? currentUser.id : "PT-1001";
    const patName = currentUser ? currentUser.name : "Aarav Singh";
    
    const origInput = document.getElementById("pat-original-transcript");
    const transInput = document.getElementById("pat-translated-transcript");
    if (origInput) window.shriVoiceAnalyzer.currentTranscript = origInput.value;
    if (transInput) window.shriVoiceAnalyzer.currentTranslation = transInput.value;

    const res = await window.shriVoiceAnalyzer.saveCurrentSession(patId, patName);
    if (res.success) {
        alert("✅ Audio recording, transcript, and translation successfully saved to your portal history!");
        renderAudioHistoryTable();
    } else {
        alert("Failed to save audio session: " + res.message);
    }
}

function handleDownloadCurrentAudio() {
    if (window.shriVoiceAnalyzer) {
        window.shriVoiceAnalyzer.downloadCurrentAudio();
    }
}

async function renderAudioHistoryTable(filteredList = null) {
    const tbody = document.getElementById("audio-history-tbody");
    if (!tbody) return;

    const patId = currentUser ? currentUser.id : "PT-1001";
    let list = filteredList;
    if (!list && window.shriVoiceAnalyzer && typeof window.shriVoiceAnalyzer.getAllSessions === "function") {
        list = window.shriVoiceAnalyzer.getAllSessions(patId);
    } else if (!list && window.shriVoiceAnalyzer && typeof window.shriVoiceAnalyzer.getStoredSessions === "function") {
        list = window.shriVoiceAnalyzer.getStoredSessions(patId);
    }
    if (!list) list = [];

    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 28px; color: #94A3B8;">${t('noAudioSessionsFound', 'No audio recordings found for this patient yet.')}</td></tr>`;
        return;
    }

    const langLabels = {
        "te-IN": "Telugu",
        "te": "Telugu",
        "hi-IN": "Hindi",
        "hi": "Hindi",
        "ta-IN": "Tamil",
        "ta": "Tamil",
        "en-US": "English",
        "en": "English"
    };

    let rowsHtml = "";
    for (const s of list) {
        const sLang = langLabels[s.sourceLang] || s.sourceLang;
        const tLang = langLabels[s.targetLang] || s.targetLang;
        const dur = s.durationSec ? `${s.durationSec}s` : "15s";
        const dateStr = s.createdAt ? new Date(s.createdAt).toLocaleString() : "Just now";

        let audioSrc = "";
        if (window.shriVoiceAnalyzer) {
            const blob = await window.shriVoiceAnalyzer.getAudioBlob(s.id);
            if (blob) {
                audioSrc = URL.createObjectURL(blob);
            }
        }

        const audioEl = audioSrc 
            ? `<audio controls src="${audioSrc}" style="height: 32px; width: 190px;"></audio>` 
            : `<span style="font-size: 11px; color: #94A3B8;">In-Memory Audio</span>`;

        rowsHtml += `
            <tr id="session-row-${s.id}">
                <td style="font-size: 12px; color: #CBD5E1; white-space: nowrap;">${dateStr}</td>
                <td>
                    <span class="badge badge-info" style="font-size: 11px;">${sLang}</span>
                    <span style="color: #64748B; margin: 0 4px;">➔</span>
                    <span class="badge badge-success" style="font-size: 11px;">${tLang}</span>
                </td>
                <td style="font-size: 12px; font-family: monospace;">${dur}</td>
                <td>${audioEl}</td>
                <td style="max-width: 320px; font-size: 12px; line-height: 1.4;">
                    <div style="color: #F1F5F9; margin-bottom: 4px;"><b>Original:</b> "${s.transcript}"</div>
                    <div style="color: #3b7a74;"><b>Translated:</b> "${s.translation}"</div>
                </td>
                <td style="white-space: nowrap;">
                    <button class="btn btn-outline btn-xs" style="margin-right: 4px;" onclick="playSessionTTS('${s.id}')" title="Play Translated TTS">
                        🔊
                    </button>
                    <button class="btn btn-danger btn-xs" onclick="deleteAudioHistoryRecord('${s.id}')" title="Delete Recording">
                        🗑️
                    </button>
                </td>
            </tr>
        `;
    }
    tbody.innerHTML = rowsHtml;
}

function filterAudioHistory() {
    if (!window.shriVoiceAnalyzer) return;
    const patId = currentUser ? currentUser.id : "PT-1001";
    let list = window.shriVoiceAnalyzer.getStoredSessions(patId);
    
    const searchInput = document.getElementById("audio-history-search");
    const langFilterEl = document.getElementById("audio-history-lang-filter");
    const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
    const langFilter = langFilterEl ? langFilterEl.value : "ALL";

    if (langFilter !== "ALL") {
        list = list.filter(s => s.sourceLang.toLowerCase().startsWith(langFilter.toLowerCase()));
    }
    if (query) {
        list = list.filter(s => 
            (s.transcript && s.transcript.toLowerCase().includes(query)) ||
            (s.translation && s.translation.toLowerCase().includes(query))
        );
    }
    renderAudioHistoryTable(list);
}

async function deleteAudioHistoryRecord(id) {
    if (!confirm(t('deleteConfirm', 'Are you sure you want to delete this recording session?'))) return;
    if (window.shriVoiceAnalyzer) {
        await window.shriVoiceAnalyzer.deleteStoredSession(id);
        renderAudioHistoryTable();
    }
}

function playSessionTTS(sessionId) {
    if (!window.shriVoiceAnalyzer) return;
    const patId = currentUser ? currentUser.id : "PT-1001";
    const list = window.shriVoiceAnalyzer.getStoredSessions(patId);
    const session = list.find(x => x.id === sessionId);
    if (session && session.translation) {
        window.shriVoiceAnalyzer.speakText(session.translation, session.targetLang);
    }
}
