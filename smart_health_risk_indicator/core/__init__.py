"""
Smart Health Risk Indicator (SHRI) - Core ML, NLP & Clinical Analytics Package
"""
from .clinical_dataset import generate_hybrid_dataset
from .feature_engineering import extract_features, get_domain_profile
from .nlp_engine import analyze_sentiment_detailed, analyze_sentiment
from .models import SmartHealthEnsemble
from .xai_explainer import compute_shap_contributions
from .cbt_library import CBT_LIBRARY, get_recommendations

__all__ = [
    "generate_hybrid_dataset",
    "extract_features",
    "get_domain_profile",
    "analyze_sentiment_detailed",
    "analyze_sentiment",
    "SmartHealthEnsemble",
    "compute_shap_contributions",
    "CBT_LIBRARY",
    "get_recommendations",
]
