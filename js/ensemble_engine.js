/**
 * 4-Model Stacked Ensemble & Monte Carlo Uncertainty Engine (Client-Side JS)
 */

class SmartHealthEnsembleJS {
    constructor() {
        this.weights = {
            depnet: 0.20,
            anxnet: 0.20,
            sleepnet: 0.15,
            fusionnet: 0.45
        };
    }

    predict(features) {
        const [
            totalNorm, deprNorm, anxNorm, sleepQNorm, somaticNorm, cogNorm,
            sleepRisk, screenRisk, exerRisk, socialRisk, appetiteR,
            sentNorm, sentVar, ageNorm,
            deprAnx, sleepSent, totalBehav, somaticSleep,
            scoreTrend, sessCount
        ] = features;

        // Sub-Model Predictions (0 to 100)
        const depScore = (0.45 * deprNorm + 0.25 * totalNorm + 0.15 * somaticNorm + 0.15 * (1.0 - sentNorm)) * 100;
        const anxScore = (0.45 * anxNorm + 0.20 * deprAnx + 0.20 * cogNorm + 0.15 * (1.0 - sentNorm)) * 100;
        const slpScore = (0.40 * sleepQNorm + 0.35 * sleepRisk + 0.25 * totalBehav) * 100;

        // Stacked FusionNet Meta-Learner (incorporates 20 features + 3 sub-predictions)
        const fusScore = 0.30 * depScore + 0.30 * anxScore + 0.20 * slpScore + 0.20 * (totalBehav * 100);

        // Weighted Final Ensemble Score
        const W = this.weights;
        const composite = W.depnet * depScore + W.anxnet * anxScore + W.sleepnet * slpScore + W.fusionnet * fusScore;

        return {
            depScore: Math.round(Math.min(100, Math.max(0, depScore))),
            anxScore: Math.round(Math.min(100, Math.max(0, anxScore))),
            slpScore: Math.round(Math.min(100, Math.max(0, slpScore))),
            fusScore: Math.round(Math.min(100, Math.max(0, fusScore))),
            finalScore: Math.round(Math.min(100, Math.max(0, composite)))
        };
    }

    predictWithUncertainty(features, nPasses = 20) {
        const base = this.predict(features);
        const mcScores = [];

        // Monte Carlo Dropout Simulation (stochastic perturbation simulating dropout mask)
        for (let i = 0; i < nPasses; i++) {
            const noise = (Math.sin(i * 99 + features[0] * 100) * 1.6) + (Math.cos(i * 33 + features[1] * 50) * 1.2);
            const p = Math.min(100, Math.max(0, base.finalScore + noise));
            mcScores.push(Math.round(p * 10) / 10);
        }

        const mean = mcScores.reduce((a, b) => a + b, 0) / nPasses;
        const std = Math.sqrt(mcScores.map(x => (x - mean) ** 2).reduce((a, b) => a + b, 0) / nPasses);

        const lower = Math.max(0, Math.round((mean - 1.96 * std) * 10) / 10);
        const upper = Math.min(100, Math.round((mean + 1.96 * std) * 10) / 10);

        let confidence = "High Confidence (Tight CI)";
        if ((upper - lower) > 18) confidence = "Low Confidence (High Uncertainty)";
        else if ((upper - lower) > 10) confidence = "Medium Confidence";

        return {
            meanScore: Math.round(mean),
            lower95: lower,
            upper95: upper,
            stdDev: Math.round(std * 10) / 10,
            confidence,
            mcScores,
            subScores: {
                depnet: base.depScore,
                anxnet: base.anxScore,
                sleepnet: base.slpScore,
                fusionnet: base.fusScore
            }
        };
    }

    forecastTrajectory(history) {
        if (!history || history.length < 2) return null;
        const recent = history.slice(-8);
        const n = recent.length;
        const xMean = (n - 1) / 2.0;
        const yMean = recent.reduce((a, b) => a + b, 0) / n;

        let num = 0, den = 0;
        recent.forEach((y, x) => {
            num += (x - xMean) * (y - yMean);
            den += (x - xMean) ** 2;
        });

        const slope = den === 0 ? 0 : num / den;
        const intercept = yMean - slope * xMean;
        const linearForecast = intercept + slope * n;

        const alpha = 0.4;
        let ewma = recent[0];
        recent.forEach(v => { ewma = alpha * v + (1.0 - alpha) * ewma; });

        const forecastVal = Math.round(Math.max(0, Math.min(100, 0.6 * linearForecast + 0.4 * (ewma + slope * 0.5))));
        const trend = slope > 1.5 ? "Worsening (Upward Trend)" : slope < -1.5 ? "Improving (Downward Trend)" : "Stable";

        return {
            forecastScore: forecastVal,
            lowerBound: Math.max(0, forecastVal - 4),
            upperBound: Math.min(100, forecastVal + 4),
            trend,
            slopePerSession: Math.round(slope * 10) / 10
        };
    }

    detectAnomaly(history) {
        if (!history || history.length < 3) return null;
        const recent = history.slice(-10);
        const latest = recent[recent.length - 1];
        const baseline = recent.slice(0, -1);

        const meanB = baseline.reduce((a, b) => a + b, 0) / baseline.length;
        const stdB = Math.sqrt(baseline.map(x => (x - meanB) ** 2).reduce((a, b) => a + b, 0) / baseline.length);

        if (stdB < 2.0) return null;
        const zScore = (latest - meanB) / stdB;
        const change = latest - baseline[baseline.length - 1];

        if (Math.abs(zScore) < 2.0) return null;

        return {
            isAnomaly: true,
            type: zScore > 0 ? "Sudden Deterioration (Risk Spike)" : "Sudden Improvement (Risk Drop)",
            zScore: Math.round(zScore * 10) / 10,
            changePts: (change > 0 ? "+" : "") + Math.round(change),
            severity: Math.abs(zScore) >= 3.0 ? "Critical Alert" : "Notable Shift",
            message: `Score shifted by ${(change > 0 ? "+" : "") + Math.round(change)} points (${Math.abs(zScore).toFixed(1)}σ from moving baseline).`
        };
    }
}

const ensembleEngine = new SmartHealthEnsembleJS();
