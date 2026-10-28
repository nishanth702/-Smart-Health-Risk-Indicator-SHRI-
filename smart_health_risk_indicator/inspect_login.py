with open(r'smart_health_risk_indicator\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="doctor-login-form"')
print(text[idx:idx+800])
