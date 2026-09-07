/**
 * Main Application UI Controller (Client-Side Vanilla JS + Chart.js)
 */

// Presets
const PRESETS = {
    pooja: {
        name: "Pooja Patel (16y, High Risk)",
        age: 16,
        history: [45, 52, 60, 68, 74],
        q: { q1: 3, q2: 3, q3: 3, q4: 2, q5: 2, q6: 3, q7: 2, q8: 2, q9: 2, q10: 2 },
        bio: { sleepHours: 4.0, screenTime: 9.0, exerciseMinutes: 5, socialInteractions: 1, appetiteChange: true },
        journal: "I can't cope with everything anymore. Feeling completely hopeless and exhausted. I don't want to get out of bed."
    },
    aarav: {
        name: "Aarav Sharma (14y, Mild Anxiety)",
        age: 14,
        history: [34, 38, 42, 39, 41],
        q: { q1: 1, q2: 1, q3: 2, q4: 1, q5: 1, q6: 0, q7: 1, q8: 2, q9: 2, q10: 1 },
        bio: { sleepHours: 6.5, screenTime: 5.5, exerciseMinutes: 25, socialInteractions: 3, appetiteChange: false },
        journal: "Felt somewhat stressed with exam preparations and had trouble falling asleep, but spent time with friends over the weekend."
    },
    rohan: {
        name: "Rohan Verma (12y, Baseline)",
        age: 12,
        history: [15, 18, 16, 14, 15],
        q: { q1: 0, q2: 0, q3: 0, q4: 0, q5: 0, q6: 0, q7: 0, q8: 1, q9: 0, q10: 0 },
        bio: { sleepHours: 8.5, screenTime: 2.0, exerciseMinutes: 60, socialInteractions: 5, appetiteChange: false },
        journal: "Had a great soccer practice today and finished homework early. Feeling happy and energetic!"
    }
};

let currentPresetKey = "pooja";
let radarChartInstance = null;
let ensembleBarInstance = null;
let mcHistInstance = null;
let shapBarInstance = null;
let trajectoryChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initSliders();
    initPresetSelector();
    initVivaTabs();
    initExportBtn();
    
    // Initial run
    applyPreset("pooja");
});

function initTabs() {
    const navBtns = document.querySelectorAll(".nav-item");
    const tabPanes = document.querySelectorAll(".tab-pane");
    const pageTitle = document.getElementById("page-title");
    const pageDesc = document.getElementById("page-desc");

    const titles = {
        assessment: { title: "🩺 Patient Assessment & Multi-Modal Scoring", desc: "Ingests psychometric items, lifestyle biomarkers, and real-time clinical NLP text." },
        ensemble: { title: "🧠 4-Model Ensemble & Uncertainty Quantification", desc: "Demonstrates specialist networks, meta-learner (FusionNet), and Monte Carlo Dropout passes." },
        shap: { title: "🔍 Explainable AI (XAI) — Permutation SHAP Attribution", desc: "Decomposes risk score into positive risk drivers and mitigating protective habits relative to baseline." },
        trajectory: { title: "📈 Longitudinal Trajectory & Anomaly Tracking", desc: "Tracks patient history across sessions, generates 30-day forecast, and flags 2σ anomalies." },
        cbt: { title: "💊 Evidence-Based CBT Intervention Protocols", desc: "Generates domain-targeted Cognitive Behavioral Therapy protocols with measurable milestones." },
        viva: { title: "👥 75% Major Project Review — 3-Member Team Viva Guide", desc: "Detailed breakdown of Member 1, Member 2, and Member 3 contributions and examiner defense scripts." }
    };

    navBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.tab;
            navBtns.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            document.getElementById(`tab-${target}`).classList.add("active");

            if (titles[target]) {
                pageTitle.textContent = titles[target].title;
                pageDesc.textContent = titles[target].desc;
            }

            // Re-render charts when visible
            setTimeout(updateAllViews, 50);
        });
    });
}

function initVivaTabs() {
    const vBtns = document.querySelectorAll(".viva-tab-btn");
    const vContents = document.querySelectorAll(".viva-content");

    vBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.dataset.viva;
            vBtns.forEach(b => b.classList.remove("active"));
            vContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            document.getElementById(`viva-${target}`).classList.add("active");
        });
    });
}

