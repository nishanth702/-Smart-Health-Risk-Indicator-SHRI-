/**
 * Real-Time Clinical NLP & Crisis Detection Engine (Client-Side JavaScript)
 */

const POSITIVE_LEXICON = {
    "happy": 1.0, "good": 0.7, "great": 0.9, "amazing": 1.2, "wonderful": 1.1, "love": 1.0,
    "excellent": 1.1, "joy": 1.2, "calm": 0.8, "peaceful": 1.0, "hopeful": 1.1, "grateful": 1.0,
    "strong": 0.8, "better": 0.9, "fine": 0.5, "okay": 0.4, "safe": 0.8, "friend": 0.7,
    "smile": 0.9, "laugh": 1.0, "excited": 0.9, "proud": 1.0, "confident": 1.1, "relaxed": 0.9,
    "energetic": 0.9, "motivated": 1.1, "supported": 1.0, "understood": 0.9, "cheerful": 1.0,
    "content": 0.8, "satisfied": 0.9, "playful": 0.8, "progress": 0.9, "improving": 1.0,
    "recovered": 1.2, "positive": 0.8, "connected": 0.9, "valued": 1.0, "worthy": 1.1, "capable": 0.9
};

const NEGATIVE_LEXICON = {
    "sad": 1.0, "bad": 0.7, "terrible": 1.3, "awful": 1.2, "hate": 1.1, "depressed": 1.5,
    "anxious": 1.3, "scared": 1.2, "alone": 1.1, "hopeless": 1.8, "worthless": 1.8,
    "useless": 1.5, "fail": 1.0, "stupid": 1.2, "tired": 0.8, "empty": 1.4, "numb": 1.5,
    "dark": 1.1, "dead": 1.8, "cry": 1.1, "hurt": 1.2, "pain": 1.3, "fear": 1.2, "worry": 1.0,
    "stress": 1.0, "dread": 1.4, "panic": 1.5, "nightmare": 1.4, "lost": 1.0, "angry": 1.1,
    "frustrated": 1.0, "overwhelmed": 1.4, "exhausted": 1.2, "lonely": 1.3, "trapped": 1.6,
    "broken": 1.5, "miserable": 1.4, "ashamed": 1.3, "guilty": 1.2, "confused": 0.8,
    "rejected": 1.4, "abandoned": 1.6, "unloved": 1.6, "suicidal": 2.5, "cutting": 2.0,
    "die": 2.0, "kill": 1.8, "suffer": 1.4, "unbearable": 1.7, "collapse": 1.3, "breakdown": 1.5
};

const CLINICAL_BIGRAMS = {
    "can't cope": 20, "cannot cope": 20, "want to die": 35, "no point": 18,
    "no hope": 22, "giving up": 18, "end it all": 35, "hurting myself": 30,
    "hurt myself": 30, "self harm": 28, "not eating": 12, "can't sleep": 10,
    "cannot sleep": 10, "panic attack": 15, "feeling better": -15, "much better": -18,
    "really good": -14, "doing well": -16, "made progress": -14, "less anxious": -12
};

const EMOJI_SENTIMENT = {
    "😊": -8, "😄": -10, "😁": -10, "🥰": -12, "😌": -8, "😎": -6,
    "😢": 10, "😭": 15, "😔": 10, "😞": 12, "😟": 10, "😰": 12, "😱": 15,
    "😠": 8, "😡": 12, "🤬": 15, "😩": 12, "😫": 14, "💔": 12, "😓": 10,
    "❤️": -8, "💪": -8, "✨": -5, "🌟": -6, "🙏": -4
};

const INTENSIFIERS = {
    "very": 1.6, "extremely": 2.0, "really": 1.5, "so": 1.4, "incredibly": 1.8,
    "absolutely": 1.7, "deeply": 1.7, "totally": 1.5, "completely": 1.6, "utterly": 1.8,
    "severely": 2.0, "highly": 1.6
};

const NEGATORS = new Set(["not", "no", "never", "don't", "doesn't", "didn't", "won't", "can't", "cannot", "barely", "hardly", "scarcely"]);

function analyzeSentimentDetailed(text) {
    if (!text || text.trim().length < 3) {
        return { score: 50, variance: 0, crisisFlags: [], dominantEmotion: "neutral", isCrisis: false };
    }

    let distressScore = 50.0;
    const crisisFlags = [];
    const sentenceScores = [];
    const lowerText = text.toLowerCase();

    // 1. Emoji Evaluation
    for (const [emoji, delta] of Object.entries(EMOJI_SENTIMENT)) {
        const count = (text.match(new RegExp(emoji, "g")) || []).length;
        if (count > 0) distressScore += delta * count;
    }

    // 2. Clinical Bigrams
    for (const [phrase, delta] of Object.entries(CLINICAL_BIGRAMS)) {
        if (lowerText.includes(phrase)) {
            distressScore += delta;
            if (delta >= 20) crisisFlags.push(phrase);
        }
    }

    // 3. Sentence-level Lexical Evaluation
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 2);
    sentences.forEach(s => {
        let sScore = 0.0;
        const words = s.toLowerCase().replace(/[.,!?;:]/g, " ").split(/\s+/).filter(Boolean);
        words.forEach((w, i) => {
            const prev = i > 0 ? words[i - 1] : "";
            const prev2 = i > 1 ? words[i - 2] : "";
            const negated = NEGATORS.has(prev) || NEGATORS.has(prev2);
            const boost = INTENSIFIERS[prev] || 1.0;

            if (POSITIVE_LEXICON[w] !== undefined) {
                const delta = POSITIVE_LEXICON[w] * 5.0 * boost;
                sScore += negated ? delta * 0.5 : -delta;
            }
            if (NEGATIVE_LEXICON[w] !== undefined) {
                const delta = NEGATIVE_LEXICON[w] * 6.0 * boost;
                sScore += negated ? -delta * 0.4 : delta;
            }
        });
        sentenceScores.push(sScore);
        distressScore += sScore;
    });

    const variance = sentenceScores.length > 1
        ? Math.sqrt(sentenceScores.map(v => v ** 2).reduce((a, b) => a + b, 0) / sentenceScores.length)
        : 0.0;

    const clampedDistress = Math.max(0, Math.min(100, distressScore));
    const posSentiment = Math.round(100.0 - clampedDistress);

    const posHits = Object.keys(POSITIVE_LEXICON).filter(w => lowerText.includes(w)).length;
    const negHits = Object.keys(NEGATIVE_LEXICON).filter(w => lowerText.includes(w)).length;

    let dominantEmotion = "neutral / mixed";
    if (negHits > posHits * 1.5 || crisisFlags.length > 0) dominantEmotion = "distress";
    else if (posHits > negHits * 1.5) dominantEmotion = "positive";

    return {
        score: posSentiment,
        variance: Math.round(variance * 10) / 10,
        crisisFlags,
        dominantEmotion,
        isCrisis: crisisFlags.length > 0 || posSentiment < 25
    };
}
