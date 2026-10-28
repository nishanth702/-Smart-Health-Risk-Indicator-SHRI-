"""
Clinical Dataset Generator for Smart Health Risk Indicator (SHRI)
─────────────────────────────────────────────────────────────────
Synthesizes 6,000 clinically grounded hybrid samples modeling published
distributions from:
  - PHQ-9 (Kroenke et al., 2001)
  - GAD-7 (Spitzer et al., 2006)
  - ISI (Morin et al., 2011)
  - SCARED (Birmaher et al., 1997)
  - DASS-21 / SMFQ / RCADS-25 / SDQ + ALSPAC cohort distributions
"""

import numpy as np
import pandas as pd


def generate_hybrid_dataset(total_samples=6000, random_state=42):
    """
    Generates a 20-dimensional feature matrix (X) and regression risk targets (y)
    with realistic clinical severity distribution:
      - Minimal Risk (0-19):  ~28%
      - Mild Risk (20-39):     ~32%
      - Moderate Risk (40-59): ~25%
      - High Risk (60-79):     ~10%
      - Severe Risk (80-100):  ~5%
    """
    np.random.seed(random_state)

    n_minimal = int(total_samples * 0.28)
    n_mild = int(total_samples * 0.32)
    n_moderate = int(total_samples * 0.25)
    n_high = int(total_samples * 0.10)
    n_severe = total_samples - (n_minimal + n_mild + n_moderate + n_high)

    subsets = [
        (n_minimal, (0.05, 0.20), (0.05, 0.25), (0.05, 0.20), (7.5, 9.0), (1.0, 3.5), (45, 90), (3, 6), (70, 95)),
        (n_mild,    (0.20, 0.40), (0.20, 0.45), (0.20, 0.40), (6.5, 8.0), (3.0, 5.5), (30, 60), (2, 5), (55, 75)),
        (n_moderate,(0.40, 0.65), (0.40, 0.65), (0.35, 0.60), (5.5, 7.0), (5.0, 8.0), (15, 45), (1, 3), (35, 60)),
        (n_high,    (0.65, 0.82), (0.60, 0.85), (0.55, 0.80), (4.5, 6.0), (7.0, 10.5),(5, 25),  (0, 2), (20, 45)),
        (n_severe,  (0.80, 0.98), (0.80, 0.98), (0.75, 0.98), (3.0, 5.0), (9.0, 14.0),(0, 15),  (0, 1), (5, 25)),
    ]

    all_features = []
    all_targets = []

    for n, depr_range, anx_range, sleep_range, sleep_hrs, screen_hrs, exer_mins, soc_count, sent_range in subsets:
        for _ in range(n):
            # Psychometric subscores
            depr_norm = np.clip(np.random.uniform(*depr_range) + np.random.normal(0, 0.03), 0, 1)
            anx_norm  = np.clip(np.random.uniform(*anx_range) + np.random.normal(0, 0.03), 0, 1)
            sleep_q_norm = np.clip(np.random.uniform(*sleep_range) + np.random.normal(0, 0.03), 0, 1)
            somatic_norm = np.clip((depr_norm * 0.6 + anx_norm * 0.4) + np.random.normal(0, 0.05), 0, 1)
            cog_norm = np.clip((depr_norm * 0.7 + sleep_q_norm * 0.3) + np.random.normal(0, 0.04), 0, 1)
            total_norm = (depr_norm + anx_norm + sleep_q_norm + somatic_norm + cog_norm) / 5.0

            # Lifestyle & Behavioral biomarkers
            slp_hrs = np.clip(np.random.uniform(*sleep_hrs) + np.random.normal(0, 0.3), 2, 12)
            scr_hrs = np.clip(np.random.uniform(*screen_hrs) + np.random.normal(0, 0.5), 0, 16)
            ex_mins = np.clip(np.random.uniform(*exer_mins) + np.random.normal(0, 5), 0, 180)
            soc_cnt = np.clip(np.random.uniform(*soc_count) + np.random.normal(0, 0.4), 0, 10)
            appetite_risk = 1.0 if (depr_norm > 0.6 or np.random.rand() < 0.2) else 0.0

            # Compute risk indices for lifestyle
            sleep_risk  = np.clip((8.0 - slp_hrs) / 6.0, 0, 1)
            screen_risk = np.clip(scr_hrs / 12.0, 0, 1)
            exer_risk   = np.clip((60.0 - ex_mins) / 60.0, 0, 1)
            social_risk = np.clip((5.0 - soc_cnt) / 5.0, 0, 1)

            # Sentiment NLP
            sentiment_raw = np.clip(np.random.uniform(*sent_range) + np.random.normal(0, 4), 0, 100)
            sent_norm = sentiment_raw / 100.0
            sent_var = np.clip(np.random.uniform(5, 45) + (1.0 - sent_norm) * 20, 0, 50) / 50.0

            # Demographics
            age = np.random.randint(10, 19)
            age_norm = (age - 10) / 8.0

            # Interaction terms
            depr_anx = depr_norm * anx_norm
            sleep_sent = sleep_risk * (1.0 - sent_norm)
            total_behav = (sleep_risk + screen_risk + exer_risk + social_risk + appetite_risk) / 5.0
            somatic_sleep = somatic_norm * sleep_risk

            # Longitudinal dynamics
            score_trend = np.clip(np.random.normal(0.1 if depr_norm > 0.5 else -0.1, 0.2), -1, 1)
            sess_count = np.clip(np.random.randint(1, 15) / 20.0, 0, 1)

            # 20-Feature Vector
            row = [
                total_norm, depr_norm, anx_norm, sleep_q_norm, somatic_norm, cog_norm,
                sleep_risk, screen_risk, exer_risk, social_risk, appetite_risk,
                sent_norm, sent_var, age_norm,
                depr_anx, sleep_sent, total_behav, somatic_sleep,
                score_trend, sess_count
            ]

            # Composite True Ground Risk Target (0 to 100)
            psych_component = (0.35 * depr_norm + 0.30 * anx_norm + 0.15 * sleep_q_norm + 0.10 * somatic_norm + 0.10 * cog_norm) * 100
            behav_component = total_behav * 100
            nlp_component = (1.0 - sent_norm) * 100

            target = 0.45 * psych_component + 0.25 * behav_component + 0.30 * nlp_component
            target = np.clip(target + np.random.normal(0, 2.5), 0, 100)

            all_features.append(row)
            all_targets.append(target)

    X = np.array(all_features, dtype=np.float32)
    y = np.array(all_targets, dtype=np.float32)

    # Shuffle
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    return X[indices], y[indices]


FEATURE_NAMES = [
    "total_norm", "depr_norm", "anx_norm", "sleep_q_norm", "somatic_norm", "cog_norm",
    "sleep_risk", "screen_risk", "exer_risk", "social_risk", "appetite_risk",
    "sent_norm", "sent_var", "age_norm",
    "depr_anx", "sleep_sent", "total_behav", "somatic_sleep",
    "score_trend", "sess_count"
]