function initSliders() {
    const qIds = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"];
    qIds.forEach(id => {
        const slider = document.getElementById(id);
        const valSpan = document.getElementById(`val-${id}`);
        slider.addEventListener("input", () => {
            valSpan.textContent = slider.value;
            runInference();
        });
    });

    ["bio-sleep", "bio-screen", "bio-exercise", "bio-social", "bio-appetite"].forEach(id => {
        document.getElementById(id).addEventListener("input", runInference);
    });

    document.getElementById("journal-text").addEventListener("input", runInference);
    document.getElementById("reset-btn").addEventListener("click", () => applyPreset(currentPresetKey));
}

function initPresetSelector() {
    const select = document.getElementById("patient-select");
    select.addEventListener("change", (e) => {
        applyPreset(e.target.value);
    });
}

function applyPreset(key) {
    currentPresetKey = key;
    const p = PRESETS[key];
    if (!p) return;

    // Set sliders
    Object.entries(p.q).forEach(([k, val]) => {
        const el = document.getElementById(k);
        const span = document.getElementById(`val-${k}`);
        if (el) el.value = val;
        if (span) span.textContent = val;
    });

    // Set Bio
    document.getElementById("bio-sleep").value = p.bio.sleepHours;
    document.getElementById("bio-screen").value = p.bio.screenTime;
    document.getElementById("bio-exercise").value = p.bio.exerciseMinutes;
    document.getElementById("bio-social").value = p.bio.socialInteractions;
    document.getElementById("bio-appetite").checked = p.bio.appetiteChange;

    // Set Journal
    document.getElementById("journal-text").value = p.journal;

    runInference();
}

function getCurrentInputs() {
    const q = {};
    for (let i = 1; i <= 10; i++) {
        q[`q${i}`] = parseInt(document.getElementById(`q${i}`).value) || 0;
    }

    const bio = {
        sleepHours: parseFloat(document.getElementById("bio-sleep").value) || 8,
        screenTime: parseFloat(document.getElementById("bio-screen").value) || 3,
        exerciseMinutes: parseInt(document.getElementById("bio-exercise").value) || 45,
        socialInteractions: parseInt(document.getElementById("bio-social").value) || 4,
        appetiteChange: document.getElementById("bio-appetite").checked
    };

    const journal = document.getElementById("journal-text").value;
    const preset = PRESETS[currentPresetKey] || PRESETS.pooja;

    return { q, bio, journal, age: preset.age, history: preset.history, name: preset.name };
}

function runInference() {
    const { q, bio, journal, age, history, name } = getCurrentInputs();

    // 1. NLP Analysis
    const nlp = analyzeSentimentDetailed(journal);
    document.getElementById("nlp-score").textContent = `${nlp.score}/100`;
    document.getElementById("nlp-emotion").textContent = nlp.dominantEmotion.toUpperCase();
    document.getElementById("nlp-variance").textContent = `±${nlp.variance}`;

    const crisisBox = document.getElementById("crisis-alert");
    if (nlp.isCrisis) {
        crisisBox.classList.add("active");
        document.getElementById("crisis-reason").innerHTML = `High-risk crisis language detected: <b>"${nlp.crisisFlags.length ? nlp.crisisFlags.join('", "') : 'Severe Distress Score'}"</b>`;
    } else {
        crisisBox.classList.remove("active");
    }

    // 2. Feature Vector & Ensemble Prediction
    const features = extractFeatures(q, bio, nlp.score, age, history, nlp.variance);
    const pred = ensembleEngine.predictWithUncertainty(features, 20);
    const riskInfo = classifyRisk(pred.meanScore);
    const domainProfile = getDomainProfile(q, bio, nlp.score);

    // Update Assessment Tab UI
    document.getElementById("composite-score").textContent = pred.meanScore;
    document.getElementById("composite-score").style.color = riskInfo.color;
    document.getElementById("risk-badge").textContent = riskInfo.label;
    document.getElementById("risk-badge").className = `badge ${riskInfo.badge}`;
    document.getElementById("ci-text").textContent = `95% CI: [${pred.lower95} – ${pred.upper95}]`;
    document.getElementById("risk-desc").textContent = riskInfo.desc;
    document.getElementById("uncertainty-rating").innerHTML = `🎯 <b>Uncertainty Rating:</b> ${pred.confidence} (std: ±${pred.stdDev} pts)`;

    // Update Radar Chart
    renderRadarChart(domainProfile);

    // Update Ensemble Tab
    updateEnsembleTab(pred);

    // Update SHAP Tab
    const baseVal = history.length ? history.reduce((a, b) => a + b, 0) / history.length : 50;
    const shap = computeShapContributions(pred.meanScore, domainProfile, baseVal);
    updateShapTab(shap);

    // Update Trajectory Tab
    const forecast = ensembleEngine.forecastTrajectory(history);
    const anomaly = ensembleEngine.detectAnomaly(history);
    updateTrajectoryTab(history, forecast, anomaly);

    // Update CBT Tab
    const recs = getRecommendations(pred.meanScore, domainProfile);
    updateCbtTab(recs);
}

