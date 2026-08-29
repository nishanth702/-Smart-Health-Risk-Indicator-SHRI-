"""
CBT & Clinical Intervention Library for Smart Health Risk Indicator (SHRI)
"""

CBT_LIBRARY = {
    "depression": [
        {
            "id": "cbt-dep-1",
            "title": "Behavioral Activation & Micro-Scheduling",
            "evidence_grade": "Grade A (NICE Guidelines)",
            "description": "Schedule 1 small, pleasurable mastery activity daily (e.g. 15-minute walk, drawing) to break depressive inertia and restore dopamine feedback loops.",
            "target_domain": "Depression / Anhedonia",
            "milestone": "Complete 5 scheduled activities in 7 days"
        },
        {
            "id": "cbt-dep-2",
            "title": "Cognitive Restructuring (3C Model)",
            "evidence_grade": "Grade A (Beck Institute)",
            "description": "Catch negative automatic thoughts ('I fail at everything'), Check the objective evidence, and Change to a balanced realistic alternative.",
            "target_domain": "Depression / Cognitive Distortions",
            "milestone": "Log 3 automatic thought records per week"
        },
        {
            "id": "cbt-dep-3",
            "title": "Gratitude & Positive Savoring Journaling",
            "evidence_grade": "Grade B (Empirically Supported)",
            "description": "Write down 3 specific things that went well each evening before bed to retrain attentional bias away from depressive rumination.",
            "target_domain": "Mood / Rumination",
            "milestone": "Maintain 10 consecutive daily logs"
        }
    ],
    "anxiety": [
        {
            "id": "cbt-anx-1",
            "title": "Physiological Grounding & 4-7-8 Diaphragmatic Breathing",
            "evidence_grade": "Grade A (Physiological Reg)",
            "description": "Inhale 4s through nose, hold 7s, exhale 8s with pursed lips. Stimulates the vagus nerve and activates the parasympathetic relaxation response.",
            "target_domain": "Anxiety / Somatic Hyperarousal",
            "milestone": "Practice 2 sessions daily for 14 days"
        },
        {
            "id": "cbt-anx-2",
            "title": "Graded Exposure Hierarchy (Systematic Desensitization)",
            "evidence_grade": "Grade A (Gold Standard)",
            "description": "Build a 1–10 fear ladder for anxiety triggers (e.g. social interactions, speaking up) and systematically expose in safe micro-steps.",
            "target_domain": "Generalized & Social Anxiety",
            "milestone": "Conquer 2 rungs on fear hierarchy within 3 weeks"
        },
        {
            "id": "cbt-anx-3",
            "title": "Worry Time Postponement Technique",
            "evidence_grade": "Grade B (CBT Standard)",
            "description": "Designate a fixed 15-minute daily 'Worry Window'. Whenever anxious intrusive thoughts arise during the day, jot them down and postpone review.",
            "target_domain": "Cognitive Worry / Overthinking",
            "milestone": "Postpone daily intrusive rumination 5 times"
        }
    ],
    "sleep": [
        {
            "id": "cbt-slp-1",
            "title": "Stimulus Control Therapy (Bed = Sleep Only)",
            "evidence_grade": "Grade A (AASM Guidelines)",
            "description": "Remove smartphones/screens from bed. If awake after 20 minutes, get out of bed and engage in a dim-light non-stimulating activity until drowsy.",
            "target_domain": "Insomnia / Sleep Latency",
            "milestone": "Achieve zero screen usage in bed for 10 days"
        },
        {
            "id": "cbt-slp-2",
            "title": "Circadian Anchoring & Sleep Restriction",
            "evidence_grade": "Grade A (Sleep Medicine)",
            "description": "Maintain a strict, identical wake-up time 7 days a week, regardless of total hours slept, to stabilize circadian melatonin oscillation.",
            "target_domain": "Circadian Rhythm / Sleep Quality",
            "milestone": "Consistent wake-time within ±15 minutes for 2 weeks"
        }
    ],
    "lifestyle": [
        {
            "id": "cbt-lif-1",
            "title": "Digital Sunsetting & Blue-Light Reduction",
            "evidence_grade": "Grade B (Digital Hygiene)",
            "description": "Establish a digital curfew 60 minutes prior to bedtime and limit recreational screen time to under 3.5 hours/day.",
            "target_domain": "Digital Overload / Sleep Quality",
            "milestone": "Reduce average screen time by 1.5 hours daily"
        },
        {
            "id": "cbt-lif-2",
            "title": "Aerobic Micro-Burst Protocol",
            "evidence_grade": "Grade A (Neurogenesis & BDNF)",
            "description": "Engage in 25–30 minutes of moderate cardiovascular movement (cycling, brisk walking, sports) 4 times a week.",
            "target_domain": "Physical Activity / Somatic Vigor",
            "milestone": "Log 120 minutes of moderate activity weekly"
        }
    ]
}


def get_recommendations(score, domain_profile):
    """
    Selects evidence-based CBT interventions based on composite risk score and dominant symptom domain.
    """
    recs = []
    depr_s = domain_profile.get("Depression", 0)
    anx_s = domain_profile.get("Anxiety", 0)
    slp_s = domain_profile.get("Sleep Disruption", 0)

    if depr_s >= anx_s and depr_s >= 30:
        recs.extend(CBT_LIBRARY["depression"])
    elif anx_s > depr_s and anx_s >= 30:
        recs.extend(CBT_LIBRARY["anxiety"])
    else:
        recs.extend(CBT_LIBRARY["anxiety"][:1] + CBT_LIBRARY["depression"][:1])

    if slp_s >= 35 or domain_profile.get("Lifestyle & Behavioral Risk", 0) >= 40:
        recs.extend(CBT_LIBRARY["sleep"])
        recs.extend(CBT_LIBRARY["lifestyle"][:1])

    return recs[:4]


def classify_risk(score):
    """
    Maps continuous 0-100 risk score to 5 clinical risk tiers.
    """
    if score < 20:
        return {"label": "Minimal Risk", "tier": 1, "color": "#10B981", "badge": "success", "description": "Symptoms within healthy normative bounds. Continued wellness monitoring."}
    elif score < 40:
        return {"label": "Mild Risk", "tier": 2, "color": "#3B82F6", "badge": "info", "description": "Mild sub-clinical symptoms. Digital psychoeducation and lifestyle self-care recommended."}
    elif score < 60:
        return {"label": "Moderate Risk", "tier": 3, "color": "#F59E0B", "badge": "warning", "description": "Moderate symptoms. Active clinician check-in and targeted CBT protocol recommended."}
    elif score < 80:
        return {"label": "High Risk", "tier": 4, "color": "#F97316", "badge": "warning", "description": "High clinical risk. Prioritize clinical safety review and formal psychiatric assessment."}
    else:
        return {"label": "Severe Risk", "tier": 5, "color": "#EF4444", "badge": "danger", "description": "Critical clinical severity. Immediate clinical escalation and emergency safety planning required."}
