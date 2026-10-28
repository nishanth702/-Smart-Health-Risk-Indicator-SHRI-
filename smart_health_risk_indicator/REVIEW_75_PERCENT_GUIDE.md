# 🏥 SMART HEALTH RISK INDICATOR (SHRI)
## 75% Major Project Review & 3-Member Team Viva Guide

---

## 👥 1. Team Role & Contribution Division (3 Members)

This project has been strategically partitioned into 3 core engineering verticals:

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               SMART HEALTH RISK INDICATOR (SHRI)                                     │
├───────────────────────────────────┬───────────────────────────────────┬───────────────────────────────┤
│ 👤 MEMBER 1: ML & ENSEMBLE LEAD  │ 👤 MEMBER 2: NLP & XAI LEAD       │ 👤 MEMBER 3: FULL-STACK LEAD  │
├───────────────────────────────────┼───────────────────────────────────┼───────────────────────────────┤
│ • 6,000 Hybrid Clinical Dataset   │ • Real-time Clinical NLP Engine   │ • Interactive Web App (UI/UX) │
│ • 20D Feature Engineering Matrix  │ • 90-Word Lexicon & Crisis Bigrams│ • 30-Day Trajectory Forecast  │
│ • DepNet, AnxNet, SleepNet Models │ • Intensifier & Negation Logic    │ • 2σ Anomaly Detection Alerts │
│ • 23-Input FusionNet Meta-Learner │ • Permutation SHAP Feature Engine │ • Automated CBT Recommender   │
│ • Monte Carlo Dropout (95% CI)    │ • Emergency Crisis UI Escalation  │ • FHIR / JSON Clinical Export │
└───────────────────────────────────┴───────────────────────────────────┴───────────────────────────────┘
```

---

## 🎤 2. What Each Member Should Speak in the 75% Review / Viva

### 👤 Member 1 (ML & Ensemble Architecture Lead)
* **Opening Statement:**
  > *"Respected Examiners, I am responsible for the core Machine Learning Pipeline, 20-dimensional Feature Engineering, and the 4-Model Stacked Ensemble with Uncertainty Quantification."*
* **Key Points to Explain:**
  1. **Dataset Grounding:** *"We built a programmatic hybrid dataset generator producing 6,000 validated samples grounded on clinical distributions from PHQ-9 (Depression), GAD-7 (Anxiety), ISI (Insomnia), and SCARED (Adolescent Anxiety)."*
  2. **Multi-Model Architecture:** *"Rather than using a single generic classifier, I designed 3 specialized neural networks: DepNet (10 features), AnxNet (11 features), and SleepNet (11 features). These feed into FusionNet, a 23-input meta-learner that dynamically weights each specialist model."*
  3. **Uncertainty Quantification:** *"In medical AI, point estimates can be dangerous. I implemented Monte Carlo Dropout with 20 stochastic test-time passes. This produces an empirical standard deviation and an exact 95% Confidence Interval ($\mu \pm 1.96\sigma$)."*

---

### 👤 Member 2 (NLP, Crisis Detection & Explainable AI Lead)
* **Opening Statement:**
  > *"Respected Examiners, my contribution encompasses the Real-Time Clinical NLP Sentiment Engine, Crisis Keyword Escalation, and Explainable AI (XAI) using SHAP Permutation Attribution."*
* **Key Points to Explain:**
  1. **Clinical NLP Engine:** *"Adolescent self-reports contain unstructured emotional context. I engineered an NLP engine with a 90-term clinical lexicon, emoji polarity mapping, linguistic intensifier multipliers (e.g., 'extremely', 'deeply'), and negation handling."*
  2. **Crisis Trigger:** *"I defined 20 critical bigrams (e.g., 'want to die', 'can't cope', 'self harm'). If detected, the system immediately bypasses routine flow to trigger an emergency crisis modal and national helpline contacts (Tele-MANAS / iCall)."*
  3. **Explainable AI (SHAP):** *"To eliminate black-box concerns, I built a SHAP-style permutation attribution module that breaks down the final score into exact risk-elevating (e.g., PHQ-9: +18.2) and protective factors (e.g., Exercise: -6.1) relative to the patient baseline."*

---

### 👤 Member 3 (Full-Stack Platform, Longitudinal Analytics & CBT Lead)
* **Opening Statement:**
  > *"Respected Examiners, I developed the interactive Web Application, the Longitudinal Trajectory & Anomaly Detection system, and the Evidence-Based CBT Intervention Engine."*
* **Key Points to Explain:**
  1. **Clinical Portal & UI/UX:** *"I developed the multi-view web application using Python, Streamlit, and Plotly, delivering real-time responsive analytics, radar charts, and uncertainty distribution histograms."*
  2. **Longitudinal Forecasting:** *"I integrated a 30-day trajectory forecast combining Linear Regression slope with Exponentially Weighted Moving Average (EWMA, $\alpha=0.4$) to predict future risk trends."*
  3. **Anomaly & Interventions:** *"I implemented a statistical anomaly detector ($|z| \ge 2.0\sigma$) to flag sudden risk spikes, alongside an evidence-graded CBT recommendation engine with FHIR/JSON export."*

---

## 💻 3. Live Demonstration Checklist for 75% Review

When you share your screen or run the live demo for examiners, showcase these 5 interactive flows:

1. **Preset Loading & Scoring:** Select *"Pooja Patel (High Risk)"* $\rightarrow$ Show the composite score (74/100, Tier 4 High Risk) and the **95% Confidence Interval** badge.
2. **Monte Carlo Dropout Tab:** Open *"4-Model Ensemble & MC Dropout"* $\rightarrow$ Show the Plotly Gauge Chart and the histogram of 20 stochastic passes with the 95% shaded region.
3. **SHAP Explainability Tab:** Open *"Explainable AI (SHAP Analysis)"* $\rightarrow$ Point to the horizontal waterfall chart showing positive risk drivers vs mitigating protective habits.
4. **Trajectory & Anomaly Tab:** Open *"Trajectory & Anomaly Tracking"* $\rightarrow$ Show the 30-day forecast line and the 2$\sigma$ anomaly alert box.
5. **Crisis NLP Trigger:** Type *"I can't cope with anything anymore and want to end it all"* in the journal box $\rightarrow$ Show the red **Immediate Crisis Alert** trigger.

---

## 🎯 4. Examiner Defense: "What is Pending in the Remaining 25%?"

If the external examiner asks: **"Your 75% is working. What is pending in the remaining 25% and how will you finish it for the final review?"**, reply with these 4 clear points:

| Pending Feature (25%) | Technical Detail | Expected Final Outcome |
|---|---|---|
| **1. Multi-Hospital Pilot Validation (10%)** | Validation on real-world anonymized EHR datasets | Formal sensitivity/specificity ROC-AUC benchmark curves across clinical cohorts. |
| **2. Audio & Voice Biomarker Ingestion (5%)** | Acoustic prosody extraction (pitch jitter, speech rate, pauses) | Multimodal fusion adding speech biomarkers to text & questionnaire inputs. |
| **3. Microservices & Dockerization (5%)** | Containerized deployment using Docker & FastAPI REST endpoints | Scalable cloud deployment ready for hospital management integration. |
| **4. Multi-Language Localization (5%)** | Translating 90-word clinical lexicon into regional Indian languages | Accessibility in Hindi, Telugu, and Tamil for rural primary health centers. |

---

## ❓ 5. Top 5 Viva Questions & Fast Answers

* **Q1: Why is this called an 'Adaptive' Risk Indicator?**
  * **Answer:** It adapts dynamically to each patient's moving baseline, updating historical slopes, recalibrating risk weights, and flagging deviations ($|z| \ge 2\sigma$) from individual trajectories.
* **Q2: Why use Monte Carlo Dropout instead of standard predictions?**
  * **Answer:** Standard neural networks give overconfident point estimates. MC Dropout keeps dropout active at test-time over 20 passes to sample model epistemic uncertainty, yielding a clinical 95% Confidence Interval.
* **Q3: What makes your NLP engine clinically sound?**
  * **Answer:** It pairs a 90-term domain lexicon with negation handling, intensifiers, and 20 critical crisis bigrams that immediately escalate potential suicide or self-harm risks.
* **Q4: How does the SHAP component work without slow Python kernel computation?**
  * **Answer:** It uses domain-partitioned permutation attribution, normalizing deviations against patient baselines to produce transparent additive contribution bars.
* **Q5: Is patient data safe?**
  * **Answer:** Yes, all ML inference runs directly within the client/local environment, ensuring patient reflections and scores remain private.
