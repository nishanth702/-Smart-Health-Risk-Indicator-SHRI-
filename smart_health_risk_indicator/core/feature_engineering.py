"""
Feature Engineering Engine for Smart Health Risk Indicator (SHRI)
─────────────────────────────────────────────────────────────────
Constructs the 20-dimensional normalized multimodal feature vector from:
  - 10-Item Questionnaire (PHQ-9, GAD-7, ISI, SCARED)
  - Behavioral Biomarkers (sleep, screen time, exercise, social)
  - Journal Sentiment & Sentiment Variance
  - Longitudinal Session History
"""

import numpy as np


def compute_trend(history):
    """
    Computes linear regression slope of last 5 risk scores, normalized to [-1, 1].
    Positive slope = worsening; Negative slope = improving.
    """
    if not history or len(history) < 2:
        return 0.0
    recent = history[-5:]
    n = len(recent)
    x_mean = (n - 1) / 2.0
    y_mean = sum(recent) / float(n)

    num = sum((i - x_mean) * (recent[i] / 100.0 - y_mean / 100.0) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    if den == 0:
        return 0.0
    slope = (num / den) * 10.0
    return float(np.clip(slope, -1.0, 1.0))


def extract_features(
    quest_answers,
    behavioural,
    sentiment_score,
    age=14,
    risk_history=None,
    sentiment_variance=0.0
):
    """
    Extracts 20-dimensional feature vector.
    
    Parameters:
      quest_answers (dict): e.g. {'q1': 2, 'q2': 1, ..., 'q10': 3} (each 0 to 3)
      behavioural (dict): {'sleep_hours': 6.5, 'screen_time': 5.0, 'exercise_minutes': 30, 'social_interactions': 2, 'appetite_change': True}
      sentiment_score (float): 0 to 100 (from NLP analyzer)
      age (int): 10 to 18
      risk_history (list): [score1, score2, ...]
      sentiment_variance (float): variance across sentences
      
    Returns:
      np.ndarray of shape (20,)
    """
    if risk_history is None:
        risk_history = []

    def sub_score(keys):
        vals = [quest_answers.get(k, 0) for k in keys]
        return sum(vals) / (len(keys) * 3.0)

    # 1. Questionnaire Normalized Sub-scores
    total_norm   = sum(quest_answers.get(f"q{i}", 0) for i in range(1, 11)) / 30.0
    depr_norm    = sub_score(["q1", "q2", "q6"])
    anx_norm     = sub_score(["q8", "q9", "q10"])
    sleep_q_norm = sub_score(["q3", "q4"])
    somatic_norm = sub_score(["q5"])
    cog_norm     = sub_score(["q7"])

    # 2. Lifestyle & Behavioral Risks (0 = no risk, 1 = maximum risk)
    sleep_hours = float(behavioural.get("sleep_hours", 8.0))
    screen_time = float(behavioural.get("screen_time", 3.0))
    exercise_minutes = float(behavioural.get("exercise_minutes", 45.0))
    social_interactions = float(behavioural.get("social_interactions", 4.0))
    appetite_change = 1.0 if behavioural.get("appetite_change", False) else 0.0

    sleep_risk  = float(np.clip((8.0 - sleep_hours) / 6.0, 0.0, 1.0))
    screen_risk = float(np.clip(screen_time / 12.0, 0.0, 1.0))
    exer_risk   = float(np.clip((60.0 - exercise_minutes) / 60.0, 0.0, 1.0))
    social_risk = float(np.clip((5.0 - social_interactions) / 5.0, 0.0, 1.0))
    appetite_r  = appetite_change

    # 3. Sentiment & Demographics
    sent_norm = float(sentiment_score / 100.0)
    sent_var  = float(np.clip(sentiment_variance / 50.0, 0.0, 1.0))
    age_norm  = float(np.clip((age - 10.0) / 8.0, 0.0, 1.0))

    # 4. Cross-Domain Interaction Terms
    depr_anx      = depr_norm * anx_norm
    sleep_sent    = sleep_risk * (1.0 - sent_norm)
    total_behav   = (sleep_risk + screen_risk + exer_risk + social_risk + appetite_r) / 5.0
    somatic_sleep = somatic_norm * sleep_risk

    # 5. Longitudinal Dynamics
    score_trend = compute_trend(risk_history)
    sess_count  = float(np.clip(len(risk_history) / 20.0, 0.0, 1.0))

    vector = [
        total_norm, depr_norm, anx_norm, sleep_q_norm, somatic_norm, cog_norm,
        sleep_risk, screen_risk, exer_risk, social_risk, appetite_r,
        sent_norm, sent_var, age_norm,
        depr_anx, sleep_sent, total_behav, somatic_sleep,
        score_trend, sess_count
    ]

    return np.array(vector, dtype=np.float32)


def get_domain_profile(quest_answers, behavioural, sentiment_score):
    """
    Computes percentage scores (0 to 100) for each clinical domain for visualization.
    """
    def sub(keys):
        return round(sum(quest_answers.get(k, 0) for k in keys) / (len(keys) * 3.0) * 100)

    sleep_hrs = behavioural.get("sleep_hours", 8)
    screen_tm = behavioural.get("screen_time", 2)
    exer_min  = behavioural.get("exercise_minutes", 45)
    soc_cnt   = behavioural.get("social_interactions", 4)
    app_chg   = behavioural.get("appetite_change", False)

    b_score = 0
    if sleep_hrs < 6: b_score += 25
    elif sleep_hrs < 7: b_score += 12
    if screen_tm > 6: b_score += 20
    elif screen_tm > 4: b_score += 10
    if exer_min < 20: b_score += 20
    elif exer_min < 30: b_score += 8
    if soc_cnt < 2: b_score += 20
    if app_chg: b_score += 15

    return {
        "Depression": sub(["q1", "q2", "q6"]),
        "Anxiety": sub(["q8", "q9", "q10"]),
        "Sleep Disruption": sub(["q3", "q4"]),
        "Somatic Symptoms": sub(["q5"]),
        "Concentration / Cognitive": sub(["q7"]),
        "Negative Sentiment": round(100 - sentiment_score),
        "Lifestyle & Behavioral Risk": min(100, b_score)
    }
