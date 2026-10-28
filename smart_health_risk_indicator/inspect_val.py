with open(r'smart_health_risk_indicator\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Occurrences of doctor-validation-view:")
for m in re.finditer(r'doctor-validation-view', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 200)
    print(text[start:end])
    print("---")