function updateAllViews() {
    runInference();
}

/* ── CHARTS ────────────────────────────────────────────────────────────── */
function renderRadarChart(domainProfile) {
    const ctx = document.getElementById("radarChart").getContext("2d");
    const labels = Object.keys(domainProfile);
    const data = Object.values(domainProfile);

    if (radarChartInstance) radarChartInstance.destroy();

    radarChartInstance = new Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: [{
                label: "Clinical Domain Severity (%)",
                data: data,
                backgroundColor: "rgba(56, 189, 248, 0.25)",
                borderColor: "#38BDF8",
                borderWidth: 2,
                pointBackgroundColor: "#0284C7"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: "rgba(255, 255, 255, 0.1)" },
                    grid: { color: "rgba(255, 255, 255, 0.1)" },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false },
                    pointLabels: { color: "#9CA3AF", font: { size: 10 } }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function updateEnsembleTab(pred) {
    // Populate Table
    const tbody = document.getElementById("ensemble-table-body");
    tbody.innerHTML = `
        <tr><td><b>🔴 DepNet</b></td><td>PHQ-9 & Mood Slices</td><td>20%</td><td><b>${pred.subScores.depnet}</b></td></tr>
        <tr><td><b>🟠 AnxNet</b></td><td>GAD-7 & Somatics</td><td>20%</td><td><b>${pred.subScores.anxnet}</b></td></tr>
        <tr><td><b>🔵 SleepNet</b></td><td>ISI & Lifestyle Risks</td><td>15%</td><td><b>${pred.subScores.sleepnet}</b></td></tr>
        <tr><td><b>🧠 FusionNet</b></td><td>Stacked Meta-Learner (23 In)</td><td>45%</td><td><b>${pred.subScores.fusionnet}</b></td></tr>
    `;

    document.getElementById("mc-mean").textContent = `${pred.meanScore}.0 pts`;
    document.getElementById("mc-std").textContent = `±${pred.stdDev} pts`;
    document.getElementById("mc-ci").textContent = `[${pred.lower95} – ${pred.upper95}]`;

    // Ensemble Bar Chart
    const ctxBar = document.getElementById("ensembleBarChart").getContext("2d");
    if (ensembleBarInstance) ensembleBarInstance.destroy();
    ensembleBarInstance = new Chart(ctxBar, {
        type: "bar",
        data: {
            labels: ["DepNet (20%)", "AnxNet (20%)", "SleepNet (15%)", "FusionNet (45%)", "Final Ensemble"],
            datasets: [{
                data: [pred.subScores.depnet, pred.subScores.anxnet, pred.subScores.sleepnet, pred.subScores.fusionnet, pred.meanScore],
                backgroundColor: ["#F87171", "#FB923C", "#60A5FA", "#A78BFA", "#34D399"]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: 0, max: 100, grid: { color: "rgba(255,255,255,0.05)" } } },
            plugins: { legend: { display: false } }
        }
    });

    // Histogram
    const ctxHist = document.getElementById("mcHistogramChart").getContext("2d");
    if (mcHistInstance) mcHistInstance.destroy();
    mcHistInstance = new Chart(ctxHist, {
        type: "line",
        data: {
            labels: pred.mcScores.map((_, i) => `Pass ${i+1}`),
            datasets: [{
                label: "Stochastic Pass Score",
                data: pred.mcScores,
                borderColor: "#38BDF8",
                backgroundColor: "rgba(56, 189, 248, 0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: Math.max(0, pred.lower95 - 5), max: Math.min(100, pred.upper95 + 5), grid: { color: "rgba(255,255,255,0.05)" } } },
            plugins: { legend: { display: false } }
        }
    });
}

function updateShapTab(shap) {
    document.getElementById("shap-score").textContent = shap.totalScore;
    document.getElementById("shap-baseline").textContent = shap.baseValue;
    document.getElementById("shap-delta").textContent = (parseFloat(shap.delta) >= 0 ? "+" : "") + shap.delta;
    document.getElementById("shap-delta").className = parseFloat(shap.delta) >= 0 ? "num text-danger" : "num text-safe";

    const riskDiv = document.getElementById("risk-factors-list");
    riskDiv.innerHTML = shap.riskFactors.length
        ? shap.riskFactors.slice(0, 4).map(f => `<div class="factor-item"><span>🔺 <b>${f.label}</b> (${f.domain})</span><span class="val-risk">+${f.contribution} pts</span></div>`).join("")
        : `<p style="font-size:12px; color:#9CA3AF;">No dominant risk-elevating factors.</p>`;

    const protDiv = document.getElementById("protective-factors-list");
    protDiv.innerHTML = shap.protectiveFactors.length
        ? shap.protectiveFactors.slice(0, 3).map(f => `<div class="factor-item"><span>🛡️ <b>${f.label}</b> (${f.domain})</span><span class="val-safe">${f.contribution} pts</span></div>`).join("")
        : `<p style="font-size:12px; color:#9CA3AF;">No mitigating protective factors.</p>`;

    // SHAP Bar Chart
    const ctx = document.getElementById("shapBarChart").getContext("2d");
    if (shapBarInstance) shapBarInstance.destroy();

    shapBarInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: shap.allContributions.map(c => c.label),
            datasets: [{
                data: shap.allContributions.map(c => c.contribution),
                backgroundColor: shap.allContributions.map(c => c.direction === "risk" ? "#EF4444" : "#10B981")
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            scales: { x: { grid: { color: "rgba(255,255,255,0.05)" } } },
            plugins: { legend: { display: false } }
        }
    });
}

function updateTrajectoryTab(history, forecast, anomaly) {
    const sessions = history.map((_, i) => `Session ${i + 1}`);
    const values = [...history];

    if (forecast) {
        sessions.push(`Session ${history.length + 1} (Forecast)`);
        values.push(forecast.forecastScore);
        document.getElementById("forecast-val").textContent = `${forecast.forecastScore} pts`;
        document.getElementById("forecast-trend").innerHTML = `<b>Trend:</b> ${forecast.trend}`;
        document.getElementById("forecast-slope").innerHTML = `<b>Slope:</b> ${forecast.slopePerSession > 0 ? "+" : ""}${forecast.slopePerSession} pts/session`;
        document.getElementById("forecast-bounds").textContent = `Bounds: [${forecast.lowerBound} – ${forecast.upperBound}]`;
    }

    const aBox = document.getElementById("anomaly-box");
    if (anomaly) {
        aBox.style.display = "block";
        document.getElementById("anomaly-msg").textContent = anomaly.message;
    } else {
        aBox.style.display = "none";
    }

    const ctx = document.getElementById("trajectoryChart").getContext("2d");
    if (trajectoryChartInstance) trajectoryChartInstance.destroy();

    trajectoryChartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: sessions,
            datasets: [{
                label: "Risk Score History",
                data: values,
                borderColor: "#38BDF8",
                backgroundColor: "rgba(56, 189, 248, 0.15)",
                pointRadius: 6,
                pointBackgroundColor: "#0284C7",
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: 0, max: 100, grid: { color: "rgba(255,255,255,0.05)" } } },
            plugins: { legend: { display: false } }
        }
    });
}

