with open(r'smart_health_risk_indicator\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print('Doctor IDs:', re.findall(r'id=["\'](doctor-[^"\']+)["\']', text))
print('Patient IDs:', re.findall(r'id=["\'](patient-[^"\']+)["\']', text))
print('Nav items:', re.findall(r'class=["\'][^"\']*nav-[^"\']*["\'][^>]*>(.*?)<', text))
