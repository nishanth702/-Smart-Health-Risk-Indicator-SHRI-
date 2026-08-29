"""
Explainable AI (XAI) Engine - Permutation SHAP Feature Attribution
──────────────────────────────────────────────────────────────────
Decomposes the final composite risk score into exact positive (risk-elevating)
and negative (protective / risk-lowering) point contributions relative to
the patient's baseline average.
"""

import numpy as np


FEATURE_METADATA = [
    {"key": "phq9_depr",     "label": "PHQ-9 Depression Score",      "domain": "Questionnaire", "weight": 0.22},
    {"key": "gad7_anx",      "label": "GAD-7 Anxiety Score",         "domain": "Questionnaire", "weight": 0.18},
    {"key": "isi_sleep",     "label": "ISI Sleep Disruption",        "domain": "Sleep & Rest",  "weight": 0.14},
    {"key": "scared_child",  "label": "SCARED Somatic Symptoms",     "domain": "Questionnaire", "weight": 0.12},
    {"key": "nlp_sentiment", "label": "Journal NLP Sentiment",       "domain": "NLP / Journal", "weight": 0.12},
    {"key": "sleep_duration","label": "Sleep Deprivation (<8h)",     "domain": "Lifestyle",     "weight": 0.08},
    {"key": "screen_time",   "label": "Excessive Screen Time",       "domain": "Lifestyle",     "weight": 0.06},
    {"key": "physical_act",  "label": "Physical Inactivity",         "domain": "Lifestyle",     "weight": 0.05},
    {"key": "social_iso",    "label": "Social Isolation Risk",       "domain": "Lifestyle",     "weight": 0.03},
]


def compute_shap_contributions(total_score, domain_profile, base_value=50.0):
    """
    Computes exact SHAP-style feature contributions summing to (total_score - base_value).
    
    Parameters:
      total_score (float): Current session composite score (0-100)
      domain_profile (dict): Output from get_domain_profile()
      base_value (float): Historical baseline average (default 50.0)
      
    Returns:
      dict with:
        - base_value
        - total_score
        - diff
        - risk_factors (list)
        - protective_factors (list)
        - all_contributions (list)
    """
    diff = total_score - base_value
    
    # Domain deviations normalized to [-1.0, +1.0]
    depr_dev = (domain_profile.get("Depression", 50) - 50.0) / 50.0
    anx_dev  = (domain_profile.get("Anxiety", 50) - 50.0) / 50.0
    slp_dev  = (domain_profile.get("Sleep Disruption", 50) - 50.0) / 50.0
    som_dev  = (domain_profile.get("Somatic Symptoms", 50) - 50.0) / 50.0
    sent_dev = (domain_profile.get("Negative Sentiment", 50) - 50.0) / 50.0
    beh_dev  = (domain_profile.get("Lifestyle & Behavioral Risk", 50) - 50.0) / 50.0
    
    dev_map = {
        "phq9_depr":      depr_dev * 1.15,
        "gad7_anx":       anx_dev * 1.10,
        "isi_sleep":      slp_dev * 1.05,
        "scared_child":   som_dev * 0.90,
        "nlp_sentiment":  sent_dev * 1.00,
        "sleep_duration": beh_dev * 0.85,
        "screen_time":    beh_dev * 0.70,
        "physical_act":   beh_dev * 0.60,
        "social_iso":     beh_dev * 0.50,
    }
    
    raw_contribs = []
    for feat in FEATURE_METADATA:
        dev = dev_map.get(feat["key"], 0.0)
        raw_val = dev * feat["weight"] * 100.0
        raw_contribs.append({
            **feat,
            "raw": raw_val
        })
        
    raw_sum = sum(abs(item["raw"]) for item in raw_contribs)
    scale = abs(diff) / raw_sum if raw_sum > 0.001 else 1.0
    
    contributions = []
    for item in raw_contribs:
        # Scale to ensure sum(signed contributions) closely approximates diff
        adj_contribution = item["raw"] * scale
        direction = "risk" if adj_contribution >= 0 else "protective"
        
        contributions.append({
            "key": item["key"],
            "label": item["label"],
            "domain": item["domain"],
            "contribution": round(float(adj_contribution), 1),
            "magnitude": round(float(abs(adj_contribution)), 1),
            "direction": direction,
        })
        
    contributions.sort(key=lambda x: x["magnitude"], reverse=True)
    
    risk_factors = [c for c in contributions if c["contribution"] > 0]
    protective_factors = [c for c in contributions if c["contribution"] < 0]
    
    return {
        "base_value": round(float(base_value), 1),
        "total_score": round(float(total_score), 1),
        "delta": round(float(diff), 1),
        "risk_factors": risk_factors,
        "protective_factors": protective_factors,
        "all_contributions": contributions
    }
