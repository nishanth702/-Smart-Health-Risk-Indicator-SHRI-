with open(r'smart_health_risk_indicator\js\app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'valView.style.display = "block"' in l:
        print(f"Line {i}: {l.strip()}")
        for k in range(max(0, i-10), min(len(lines), i+10)):
            print(f"  {k}: {lines[k].strip()}")
