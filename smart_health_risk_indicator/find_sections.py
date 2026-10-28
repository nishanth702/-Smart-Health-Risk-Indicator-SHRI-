with open(r'smart_health_risk_indicator\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("IDs with voice:")
for m in re.finditer(r'id=["\']([^"\']*voice[^"\']*)["\']', text, re.IGNORECASE):
    print("  id:", m.group(1))

print("\nAll Section IDs:")
for m in re.finditer(r'<section[^>]*id=["\']([^"\']*)["\']', text):
    print("  section id:", m.group(1))

print("\nAll Buttons with IDs or onclick:")
for m in re.finditer(r'<button[^>]*(?:id|onclick)=["\']([^"\']*)["\'][^>]*>(.*?)</button>', text, re.DOTALL):
    print("  btn:", m.group(1), "text:", m.group(2).strip()[:40])