function updateCbtTab(recs) {
    const container = document.getElementById("cbt-container");
    container.innerHTML = recs.map((r, i) => `
        <div class="cbt-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <h4>${i + 1}. ${r.title}</h4>
                <span class="badge badge-mild">${r.grade}</span>
            </div>
            <p>${r.desc}</p>
            <div class="cbt-meta">🎯 <b>Domain:</b> ${r.domain} | 🏁 <b>Milestone:</b> ${r.milestone}</div>
        </div>
    `).join("");
}

function initExportBtn() {
    document.getElementById("export-json-btn").addEventListener("click", () => {
        const { q, bio, journal, name, history } = getCurrentInputs();
        const nlp = analyzeSentimentDetailed(journal);
        const features = extractFeatures(q, bio, nlp.score, 14, history, nlp.variance);
        const pred = ensembleEngine.predictWithUncertainty(features, 20);
        const domainProfile = getDomainProfile(q, bio, nlp.score);
        const recs = getRecommendations(pred.meanScore, domainProfile);

        const fhir = generateFHIRJSON(name, pred.meanScore, [pred.lower95, pred.upper95], domainProfile, recs);
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(fhir, null, 2));
        const a = document.createElement("a");
        a.setAttribute("href", dataStr);
        a.setAttribute("download", `SHRI_DiagnosticReport_${name.split(" ")[0]}.json`);
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
}
