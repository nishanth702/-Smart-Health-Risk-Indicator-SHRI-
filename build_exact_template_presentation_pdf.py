"""
Build Review-2 Presentation PDF in the EXACT template from the screenshots.
- 16:9 Widescreen (960 x 540 pt)
- Pure white background
- SRM Logo in top-right corner on every slide
- Centered bold serif headings (Times-Bold)
- Exact slide text, bullet formatting, tables, and images
- Footer with Date (07-09-2026), Title, and Slide Number
"""

import os
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

IMG_DIR = r"c:\Users\nishanth golakoti\Downloads\ADMRI-main\extracted_images"
LOGO_PATH = os.path.join(IMG_DIR, "slide_1_img_1_Image11.jpg")

class ExactTemplateCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(ExactTemplateCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_template_decorations(num_pages)
            super(ExactTemplateCanvas, self).showPage()
        super(ExactTemplateCanvas, self).save()

    def draw_template_decorations(self, page_count):
        self.saveState()
        w, h = 960, 540  # 16:9 widescreen
        
        # 1. Pure White Background
        self.setFillColor(colors.white)
        self.rect(0, 0, w, h, fill=1, stroke=0)
        
        # 2. SRM Logo in Top-Right Corner (on every page)
        if os.path.exists(LOGO_PATH):
            logo_w = 58
            logo_h = 58
            self.drawImage(LOGO_PATH, w - logo_w - 30, h - logo_h - 22, width=logo_w, height=logo_h, mask='auto', preserveAspectRatio=True)
            
        # 3. Footer (on pages 2 to 21)
        if self._pageNumber >= 2:
            self.setFillColor(colors.HexColor('#888888'))
            self.setFont("Helvetica", 9)
            # Left: Date
            self.drawString(50, 22, "07-09-2026")
            # Center: Title
            self.drawCentredString(w / 2.0, 22, "Title")
            # Right: Slide number
            self.drawRightString(w - 50, 22, str(self._pageNumber))
            
        self.restoreState()

def build_pdf(output_path):
    W, H = 960, 540
    doc = SimpleDocTemplate(
        output_path,
        pagesize=(W, H),
        leftMargin=60,
        rightMargin=60,
        topMargin=35,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    # Custom exact-template styles
    st_title_main = ParagraphStyle(
        'ExactTitleMain',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.black,
        alignment=1, # Center
        spaceAfter=14
    )
    
    st_title_sub = ParagraphStyle(
        'ExactTitleSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=17,
        textColor=colors.black,
        alignment=1,
        spaceAfter=30
    )
    
    st_slide_h1 = ParagraphStyle(
        'ExactSlideH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=30,
        leading=36,
        textColor=colors.black,
        alignment=1, # Center
        spaceAfter=20
    )
    
    st_body_p = ParagraphStyle(
        'ExactBodyP',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13.5,
        leading=20,
        textColor=colors.black,
        spaceAfter=12
    )
    
    st_bullet = ParagraphStyle(
        'ExactBullet',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13,
        leading=19,
        textColor=colors.black,
        leftIndent=24,
        firstLineIndent=-14,
        spaceAfter=10
    )
    
    st_bullet_tight = ParagraphStyle(
        'ExactBulletTight',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=17,
        textColor=colors.black,
        leftIndent=20,
        firstLineIndent=-12,
        spaceAfter=6
    )

    st_ref_bullet = ParagraphStyle(
        'ExactRefBullet',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=15,
        textColor=colors.black,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )

    st_meta_left = ParagraphStyle(
        'ExactMetaLeft',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13,
        leading=18,
        textColor=colors.black
    )

    st_meta_right = ParagraphStyle(
        'ExactMetaRight',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=13,
        leading=18,
        textColor=colors.black,
        alignment=2 # Right
    )

    story = []

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("ADAPTIVE DIGITAL MENTAL HEALTH<br/>RISK INDEX (SHRI)", st_title_main))
    story.append(Paragraph("Project Category: RESEARCH", st_title_sub))
    story.append(Spacer(1, 45))
    
    t_meta_data = [
        [
            Paragraph("<b>Guide Name</b><br/>"
                      "Dr. Ramesh S<br/>"
                      "Assistant Professor<br/>"
                      "Department of NWC", st_meta_left),
            Paragraph("<b>Student Name & Registration Number</b><br/>"
                      "A GEETHIKA-RA2311028010076<br/>"
                      "PRATEEK YADAV-RA2311028010110<br/>"
                      "NISHANTH GOLAKOTI-RA2311028010214", st_meta_right)
        ]
    ]
    t_meta = Table(t_meta_data, colWidths=[400, 440])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: ABSTRACT
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("ABSTRACT", st_slide_h1))
    story.append(Spacer(1, 10))
    
    abs_txt = (
        "• Depression, anxiety, and sleep disorders are increasingly common among "
        "adolescents, yet continuous clinical monitoring remains limited due to privacy and "
        "infrastructure constraints. This paper presents ADMRI / Smart Health Risk "
        "Indicator (SHRI), a secure, doctor-access-only, browser-native AI clinical decision "
        "support system for screening and longitudinal monitoring of adolescents aged 10–"
        "18. The platform integrates validated clinical instruments, real-time NLP-based "
        "journal analysis, and behavioural biomarkers within a four-model stacked "
        "ensemble implemented entirely in TensorFlow.js, ensuring all data remains on-"
        "device. ADMRI generates a 0–100 risk score with severity levels, confidence "
        "intervals, anomaly detection, and trajectory forecasting, providing a privacy-"
        "preserving and infrastructure-independent solution for early detection and "
        "evidence-based clinical decision-making."
    )
    story.append(Paragraph(abs_txt, st_body_p))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: INTRODUCTION
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("INTRODUCTION", st_slide_h1))
    story.append(Spacer(1, 5))
    
    intro_pts = [
        "• Adolescent mental health disorders such as depression, anxiety, and sleep disturbances are rising globally, yet early detection remains limited due to stigma, resource constraints, and lack of accessible screening tools.",
        "• Traditional assessment methods rely on manual questionnaire scoring and subjective evaluation, often lacking predictive analytics, real-time monitoring, and data privacy safeguards.",
        "• Existing digital mental health tools frequently depend on cloud-based APIs and single-model scoring systems, raising confidentiality concerns and limiting clinical explainability.",
        "• ADMRI (Adaptive Digital Mental Risk Index / SHRI) addresses these gaps through a browser-native, AI-powered, multimodal screening platform that integrates validated clinical instruments, NLP-based analysis, behavioural biomarkers, and a stacked ensemble architecture for secure, personalised, and data-driven mental health assessment."
    ]
    for pt in intro_pts:
        story.append(Paragraph(pt, st_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("PROBLEM STATEMENT", st_slide_h1))
    story.append(Spacer(1, 5))
    
    ps_p = (
        "Adolescent mental health disorders such as depression, anxiety, and sleep "
        "disturbances are increasing globally, yet early identification remains limited due to "
        "lack of accessible and privacy-preserving screening systems. Traditional assessment "
        "approaches rely on manual questionnaire scoring and subjective evaluation, offering "
        "limited predictive insights and no real-time monitoring. Existing digital tools often "
        "depend on cloud-based infrastructures, raising data privacy concerns and restricting "
        "use in low-resource settings."
    )
    story.append(Paragraph(ps_p, st_body_p))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• <b>Key Issues:</b>", st_body_p))
    story.append(Paragraph("• Absence of secure, browser-native AI systems for adolescent mental health screening.", st_bullet))
    story.append(Paragraph("• Lack of multimodal integration with uncertainty estimation and longitudinal monitoring.", st_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: LITERATURE REVIEW (Part 1 - Papers 1 to 5)
    # =========================================================================
    story.append(Paragraph("Literature Review", st_slide_h1))
    img5 = os.path.join(IMG_DIR, "slide_5_img_2_Image33.png")
    if os.path.exists(img5):
        story.append(RLImage(img5, width=840, height=376))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: LITERATURE REVIEW (Part 2 - Papers 6 to 10)
    # =========================================================================
    story.append(Paragraph("Literature Review", st_slide_h1))
    img6 = os.path.join(IMG_DIR, "slide_6_img_2_Image37.png")
    if os.path.exists(img6):
        story.append(RLImage(img6, width=840, height=376))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: LITERATURE REVIEW (Part 3 - Papers 11 to 16)
    # =========================================================================
    story.append(Paragraph("Literature Review", st_slide_h1))
    img7 = os.path.join(IMG_DIR, "slide_7_img_2_Image41.png")
    if os.path.exists(img7):
        story.append(RLImage(img7, width=840, height=376))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: EXISTING SYSTEM
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("EXISTING SYSTEM", st_slide_h1))
    story.append(Spacer(1, 15))
    
    es_pts = [
        "• Existing adolescent mental health screening systems mainly rely on manual questionnaire-based assessments such as PHQ-9 and GAD-7 conducted in clinical settings.",
        "• These methods depend on periodic evaluations and clinician interpretation, limiting real-time monitoring and early detection.",
        "• Many digital tools use cloud-based processing, raising privacy concerns and typically providing only static risk scores without personalised tracking or uncertainty estimation."
    ]
    for pt in es_pts:
        story.append(Paragraph(pt, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: PROPOSED SYSTEM
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("PROPOSED SYSTEM", st_slide_h1))
    story.append(Spacer(1, 5))
    
    ps_pts = [
        "• Develop ADMRI / SHRI as a browser-native, AI-powered adolescent mental health screening platform ensuring complete data privacy without server dependency.",
        "• Integrate multimodal inputs including validated questionnaires, NLP-based journal sentiment analysis with real-time crisis detection, and behavioural biomarkers.",
        "• Implement a four-model stacked ensemble architecture in TensorFlow.js to generate a 0–100 risk score with severity levels and confidence intervals.",
        "• Enable longitudinal monitoring through anomaly detection, trajectory forecasting, and per-patient continual learning.",
        "• Provide clinician decision-support features including CBT recommendations, dashboard analytics, and automated PDF report generation."
    ]
    for pt in ps_pts:
        story.append(Paragraph(pt, st_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: ARCHITECTURE DIAGRAM
    # =========================================================================
    story.append(Paragraph("Architecture Diagram", st_slide_h1))
    img10 = os.path.join(IMG_DIR, "slide_10_img_2_Image49.jpg")
    if os.path.exists(img10):
        story.append(RLImage(img10, width=760, height=380))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: MODULES
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("MODULES", st_slide_h1))
    story.append(Spacer(1, 5))
    
    mod_pts = [
        "• Data Collection and Preprocessing",
        "• Multimodal Feature Engineering",
        "• Proposed Stacked Ensemble Model",
        "• Model Training and Optimization",
        "• Uncertainty Estimation and Forecasting",
        "• Frontend Design and User Experience (UI)",
        "• Clinical Dashboard and Reporting",
        "• Deployment and Browser-Based Integration"
    ]
    for pt in mod_pts:
        story.append(Paragraph(pt, st_bullet_tight))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: MODULE DESCRIPTION (Part 1: Modules 1 to 5)
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("Module Description", st_slide_h1))
    story.append(Spacer(1, 5))
    
    md1_5 = [
        "<b>1. Data Collection and Preprocessing</b><br/>"
        "• Collects structured questionnaire responses, journal text entries, and behavioural biomarkers from users. Performs data cleaning, normalization, scoring conversion, and feature encoding for model readiness.",
        "<b>2. Multimodal Feature Engineering</b><br/>"
        "• Transforms clinical scores, NLP sentiment outputs, and behavioural metrics into engineered input features. Applies weighting, scaling, and composite index formulation for unified risk representation.",
        "<b>3. Proposed Stacked Ensemble Model</b><br/>"
        "• Implements DepNet, AnxNet, and SleepNet specialist models with a FusionNet meta-learner. Combines predictions using stacked generalisation to improve accuracy and robustness.",
        "<b>4. Model Training and Optimization</b><br/>"
        "• Trains TensorFlow.js models using synthetic clinically validated datasets. Applies Batch Normalization, Dropout, and hyperparameter tuning for performance optimization.",
        "<b>5. Uncertainty Estimation and Forecasting</b><br/>"
        "• Uses Monte Carlo Dropout to generate confidence intervals for predictions. Implements anomaly detection and trajectory forecasting for longitudinal monitoring."
    ]
    for pt in md1_5:
        story.append(Paragraph(pt, st_bullet_tight))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 13: MODULE DESCRIPTION (Part 2: Modules 6 to 8)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Module Description", st_slide_h1))
    story.append(Spacer(1, 10))
    
    md6_8 = [
        "• <b>6. Frontend Design and User Experience (UI)</b><br/>"
        "• Develops an interactive React-based interface for clinicians and users. Includes dashboards, charts, severity gauges, and responsive design components.",
        "• <b>7. Clinical Dashboard and Reporting</b><br/>"
        "• Provides patient registry, trend visualization, radar charts, and CBT recommendations. Generates automated PDF reports for clinical documentation and sharing.",
        "• <b>8. Deployment and Browser-Based Integration</b><br/>"
        "• Deploys the system entirely in-browser using TensorFlow.js and IndexedDB. Ensures data privacy, offline capability, and infrastructure-independent operation."
    ]
    for pt in md6_8:
        story.append(Paragraph(pt, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 14: IMPLEMENTATION FLOW
    # =========================================================================
    story.append(Paragraph("IMPLEMENTATION FLOW", st_slide_h1))
    img14 = os.path.join(IMG_DIR, "slide_14_img_2_Image60.jpg")
    if os.path.exists(img14):
        story.append(RLImage(img14, width=380, height=380))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 15: SAMPLE CODE AND RESULT (Code)
    # =========================================================================
    story.append(Paragraph("SAMPLE CODE AND RESULT", st_slide_h1))
    img15_1 = os.path.join(IMG_DIR, "slide_15_img_2_Image63.jpg")
    img15_2 = os.path.join(IMG_DIR, "slide_15_img_3_Image64.jpg")
    if os.path.exists(img15_1) and os.path.exists(img15_2):
        t_code_imgs = Table([
            [RLImage(img15_1, width=400, height=260), RLImage(img15_2, width=410, height=260)]
        ], colWidths=[420, 420])
        t_code_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_code_imgs)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 16: SAMPLE CODE AND RESULT (Result UI)
    # =========================================================================
    story.append(Paragraph("SAMPLE CODE AND RESULT", st_slide_h1))
    img16_1 = os.path.join(IMG_DIR, "slide_16_img_2_Image67.jpg")
    img16_2 = os.path.join(IMG_DIR, "slide_16_img_3_Image68.jpg")
    if os.path.exists(img16_1) and os.path.exists(img16_2):
        t_res_imgs = Table([
            [RLImage(img16_1, width=380, height=270), RLImage(img16_2, width=390, height=270)]
        ], colWidths=[410, 410])
        t_res_imgs.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(t_res_imgs)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 17: CONCLUSION
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("CONCLUSION", st_slide_h1))
    story.append(Spacer(1, 10))
    
    concl_pts = [
        "• ADMRI / SHRI provides a secure, browser-native AI platform for adolescent mental health risk assessment without server dependency.",
        "• It integrates validated clinical instruments, NLP-based journal analysis, and behavioural biomarkers using a stacked ensemble architecture.",
        "• The system generates risk scores with severity levels, confidence intervals, anomaly detection, and trajectory forecasting for longitudinal monitoring.",
        "• With clinician dashboards, CBT recommendations, and automated reporting, ADMRI enables early identification and data-driven intervention in low-resource settings."
    ]
    for pt in concl_pts:
        story.append(Paragraph(pt, st_bullet))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 18: FUTURE SCOPE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("FUTURE SCOPE", st_slide_h1))
    story.append(Spacer(1, 10))
    
    fs_pts = [
        "• Integration with wearable devices for real-time behavioural and physiological data collection.",
        "• Expansion to multilingual NLP models for broader regional and global deployment.",
        "• Incorporation of real clinical dataset validation to enhance model robustness and generalisability.",
        "• Development of mobile application support for wider accessibility.",
        "• Integration with electronic health record (EHR) systems for seamless clinical workflow adoption."
    ]
    for pt in fs_pts:
        story.append(Paragraph(pt, st_bullet))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 19: REFERENCES (Studies 1 to 7)
    # =========================================================================
    story.append(Paragraph("References", st_slide_h1))
    
    r1_7 = [
        "[1] S. A. Suresh and S. Agarwal, \"Hybrid ML Approach for Mental Health Prediction,\" in Proc. 4th Int. Conf. Innovative Mechanisms for Industry Applications (ICIMIA), IEEE, 2025.",
        "[2] L. Hermawan, Meilinda, D. Stiawan, D. S. Ikhsan, and R. A. Syakurah, \"Mental Health with Machine Learning: A Prediction-Based Intervention Chatbot for Mental Health Conversations,\" in Proc. IEEE Conf., 2024.",
        "[3] H. Dhawale, D. Thakare, N. C. Morris, R. Agrawal, and C. Dhule, \"The Prediction of Mental Health Using Machine Learning,\" in Proc. 15th Int. Conf. Computing Communication and Networking Technologies (ICCCNT), IEEE, 2024.",
        "[4] N. Jayakumar and R. N., \"Modeling Mental Health: Advances in Predictive Science towards Proactive Health Care,\" in Proc. IEEE Int. Conf. for Women in Innovation, Technology & Entrepreneurship (ICWITE), 2024.",
        "[5] S. Purohit, R. Mudgal, S. Vats, P. Rana, and A. Verma, \"Analyzing the Impact of Social Media Usage on Mental Health: A Machine Learning Approach,\" in Proc. 15th ICCCNT, IEEE, 2024.",
        "[6] J. Cherian et al., \"Multimodal Markers of Transdiagnostic Childhood Mental Health Impairment,\" in Proc. IEEE Conf., 2024.",
        "[7] Y. Koh, C. Lee, Y. Ku, and U. Lee, \"Data Visualization for Mental Health Monitoring in Smart Home Environment: A Case Study,\" in Proc. IEEE Conf., 2023."
    ]
    for r in r1_7:
        story.append(Paragraph(r, st_ref_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 20: REFERENCES (Studies 8 to 16)
    # =========================================================================
    story.append(Paragraph("References", st_slide_h1))
    
    r8_16 = [
        "[8] B. Li and Y. Xu, \"Research on Evaluation Model of College Students' Mental Health,\" in Proc. Int. Conf. Health Big Data and Smart Sports (HBDSS), IEEE, 2021.",
        "[9] G. Peng and W. Y. Leong, \"Brain Wave Response of Style Geometry in Artistic Creation in VR Environments: An Impact Study on Cognitive Function and Mental Health of Autistic Children,\" in Proc. IEEE Int. Conf. Signal and Image Processing Applications (ICSIPA), 2024.",
        "[10] D. Pant et al., \"Visualizing Patient Trajectories and Disorder Co-occurrences in Child and Adolescent Mental Health,\" in Proc. IEEE Int. Conf. Bioinformatics and Biomedicine (BIBM), 2024.",
        "[11] S. Kataru, K. King, and L. Fernando, \"Machine Learning-Based Early Detection and Intervention for Mental Health Issues in Children,\" in Proc. IEEE 48th Annual Computers, Software, and Applications Conf. (COMPSAC), 2024.",
        "[12] C. R. Madhuri, M. Srinu, J. S. K. Bandaru, and G. M. A. Vardhan, \"AI-Powered Mental Health Screening and Support for Homeless Children,\" in Proc. AI-Driven Smart Healthcare for Society 5.0, IEEE, 2025.",
        "[13] X. Yuan, \"Study on the Correlation between Growth Environment and Mental Health of Left-Behind Children,\" in Proc. IEEE Conf., 2023.",
        "[14] N. L. Gowda, N. Kumar, and N. S. L. Gowda, \"A Comparative Study on Various Detection Techniques to Detect Mental Health Disorders in Children,\" in Proc. IEEE Int. Conf. Next Generation Electronics (NEleX), 2023.",
        "[15] M. H. Amirhosseini, A. L. Ayodele, and A. Karami, \"Prediction of Depression Severity and Personalised Risk Factors Using Machine Learning on Multimodal Data,\" in Proc. IEEE 12th Int. Conf. Intelligent Systems (IS), 2024.",
        "[16] H. K. Marrapu, B. Maram, and P. Reddi, \"New Analytic Framework of Public Mental Health Prediction Using Data Science,\" in Proc. Int. Conf. Smart Technologies and Systems for Next Generation Computing (ICSTSN), IEEE, 2022."
    ]
    for r in r8_16:
        story.append(Paragraph(r, st_ref_bullet))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 21: THANK YOU
    # =========================================================================
    story.append(Spacer(1, 160))
    story.append(Paragraph("Thank You", ParagraphStyle(
        'ThankYouStyle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=48,
        leading=56,
        textColor=colors.black,
        alignment=1
    )))

    doc.build(story, canvasmaker=ExactTemplateCanvas)
    print(f"Successfully generated presentation PDF in exact template at: {output_path}")

if __name__ == "__main__":
    out_desktop = r"C:\Users\nishanth golakoti\Desktop\Smart_Health_Risk_Indicator_Review2.pdf"
    build_pdf(out_desktop)
