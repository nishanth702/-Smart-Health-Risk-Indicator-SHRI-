import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

screenshots_dir = os.path.abspath(r"smart_health_risk_indicator\screenshots")
os.makedirs(screenshots_dir, exist_ok=True)

html_path = os.path.abspath(r"smart_health_risk_indicator\index.html").replace("\\", "/")
url = f"file:///{html_path}"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1600,1100")
options.add_argument("--force-device-scale-factor=1")
options.add_argument("--disable-gpu")

driver = webdriver.Edge(options=options)
driver.set_window_size(1600, 1100)

try:
    print(f"Loading {url}...")
    driver.get(url)
    time.sleep(2)

    # 1. Login Screen
    shot1 = os.path.join(screenshots_dir, "01_login_screen.png")
    driver.save_screenshot(shot1)
    print("Saved 1:", shot1)

    # Login by submitting doctor login form
    driver.execute_script("""
        const form = document.getElementById('doctor-login-form');
        if (form) form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    """)
    time.sleep(1.5)

    # 2. Patient Registry Dashboard
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.5)
    shot2 = os.path.join(screenshots_dir, "02_patient_registry.png")
    driver.save_screenshot(shot2)
    print("Saved 2:", shot2)

    # Open Dossier for first patient
    driver.execute_script("""
        if (typeof patientsDB !== 'undefined' && patientsDB.length > 0) {
            loadPatientFromDataset(patientsDB[0].id);
        } else {
            const firstCard = document.querySelector('.patient-card');
            if (firstCard) firstCard.click();
        }
    """)
    time.sleep(1.5)

    # 3. Clinical Dossier - Assessment Form
    driver.execute_script("switchDossierTab('assessment'); window.scrollTo(0, 220);")
    time.sleep(1.0)
    shot3 = os.path.join(screenshots_dir, "03_clinical_dossier.png")
    driver.save_screenshot(shot3)
    print("Saved 3:", shot3)

    # 4. Ensemble & SHAP
    driver.execute_script("switchDossierTab('ensemble'); window.scrollTo(0, 220);")
    time.sleep(1.0)
    shot4 = os.path.join(screenshots_dir, "04_ensemble_shap.png")
    driver.save_screenshot(shot4)
    print("Saved 4:", shot4)

    # 5. Voice Analyzer Tab
    driver.execute_script("switchDossierTab('voice'); window.scrollTo(0, 200);")
    time.sleep(1.0)
    shot5 = os.path.join(screenshots_dir, "05_voice_analyzer.png")
    driver.save_screenshot(shot5)
    print("Saved 5:", shot5)

    # 6. Benchmark Validation View
    driver.execute_script("showValidationBenchmark(); window.scrollTo(0, 150);")
    time.sleep(1.0)
    shot6 = os.path.join(screenshots_dir, "06_benchmark_validation.png")
    driver.save_screenshot(shot6)
    print("Saved 6:", shot6)

    # 7. Multi-Source Datasets Explorer View
    try:
        driver.execute_script("showDatasetsExplorer(); window.scrollTo(0, 150);")
        time.sleep(1.0)
        shot7 = os.path.join(screenshots_dir, "07_datasets_explorer.png")
        driver.save_screenshot(shot7)
        print("Saved 7:", shot7)
    except Exception as e:
        print("Datasets view error:", e)

    print("All screenshots successfully captured!")

finally:
    driver.quit()
