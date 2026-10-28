"""
Natural Language Processing & Crisis Detection Engine
─────────────────────────────────────────────────────
Real-time clinical sentiment scoring with:
  - 90+ Word Positive & Negative Clinical Lexicons
  - 20 High-Risk Clinical Bigrams (Crisis / Self-Harm)
  - Intensifier Multipliers & Negation Inversion
  - Emoji Sentiment Polarities
  - Automated Crisis Escalation Alerts
"""

import re
import math


POSITIVE_LEXICON = {
    "happy": 1.0, "good": 0.7, "great": 0.9, "amazing": 1.2, "wonderful": 1.1, "love": 1.0,
    "excellent": 1.1, "joy": 1.2, "calm": 0.8, "peaceful": 1.0, "hopeful": 1.1, "grateful": 1.0,
    "strong": 0.8, "better": 0.9, "fine": 0.5, "okay": 0.4, "safe": 0.8, "friend": 0.7,
    "smile": 0.9, "laugh": 1.0, "excited": 0.9, "proud": 1.0, "confident": 1.1, "relaxed": 0.9,
    "energetic": 0.9, "motivated": 1.1, "supported": 1.0, "understood": 0.9, "cheerful": 1.0,
    "content": 0.8, "satisfied": 0.9, "playful": 0.8, "progress": 0.9, "improving": 1.0,
    "recovered": 1.2, "positive": 0.8, "connected": 0.9, "valued": 1.0, "worthy": 1.1, "capable": 0.9,
}

NEGATIVE_LEXICON = {
    "sad": 1.0, "bad": 0.7, "terrible": 1.3, "awful": 1.2, "hate": 1.1, "depressed": 1.5,
    "anxious": 1.3, "scared": 1.2, "alone": 1.1, "hopeless": 1.8, "worthless": 1.8,
    "useless": 1.5, "fail": 1.0, "stupid": 1.2, "tired": 0.8, "empty": 1.4, "numb": 1.5,
    "dark": 1.1, "dead": 1.8, "cry": 1.1, "hurt": 1.2, "pain": 1.3, "fear": 1.2, "worry": 1.0,
    "stress": 1.0, "dread": 1.4, "panic": 1.5, "nightmare": 1.4, "lost": 1.0, "angry": 1.1,
    "frustrated": 1.0, "overwhelmed": 1.4, "exhausted": 1.2, "lonely": 1.3, "trapped": 1.6,
    "broken": 1.5, "miserable": 1.4, "ashamed": 1.3, "guilty": 1.2, "confused": 0.8,
    "rejected": 1.4, "abandoned": 1.6, "unloved": 1.6, "suicidal": 2.5, "cutting": 2.0,
    "die": 2.0, "kill": 1.8, "suffer": 1.4, "unbearable": 1.7, "collapse": 1.3, "breakdown": 1.5,
}

CLINICAL_BIGRAMS = {
    "can't cope": +20, "cannot cope": +20, "want to die": +35, "no point": +18,
    "no hope": +22, "giving up": +18, "end it all": +35, "hurting myself": +30,
    "hurt myself": +30, "self harm": +28, "not eating": +12, "can't sleep": +10,
    "cannot sleep": +10, "panic attack": +15, "feeling better": -15, "much better": -18,
    "really good": -14, "doing well": -16, "made progress": -14, "less anxious": -12,
}

EMOJI_SENTIMENT = {
    "😊": -8, "😄": -10, "😁": -10, "🥰": -12, "😌": -8, "😎": -6,
    "😢": +10, "😭": +15, "😔": +10, "😞": +12, "😟": +10, "😰": +12, "😱": +15,
    "😠": +8, "😡": +12, "🤬": +15, "😩": +12, "😫": +14, "💔": +12, "😓": +10,
    "❤️": -8, "💪": -8, "✨": -5, "🌟": -6, "🙏": -4,
}

