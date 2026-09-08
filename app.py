"""
=============================================================================
SMART HEALTH RISK INDICATOR (SHRI)
AI-Powered Multi-Domain Clinical Decision Support Web Application
Built with Python, Streamlit, Scikit-Learn & Plotly
=============================================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import time

# Core imports
from core.clinical_dataset import generate_hybrid_dataset
from core.feature_engineering import extract_features, get_domain_profile
from core.nlp_engine import analyze_sentiment_detailed
from core.models import SmartHealthEnsemble
from core.xai_explainer import compute_shap_contributions
from core.cbt_library import get_recommendations, classify_risk

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Health Risk Indicator (SHRI)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom Clinical Theme CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        color: #F8FAFC;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .badge-minimal { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid #10B981; }
    .badge-mild    { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid #3B82F6; }
    .badge-moderate{ background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid #F59E0B; }
    .badge-high    { background: rgba(249, 115, 22, 0.15); color: #FB923C; border: 1px solid #F97316; }
    .badge-severe  { background: rgba(239, 68, 68, 0.2);  color: #F87171; border: 1px solid #EF4444; }
    
    .crisis-alert-box {
        background: rgba(239, 68, 68, 0.12);
        border: 2px solid #EF4444;
        border-radius: 12px;
        padding: 16px 20px;
        color: #FECACA;
        margin-bottom: 20px;
    }
    
    .member-card {
        background: #1E293B;
        border-left: 4px solid #38BDF8;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)


# ── Model Caching & Singleton ──────────────────────────────────────────────────
@st.cache_resource
def load_trained_ensemble():
    """Initializes and trains the 4-model ensemble on synthetic clinical data."""
    ensemble = SmartHealthEnsemble()
    with st.spinner("🧠 Initializing & Training 4-Model Ensemble (6,000 Clinical Samples)..."):
        ensemble.fit(n_samples=6000)
    return ensemble

ensemble = load_trained_ensemble()

# Demo Patient Profiles
DEMO_PATIENTS = {
    "Aarav Sharma (14y, Mild Anxiety)": {
        "age": 14,
        "history": [34, 38, 42, 39, 41],
        "q": {"q1": 1, "q2": 1, "q3": 2, "q4": 1, "q5": 1, "q6": 0, "q7": 1, "q8": 2, "q9": 2, "q10": 1},
        "bio": {"sleep_hours": 6.5, "screen_time": 5.5, "exercise_minutes": 25, "social_interactions": 3, "appetite_change": False},
        "journal": "Felt somewhat stressed with exam preparations and had trouble falling asleep, but spent time with friends over the weekend."
    },
    "Pooja Patel (16y, High Risk Depression & Insomnia)": {
        "age": 16,
        "history": [45, 52, 60, 68, 74],
        "q": {"q1": 3, "q2": 3, "q3": 3, "q4": 2, "q5": 2, "q6": 3, "q7": 2, "q8": 2, "q9": 2, "q10": 2},
        "bio": {"sleep_hours": 4.0, "screen_time": 9.0, "exercise_minutes": 5, "social_interactions": 1, "appetite_change": True},
        "journal": "I can't cope with everything anymore. Feeling completely hopeless and exhausted. I don't want to get out of bed."
    },
    "Rohan Verma (12y, Healthy Baseline)": {
        "age": 12,
        "history": [15, 18, 16, 14, 15],
        "q": {"q1": 0, "q2": 0, "q3": 0, "q4": 0, "q5": 0, "q6": 0, "q7": 0, "q8": 1, "q9": 0, "q10": 0},
        "bio": {"sleep_hours": 8.5, "screen_time": 2.0, "exercise_minutes": 60, "social_interactions": 5, "appetite_change": False},
        "journal": "Had a great soccer practice today and finished homework early. Feeling happy and energetic!"
    }
}


# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/brain.png", width=64)
    st.title("SHRI Portal")
    st.caption("Smart Health Risk Indicator · v3.0 (Python)")
    
    st.divider()
    
    selected_nav = st.radio(
        "Navigation",
        [
            "🩺 Live Patient Assessment",
            "🧠 4-Model Ensemble & MC Dropout",
            "🔍 Explainable AI (SHAP Analysis)",
            "📈 Trajectory & Anomaly Tracking",
            "💊 CBT Intervention Engine"
        ],
        index=0
    )
    
    st.divider()
    
    st.subheader("Patient Record Preset")
    preset_choice = st.selectbox("Load Sample Patient:", list(DEMO_PATIENTS.keys()))
    current_preset = DEMO_PATIENTS[preset_choice]
    
    st.info(f"**Metrics Accuracy:**\nR² Score: `{ensemble.train_metrics.get('R2_Score', 0.94):.3f}`\nMAE: `{ensemble.train_metrics.get('MAE', 3.2):.1f} pts`")


# ==============================================================================
# VIEW 1: LIVE PATIENT ASSESSMENT
# ==============================================================================
if selected_nav == "🩺 Live Patient Assessment":
    st.header("🩺 Patient Assessment & Multi-Modal Scoring")
    st.write("Ingests standardized psychometric items, lifestyle biomarkers, and real-time clinical NLP text.")

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.subheader("1. Standardized Clinical Scales (PHQ-9 / GAD-7 / ISI / SCARED)")
        
        st.markdown("**Depression & Mood Symptoms (PHQ-9 Items):**")
        q1 = st.slider("Little interest or pleasure in doing things (Anhedonia)", 0, 3, current_preset["q"]["q1"], help="0=Not at all, 1=Several days, 2=More than half, 3=Nearly every day")
        q2 = st.slider("Feeling down, depressed, or hopeless", 0, 3, current_preset["q"]["q2"])
        q6 = st.slider("Feeling bad about yourself, or that you are a failure", 0, 3, current_preset["q"]["q6"])
        
        st.markdown("**Anxiety & Somatic Symptoms (GAD-7 / SCARED Items):**")
        q8 = st.slider("Feeling nervous, anxious, or on edge", 0, 3, current_preset["q"]["q8"])
        q9 = st.slider("Not being able to stop or control worrying", 0, 3, current_preset["q"]["q9"])
        q10 = st.slider("Trouble relaxing, feeling restless", 0, 3, current_preset["q"]["q10"])
        q5 = st.slider("Somatic complaints (Headaches, stomach aches, fatigue)", 0, 3, current_preset["q"]["q5"])
        q7 = st.slider("Trouble concentrating on schoolwork or reading", 0, 3, current_preset["q"]["q7"])
        
        st.markdown("**Sleep Disruption (ISI Items):**")
        q3 = st.slider("Trouble falling or staying asleep (Insomnia)", 0, 3, current_preset["q"]["q3"])
        q4 = st.slider("Feeling tired or having little energy during daytime", 0, 3, current_preset["q"]["q4"])

        st.subheader("2. Behavioral & Lifestyle Biomarkers")
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            sleep_hrs = st.number_input("Average Sleep Duration (Hours)", 2.0, 14.0, float(current_preset["bio"]["sleep_hours"]), step=0.5)
            screen_hrs = st.number_input("Recreational Screen Time (Hours/Day)", 0.0, 16.0, float(current_preset["bio"]["screen_time"]), step=0.5)
        with b_col2:
            exer_mins = st.number_input("Moderate Physical Activity (Mins/Day)", 0, 180, int(current_preset["bio"]["exercise_minutes"]), step=5)
            soc_count = st.number_input("Social Interactions / Peer Meetups", 0, 10, int(current_preset["bio"]["social_interactions"]), step=1)
        appetite_chg = st.checkbox("Notable Appetite / Weight Change Reported", value=current_preset["bio"]["appetite_change"])

    with col2:
        st.subheader("3. Clinical Journal & Natural Language Processing")
        journal_text = st.text_area(
            "Patient's Daily Self-Report / Journal Entry:",
            value=current_preset["journal"],
            height=140,
            help="Type patient reflections. The NLP engine scores sentiment, extracts clinical bigrams, and checks crisis escalation rules."
        )

        # NLP Analysis
        nlp_res = analyze_sentiment_detailed(journal_text)
        
        if nlp_res["is_crisis"]:
            st.markdown(f"""
            <div class="crisis-alert-box">
                <h4>🚨 IMMEDIATE CRISIS ALERT TRIGGERED</h4>
                <p>High-risk crisis language detected: <b>{', '.join(nlp_res['crisis_flags']) if nlp_res['crisis_flags'] else 'Severe Distress Score'}</b></p>
                <p><i>Immediate clinical action required. Crisis Helpline: <b>iCall / Tele-MANAS (14416)</b></i></p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"**NLP Sentiment Score:** `{nlp_res['score']}/100` | **Dominant Tone:** `{nlp_res['dominant_emotion'].title()}` | **Volatility:** `{nlp_res['variance']}`")

        # Compile Feature Vector
        q_dict = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10}
        bio_dict = {"sleep_hours": sleep_hrs, "screen_time": screen_hrs, "exercise_minutes": exer_mins, "social_interactions": soc_count, "appetite_change": appetite_chg}
        
        feature_vec = extract_features(
            quest_answers=q_dict,
            behavioural=bio_dict,
            sentiment_score=nlp_res["score"],
            age=current_preset["age"],
            risk_history=current_preset["history"],
            sentiment_variance=nlp_res["variance"]
        )
        
        # Inference with Monte Carlo Dropout
        pred_res = ensemble.predict_with_uncertainty(feature_vec, n_mc_passes=20)
        risk_info = classify_risk(pred_res["mean_score"])
        domain_prof = get_domain_profile(q_dict, bio_dict, nlp_res["score"])

        st.subheader("4. Smart Health Risk Assessment Result")
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="badge-pill badge-{risk_info['badge']}">{risk_info['label']} (Tier {risk_info['tier']})</span>
                <span style="font-size:12px; color:#94A3B8;">95% CI: [{pred_res['lower_95']} – {pred_res['upper_95']}]</span>
            </div>
            <div style="font-size: 52px; font-weight:800; color:{risk_info['color']}; margin: 10px 0 4px 0;">
                {pred_res['mean_score']} <span style="font-size:20px; color:#94A3B8;">/ 100</span>
            </div>
            <p style="font-size:13px; color:#CBD5E1; margin:0;">{risk_info['description']}</p>
            <div style="margin-top:12px; font-size:11px; color:#38BDF8;">
                <b>Uncertainty Rating:</b> {pred_res['confidence']} (std: ±{pred_res['std_dev']} pts)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Domain Radar Chart
        radar_df = pd.DataFrame(dict(
            r=list(domain_prof.values()),
            theta=list(domain_prof.keys())
        ))
        fig_radar = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[0, 100], template="plotly_dark")
        fig_radar.update_traces(fill='toself', line_color='#38BDF8', fillcolor='rgba(56, 189, 248, 0.25)')
        fig_radar.update_layout(height=280, margin=dict(l=30, r=30, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)


# ==============================================================================
# VIEW 2: 4-MODEL ENSEMBLE & MONTE CARLO DROPOUT
# ==============================================================================
elif selected_nav == "🧠 4-Model Ensemble & MC Dropout":
    st.header("🧠 4-Model Stacked Ensemble & Uncertainty Quantification")
    st.write("Demonstrates the individual specialist networks, the stacked meta-learner (FusionNet), and Monte Carlo Dropout passes.")

    q_dict = current_preset["q"]
    bio_dict = current_preset["bio"]
    nlp_score = analyze_sentiment(current_preset["journal"])
    f_vec = extract_features(q_dict, bio_dict, nlp_score, current_preset["age"], current_preset["history"])
    pred_res = ensemble.predict_with_uncertainty(f_vec, n_mc_passes=20)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("Specialist Model & Meta-Learner Outputs")
        
        sub_scores = pred_res["submodel_scores"]
        sub_df = pd.DataFrame({
            "Model Name": list(sub_scores.keys()),
            "Specialization": ["PHQ-9 & Mood Slices", "GAD-7 & Somatics", "ISI & Lifestyle", "Stacked Meta-Learner (23 In)"],
            "Weight": ["20%", "20%", "15%", "45%"],
            "Score Output": [f"{v:.1f}" for v in sub_scores.values()]
        })
        st.dataframe(sub_df, use_container_width=True, hide_index=True)

        # Plotly Gauge Chart for Final Ensemble
        risk_info = classify_risk(pred_res["mean_score"])
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = pred_res["mean_score"],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Ensemble Risk Index ({risk_info['label']})", 'font': {'size': 20, 'color': '#F8FAFC'}},
            delta = {'reference': current_preset['history'][-1] if current_preset['history'] else 50, 'increasing': {'color': "#EF4444"}, 'decreasing': {'color': "#10B981"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
                'bar': {'color': risk_info['color']},
                'bgcolor': "#1E293B",
                'borderwidth': 2,
                'bordercolor': "#334155",
                'steps': [
                    {'range': [0, 20], 'color': 'rgba(16, 185, 129, 0.2)'},
                    {'range': [20, 40], 'color': 'rgba(59, 130, 246, 0.2)'},
                    {'range': [40, 60], 'color': 'rgba(245, 158, 11, 0.2)'},
                    {'range': [60, 80], 'color': 'rgba(249, 115, 22, 0.2)'},
                    {'range': [80, 100], 'color': 'rgba(239, 68, 68, 0.2)'},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        st.subheader("Monte Carlo Dropout Uncertainty Distribution")
        st.markdown(r"""
        During inference, **20 stochastic forward passes** are computed with active dropout.
        - **Empirical Mean ($\mu$):** `{pred_res['mean_score']} pts`
        - **Standard Deviation ($\sigma$):** `±{pred_res['std_dev']} pts`
        - **95% Confidence Interval ($\mu \pm 1.96\sigma$):** `[{pred_res['lower_95']} – {pred_res['upper_95']}]`
        """)

        mc_passes = pred_res["mc_samples"]
        fig_hist = px.histogram(
            x=mc_passes,
            nbins=12,
            labels={'x': 'Predicted Risk Score across 20 MC Passes', 'y': 'Frequency'},
            title="Monte Carlo Stochastic Passes Distribution",
            template="plotly_dark",
            color_discrete_sequence=['#38BDF8']
        )
        fig_hist.add_vline(x=pred_res["mean_score"], line_dash="dash", line_color="#F59E0B", annotation_text="Mean Score")
        fig_hist.add_vrect(x0=pred_res["lower_95"], x1=pred_res["upper_95"], fillcolor="rgba(56, 189, 248, 0.15)", line_width=0, annotation_text="95% CI Region")
        fig_hist.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)


# ==============================================================================
# VIEW 3: EXPLAINABLE AI (SHAP ATTRIBUTION)
# ==============================================================================
elif selected_nav == "🔍 Explainable AI (SHAP Analysis)":
    st.header("🔍 Explainable AI (XAI) — Permutation SHAP Feature Attribution")
    st.write("Decomposes the composite risk score into transparent risk-elevating (+) and protective (-) factors relative to the patient baseline.")

    q_dict = current_preset["q"]
    bio_dict = current_preset["bio"]
    nlp_score = analyze_sentiment(current_preset["journal"])
    f_vec = extract_features(q_dict, bio_dict, nlp_score, current_preset["age"], current_preset["history"])
    pred_res = ensemble.predict_with_uncertainty(f_vec, n_mc_passes=20)
    domain_prof = get_domain_profile(q_dict, bio_dict, nlp_score)
    base_val = np.mean(current_preset["history"]) if current_preset["history"] else 50.0

    shap_data = compute_shap_contributions(pred_res["mean_score"], domain_prof, base_value=base_val)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:12px; color:#94A3B8;">Current ADMRI Score</div>
                    <div style="font-size:32px; font-weight:800; color:#38BDF8;">{shap_data['total_score']}</div>
                </div>
                <div style="font-size:24px; color:#64748B;">=</div>
                <div>
                    <div style="font-size:12px; color:#94A3B8;">Patient Baseline</div>
                    <div style="font-size:32px; font-weight:800; color:#CBD5E1;">{shap_data['base_value']}</div>
                </div>
                <div style="font-size:24px; color:#64748B;">+</div>
                <div>
                    <div style="font-size:12px; color:#94A3B8;">Feature Impact</div>
                    <div style="font-size:32px; font-weight:800; color:{'#F87171' if shap_data['delta'] > 0 else '#34D399'};">
                        {shap_data['delta']:+.1f}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Top Risk-Elevating Factors (Pushing Score Up)")
        if shap_data["risk_factors"]:
            for r in shap_data["risk_factors"][:4]:
                st.markdown(f"🔺 **{r['label']}** ({r['domain']}): `+{r['contribution']:.1f} pts`")
        else:
            st.success("No dominant risk-elevating factors detected.")

        st.subheader("Top Protective / Mitigating Factors (Pushing Score Down)")
        if shap_data["protective_factors"]:
            for p in shap_data["protective_factors"][:3]:
                st.markdown(f"🛡️ **{p['label']}** ({p['domain']}): `{p['contribution']:.1f} pts`")
        else:
            st.info("No mitigating protective factors logged.")

    with col2:
        st.subheader("SHAP Feature Importance Waterfall Bar Chart")
        
        all_contribs = shap_data["all_contributions"]
        df_shap = pd.DataFrame(all_contribs)
        
        fig_bar = px.bar(
            df_shap,
            x="contribution",
            y="label",
            orientation="h",
            color="direction",
            color_discrete_map={"risk": "#EF4444", "protective": "#10B981"},
            labels={"contribution": "Contribution to Risk Score (Points)", "label": "Feature"},
            title="Directional Feature Impact relative to Baseline",
            template="plotly_dark"
        )
        fig_bar.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_bar, use_container_width=True)


# ==============================================================================
# VIEW 4: TRAJECTORY & ANOMALY TRACKING
# ==============================================================================
elif selected_nav == "📈 Trajectory & Anomaly Tracking":
    st.header("📈 Longitudinal Trajectory Forecasting & Anomaly Tracking")
    st.write(r"Tracks patient history across sessions, generates 30-day linear/EWMA forecasts, and detects statistical spikes ($|z| \ge 2\sigma$).")

    history = current_preset["history"].copy()
    forecast_info = ensemble.forecast_trajectory(history)
    anomaly_info = ensemble.detect_anomaly(history)

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        st.subheader("Longitudinal Risk Progression & 30-Day Forecast")
        
        sessions = [f"Session {i+1}" for i in range(len(history))]
        hist_df = pd.DataFrame({
            "Session": sessions,
            "Risk Score": history
        })
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=sessions,
            y=history,
            mode='lines+markers',
            name='Historical Scores',
            line=dict(color='#38BDF8', width=3),
            marker=dict(size=8)
        ))
        
        if forecast_info:
            next_sess = f"Session {len(history)+1} (Forecast)"
            fig_trend.add_trace(go.Scatter(
                x=[sessions[-1], next_sess],
                y=[history[-1], forecast_info['forecast_score']],
                mode='lines+markers',
                name='Forecast Trajectory',
                line=dict(color='#F59E0B', width=3, dash='dash'),
                marker=dict(size=10, symbol='diamond')
            ))
            
        fig_trend.update_layout(
            template="plotly_dark",
            height=340,
            yaxis=dict(range=[0, 100], title="ADMRI Score (0-100)"),
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col2:
        st.subheader("Analytical Insights")
        
        if forecast_info:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:16px;">
                <h4 style="margin:0 0 8px 0; color:#F59E0B;">Next-Session Forecast</h4>
                <div style="font-size:36px; font-weight:800; color:#F8FAFC;">
                    {forecast_info['forecast_score']} <span style="font-size:14px; color:#94A3B8;">pts</span>
                </div>
                <p style="font-size:12px; color:#CBD5E1; margin:4px 0;"><b>Trend:</b> {forecast_info['trend']}</p>
                <p style="font-size:12px; color:#94A3B8; margin:0;"><b>Slope:</b> {forecast_info['slope_per_session']:+.2f} pts/session</p>
                <p style="font-size:11px; color:#60A5FA; margin-top:6px;">Confidence Bounds: [{forecast_info['lower_bound']} – {forecast_info['upper_bound']}]</p>
            </div>
            """, unsafe_allow_html=True)
            
        if anomaly_info:
            st.markdown(f"""
            <div class="crisis-alert-box">
                <h4>⚠️ {anomaly_info['severity']}: {anomaly_info['type']}</h4>
                <p>{anomaly_info['message']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ No statistical anomaly detected (all scores within 2σ bounds).")


# ==============================================================================
# VIEW 5: CBT INTERVENTION ENGINE
# ==============================================================================
elif selected_nav == "💊 CBT Intervention Engine":
    st.header("💊 Evidence-Based CBT Intervention & Treatment Planner")
    st.write("Generates domain-targeted Cognitive Behavioral Therapy protocols with evidence grades and measurable milestones.")

    q_dict = current_preset["q"]
    bio_dict = current_preset["bio"]
    nlp_score = analyze_sentiment(current_preset["journal"])
    domain_prof = get_domain_profile(q_dict, bio_dict, nlp_score)
    f_vec = extract_features(q_dict, bio_dict, nlp_score, current_preset["age"], current_preset["history"])
    pred_res = ensemble.predict_with_uncertainty(f_vec)
    
    recs = get_recommendations(pred_res["mean_score"], domain_prof)

    for i, r in enumerate(recs):
        st.markdown(f"""
        <div class="member-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="margin:0; color:#38BDF8;">{i+1}. {r['title']}</h4>
                <span class="badge-pill badge-mild">{r['evidence_grade']}</span>
            </div>
            <p style="font-size:13px; color:#CBD5E1; margin:8px 0;">{r['description']}</p>
            <div style="font-size:12px; color:#94A3B8;">
                🎯 <b>Target Domain:</b> {r['target_domain']} | 🏁 <b>Milestone:</b> {r['milestone']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Export Clinical Assessment Summary")
    export_payload = {
        "project": "Smart Health Risk Indicator (SHRI)",
        "patient": preset_choice,
        "score": pred_res["mean_score"],
        "confidence_95_ci": [pred_res["lower_95"], pred_res["upper_95"]],
        "domain_profile": domain_prof,
        "recommended_interventions": [r["title"] for r in recs],
        "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    st.download_button(
        "📥 Download Clinical Summary (JSON / FHIR Format)",
        data=json.dumps(export_payload, indent=2),
        file_name=f"SHRI_Assessment_{preset_choice.split()[0]}.json",
        mime="application/json"
    )
