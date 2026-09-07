/**
 * 20-Dimensional Multimodal Feature Engineering Engine (Client-Side JS)
 */

function computeTrend(history) {
    if (!history || history.length < 2) return 0.0;
    const recent = history.slice(-5);
    const n = recent.length;
    const xMean = (n - 1) / 2.0;
    const yMean = recent.reduce((a, b) => a + b, 0) / n;

    let num = 0, den = 0;
    recent.forEach((y, x) => {
        num += (x - xMean) * (y / 100.0 - yMean / 100.0);
        den += (x - xMean) ** 2;
    });

    if (den === 0) return 0.0;
    const slope = (num / den) * 10.0;
    return Math.max(-1.0, Math.min(1.0, slope));
}

function extractFeatures(questAnswers, behavioural, sentimentScore, age = 14, riskHistory = [], sentimentVariance = 0) {
    const subScore = (keys) => keys.map(k => questAnswers[k] ?? 0).reduce((a, b) => a + b, 0) / (keys.length * 3.0);

    const totalNorm   = Object.values(questAnswers).reduce((a, b) => a + b, 0) / (10 * 3.0);
    const deprNorm    = subScore(["q1", "q2", "q6"]);
    const anxNorm     = subScore(["q8", "q9", "q10"]);
    const sleepQNorm  = subScore(["q3", "q4"]);
    const somaticNorm = subScore(["q5"]);
    const cogNorm     = subScore(["q7"]);

    const sleepRisk  = Math.max(0, Math.min(1, (8.0 - (behavioural.sleepHours || 8)) / 6.0));
    const screenRisk = Math.min(1, (behavioural.screenTime || 3) / 12.0);
    const exerRisk   = Math.max(0, Math.min(1, (60.0 - (behavioural.exerciseMinutes || 45)) / 60.0));
    const socialRisk = Math.max(0, Math.min(1, (5.0 - (behavioural.socialInteractions || 4)) / 5.0));
    const appetiteR  = behavioural.appetiteChange ? 1.0 : 0.0;

    const sentNorm = sentimentScore / 100.0;
    const sentVar  = Math.min(1, sentimentVariance / 50.0);
    const ageNorm  = Math.max(0, Math.min(1, (age - 10.0) / 8.0));

    const deprAnx      = deprNorm * anxNorm;
    const sleepSent    = sleepRisk * (1.0 - sentNorm);
    const totalBehav   = (sleepRisk + screenRisk + exerRisk + socialRisk + appetiteR) / 5.0;
    const somaticSleep = somaticNorm * sleepRisk;

    const scoreTrend = computeTrend(riskHistory);
    const sessCount  = Math.min(1, riskHistory.length / 20.0);

    return [
        totalNorm, deprNorm, anxNorm, sleepQNorm, somaticNorm, cogNorm,
        sleepRisk, screenRisk, exerRisk, socialRisk, appetiteR,
        sentNorm, sentVar, ageNorm,
        deprAnx, sleepSent, totalBehav, somaticSleep,
        scoreTrend, sessCount
    ];
}

function getDomainProfile(questAnswers, behavioural, sentimentScore) {
    const sub = (keys) => Math.round(keys.map(k => questAnswers[k] ?? 0).reduce((a, b) => a + b, 0) / (keys.length * 3.0) * 100);

    let bScore = 0;
    const sHrs = behavioural.sleepHours || 8;
    const scrT = behavioural.screenTime || 3;
    const exM  = behavioural.exerciseMinutes || 45;
    const soc  = behavioural.socialInteractions || 4;

    if (sHrs < 6) bScore += 25; else if (sHrs < 7) bScore += 12;
    if (scrT > 6) bScore += 20; else if (scrT > 4) bScore += 10;
    if (exM < 20) bScore += 20; else if (exM < 30) bScore += 8;
    if (soc < 2) bScore += 20;
    if (behavioural.appetiteChange) bScore += 15;

    return {
        "Depression": sub(["q1", "q2", "q6"]),
        "Anxiety": sub(["q8", "q9", "q10"]),
        "Sleep Disruption": sub(["q3", "q4"]),
        "Somatic Symptoms": sub(["q5"]),
        "Concentration / Cognitive": sub(["q7"]),
        "Negative Sentiment": Math.max(0, Math.round(100 - sentimentScore)),
        "Lifestyle & Behavioral Risk": Math.min(100, bScore)
    };
}
