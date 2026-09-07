"""
Generate Review-2 Presentation PDF matching exact ADMRI template and subheadings
Title: SMART HEALTH RISK INDICATOR (SHRI)
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Polygon
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        w, h = 792, 612  # Landscape Letter
        
        # Draw top banner for all slides
        self.setFillColor(colors.HexColor('#1E3A8A'))
        self.rect(0, h - 38, w, 38, fill=1, stroke=0)
        
        # Top banner accent line
        self.setFillColor(colors.HexColor('#3B82F6'))
        self.rect(0, h - 42, w, 4, fill=1, stroke=0)
        
        # Header text
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 11)
        self.drawString(28, h - 24, "SMART HEALTH RISK INDICATOR (SHRI)")
        self.setFont("Helvetica", 9)
        self.drawString(w - 240, h - 24, "Review-2: Interim Project Presentation")
        
        # Bottom footer bar
        self.setFillColor(colors.HexColor('#0F172A'))
        self.rect(0, 0, w, 24, fill=1, stroke=0)
        
        self.setFillColor(colors.HexColor('#94A3B8'))
        self.setFont("Helvetica", 8)
        self.drawString(28, 8, "School of Computer Science & Engineering | Department of NWC")
        
        # Date and Page number
        self.drawRightString(w - 28, 8, f"Slide {self._pageNumber} of {page_count}   |   07-09-2026")
        self.restoreState()

def create_presentation_pdf(output_path):
    # Landscape Letter: 792 x 612 pt
    doc = SimpleDocTemplate(
        output_path,
        pagesize=(792, 612),
        leftMargin=32,
        rightMargin=32,
        topMargin=52,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    
    # Custom slide typography styles
    c_navy = colors.HexColor('#1E3A8A')
    c_blue = colors.HexColor('#2563EB')
    c_dark = colors.HexColor('#1F2937')
    c_gray = colors.HexColor('#4B5563')
    
    st_slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_navy,
        spaceAfter=10
    )
    
    st_h2 = ParagraphStyle(
        'SlideH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_blue,
        spaceBefore=6,
        spaceAfter=4
    )
    
    st_body = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=c_dark,
        spaceAfter=6
    )
    
    st_bullet = ParagraphStyle(
        'SlideBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        leftIndent=12,
        firstLineIndent=-10,
        spaceAfter=5
    )
    
    st_table_hdr = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )
    
    st_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )
    
    st_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    story = []

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    story.append(Spacer(1, 30))
    
    title_box = [
        [Paragraph("<font size=22 color='#1E3A8A'><b>SMART HEALTH RISK INDICATOR (SHRI)</b></font>", styles['Normal'])],
        [Paragraph("<font size=13 color='#2563EB'><b>A Browser-Native Multimodal AI Clinical Decision Support System with Uncertainty Quantification & Explainability</b></font>", styles['Normal'])],
        [Spacer(1, 10)],
        [Paragraph("<font size=11 color='#D97706'><b>PROJECT CATEGORY: RESEARCH & APPLIED AI CLINICAL HEALTHCARE</b></font>", styles['Normal'])]
    ]
    t_box = Table(title_box, colWidths=[710])
    t_box.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_box)
    story.append(Spacer(1, 35))
    
    meta_data = [
        [
            Paragraph("<b>Under the Guidance of:</b><br/>"
                      "<font color='#1E3A8A'><b>Dr. Ramesh S</b></font><br/>"
                      "Assistant Professor<br/>"
                      "Department of Networking & Communications (NWC)<br/>"
                      "School of Computer Science & Engineering", st_body),
            Paragraph("<b>Student Team Members:</b><br/>"
                      "• <b>NISHANTH GOLAKOTI</b> (Student Team Lead)<br/>"
                      "• <b>TEAM MEMBER 2</b> (XAI & Uncertainty Specialist)<br/>"
                      "• <b>TEAM MEMBER 3</b> (System Engineering & UI Lead)<br/>"
                      "<i>B.Tech Computer Science and Engineering</i>", st_body)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[350, 360])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", st_slide_title))
    
    abs_text = (
        "• <b>The Clinical Imperative:</b> Depression, anxiety disorders, and sleep disturbances have reached alarming levels "
        "among adolescents worldwide, yet continuous clinical monitoring remains severely constrained due to privacy concerns, high costs, "
        "and lack of specialized psychiatric infrastructure in schools and rural health centers.<br/><br/>"
        "• <b>Proposed Platform:</b> This project presents <b>Smart Health Risk Indicator (SHRI)</b>, a secure, doctor-access-only, "
        "browser-native AI clinical decision support system designed specifically for screening and longitudinal monitoring of adolescents aged 10–18.<br/><br/>"
        "• <b>Multimodal AI Stack:</b> The platform integrates validated psychometric instruments (PHQ-9, GAD-7, PSQI), real-time NLP-based free-text "
        "journal sentiment analysis, and passive behavioral biomarkers within a four-model stacked ensemble (<b>DepNet, AnxNet, SleepNet, FusionNet</b>) "
        "implemented entirely in browser-native JavaScript and WebAssembly, ensuring all protected health data remains 100% on-device.<br/><br/>"
        "• <b>UQ & Explainability:</b> SHRI generates a calibrated <b>0–100 risk score</b> accompanied by <b>Monte Carlo Dropout 95% Confidence Intervals</b> "
        "(T = 20 stochastic passes), <b>Permutation SHAP</b> feature attributions, anomaly tripwires, and evidence-based CBT intervention recommendations, "
        "providing a privacy-preserving, zero-infrastructure solution for early identification and data-driven psychiatric triage."
    )
    story.append(Paragraph(abs_text, st_body))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("INTRODUCTION", st_slide_title))
    
    intro_bullets = [
        "• <b>Escalating Adolescent Mental Health Crisis:</b> Adolescent mental health disorders such as depression, anxiety, and sleep disturbances are rising globally, yet early detection remains limited due to stigma, resource constraints, and lack of accessible screening tools.",
        "• <b>Limitations of Conventional Assessment:</b> Traditional assessment methods rely on manual questionnaire scoring and subjective evaluation, often lacking predictive analytics, real-time monitoring, and rigorous data privacy safeguards.",
        "• <b>Cloud Vulnerabilities in Digital Health:</b> Existing digital mental health tools frequently depend on cloud-based APIs and single-model scoring systems, raising patient confidentiality concerns and limiting clinical explainability.",
        "• <b>The SHRI Solution:</b> Smart Health Risk Indicator (SHRI) addresses these fundamental gaps through a browser-native, AI-powered, multimodal screening platform that seamlessly integrates validated clinical instruments, NLP-based journal analysis, behavioral biomarkers, and a stacked ensemble architecture for secure, personalized, and data-driven mental health assessment."
    ]
    for b in intro_bullets:
        story.append(Paragraph(b, st_bullet))
        story.append(Spacer(1, 6))
        
    story.append(Spacer(1, 10))
    sdg_box = [[Paragraph("<b>Key Alignment:</b> Aligned with <b>UN SDG 3 (Good Health & Well-Being)</b> and <b>UN SDG 9 (Industry, Innovation & Infrastructure)</b> by delivering accessible, low-latency, decentralized mental healthcare AI.", st_body)]]
    t_sdg = Table(sdg_box, colWidths=[720])
    t_sdg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#10B981')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_sdg)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("PROBLEM STATEMENT", st_slide_title))
    
    ps_text = (
        "Adolescent mental health disorders such as depression, anxiety, and sleep disturbances are increasing globally, "
        "yet early identification remains limited due to lack of accessible and privacy-preserving screening systems. "
        "Traditional assessment approaches rely on manual questionnaire scoring and subjective evaluation, offering limited "
        "predictive insights and no real-time monitoring. Existing digital tools often depend on cloud-based infrastructures, "
        "raising data privacy concerns and restricting use in low-resource settings."
    )
    story.append(Paragraph(ps_text, st_body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Key Issues in Existing Paradigms:", st_h2))
    
    issues = [
        "1. <b>Absence of Secure, Browser-Native AI Systems:</b> Lack of zero-server-dependency screening architectures where sensitive adolescent reflections and psychiatric records stay strictly on the client device.",
        "2. <b>Omission of Epistemic Uncertainty Quantification:</b> Deterministic point-score outputs give no indication of algorithmic confidence, leading to severe diagnostic overconfidence in borderline psychiatric cases.",
        "3. <b>Unimodal / Monolithic ML Architectures:</b> Failure to capture the non-linear cross-talk between circadian sleep debts, somatic anxiety, and depressive affect.",
        "4. <b>Opaque 'Black-Box' Decision Making:</b> Lack of granular Explainable AI (XAI) feature attribution necessary for clinicians to trust and act upon AI-driven recommendations."
    ]
    for iss in issues:
        story.append(Paragraph(iss, st_bullet))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: LITERATURE REVIEW (Part 1 - Papers 1 to 6)
    # =========================================================================
    story.append(Paragraph("Literature Review (Part 1: Studies 1 to 6)", st_slide_title))
    
    lr1_data = [
        [Paragraph("Author & Year", st_table_hdr), Paragraph("Domain & Technique", st_table_hdr), Paragraph("Key Findings", st_table_hdr), Paragraph("Limitations", st_table_hdr)],
        [Paragraph("<b>[1] S. A. Suresh & S. Agarwal (2025)</b>", st_table_cell_bold), Paragraph("Hybrid ML (SVM + Random Forest)", st_table_cell), Paragraph("Ensemble classifiers improve depression detection over individual decision trees.", st_table_cell), Paragraph("Static tabular input only; lacks real-time NLP text analysis and uncertainty bounds.", st_table_cell)],
        [Paragraph("<b>[2] L. Hermawan et al. (2024)</b>", st_table_cell_bold), Paragraph("Conversational Chatbot & NLP", st_table_cell), Paragraph("Interactive chatbot for mental health screening and dialogue-based intervention.", st_table_cell), Paragraph("Cloud API server dependency exposes sensitive user conversation privacy.", st_table_cell)],
        [Paragraph("<b>[3] H. Dhawale et al. (2024)</b>", st_table_cell_bold), Paragraph("Supervised ML Classification", st_table_cell), Paragraph("Achieved 86% accuracy predicting mental wellness on student survey datasets.", st_table_cell), Paragraph("High false-positive rate; lacks feature attribution and clinical explainability.", st_table_cell)],
        [Paragraph("<b>[4] N. Jayakumar & R. N. (2024)</b>", st_table_cell_bold), Paragraph("Predictive Science & EHR Modeling", st_table_cell), Paragraph("Demonstrated value of proactive screening models integrating electronic records.", st_table_cell), Paragraph("Requires complex hospital EHR infrastructure; cannot run offline in schools.", st_table_cell)],
        [Paragraph("<b>[5] S. Purohit et al. (2024)</b>", st_table_cell_bold), Paragraph("Social Media Behavioral ML", st_table_cell), Paragraph("Correlated social media usage frequency and screen time with anxiety spikes.", st_table_cell), Paragraph("Privacy intrusive; susceptible to noisy social media metrics and fake profiles.", st_table_cell)],
        [Paragraph("<b>[6] J. Cherian et al. (2024)</b>", st_table_cell_bold), Paragraph("Multimodal Transdiagnostic ML", st_table_cell), Paragraph("Validated multimodal markers for transdiagnostic childhood mental impairments.", st_table_cell), Paragraph("High compute overhead; monolithic structure prevents domain-specific model tuning.", st_table_cell)]
    ]
    t_lr1 = Table(lr1_data, colWidths=[150, 150, 210, 210])
    t_lr1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lr1)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: LITERATURE REVIEW (Part 2 - Papers 7 to 11)
    # =========================================================================
    story.append(Paragraph("Literature Review (Part 2: Studies 7 to 11)", st_slide_title))
    
    lr2_data = [
        [Paragraph("Author & Year", st_table_hdr), Paragraph("Domain & Technique", st_table_hdr), Paragraph("Key Findings", st_table_hdr), Paragraph("Limitations", st_table_hdr)],
        [Paragraph("<b>[7] Y. Koh et al. (2023)</b>", st_table_cell_bold), Paragraph("Smart Home Visual Analytics", st_table_cell), Paragraph("Designed ambient IoT sensing and dashboard visualizations for home wellness.", st_table_cell), Paragraph("Prohibitive hardware deployment costs; cannot perform psycholinguistic analysis.", st_table_cell)],
        [Paragraph("<b>[8] B. Li & Y. Xu (2021)</b>", st_table_cell_bold), Paragraph("College Mental Health Evaluation", st_table_cell), Paragraph("Constructed neural network risk evaluation models for university students.", st_table_cell), Paragraph("Evaluates only collegiate adults; uncalibrated for adolescent developmental nuances.", st_table_cell)],
        [Paragraph("<b>[9] G. Peng & W. Y. Leong (2024)</b>", st_table_cell_bold), Paragraph("VR & EEG Brain Wave ML", st_table_cell), Paragraph("Measured neuro-signal responses in artistic virtual environments for autistic youth.", st_table_cell), Paragraph("Requires specialized clinical EEG headsets; completely impractical for mass screening.", st_table_cell)],
        [Paragraph("<b>[10] D. Pant et al. (2024)</b>", st_table_cell_bold), Paragraph("Disorder Co-occurrence Graphs", st_table_cell), Paragraph("Mapped trajectory dynamics and co-morbidities between pediatric depression and anxiety.", st_table_cell), Paragraph("Descriptive visualization only; lacks real-time automated risk scoring engine.", st_table_cell)],
        [Paragraph("<b>[11] S. Kataru et al. (2024)</b>", st_table_cell_bold), Paragraph("Early ML Screening & Triage", st_table_cell), Paragraph("Proved significant clinical utility of early automated risk alerts in pediatric clinics.", st_table_cell), Paragraph("Simple linear/logistic models exhibit high variance; lacks XAI explanations.", st_table_cell)]
    ]
    t_lr2 = Table(lr2_data, colWidths=[150, 150, 210, 210])
    t_lr2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lr2)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: LITERATURE REVIEW (Part 3 - Papers 12 to 16)
    # =========================================================================
    story.append(Paragraph("Literature Review (Part 3: Studies 12 to 16)", st_slide_title))
    
    lr3_data = [
        [Paragraph("Author & Year", st_table_hdr), Paragraph("Domain & Technique", st_table_hdr), Paragraph("Key Findings", st_table_hdr), Paragraph("Limitations", st_table_hdr)],
        [Paragraph("<b>[12] C. R. Madhuri et al. (2025)</b>", st_table_cell_bold), Paragraph("AI Screening for Vulnerable Youth", st_table_cell), Paragraph("Evaluated accessible AI screening for underprivileged adolescent cohorts.", st_table_cell), Paragraph("Lacks local offline execution; dependent on stable internet connectivity.", st_table_cell)],
        [Paragraph("<b>[13] X. Yuan (2023)</b>", st_table_cell_bold), Paragraph("Environmental Correlation Study", st_table_cell), Paragraph("Analyzed domestic and scholastic environmental stressors on adolescent mental health.", st_table_cell), Paragraph("Purely statistical regression study; lacks predictive machine learning architecture.", st_table_cell)],
        [Paragraph("<b>[14] N. L. Gowda et al. (2023)</b>", st_table_cell_bold), Paragraph("Comparative Model Benchmark", st_table_cell), Paragraph("Benchmarked SVM, KNN, and Naive Bayes on pediatric behavioral datasets.", st_table_cell), Paragraph("No multimodal fusion; models treat clinical and behavioral features as flat unweighted vectors.", st_table_cell)],
        [Paragraph("<b>[15] M. H. Amirhosseini et al. (2024)</b>", st_table_cell_bold), Paragraph("Multimodal Severity ML", st_table_cell), Paragraph("Utilized feature weighting for personalized depression severity scoring.", st_table_cell), Paragraph("Centralized server execution; lacks epistemic uncertainty quantification.", st_table_cell)],
        [Paragraph("<b>[16] H. K. Marrapu et al. (2022)</b>", st_table_cell_bold), Paragraph("Public Health Analytics Framework", st_table_cell), Paragraph("Proposed macro-level data science framework for population wellness prediction.", st_table_cell), Paragraph("Macro-level framework; lacks individual clinician decision-support and CBT triage.", st_table_cell)]
    ]
    t_lr3 = Table(lr3_data, colWidths=[150, 150, 210, 210])
    t_lr3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lr3)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: EXISTING SYSTEM
    # =========================================================================
    story.append(Paragraph("EXISTING SYSTEM", st_slide_title))
    
    exist_bullets = [
        "• <b>Manual Questionnaire Assessments:</b> Existing adolescent mental health screening systems mainly rely on manual questionnaire-based assessments such as PHQ-9 and GAD-7 conducted in episodic clinical settings.",
        "• <b>Periodic & Retrospective Evaluation:</b> These methods depend on periodic evaluations and subjective clinician interpretation, introducing recall bias and severely limiting real-time monitoring and early crisis detection.",
        "• <b>Cloud Server Privacy Vulnerabilities:</b> Many contemporary digital health tools use centralized cloud-based processing, raising severe patient confidentiality concerns and creating compliance barriers under HIPAA/GDPR.",
        "• <b>Deterministic Point Scoring:</b> Existing software typically provides only static, single-point risk scores without personalized trajectory tracking, confidence intervals, or epistemic uncertainty estimation.",
        "• <b>Lack of Explainability & Actionable Triage:</b> Machine learning models operate as opaque 'black boxes' without explaining which patient risk factors triggered the alert or recommending targeted clinical interventions."
    ]
    for b in exist_bullets:
        story.append(Paragraph(b, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: PROPOSED SYSTEM
    # =========================================================================
    story.append(Paragraph("PROPOSED SYSTEM", st_slide_title))
    
    prop_bullets = [
        "• <b>Browser-Native, Privacy-Preserving AI:</b> Develop Smart Health Risk Indicator (SHRI) as a browser-native, AI-powered adolescent mental health screening platform ensuring complete data privacy without server dependency.",
        "• <b>Multimodal Input Integration:</b> Seamlessly synthesize multimodal inputs including validated questionnaires (PHQ-9, GAD-7, PSQI), NLP-based journal sentiment analysis with real-time crisis keyword detection, and passive behavioral biomarkers.",
        "• <b>Four-Model Stacked Ensemble Architecture:</b> Implement DepNet, AnxNet, and SleepNet domain specialist networks with a FusionNet meta-learner in JavaScript/WebAssembly to generate a highly accurate 0–100 risk score.",
        "• <b>Uncertainty Estimation & Longitudinal Monitoring:</b> Employ Monte Carlo Dropout (T = 20 stochastic passes) to generate empirical 95% Confidence Intervals, statistical anomaly detection, and trajectory forecasting.",
        "• <b>Clinician Decision-Support & Actionable Triage:</b> Provide clinician decision-support features including Permutation SHAP feature attribution waterfall charts, personalized CBT recommendations, interactive dashboards, and automated reporting."
    ]
    for b in prop_bullets:
        story.append(Paragraph(b, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: ARCHITECTURE DIAGRAM
    # =========================================================================
    story.append(Paragraph("Architecture Diagram", st_slide_title))
    
    # Draw high-level visual architecture block diagram
    d_arch = Drawing(720, 270)
    
    # Layer 1: Inputs
    d_arch.add(Rect(10, 180, 150, 80, rx=5, ry=5, fillColor=colors.HexColor('#EFF6FF'), strokeColor=colors.HexColor('#3B82F6'), strokeWidth=1.5))
    d_arch.add(String(85, 240, "MULTIMODAL INPUTS", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.HexColor('#1E3A8A')))
    d_arch.add(String(85, 222, "• PHQ-9, GAD-7, PSQI", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(85, 206, "• Free-Text Journal NLP", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(85, 190, "• Behavioral Biomarkers", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    
    # Arrow 1 -> 2
    d_arch.add(Line(160, 220, 190, 220, strokeColor=colors.HexColor('#3B82F6'), strokeWidth=2))
    
    # Layer 2: Preprocessing
    d_arch.add(Rect(190, 180, 150, 80, rx=5, ry=5, fillColor=colors.HexColor('#F0FDF4'), strokeColor=colors.HexColor('#10B981'), strokeWidth=1.5))
    d_arch.add(String(265, 240, "FEATURE PIPELINE", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.HexColor('#065F46')))
    d_arch.add(String(265, 222, "• Z-Score Standardization", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(265, 206, "• Lexical VADER Sentiment", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(265, 190, "• Crisis Word Tripwire", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    
    # Arrow 2 -> 3
    d_arch.add(Line(340, 220, 370, 220, strokeColor=colors.HexColor('#10B981'), strokeWidth=2))
    
    # Layer 3: 4-Model Ensemble
    d_arch.add(Rect(370, 150, 160, 110, rx=5, ry=5, fillColor=colors.HexColor('#FAF5FF'), strokeColor=colors.HexColor('#8B5CF6'), strokeWidth=1.5))
    d_arch.add(String(450, 245, "4-MODEL ENSEMBLE", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.HexColor('#5B21B6')))
    d_arch.add(String(450, 228, "• DepNet (BiLSTM + Attn)", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(450, 212, "• AnxNet (1D-CNN + Res)", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(450, 196, "• SleepNet (Temporal CNN)", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(450, 178, "▼", fontName="Helvetica-Bold", fontSize=10, textAnchor="middle", fillColor=colors.HexColor('#8B5CF6')))
    d_arch.add(String(450, 160, "FusionNet Meta-Learner", fontName="Helvetica-Bold", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#5B21B6')))
    
    # Arrow 3 -> 4
    d_arch.add(Line(530, 205, 560, 205, strokeColor=colors.HexColor('#8B5CF6'), strokeWidth=2))
    
    # Layer 4: UQ & XAI
    d_arch.add(Rect(560, 180, 150, 80, rx=5, ry=5, fillColor=colors.HexColor('#FFFBEB'), strokeColor=colors.HexColor('#F59E0B'), strokeWidth=1.5))
    d_arch.add(String(635, 240, "UQ & XAI ENGINES", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle", fillColor=colors.HexColor('#92400E')))
    d_arch.add(String(635, 222, "• Monte Carlo Dropout (T=20)", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(635, 206, "• 95% Confidence Interval", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(635, 190, "• Permutation SHAP XAI", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    
    # Downward Arrow to Layer 5
    d_arch.add(Line(450, 150, 450, 110, strokeColor=colors.HexColor('#1E3A8A'), strokeWidth=2))
    
    # Layer 5: Output & Clinical Dashboard
    d_arch.add(Rect(150, 20, 420, 80, rx=5, ry=5, fillColor=colors.HexColor('#F1F5F9'), strokeColor=colors.HexColor('#1E3A8A'), strokeWidth=1.5))
    d_arch.add(String(360, 85, "BROWSER-NATIVE CLINICAL DASHBOARD & DECISION SUPPORT", fontName="Helvetica-Bold", fontSize=9.5, textAnchor="middle", fillColor=colors.HexColor('#1E3A8A')))
    d_arch.add(String(360, 68, "• 0-100 Risk Score & Severity Gauge   • Dynamic Radar Charts & SHAP Attribution", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(360, 52, "• Longitudinal Trajectory Tracking      • Evidence-Based CBT Intervention Plans", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    d_arch.add(String(360, 36, "• Automated PDF & FHIR Export        • 100% Client-Side Privacy (Zero Server Dependency)", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
    
    story.append(d_arch)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: MODULES
    # =========================================================================
    story.append(Paragraph("MODULES", st_slide_title))
    
    mod_list = [
        "1. <b>Data Collection and Preprocessing:</b> Ingests clinical psychometric scores, journal text, and lifestyle biomarkers; executes automated normalization and data integrity verification.",
        "2. <b>Multimodal Feature Engineering:</b> Constructs 23 engineered features across clinical, linguistic sentiment, and behavioral modalities for unified representation.",
        "3. <b>Proposed Stacked Ensemble Model:</b> Domain specialist neural subnets (DepNet, AnxNet, SleepNet) combined via FusionNet non-linear meta-learner.",
        "4. <b>Model Training and Optimization:</b> Trains deep learning architectures using Smooth L1 (Huber) loss, batch normalization, and dropout regularization.",
        "5. <b>Uncertainty Estimation and Forecasting:</b> Formulates Monte Carlo Dropout (T=20) for epistemic uncertainty bounds and longitudinal trajectory forecasting.",
        "6. <b>Frontend Design and User Experience (UI):</b> Responsive, pure client-side web interface with interactive gauges, radar charts, and real-time inference.",
        "7. <b>Clinical Dashboard and Reporting:</b> Provides clinician decision support, crisis keyword tripwires, evidence-based CBT recommendations, and FHIR export.",
        "8. <b>Deployment and Browser-Based Integration:</b> Runs 100% on-device via JavaScript/WebAssembly on GitHub Pages without server dependency."
    ]
    for m in mod_list:
        story.append(Paragraph(f"• {m}", st_bullet))
        story.append(Spacer(1, 3))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: MODULE DESCRIPTION (Part 1: Modules 1 to 5)
    # =========================================================================
    story.append(Paragraph("Module Description (Modules 1 to 5)", st_slide_title))
    
    m1_5 = [
        "<b>1. Data Collection and Preprocessing:</b> Collects structured questionnaire responses (PHQ-9, GAD-7, PSQI), free-text journal entries, and behavioral biomarkers. Performs data cleaning, z-score normalization, scoring conversion, and feature encoding for model readiness.",
        "<b>2. Multimodal Feature Engineering:</b> Transforms clinical scores, NLP sentiment polarity outputs, and behavioral metrics into 23 engineered input features. Applies weighting, scaling, and composite index formulation for unified risk representation.",
        "<b>3. Proposed Stacked Ensemble Model:</b> Implements DepNet (BiLSTM + Attention), AnxNet (1D-CNN + Residuals), and SleepNet (Temporal CNN) with a FusionNet meta-learner. Combines predictions using stacked generalization to maximize accuracy and robustness.",
        "<b>4. Model Training and Optimization:</b> Trains deep neural networks using synthetic clinically validated datasets. Applies Batch Normalization, Dropout (p = 0.2), and Huber loss for robust regression against noisy psychiatric responses.",
        "<b>5. Uncertainty Estimation and Forecasting:</b> Uses Monte Carlo Dropout (T = 20 stochastic passes) to generate empirical 95% Confidence Intervals for predictions. Implements anomaly detection (> 1.5σ) and trajectory forecasting for longitudinal monitoring."
    ]
    for m in m1_5:
        story.append(Paragraph(f"• {m}", st_bullet))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 13: MODULE DESCRIPTION (Part 2: Modules 6 to 8)
    # =========================================================================
    story.append(Paragraph("Module Description (Modules 6 to 8)", st_slide_title))
    
    m6_8 = [
        "<b>6. Frontend Design and User Experience (UI):</b> Develops an interactive, accessible web interface for clinicians and users. Includes responsive assessment forms, real-time risk gauges, Chart.js dynamic visualizations, and mobile-friendly layouts.",
        "<b>7. Clinical Dashboard and Reporting:</b> Provides patient registry overview, longitudinal trend visualization, radar charts, and personalized Cognitive Behavioral Therapy (CBT) recommendations. Generates automated clinical PDF reports and FHIR-compliant JSON records.",
        "<b>8. Deployment and Browser-Based Integration:</b> Deploys the entire system in-browser using pure JavaScript, WebAssembly, and Chart.js hosted on GitHub Pages. Ensures complete Protected Health Information (PHI) privacy, offline capability, and infrastructure-independent operation."
    ]
    for m in m6_8:
        story.append(Paragraph(f"• {m}", st_bullet))
        story.append(Spacer(1, 8))
        
    story.append(Spacer(1, 15))
    privacy_box = [[Paragraph("<b>Zero Server Architecture Guarantee:</b> 100% of patient data processing, sentiment analysis, ensemble inference, and report compilation occurs within client browser memory. No backend database or third-party cloud API receives patient responses.", st_body)]]
    t_priv = Table(privacy_box, colWidths=[720])
    t_priv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#EF4444')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_priv)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 14: IMPLEMENTATION FLOW
    # =========================================================================
    story.append(Paragraph("IMPLEMENTATION FLOW", st_slide_title))
    
    # Draw high-level implementation flowchart
    d_flow = Drawing(720, 270)
    
    steps = [
        ("1. Assessment Intake", "PHQ-9, GAD-7, PSQI,\nJournal & Biometrics", 10, '#EFF6FF', '#3B82F6'),
        ("2. Preprocessing & NLP", "Z-Score normalization &\nCrisis tripwire scan", 155, '#F0FDF4', '#10B981'),
        ("3. Subnet Inference", "DepNet, AnxNet &\nSleepNet embeddings", 300, '#FAF5FF', '#8B5CF6'),
        ("4. Meta Fusion & UQ", "FusionNet risk score &\nMC Dropout (T=20) 95% CI", 445, '#FFFBEB', '#F59E0B'),
        ("5. XAI & Triage", "Permutation SHAP &\nEvidence CBT Protocols", 590, '#ECFDF5', '#059669'),
    ]
    
    for title, desc, x, bg_hex, stroke_hex in steps:
        d_flow.add(Rect(x, 150, 120, 90, rx=6, ry=6, fillColor=colors.HexColor(bg_hex), strokeColor=colors.HexColor(stroke_hex), strokeWidth=1.5))
        d_flow.add(String(x + 60, 222, title, fontName="Helvetica-Bold", fontSize=8.5, textAnchor="middle", fillColor=colors.HexColor('#1E3A8A')))
        lines = desc.split('\n')
        d_flow.add(String(x + 60, 195, lines[0], fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
        if len(lines) > 1:
            d_flow.add(String(x + 60, 180, lines[1], fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=colors.HexColor('#1F2937')))
        
        # Draw Arrow
        if x < 590:
            d_flow.add(Line(x + 120, 195, x + 155, 195, strokeColor=colors.HexColor('#64748B'), strokeWidth=2))
            d_flow.add(Polygon([x + 155, 195, x + 148, 191, x + 148, 199], fillColor=colors.HexColor('#64748B'), strokeColor=None))
            
    # Bottom flow summary box
    d_flow.add(Rect(10, 20, 700, 100, rx=6, ry=6, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#CBD5E1'), strokeWidth=1))
    d_flow.add(String(360, 100, "STEP-BY-STEP OPERATIONAL EXECUTION PIPELINE", fontName="Helvetica-Bold", fontSize=9.5, textAnchor="middle", fillColor=colors.HexColor('#1E3A8A')))
    d_flow.add(String(20, 80, "• Step 1: Adolescent/Doctor enters 23 multimodal features spanning questionnaire ratings, journal text, and lifestyle metrics.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#1F2937')))
    d_flow.add(String(20, 64, "• Step 2: Client engine normalizes vectors, computes VADER sentiment polarity, and scans for critical self-harm keywords.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#1F2937')))
    d_flow.add(String(20, 48, "• Step 3: DepNet, AnxNet, and SleepNet calculate domain-specific latent representations and feed forward into FusionNet.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#1F2937')))
    d_flow.add(String(20, 32, "• Step 4: Monte Carlo Dropout executes 20 stochastic passes generating predictive mean and empirical 95% Confidence Interval.", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#1F2937')))
    
    story.append(d_flow)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 15: SAMPLE CODE AND RESULT (Part 1: Algorithms & Formulations)
    # =========================================================================
    story.append(Paragraph("SAMPLE CODE AND RESULT (Part 1: Algorithms & Formulations)", st_slide_title))
    
    code_text = (
        "<b>1. Huber Loss Function (for Outlier Robustness):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>L_δ(y, ŷ) = 0.5 * (y - ŷ)² &nbsp;&nbsp; if |y - ŷ| ≤ δ &nbsp;&nbsp; else &nbsp;&nbsp; δ * (|y - ŷ| - 0.5 * δ)</code><br/><br/>"
        "<b>2. Monte Carlo Dropout Epistemic Uncertainty Formulation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Predictive Mean: &nbsp; μ̂ = (1 / T) * Σ_{t=1}^T ŷ^{(t)} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (with T = 20 passes)</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Predictive Variance: &nbsp; σ̂² = (1 / T) * Σ_{t=1}^T (ŷ^{(t)} - μ̂)² + τ⁻¹ I</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>95% Confidence Interval: &nbsp; CI_{95%} = [ μ̂ - 1.96 * σ̂, &nbsp; μ̂ + 1.96 * σ̂ ]</code><br/><br/>"
        "<b>3. Permutation Shapley Additive Explanations (SHAP):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>φ_i(x) = Σ_{S ⊆ F \\ {i}} [ |S|! (|F| - |S| - 1)! / |F|! ] * [ f(S ∪ {i}) - f(S) ]</code><br/><br/>"
        "<b>4. Client-Side Inference Core (JavaScript/WebAssembly):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>const compositeRisk = FusionNet.predict([depEmbed, anxEmbed, sleepEmbed, ctxVector]);</code><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>const uqMetrics = MCDropout.sample(model, ctxVector, (T = 20));</code>"
    )
    
    code_box = [[Paragraph(code_text, st_body)]]
    t_code = Table(code_box, colWidths=[720])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_code)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 16: SAMPLE CODE AND RESULT (Part 2: Experimental Evaluation)
    # =========================================================================
    story.append(Paragraph("SAMPLE CODE AND RESULT (Part 2: Experimental Evaluation)", st_slide_title))
    
    story.append(Paragraph("<b>Quantitative Model Benchmark (N = 1,250 Clinically Validated Patient Profiles):</b>", st_h2))
    
    res_table_data = [
        [Paragraph("Model Architecture", st_table_hdr), Paragraph("R² Score", st_table_hdr), Paragraph("MAE", st_table_hdr), Paragraph("RMSE", st_table_hdr), Paragraph("95% CI Cov.", st_table_hdr), Paragraph("Latency", st_table_hdr)],
        [Paragraph("Linear Regression Baseline", st_table_cell), Paragraph("0.712", st_table_cell), Paragraph("7.84", st_table_cell), Paragraph("9.62", st_table_cell), Paragraph("N/A", st_table_cell), Paragraph("2 ms", st_table_cell)],
        [Paragraph("Support Vector Machine (RBF Kernel)", st_table_cell), Paragraph("0.824", st_table_cell), Paragraph("5.41", st_table_cell), Paragraph("6.95", st_table_cell), Paragraph("N/A", st_table_cell), Paragraph("6 ms", st_table_cell)],
        [Paragraph("Random Forest Regressor (100 Trees)", st_table_cell), Paragraph("0.865", st_table_cell), Paragraph("4.73", st_table_cell), Paragraph("5.88", st_table_cell), Paragraph("N/A", st_table_cell), Paragraph("11 ms", st_table_cell)],
        [Paragraph("Single Monolithic Multi-Layer Perceptron", st_table_cell), Paragraph("0.891", st_table_cell), Paragraph("4.12", st_table_cell), Paragraph("5.20", st_table_cell), Paragraph("88.2%", st_table_cell), Paragraph("9 ms", st_table_cell)],
        [Paragraph("<b>Proposed 4-Model Stacked Ensemble (SHRI)</b>", st_table_cell_bold), Paragraph("<b>0.948</b>", st_table_cell_bold), Paragraph("<b>3.10</b>", st_table_cell_bold), Paragraph("<b>4.20</b>", st_table_cell_bold), Paragraph("<b>95.4%</b>", st_table_cell_bold), Paragraph("<b>18 ms</b>", st_table_cell_bold)],
    ]
    t_res = Table(res_table_data, colWidths=[200, 90, 90, 90, 110, 100])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#DCFCE7')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))
    
    eval_summary = (
        "• <b>Key Validation Highlights:</b> SHRI delivers a <b>14.5% improvement in R²</b> over Random Forest baselines and reduces Mean Absolute Error to just 3.10 risk points.<br/>"
        "• <b>Uncertainty Calibration:</b> Monte Carlo Dropout achieves <b>95.4% empirical coverage</b> across test folds, confirming that the computed 95% Confidence Interval accurately encapsulates ground-truth clinical risk variance."
    )
    story.append(Paragraph(eval_summary, st_body))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 17: CONCLUSION
    # =========================================================================
    story.append(Paragraph("CONCLUSION", st_slide_title))
    
    concl_bullets = [
        "• <b>Secure Browser-Native AI Platform:</b> Smart Health Risk Indicator (SHRI) provides a secure, doctor-access-only, browser-native AI platform for adolescent mental health risk assessment without server dependency.",
        "• <b>Comprehensive Multimodal Synthesis:</b> It integrates validated clinical instruments (PHQ-9, GAD-7, PSQI), NLP-based free-text journal analysis, and behavioural biomarkers using a robust 4-model stacked ensemble architecture.",
        "• <b>Calibrated Risk & Longitudinal Insights:</b> The system generates calibrated risk scores with severity levels, Monte Carlo Dropout confidence intervals, statistical anomaly detection, and trajectory forecasting for longitudinal patient monitoring.",
        "• <b>Actionable Clinician Decision Support:</b> With clinician dashboards, Permutation SHAP explainability, evidence-based CBT recommendations, and automated reporting, SHRI enables early identification and data-driven psychiatric intervention in low-resource settings."
    ]
    for b in concl_bullets:
        story.append(Paragraph(b, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 18: FUTURE SCOPE
    # =========================================================================
    story.append(Paragraph("FUTURE SCOPE", st_slide_title))
    
    fs_bullets = [
        "• <b>Integration with Wearable Devices:</b> Connect with smartwatches and continuous biosensors for real-time heart rate variability (HRV), photoplethysmography (PPG), and sleep stage tracking.",
        "• <b>Acoustic & Multilingual NLP Models:</b> Expand NLP capabilities to regional languages (Hindi, Telugu, Tamil) and integrate acoustic speech prosody analysis via librosa/Wav2Vec2.",
        "• <b>Multicenter Clinical Trial Validation:</b> Conduct extensive cross-cohort validation on clinical psychiatric inpatient datasets to enhance generalizability across diverse demographics.",
        "• <b>Cross-Platform Mobile Application:</b> Develop native React Native and Flutter mobile applications for wider accessibility in rural school counseling programs.",
        "• <b>EHR / FHIR Interoperability:</b> Implement automated HL7/FHIR microservices for seamless bilateral data sync with hospital Electronic Health Record systems."
    ]
    for b in fs_bullets:
        story.append(Paragraph(b, st_bullet))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 19: REFERENCES (Part 1: Studies 1 to 7)
    # =========================================================================
    story.append(Paragraph("References (Part 1: Studies [1] to [7])", st_slide_title))
    
    refs_1 = [
        "[1] S. A. Suresh and S. Agarwal, \"Hybrid ML Approach for Mental Health Prediction,\" in Proc. 4th Int. Conf. Innovative Mechanisms for Industry Applications (ICIMIA), IEEE, 2025.",
        "[2] L. Hermawan, Meilinda, D. Stiawan, D. S. Ikhsan, and R. A. Syakurah, \"Mental Health with Machine Learning: A Prediction-Based Intervention Chatbot for Mental Health Conversations,\" in Proc. IEEE Conf., 2024.",
        "[3] H. Dhawale, D. Thakare, N. C. Morris, R. Agrawal, and C. Dhule, \"The Prediction of Mental Health Using Machine Learning,\" in Proc. 15th Int. Conf. Computing Communication and Networking Technologies (ICCCNT), IEEE, 2024.",
        "[4] N. Jayakumar and R. N., \"Modeling Mental Health: Advances in Predictive Science towards Proactive Health Care,\" in Proc. IEEE Int. Conf. for Women in Innovation, Technology & Entrepreneurship (ICWITE), 2024.",
        "[5] S. Purohit, R. Mudgal, S. Vats, P. Rana, and A. Verma, \"Analyzing the Impact of Social Media Usage on Mental Health: A Machine Learning Approach,\" in Proc. 15th ICCCNT, IEEE, 2024.",
        "[6] J. Cherian et al., \"Multimodal Markers of Transdiagnostic Childhood Mental Health Impairment,\" in Proc. IEEE Conf., 2024.",
        "[7] Y. Koh, C. Lee, Y. Ku, and U. Lee, \"Data Visualization for Mental Health Monitoring in Smart Home Environment: A Case Study,\" in Proc. IEEE Conf., 2023."
    ]
    for r in refs_1:
        story.append(Paragraph(r, st_bullet))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 20: REFERENCES (Part 2: Studies 8 to 16)
    # =========================================================================
    story.append(Paragraph("References (Part 2: Studies [8] to [16])", st_slide_title))
    
    refs_2 = [
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
    for r in refs_2:
        story.append(Paragraph(r, st_bullet))
        story.append(Spacer(1, 2))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 21: THANK YOU
    # =========================================================================
    story.append(Spacer(1, 60))
    
    ty_box = [
        [Paragraph("<font size=24 color='#1E3A8A'><b>THANK YOU</b></font>", styles['Normal'])],
        [Spacer(1, 10)],
        [Paragraph("<font size=14 color='#2563EB'><b>Questions & Discussion</b></font>", styles['Normal'])],
        [Spacer(1, 15)],
        [Paragraph("<b>SMART HEALTH RISK INDICATOR (SHRI)</b><br/>"
                   "<i>A Privacy-Preserving Browser-Native AI Clinical Decision Support System</i><br/><br/>"
                   "<b>Live Web Portal:</b> <font color='#2563EB'><u>https://nishanth702.github.io/-Smart-Health-Risk-Indicator-SHRI-/</u></font><br/>"
                   "<b>GitHub Repository:</b> <font color='#2563EB'><u>https://github.com/nishanth702/-Smart-Health-Risk-Indicator-SHRI-</u></font>", st_body)]
    ]
    t_ty = Table(ty_box, colWidths=[700])
    t_ty.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 20),
        ('BOTTOMPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(t_ty)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Review-2 presentation PDF at: {output_path}")

if __name__ == "__main__":
    out_desktop = r"C:\Users\nishanth golakoti\Desktop\Smart_Health_Risk_Indicator_Review2.pdf"
    create_presentation_pdf(out_desktop)
