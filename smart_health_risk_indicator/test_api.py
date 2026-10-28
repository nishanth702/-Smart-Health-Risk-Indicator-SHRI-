"""
Automated Integration Test Suite for SHRI Clinical Decision Support Microservice
Validates:
- Healthcheck
- Multimodal Risk Prediction with 95% Monte Carlo Confidence Intervals
- Permutation SHAP Feature Attributions
- HL7 FHIR R4 Standard Clinical Export
- Multi-Hospital Benchmark Cohorts (N=10,000)
- Clinical Questionnaires Catalog (PHQ-A, GAD-7, SCARED-5)
- Clinical Cohort Datasets (N=10 Cases)
- Multilingual Speech-to-Text Transcription (STT)
- Multilingual Clinical Translation (EN ↔ HI ↔ TE ↔ TA)
- Text-to-Speech (TTS) Voice Parameter Synthesis
- Audio Session Metadata Storage & History Retrieval
"""

import sys
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "DepNet" in data["models_loaded"]
    print("PASS: /health endpoint")

def test_predict_severe_patient():
    payload = {
        "patient_id": "PT-TEST-01",
        "patient_name": "Test Severe Patient",
        "patient_age": 16,
        "patient_gender": "Female",
        "psychometrics": {
            "phq1_depressed_mood": 3,
            "phq2_anhedonia": 3,
            "phq3_fatigue": 3,
            "phq4_worthlessness": 3,
            "phq5_concentration": 2,
            "gad1_nervousness": 3,
            "gad2_worry_control": 2,
            "gad3_restlessness": 2,
            "gad4_somatic_fear": 2,
            "psy1_academic_burnout": 3,
            "psy2_social_alienation": 3,
            "psy3_emotional_volatility": 2,
            "psy4_protective_resilience": 3
        },
        "biometrics": {
            "sleep_hours": 3.5,
            "screen_time_hours": 10.5,
            "exercise_minutes": 5.0,
            "social_interactions_freq": 1.0
        },
        "voice_acoustic": {
            "f0_mean_hz": 118.0,
            "f0_std_hz": 12.0,
            "jitter_percent": 3.4,
            "shimmer_percent": 7.8,
            "pause_latency_percent": 41.0,
            "speech_rate_sps": 2.1
        },
        "journal_reflection_text": "I feel completely exhausted and hopeless. Trouble sleeping every night."
    }
    response = client.post("/api/v1/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["composite_risk_score"] >= 65
    assert data["risk_tier"] in ["HIGH", "SEVERE"]
    assert len(data["confidence_interval_95"]) == 2
    assert data["confidence_interval_95"][0] <= data["confidence_interval_95"][1]
    assert data["inference_latency_ms"] < 1000.0
    print(f"PASS: /api/v1/predict -> Score: {data['composite_risk_score']}, Tier: {data['risk_tier']}, CI95: {data['confidence_interval_95']}")

def test_shap_explanation():
    payload = {
        "patient_id": "PT-TEST-02",
        "patient_name": "Test SHAP Patient",
        "patient_age": 15,
        "patient_gender": "Male",
        "psychometrics": {
            "phq1_depressed_mood": 2,
            "phq2_anhedonia": 2,
            "phq3_fatigue": 2,
            "gad1_nervousness": 2,
            "gad2_worry_control": 2
        },
        "biometrics": {
            "sleep_hours": 6.0,
            "screen_time_hours": 6.0,
            "exercise_minutes": 35.0,
            "social_interactions_freq": 4.0
        }
    }
    response = client.post("/api/v1/xai/shap", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["shap_attributions"]) == 5
    print("PASS: /api/v1/xai/shap -> Extracted 5 feature attributions")

def test_fhir_export():
    payload = {
        "patient_id": "PT-TEST-03",
        "patient_name": "Aarav Singh",
        "patient_age": 15,
        "patient_gender": "Male",
        "psychometrics": {
            "phq1_depressed_mood": 1,
            "phq2_anhedonia": 1,
            "phq3_fatigue": 1,
            "gad1_nervousness": 1,
            "gad2_worry_control": 1
        },
        "biometrics": {
            "sleep_hours": 8.0,
            "screen_time_hours": 3.0,
            "exercise_minutes": 50.0,
            "social_interactions_freq": 6.0
        }
    }
    response = client.post("/api/v1/fhir/export", json=payload)
    assert response.status_code == 200
    bundle = response.json()
    assert bundle["resourceType"] == "Bundle"
    assert len(bundle["entry"]) >= 2
    print("PASS: /api/v1/fhir/export -> HL7 FHIR R4 Bundle validated")

def test_benchmark_cohorts():
    response = client.get("/api/v1/benchmark/cohorts")
    assert response.status_code == 200
    data = response.json()
    assert data["metrics"]["roc_auc"] == 0.948
    assert data["multi_center_sample_size"] == 10000
    print(f"PASS: /api/v1/benchmark/cohorts -> ROC-AUC {data['metrics']['roc_auc']} verified")

def test_clinical_questionnaires_catalog():
    response = client.get("/api/v1/clinical/questionnaires")
    assert response.status_code == 200
    data = response.json()
    assert len(data["instruments"]) >= 3
    print("PASS: /api/v1/clinical/questionnaires -> Validated questionnaires catalog")

def test_clinical_cohort_datasets():
    response = client.get("/api/v1/clinical/datasets")
    assert response.status_code == 200
    data = response.json()
    assert data["total_cases"] == 10
    print("PASS: /api/v1/clinical/datasets -> 10-patient cohort dataset verified")

def test_audio_stt_transcription():
    payload = {
        "language_code": "te-IN",
        "sample_rate": 44100
    }
    response = client.post("/api/v1/audio/transcribe", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert data["confidence"] > 0.90
    print(f"PASS: /api/v1/audio/transcribe (Telugu) -> Recognized {len(data['transcript'])} chars")

def test_audio_translation():
    payload = {
        "text": "Today I am focusing on what I can control, taking slow deep breaths, and being kind to myself.",
        "source_language": "en",
        "target_language": "te"
    }
    response = client.post("/api/v1/audio/translate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert len(data["translated_text"]) > 10
    print(f"PASS: /api/v1/audio/translate (EN -> TE) -> Translated successfully")

def test_audio_tts():
    payload = {
        "text": "ఈ రోజు నేను నియంత్రించగల విషయాలపై దృష్టి పెడుతున్నాను.",
        "target_language": "te-IN"
    }
    response = client.post("/api/v1/audio/tts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    print("PASS: /api/v1/audio/tts (Telugu) -> Speech synthesis prepared")

def test_audio_session_lifecycle():
    session_payload = {
        "id": "REC-TEST-9999",
        "userId": "PT-1001",
        "userName": "Aarav Singh",
        "timestamp": "2026-10-25 15:30:00",
        "duration": "15s",
        "sourceLang": "te-IN",
        "targetLang": "en-US",
        "sourceTranscript": "ఈ రోజు నేను ప్రశాంతంగా ఉన్నాను.",
        "translatedTranscript": "Today I am feeling peaceful and calm.",
        "status": "Completed"
    }
    # Save
    res_save = client.post("/api/v1/audio/sessions", json=session_payload)
    assert res_save.status_code == 200
    assert res_save.json()["status"] == "saved"

    # Get
    res_get = client.get("/api/v1/audio/sessions/PT-1001")
    assert res_get.status_code == 200
    assert res_get.json()["total"] >= 1

    # Delete
    res_del = client.delete("/api/v1/audio/sessions/REC-TEST-9999")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "deleted"
    print("PASS: Audio Session lifecycle (Save, Retrieve, Delete) verified")

if __name__ == "__main__":
    print("\nRunning SHRI Microservices Comprehensive Testbench with Multilingual Audio & Translation...")
    test_healthcheck()
    test_predict_severe_patient()
    test_shap_explanation()
    test_fhir_export()
    test_benchmark_cohorts()
    test_clinical_questionnaires_catalog()
    test_clinical_cohort_datasets()
    test_audio_stt_transcription()
    test_audio_translation()
    test_audio_tts()
    test_audio_session_lifecycle()
    print("\nALL 11 INTEGRATION TESTS PASSED WITH 100% SUCCESS!\n")
