"""
Generate Review 2 Presentation PDF for Smart Health Risk Indicator (SHRI)
Matching the exact structure and content from ADMRI PPT & Review 2 slides.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header for slide pages > 1
        if self._pageNumber > 1:
            self.drawString(40, 570, "SMART HEALTH RISK INDICATOR (SHRI) — REVIEW 2 PRESENTATION")
            self.drawRightString(752, 570, "PROJECT REVIEW - II")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(40, 564, 752, 564)
            
        # Footer
        self.setFont("Helvetica", 8)
        self.drawString(40, 25, "School of Computer Science & Engineering | Smart Health Risk Indicator (SHRI)")
        self.drawRightString(752, 25, f"Slide {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(40, 35, 752, 35)
        self.restoreState()


def build_review2_pdf(output_path):
    # Landscape orientation for slides format (792 x 612)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0F172A")
    ACCENT = colors.HexColor("#0284C7")
    ACCENT_LIGHT = colors.HexColor("#F0F9FF")
    SECONDARY = colors.HexColor("#334155")
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#64748B")
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    SUCCESS_BG = colors.HexColor("#F0FDF4")
    SUCCESS_BORDER = colors.HexColor("#10B981")

    slide_title = ParagraphStyle(
        'SlideTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=10
    )
    cover_title = ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=PRIMARY,
        alignment=1,
        spaceAfter=10
    )
    cover_subtitle = ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=ACCENT,
        alignment=1,
        spaceAfter=20
    )
    body_style = ParagraphStyle(
        'SlideBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'SlideBullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=TEXT_DARK,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    table_header = ParagraphStyle(
        'THeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )
    table_body = ParagraphStyle(
        'TBody',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=TEXT_DARK
    )

    story = []

    # ── SLIDE 1: TITLE SLIDE ──────────────────────────────────────────────────
    story.append(Spacer(1, 40))
    story.append(Paragraph("SMART HEALTH RISK INDICATOR (SHRI)", cover_title))
    story.append(Paragraph("A Browser-Native AI-Powered Clinical Decision Support System for Adolescent Mental Health Monitoring", cover_subtitle))
    story.append(HRFlowable(width="80%", thickness=2, color=ACCENT, spaceAfter=25))
    
    meta_box = [
        [
            Paragraph("<b>Project Category:</b> RESEARCH / APPLIED HEALTHCARE AI", body_style),
            Paragraph("<b>Course:</b> BCSE497J — PROJECT 1 (REVIEW 2)", body_style)
        ],
        [
            Paragraph("<b>Programme:</b> B.Tech in Computer Science and Engineering", body_style),
            Paragraph("<b>Specialization:</b> Artificial Intelligence & Machine Learning", body_style)
        ]
    ]
    t_meta = Table(meta_box, colWidths=[350, 350])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # ── SLIDE 2: ABSTRACT ─────────────────────────────────────────────────────
    story.append(Paragraph("Abstract", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    story.append(Paragraph(
        "• Depression, anxiety, and sleep disturbances are increasingly prevalent among adolescents (ages 10–18), yet continuous proactive clinical monitoring remains constrained by privacy risks, stigma, and heavy cloud infrastructure costs.<br/>"
        "• This project presents <b>Smart Health Risk Indicator (SHRI)</b>, a secure, browser-native AI clinical decision support platform for multi-domain screening and longitudinal monitoring.<br/>"
        "• The platform seamlessly integrates validated clinical psychometric instruments (<b>PHQ-9</b>, <b>GAD-7</b>, <b>ISI</b>, <b>SCARED</b>), real-time NLP-based clinical journal sentiment analysis with crisis keyword escalation, and physiological/behavioral biomarkers.<br/>"
        "• A <b>four-model stacked ensemble neural network</b> is implemented entirely in the browser (TensorFlow.js / local Python client), ensuring zero sensitive patient biometrics leave the device.<br/>"
        "• The system generates an adaptive <b>0–100 composite risk score</b> with severity tiers, <b>Monte Carlo Dropout 95% Confidence Intervals</b>, statistical anomaly detection (|z| ≥ 2.0σ), trajectory forecasting (Linear Regression + EWMA), and automated CBT action plans with FHIR export.",
        body_style
    ))
    story.append(PageBreak())

    # ── SLIDE 3: INTRODUCTION & PROBLEM STATEMENT ─────────────────────────────
    story.append(Paragraph("Introduction & Problem Statement", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))
    story.append(Paragraph("<b>Background & Motivation:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=10, textColor=ACCENT, spaceAfter=4)))
    story.append(Paragraph("• Adolescent mental health disorders are rising globally, yet early detection is limited due to subjective manual scoring, lack of real-time tracking, and privacy barriers in cloud-hosted solutions.", bullet_style))
    story.append(Paragraph("• Traditional evaluations rely on periodic questionnaires with zero continuous predictive insights, failing to capture subtle daily behavioral shifts or acute crisis events.", bullet_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Key Problem Statements Identified:</b>", ParagraphStyle('SubH2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#EF4444"), spaceAfter=4)))
    story.append(Paragraph("1. <b>Absence of Privacy-Preserving Browser-Native AI:</b> Most existing tools require sending sensitive adolescent psychological reflections to remote cloud servers, violating HIPAA/data-protection standards.", bullet_style))
    story.append(Paragraph("2. <b>Lack of Multimodal Integration & Uncertainty Estimation:</b> Existing digital screeners use single-model point estimates without epistemic uncertainty quantification (confidence intervals) or cross-domain behavioral modeling.", bullet_style))
    story.append(Paragraph("3. <b>Static vs. Longitudinal Predictive Gaps:</b> Clinicians lack automated statistical anomaly detection and trajectory forecasting tools to predict 30-day symptom progression.", bullet_style))
    story.append(PageBreak())

    # ── SLIDE 4: LITERATURE REVIEW (TABLE 1: PAPERS 1 - 8) ────────────────────
    story.append(Paragraph("Literature Review (Summary of Key Studies: 1 to 8)", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    
    lit1_data = [
        [Paragraph("S.No", table_header), Paragraph("Title, Author & Year", table_header), Paragraph("Methodology & Findings", table_header), Paragraph("Identified Gaps & Limitations", table_header)],
        [
            Paragraph("1", table_body),
            Paragraph("<b>Hybrid ML Approach for Mental Health Prediction</b><br/>Suresh & Agarwal (IEEE, 2025)", table_body),
            Paragraph("Ensemble models (RF, GB, LightGBM, CatBoost) + GNN on synthetic workplace dataset. Accuracy up to 99%.", table_body),
            Paragraph("Synthetic dataset limits real-world generalization; limited clinical interpretability in GNN.", table_body)
        ],
        [
            Paragraph("2", table_body),
            Paragraph("<b>Prediction-Based Intervention Chatbot</b><br/>Hermawan et al. (IEEE, 2024)", table_body),
            Paragraph("DASS-21 dataset (424 records). Evaluated RFC (82.5%) vs MNB (66%) for conversation triggers.", table_body),
            Paragraph("Small dataset; limited demographic diversity; no unified clinical deployment validation.", table_body)
        ],
        [
            Paragraph("3", table_body),
            Paragraph("<b>Prediction of Mental Health Using ML</b><br/>Dhawale et al. (ICCCNT, 2024)", table_body),
            Paragraph("KNN (82.5%) and Logistic Regression on employee dataset with visual analytics.", table_body),
            Paragraph("Limited algorithms; small sample size; no multimodal inputs (questionnaires only).", table_body)
        ],
        [
            Paragraph("4", table_body),
            Paragraph("<b>Advances in Predictive Mental Health</b><br/>Jayakumar & R.N. (ICWITE, 2024)", table_body),
            Paragraph("Systematic review of SVM, RF, XGBoost, and Transfer Learning in psychiatry.", table_body),
            Paragraph("Review-based; lacks unified experimental benchmark or client-side runtime deployment.", table_body)
        ],
        [
            Paragraph("5", table_body),
            Paragraph("<b>Impact of Social Media on Mental Health</b><br/>Purohit et al. (ICCCNT, 2024)", table_body),
            Paragraph("Kaggle dataset (481 rows). Logistic Regression (99.3%) and Gaussian NB (94.4%).", table_body),
            Paragraph("Cross-sectional study with high risk of overfitting on tiny sample size.", table_body)
        ],
        [
            Paragraph("6", table_body),
            Paragraph("<b>Multimodal Markers of Childhood Impairment</b><br/>Cherian et al. (IEEE, 2024)", table_body),
            Paragraph("Smartphone sensor data + canonical correlation analysis under RDoC clinical framework.", table_body),
            Paragraph("Heavy smartphone sensor dependency; small clinical cohort; no local edge inference.", table_body)
        ],
        [
            Paragraph("7", table_body),
            Paragraph("<b>Data Visualization in Smart Homes</b><br/>Koh et al. (KAIST / IEEE, 2023)", table_body),
            Paragraph("Web-based visualization correlating IoT smart home sensor data with self-reports.", table_body),
            Paragraph("Focuses solely on UI visualization; lacks predictive ML modeling or uncertainty metrics.", table_body)
        ],
        [
            Paragraph("8", table_body),
            Paragraph("<b>Evaluation Model of College Mental Health</b><br/>Li & Xu (IEEE HBDSS, 2021)", table_body),
            Paragraph("AHP, fuzzy complementary judgment matrix, clustering, and social network mining.", table_body),
            Paragraph("Fuzzy scoring is not predictive ML-based; limited scalability across general cohorts.", table_body)
        ]
    ]
    t_lit1 = Table(lit1_data, colWidths=[25, 210, 240, 237])
    t_lit1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_lit1)
    story.append(PageBreak())

    # ── SLIDE 5: LITERATURE REVIEW (TABLE 2: PAPERS 9 - 16) ───────────────────
    story.append(Paragraph("Literature Review (Summary of Key Studies: 9 to 16)", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    
    lit2_data = [
        [Paragraph("S.No", table_header), Paragraph("Title, Author & Year", table_header), Paragraph("Methodology & Findings", table_header), Paragraph("Identified Gaps & Limitations", table_header)],
        [
            Paragraph("9", table_body),
            Paragraph("<b>Brain Wave Response in VR for Autistic Children</b><br/>Peng & Leong (ICSIPA, 2024)", table_body),
            Paragraph("EEG signals (30 autistic children) in VR artistic environments with cognitive tests.", table_body),
            Paragraph("Tiny sample (n=30); expensive proprietary EEG hardware required; unsuited for daily use.", table_body)
        ],
        [
            Paragraph("10", table_body),
            Paragraph("<b>Visualizing Trajectories in CAMHS EHR</b><br/>Pant et al. (IEEE BIBM, 2024)", table_body),
            Paragraph("35-year CAMHS EHR data. Trajectory visualization + ADHD co-occurrence graphs.", table_body),
            Paragraph("Retrospective statistical analysis; no real-time predictive model; privacy concerns with raw EHR.", table_body)
        ],
        [
            Paragraph("11", table_body),
            Paragraph("<b>Early Detection for Mental Issues in Children</b><br/>Kataru et al. (COMPSAC, 2024)", table_body),
            Paragraph("2,600 students dataset. Multi-tier ML pipeline achieving 94.5% accuracy.", table_body),
            Paragraph("Limited strictly to elementary students; geographic restrictions; lacks explainability.", table_body)
        ],
        [
            Paragraph("12", table_body),
            Paragraph("<b>AI Screening for Homeless Children</b><br/>Madhuri et al. (IEEE, 2025)", table_body),
            Paragraph("Pediatric Symptom Checklist (PSC) dataset with SVM classifier (90% accuracy).", table_body),
            Paragraph("Questionnaire-only; lacks multimodal text NLP or uncertainty quantification.", table_body)
        ],
        [
            Paragraph("13", table_body),
            Paragraph("<b>Environment & Health of Left-Behind Children</b><br/>Xia Yuan (IEEE, 2023)", table_body),
            Paragraph("Structural Equation Modeling (SEM) analyzing family/environmental factors.", table_body),
            Paragraph("Purely correlational statistical study; not predictive ML; context-specific.", table_body)
        ],
        [
            Paragraph("14", table_body),
            Paragraph("<b>Comparative Study on Detection in Children</b><br/>Gowda et al. (NEleX, 2023)", table_body),
            Paragraph("Review of physiological signal-based ML detection techniques in child psychiatry.", table_body),
            Paragraph("Literature review only; no implementation benchmarking or software framework.", table_body)
        ],
        [
            Paragraph("15", table_body),
            Paragraph("<b>Personalised Risk Factors on Multimodal Data</b><br/>Amirhosseini et al. (IEEE IS, 2024)", table_body),
            Paragraph("NHANES multimodal dataset (19,560 records). LR, SVM, LASSO, RF (R²=0.93, MAE=0.51).", table_body),
            Paragraph("US adult cohort; high computational complexity; lacks edge browser deployment.", table_body)
        ],
        [
            Paragraph("16", table_body),
            Paragraph("<b>Public Mental Health Analytics Framework</b><br/>Marrapu et al. (ICSTSN, 2022)", table_body),
            Paragraph("KDD, data fusion, visualization, Low/Med/High classification (85.06% accuracy).", table_body),
            Paragraph("Framework design; lacks deep learning integration and automated crisis triggers.", table_body)
        ]
    ]
    t_lit2 = Table(lit2_data, colWidths=[25, 210, 240, 237])
    t_lit2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_lit2)
    story.append(PageBreak())

    # ── SLIDE 6: EXISTING VS PROPOSED SYSTEM ──────────────────────────────────
    story.append(Paragraph("Comparison: Existing Systems vs. Proposed SHRI", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    
    comp_data = [
        [Paragraph("Feature / Dimension", table_header), Paragraph("Existing Clinical Screening Systems", table_header), Paragraph("Proposed Smart Health Risk Indicator (SHRI)", table_header)],
        [
            Paragraph("<b>Data Privacy & Execution</b>", table_body),
            Paragraph("Cloud-hosted servers / third-party APIs; sensitive adolescent text transmitted over public web.", table_body),
            Paragraph("<b>100% Browser-Native / Client-Side (TensorFlow.js)</b>; zero sensitive patient biometrics leave the device.", table_body)
        ],
        [
            Paragraph("<b>Model Architecture</b>", table_body),
            Paragraph("Single generic classifier (SVM, Random Forest, or linear regression).", table_body),
            Paragraph("<b>4-Model Stacked Ensemble</b> (DepNet, AnxNet, SleepNet + FusionNet Meta-Learner).", table_body)
        ],
        [
            Paragraph("<b>Uncertainty Quantification</b>", table_body),
            Paragraph("Single point estimates (e.g. 'Score: 70') without confidence bounds.", table_body),
            Paragraph("<b>Monte Carlo Dropout (20 passes)</b> computing exact 95% Confidence Interval (±1.96σ).", table_body)
        ],
        [
            Paragraph("<b>Explainable AI (XAI)</b>", table_body),
            Paragraph("Black-box predictions with little to no clinical interpretability.", table_body),
            Paragraph("<b>Permutation SHAP Attribution</b> decomposing score into exact positive risk and protective points.", table_body)
        ],
        [
            Paragraph("<b>Longitudinal Tracking</b>", table_body),
            Paragraph("Isolated, static snapshots conducted during sporadic clinic visits.", table_body),
            Paragraph("<b>30-Day Trajectory Forecasting (LR + EWMA)</b> & <b>2σ Statistical Anomaly Detection</b>.", table_body)
        ],
        [
            Paragraph("<b>Clinical Decision Support</b>", table_body),
            Paragraph("Manual score summation without automated intervention paths.", table_body),
            Paragraph("Automated <b>evidence-graded CBT protocols</b> and <b>HL7 FHIR JSON / PDF export</b>.", table_body)
        ]
    ]
    t_comp = Table(comp_data, colWidths=[130, 280, 302])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(PageBreak())

    # ── SLIDE 7: ARCHITECTURE DIAGRAM & PIPELINE ──────────────────────────────
    story.append(Paragraph("System Architecture & Pipeline Flow", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))
    
    arch_flow = [
        [
            Paragraph("<b>1. INPUT LAYER</b>", ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY)),
            Paragraph("<b>2. 20D FEATURE MATRIX</b>", ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY)),
            Paragraph("<b>3. SPECIALIST NETS</b>", ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY)),
            Paragraph("<b>4. FUSIONNET & MC</b>", ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY)),
            Paragraph("<b>5. CLINICAL OUTPUTS</b>", ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY))
        ],
        [
            Paragraph("• PHQ-9 (Depression)<br/>• GAD-7 (Anxiety)<br/>• ISI (Insomnia)<br/>• SCARED (Child Anx)<br/>• Journal Text NLP<br/>• Lifestyle Biomarkers", table_body),
            Paragraph("• Normalized Subscores<br/>• Sleep/Screen/Exer Risk<br/>• Depr x Anx Interaction<br/>• Sleep x Sentiment Term<br/>• Trend & Session Count", table_body),
            Paragraph("• <b>🔴 DepNet</b> (10 Feats)<br/>• <b>🟠 AnxNet</b> (11 Feats)<br/>• <b>🔵 SleepNet</b> (11 Feats)<br/>Trained on 6,000 hybrid clinical samples.", table_body),
            Paragraph("• <b>🧠 FusionNet</b> (23 In)<br/>Stacked Meta-Learner<br/>• <b>🎲 MC Dropout</b><br/>20 Stochastic Passes<br/>Mean + 95% CI (±1.96σ)", table_body),
            Paragraph("• 0-100 Risk Score<br/>• SHAP XAI Waterfall<br/>• 30-Day Forecast (EWMA)<br/>• 2σ Anomaly Alerts<br/>• CBT Action Plans<br/>• FHIR / PDF Export", table_body)
        ]
    ]
    t_arch = Table(arch_flow, colWidths=[142, 142, 142, 142, 144])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,1), (-1,1), ACCENT_LIGHT),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor("#38BDF8")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Mathematical Formulations:</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=10, textColor=ACCENT)))
    story.append(Paragraph("• <b>Monte Carlo Dropout:</b> &nbsp; $\\mu = \\frac{1}{N}\\sum_{i=1}^{N}\\hat{y}_i, \\quad \\sigma = \\sqrt{\\frac{1}{N}\\sum (\\hat{y}_i - \\mu)^2}, \\quad 95\\%\\text{ CI} = [\\mu - 1.96\\sigma, \\, \\mu + 1.96\\sigma]$", bullet_style))
    story.append(Paragraph("• <b>Hybrid Forecast:</b> &nbsp; $\\text{Forecast} = 0.6 \\cdot (\\text{Intercept} + \\text{Slope} \\cdot n) + 0.4 \\cdot (\\text{EWMA}_t + 0.5 \\cdot \\text{Slope}), \\quad \\text{where } \\text{EWMA}_t = 0.4Y_t + 0.6\\text{EWMA}_{t-1}$", bullet_style))
    story.append(Paragraph("• <b>Statistical Anomaly Z-Score:</b> &nbsp; $z = (Y_{\\text{latest}} - \\mu_{\\text{baseline}}) / \\sigma_{\\text{baseline}} \\quad \\text{Trigger Alert if } |z| \\ge 2.0$", bullet_style))
    story.append(PageBreak())

    # ── SLIDE 8: THE 8 CORE MODULES ───────────────────────────────────────────
    story.append(Paragraph("Project Architecture: 8 Core Modules Description", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    
    mod_data = [
        [Paragraph("Module", table_header), Paragraph("Description & Engineering Implementation", table_header), Paragraph("Status", table_header)],
        [
            Paragraph("<b>1. Data Ingestion & Preprocessing</b>", table_body),
            Paragraph("Ingests 10 questionnaire items, lifestyle biomarkers, and journal reflections. Performs zero-loss scaling and feature normalization.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>2. Multimodal Feature Engineering</b>", table_body),
            Paragraph("Generates 20-dimensional feature representations including cross-domain interaction terms ($Depression \\times Anxiety$, $Sleep \\times Sentiment$).", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>3. 4-Model Stacked Ensemble</b>", table_body),
            Paragraph("Builds DepNet, AnxNet, and SleepNet specialist networks fused by the 23-input FusionNet meta-learner using Stacked Generalization.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>4. Clinical Dataset & Optimization</b>", table_body),
            Paragraph("Synthesizes 6,000 hybrid samples modeling published distributions (PHQ-9, GAD-7, ISI, SCARED) with SMOTE oversampling and L2 regularization.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>5. Uncertainty & Forecasting</b>", table_body),
            Paragraph("Monte Carlo Dropout (20 stochastic passes, 95% CI), 30-day EWMA trajectory forecasting, and 2σ statistical anomaly detection.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>6. Real-Time Clinical NLP Engine</b>", table_body),
            Paragraph("90-word clinical lexicon, 20 crisis bigrams ('want to die', 'can't cope'), intensifiers/negators, and instant emergency helpline alerts.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>7. Explainable AI & Clinical Interventions</b>", table_body),
            Paragraph("Permutation SHAP feature attribution bars, evidence-graded CBT action plans, and HL7 FHIR DiagnosticReport JSON export.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ],
        [
            Paragraph("<b>8. Interactive Web UI & Deployment</b>", table_body),
            Paragraph("Client-side web portal (HTML5/CSS3/JS + Streamlit Python), 24/7 public hosting via GitHub Pages without cloud server dependency.", table_body),
            Paragraph("<font color='#10B981'><b>Completed (100%)</b></font>", table_body)
        ]
    ]
    t_mod = Table(mod_data, colWidths=[150, 480, 82])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_mod)
    story.append(PageBreak())

    # ── SLIDE 9: EXPERIMENTAL RESULTS & BENCHMARKS ────────────────────────────
    story.append(Paragraph("Experimental Results & Benchmarking", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))
    
    res_data = [
        [Paragraph("Model Architecture", table_header), Paragraph("Input Features", table_header), Paragraph("MAE (pts)", table_header), Paragraph("RMSE (pts)", table_header), Paragraph("R² Score", table_header), Paragraph("Inference Latency", table_header)],
        [
            Paragraph("<b>🔴 DepNet (Depression Specialist)</b>", table_body),
            Paragraph("10 Features", table_body),
            Paragraph("4.2", table_body),
            Paragraph("5.3", table_body),
            Paragraph("0.912", table_body),
            Paragraph("2.8 ms", table_body)
        ],
        [
            Paragraph("<b>🟠 AnxNet (Anxiety Specialist)</b>", table_body),
            Paragraph("11 Features", table_body),
            Paragraph("4.5", table_body),
            Paragraph("5.6", table_body),
            Paragraph("0.904", table_body),
            Paragraph("2.9 ms", table_body)
        ],
        [
            Paragraph("<b>🔵 SleepNet (Sleep & Lifestyle)</b>", table_body),
            Paragraph("11 Features", table_body),
            Paragraph("4.8", table_body),
            Paragraph("5.9", table_body),
            Paragraph("0.887", table_body),
            Paragraph("2.4 ms", table_body)
        ],
        [
            Paragraph("<b>🧠 FusionNet (Stacked Meta-Learner)</b>", table_body),
            Paragraph("<b>23 Features (20 + 3 Sub-Preds)</b>", table_body),
            Paragraph("<b>3.2</b>", table_body),
            Paragraph("<b>4.1</b>", table_body),
            Paragraph("<b>0.942</b>", table_body),
            Paragraph("<b>4.6 ms</b>", table_body)
        ],
        [
            Paragraph("<b>🎲 Ensemble + 20 MC Dropout Passes</b>", table_body),
            Paragraph("Full Multimodal Array", table_body),
            Paragraph("<b>3.1</b>", table_body),
            Paragraph("<b>3.9</b>", table_body),
            Paragraph("<b>0.948</b>", table_body),
            Paragraph("<b>11.2 ms (Real-Time)</b>", table_body)
        ]
    ]
    t_res = Table(res_data, colWidths=[180, 110, 80, 80, 80, 182])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>Key Findings & Validation Highlights:</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=10, textColor=ACCENT)))
    story.append(Paragraph("• <b>Stacked Ensemble Outperformance:</b> FusionNet achieves a superior $R^2 = 0.948$ with a mean absolute error of just $3.1$ points across the 6,000 hybrid clinical dataset, outperforming all single-model baselines.", bullet_style))
    story.append(Paragraph("• <b>Ultra-Low Edge Latency:</b> Full 20-pass Monte Carlo Dropout inference runs in <b>11.2 ms</b> on client hardware, enabling instantaneous 60 FPS slider reactivity.", bullet_style))
    story.append(Paragraph("• <b>High Crisis Sensitivity:</b> The clinical NLP engine achieved <b>98.4% sensitivity</b> on emergency crisis bigram detection with zero false-negative bypass.", bullet_style))
    story.append(PageBreak())

    # ── SLIDE 10: CONCLUSION & FUTURE SCOPE ───────────────────────────────────
    story.append(Paragraph("Conclusion & Future Scope (Remaining 25%)", slide_title))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))
    
    concl_box = [
        Paragraph("<b>Conclusion of Review 2 (75% Milestone):</b>", ParagraphStyle('CH', fontName='Helvetica-Bold', fontSize=10, textColor=PRIMARY)),
        Paragraph("• Successfully developed and validated <b>Smart Health Risk Indicator (SHRI)</b> as a privacy-first, browser-native AI decision support system.<br/>"
                  "• Demonstrated robust multimodal integration (PHQ-9, GAD-7, ISI, SCARED, NLP sentiment, lifestyle biomarkers) with 4-model stacked generalization.<br/>"
                  "• Provided clinical transparency via Permutation SHAP attribution and safety via Monte Carlo Dropout 95% Confidence Intervals.<br/>"
                  "• Deployed live on GitHub Pages with zero server cost or cloud exposure.", body_style)
    ]
    t_c = Table([[concl_box]], colWidths=[712])
    t_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SUCCESS_BG),
        ('BOX', (0,0), (-1,-1), 1, SUCCESS_BORDER),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_c)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Future Scope for 100% Final Defense (Remaining 25%):</b>", ParagraphStyle('FH', fontName='Helvetica-Bold', fontSize=10, textColor=ACCENT)))
    story.append(Paragraph("1. <b>Multi-Hospital Clinical EHR Validation (10%):</b> Prospective ROC-AUC and Sensitivity/Specificity benchmarking on real-world clinical cohorts.", bullet_style))
    story.append(Paragraph("2. <b>Acoustic Speech Biomarker Ingestion (5%):</b> Voice prosody extraction (vocal jitter, shimmer, pause latency) via Python <i>librosa</i> for tri-modal scoring.", bullet_style))
    story.append(Paragraph("3. <b>Microservice Architecture & Docker (5%):</b> Asynchronous FastAPI REST microservices with Docker containerization and Swagger documentation.", bullet_style))
    story.append(Paragraph("4. <b>Regional Multi-Language Localization (5%):</b> Translating psychometric questionnaires and crisis lexicons into Hindi and Telugu for rural health access.", bullet_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Live Web Portal:</b> <font color='#0284C7'><u>https://nishanth702.github.io/-Smart-Health-Risk-Indicator-SHRI-/</u></font>", ParagraphStyle('URL', fontName='Helvetica-Bold', fontSize=10, alignment=1)))

    doc.build(story, canvasmaker=SlideCanvas)
    print(f"[SUCCESS] Review 2 PDF generated at: {output_path}")


if __name__ == "__main__":
    desktop_path = r"C:\Users\nishanth golakoti\Desktop\Smart_Health_Risk_Indicator_Review2.pdf"
    build_review2_pdf(desktop_path)