INTENSIFIERS = {
    "very": 1.6, "extremely": 2.0, "really": 1.5, "so": 1.4, "incredibly": 1.8,
    "absolutely": 1.7, "deeply": 1.7, "totally": 1.5, "completely": 1.6, "utterly": 1.8,
    "severely": 2.0, "highly": 1.6
}

NEGATORS = {"not", "no", "never", "don't", "doesn't", "didn't", "won't", "can't", "cannot", "barely", "hardly", "scarcely"}


def analyze_sentiment_detailed(text):
    """
    Analyzes raw text journal entries, outputting:
      - score (0 to 100): 100 = completely positive, 0 = severe distress
      - variance: sentence-level volatility
      - crisis_flags: list of triggered emergency keywords/bigrams
      - dominant_emotion: 'positive', 'distress', or 'neutral'
    """
    if not text or len(text.strip()) < 3:
        return {
            "score": 50.0,
            "variance": 0.0,
            "crisis_flags": [],
            "dominant_emotion": "neutral",
            "is_crisis": False
        }

    # Start at neutral 50
    distress_score = 50.0
    crisis_flags = []
    sentence_scores = []
    lower_text = text.lower()

    # 1. Emoji Sentiment
    for emoji_char, delta in EMOJI_SENTIMENT.items():
        count = text.count(emoji_char)
        if count > 0:
            distress_score += delta * count

    # 2. Clinical Bigrams & High-Risk phrases
    for phrase, delta in CLINICAL_BIGRAMS.items():
        if phrase in lower_text:
            distress_score += delta
            if delta >= 25:
                crisis_flags.append(phrase)

    # 3. Sentence-level lexical evaluation
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if len(s.strip()) > 2]
    for s in sentences:
        s_score = 0.0
        words = re.sub(r"[.,!?;:]", " ", s.lower()).split()
        for i, w in enumerate(words):
            prev = words[i - 1] if i > 0 else ""
            prev2 = words[i - 2] if i > 1 else ""
            negated = (prev in NEGATORS) or (prev2 in NEGATORS)
            boost = INTENSIFIERS.get(prev, 1.0)

            if w in POSITIVE_LEXICON:
                delta = POSITIVE_LEXICON[w] * 5.0 * boost
                s_score += (+delta * 0.5) if negated else (-delta)
            if w in NEGATIVE_LEXICON:
                delta = NEGATIVE_LEXICON[w] * 6.0 * boost
                s_score += (-delta * 0.4) if negated else (+delta)

        sentence_scores.append(s_score)
        distress_score += s_score

    # Variance computation across sentences
    if len(sentence_scores) > 1:
        mean_s = sum(sentence_scores) / len(sentence_scores)
        variance = math.sqrt(sum((s - mean_s) ** 2 for s in sentence_scores) / len(sentence_scores))
    else:
        variance = 0.0

    # Invert distress score to positive sentiment scale (100 = peaceful/happy, 0 = severe crisis)
    clamped_distress = max(0.0, min(100.0, distress_score))
    pos_sentiment = round(100.0 - clamped_distress, 1)

    pos_hits = sum(1 for w in POSITIVE_LEXICON if w in lower_text)
    neg_hits = sum(1 for w in NEGATIVE_LEXICON if w in lower_text)

    if neg_hits > pos_hits * 1.5 or len(crisis_flags) > 0:
        dominant_emotion = "distress"
    elif pos_hits > neg_hits * 1.5:
        dominant_emotion = "positive"
    else:
        dominant_emotion = "neutral / mixed"

    return {
        "score": float(pos_sentiment),
        "variance": float(round(variance, 1)),
        "crisis_flags": crisis_flags,
        "dominant_emotion": dominant_emotion,
        "is_crisis": len(crisis_flags) > 0 or pos_sentiment < 20.0
    }


def analyze_sentiment(text):
    """Returns scalar sentiment score (0 to 100)."""
    return analyze_sentiment_detailed(text)["score"]
