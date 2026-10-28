with open(r'smart_health_risk_indicator\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('patient-card')
print(text[idx-100:idx+300])
