with open(r'smart_health_risk_indicator\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function (?:open|select|view|load)Patient[^\)]*\)', text)
print("Patient funcs:", matches)

matches2 = re.findall(r'renderPatientRegistry[^\)]*\)', text)
print("Registry funcs:", matches2)
