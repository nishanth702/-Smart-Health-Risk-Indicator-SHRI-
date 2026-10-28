with open(r'smart_health_risk_indicator\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderPatientCards')
print(text[idx:idx+1200])
