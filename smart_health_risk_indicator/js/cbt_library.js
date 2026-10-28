/**
 * CBT Interventions & FHIR Export Engine (Client-Side JS)
 */

const CBT_DATA = {
    depression: [
        {
            title: "Behavioral Activation & Micro-Scheduling",
            grade: "Grade A (NICE Guidelines)",
            desc: "Schedule 1 small, pleasurable mastery activity daily (15-min walk, drawing) to break depressive inertia and restore dopamine feedback loops.",
            domain: "Depression / Anhedonia",
            milestone: "Complete 5 scheduled activities in 7 days"
        },
        {
            title: "Cognitive Restructuring (3C Model)",
            grade: "Grade A (Beck Institute)",
            desc: "Catch negative automatic thoughts ('I fail at everything'), Check the objective evidence, and Change to a balanced realistic alternative.",
            domain: "Depression / Cognitive Distortions",
            milestone: "Log 3 automatic thought records per week"
        }
    ],
    anxiety: [
        {
            title: "Physiological Grounding & 4-7-8 Diaphragmatic Breathing",
            grade: "Grade A (Physiological Reg)",
            desc: "Inhale 4s through nose, hold 7s, exhale 8s with pursed lips. Stimulates the vagus nerve and activates the parasympathetic relaxation response.",
            domain: "Anxiety / Somatic Hyperarousal",
            milestone: "Practice 2 sessions daily for 14 days"
        },
        {
            title: "Graded Exposure Hierarchy (Systematic Desensitization)",
            grade: "Grade A (Gold Standard)",
            desc: "Build a 1–10 fear ladder for anxiety triggers (social interactions, speaking up) and systematically expose in safe micro-steps.",
            domain: "Generalized & Social Anxiety",
            milestone: "Conquer 2 rungs on fear hierarchy within 3 weeks"
        }
    ],
    sleep: [
        {
            title: "Stimulus Control Therapy (Bed = Sleep Only)",
            grade: "Grade A (AASM Guidelines)",
            desc: "Remove smartphones/screens from bed. If awake after 20 minutes, get out of bed and engage in a dim-light non-stimulating activity until drowsy.",
            domain: "Insomnia / Sleep Latency",
            milestone: "Achieve zero screen usage in bed for 10 days"
        }
    ],
    lifestyle: [
        {
            title: "Digital Sunsetting & Blue-Light Curfew",
            grade: "Grade B (Digital Hygiene)",
            desc: "Establish a digital curfew 60 minutes prior to bedtime and limit recreational screen time to under 3.5 hours/day.",
            domain: "Digital Overload / Sleep Quality",
            milestone: "Reduce average screen time by 1.5 hours daily"
        }
    ]
};

function getRecommendations(score, domainProfile) {
    const recs = [];
    const depr = domainProfile["Depression"] || 0;
    const anx  = domainProfile["Anxiety"] || 0;
    const slp  = domainProfile["Sleep Disruption"] || 0;

    if (depr >= anx && depr >= 30) {
        recs.push(...CBT_DATA.depression);
    } else if (anx > depr && anx >= 30) {
        recs.push(...CBT_DATA.anxiety);
    } else {
        recs.push(CBT_DATA.anxiety[0], CBT_DATA.depression[0]);
    }

    if (slp >= 35 || domainProfile["Lifestyle & Behavioral Risk"] >= 40) {
        recs.push(CBT_DATA.sleep[0]);
        recs.push(CBT_DATA.lifestyle[0]);
    }

    return recs.slice(0, 4);
}

function classifyRisk(score) {
    if (score < 20) return { label: "Tier 1: Minimal Risk", badge: "badge-minimal", color: "#10B981", desc: "Symptoms within healthy normative bounds. Continued wellness monitoring." };
    if (score < 40) return { label: "Tier 2: Mild Risk", badge: "badge-mild", color: "#3B82F6", desc: "Mild sub-clinical symptoms. Digital psychoeducation and lifestyle self-care recommended." };
    if (score < 60) return { label: "Tier 3: Moderate Risk", badge: "badge-moderate", color: "#F59E0B", desc: "Moderate symptoms. Active clinician check-in and targeted CBT protocol recommended." };
    if (score < 80) return { label: "Tier 4: High Risk", badge: "badge-high", color: "#F97316", desc: "High clinical risk. Prioritize clinical safety review and formal psychiatric assessment." };
    return { label: "Tier 5: Severe Risk", badge: "badge-severe", color: "#EF4444", desc: "Critical clinical severity. Immediate clinical escalation and emergency safety planning required." };
}

function generateFHIRJSON(patientName, score, ci, domainProfile, recs) {
    return {
        resourceType: "DiagnosticReport",
        id: "shri-assessment-" + Date.now(),
        status: "final",
        category: [{ coding: [{ system: "http://terminology.hl7.org/CodeSystem/v2-0074", code: "MB", display: "Behavioral Health" }] }],
        code: { coding: [{ system: "http://loinc.org", code: "96767-9", display: "Mental Health Risk Assessment" }] },
        subject: { display: patientName },
        effectiveDateTime: new Date().toISOString(),
        issued: new Date().toISOString(),
        conclusion: `Smart Health Risk Score: ${score}/100 with 95% CI [${ci[0]} - ${ci[1]}]. Clinical Tier: ${classifyRisk(score).label}`,
        domainScores: domainProfile,
        recommendedActions: recs.map(r => r.title)
    };
}
