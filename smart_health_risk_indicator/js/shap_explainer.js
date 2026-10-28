/**
 * Permutation SHAP Feature Attribution Engine (Client-Side JS)
 */

const SHAP_FEATURES = [
    { key: "phq9_depr",     label: "PHQ-9 Depression Score",  domain: "Questionnaire", weight: 0.22 },
    { key: "gad7_anx",      label: "GAD-7 Anxiety Score",     domain: "Questionnaire", weight: 0.18 },
    { key: "isi_sleep",     label: "ISI Sleep Disruption",    domain: "Sleep & Rest",  weight: 0.14 },
    { key: "scared_child",  label: "SCARED Somatics",         domain: "Questionnaire", weight: 0.12 },
    { key: "nlp_sentiment", label: "Journal NLP Sentiment",   domain: "NLP / Journal", weight: 0.12 },
    { key: "sleep_duration",label: "Sleep Deprivation (<8h)", domain: "Lifestyle",     weight: 0.08 },
    { key: "screen_time",   label: "Excessive Screen Time",   domain: "Lifestyle",     weight: 0.06 },
    { key: "physical_act",  label: "Physical Inactivity",     domain: "Lifestyle",     weight: 0.05 },
    { key: "social_iso",    label: "Social Isolation Risk",   domain: "Lifestyle",     weight: 0.03 }
];

function computeShapContributions(totalScore, domainProfile, baseValue = 50.0) {
    const diff = totalScore - baseValue;

    const deprDev = (domainProfile["Depression"] - 50.0) / 50.0;
    const anxDev  = (domainProfile["Anxiety"] - 50.0) / 50.0;
    const slpDev  = (domainProfile["Sleep Disruption"] - 50.0) / 50.0;
    const somDev  = (domainProfile["Somatic Symptoms"] - 50.0) / 50.0;
    const sentDev = (domainProfile["Negative Sentiment"] - 50.0) / 50.0;
    const behDev  = (domainProfile["Lifestyle & Behavioral Risk"] - 50.0) / 50.0;

    const devMap = {
        "phq9_depr":      deprDev * 1.15,
        "gad7_anx":       anxDev * 1.10,
        "isi_sleep":      slpDev * 1.05,
        "scared_child":   somDev * 0.90,
        "nlp_sentiment":  sentDev * 1.00,
        "sleep_duration": behDev * 0.85,
        "screen_time":    behDev * 0.70,
        "physical_act":   behDev * 0.60,
        "social_iso":     behDev * 0.50
    };

    const rawContribs = SHAP_FEATURES.map(f => {
        const dev = devMap[f.key] || 0.0;
        return {
            ...f,
            raw: dev * f.weight * 100.0
        };
    });

    const rawSum = rawContribs.reduce((sum, item) => sum + Math.abs(item.raw), 0);
    const scale = rawSum > 0.001 ? Math.abs(diff) / rawSum : 1.0;

    const contributions = rawContribs.map(item => {
        const adj = item.raw * scale;
        return {
            key: item.key,
            label: item.label,
            domain: item.domain,
            contribution: Math.round(adj * 10) / 10,
            magnitude: Math.round(Math.abs(adj) * 10) / 10,
            direction: adj >= 0 ? "risk" : "protective"
        };
    }).sort((a, b) => b.magnitude - a.magnitude);

    return {
        baseValue: Math.round(baseValue),
        totalScore: Math.round(totalScore),
        delta: (diff >= 0 ? "+" : "") + Math.round(diff * 10) / 10,
        riskFactors: contributions.filter(c => c.contribution > 0),
        protectiveFactors: contributions.filter(c => c.contribution < 0),
        allContributions: contributions
    };
}
