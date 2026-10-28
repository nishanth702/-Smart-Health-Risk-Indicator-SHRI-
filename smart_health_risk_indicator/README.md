# 🏥 Smart Health Risk Indicator (SHRI)
> **AI-Powered Multi-Domain Clinical Decision Support Web Application**  
> *Developed with Python, Streamlit, Scikit-Learn, and Plotly*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E.svg?logo=scikit-learn)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75.svg?logo=plotly)](https://plotly.com)
[![SDG](https://img.shields.io/badge/SDG-3%20Good%20Health-4C9F38?style=flat-square)](https://sdgs.un.org/goals/goal3)

---

## 📖 Overview

**Smart Health Risk Indicator (SHRI)** is an intelligent clinical decision support system designed to assess adolescent mental health risk (ages 10–18). It synthesizes:
1. **Clinical Scales**: PHQ-9 (Depression), GAD-7 (Anxiety), ISI (Insomnia), and SCARED.
2. **Behavioral & Lifestyle Biomarkers**: Sleep duration, screen time, physical activity, and social interactions.
3. **Clinical NLP Text**: Real-time journal sentiment scoring, 90-word clinical lexicon, and crisis detection bigrams.

---

## 🏗️ Architecture

```
INPUT LAYER (Questionnaires + Lifestyle + NLP Journal)
                        │
                        ▼
       20-DIMENSIONAL FEATURE ENGINEERING
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
   🔴 DepNet        🟠 AnxNet        🔵 SleepNet
  (Depression)      (Anxiety)        (Sleep/Bio)
       │                │                │
       └────────────────┼────────────────┘
                        ▼
          🧠 FusionNet (Meta-Learner)
          23 Inputs · Stacked Ensemble
                        │
                        ▼
          🎲 Monte Carlo Dropout
          20 Passes → 95% Confidence Interval
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
  ADMRI Score      Explainable AI    CBT Recommendations
  (0-100 Gauge)    (SHAP Waterfall)  & Crisis Escalation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+ installed
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/smart_health_risk_indicator.git
cd smart_health_risk_indicator

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Web Application
```bash
streamlit run app.py
```

The application opens automatically at `http://localhost:8501`.

---

## 📊 Modules & Features

| Module | File | Purpose |
|---|---|---|
| **Clinical Dataset** | `core/clinical_dataset.py` | 6,000 hybrid samples grounded on published psychiatric instruments. |
| **Feature Extraction** | `core/feature_engineering.py` | 20-dimensional multimodal vector + interaction terms. |
| **NLP Crisis Engine** | `core/nlp_engine.py` | 90-term lexicon, 20 crisis bigrams, intensifier/negation parser. |
| **4-Model Ensemble** | `core/models.py` | DepNet, AnxNet, SleepNet + FusionNet with Monte Carlo Dropout. |
| **Explainable AI (XAI)** | `core/xai_explainer.py` | Permutation-based SHAP feature attribution. |
| **CBT Interventions** | `core/cbt_library.py` | Evidence-graded CBT protocols & FHIR export. |
| **Web Application** | `app.py` | Full interactive Streamlit clinician portal with Plotly charts. |

---

## 👥 3-Member Review Guide

See [`REVIEW_75_PERCENT_GUIDE.md`](REVIEW_75_PERCENT_GUIDE.md) for the complete viva scripts, 3-member contribution breakdown, live demonstration checklist, and defense points for the pending 25%.
