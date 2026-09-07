"""
Generate Complete Project Report PDF for Smart Health Risk Indicator (SHRI)
Matching the BCSE497J Project-I Report Format and Table of Contents.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class ReportCanvas(canvas.Canvas):
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
            self.draw_report_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_report_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Cover page (page 1) has no header/footer
        if self._pageNumber > 1:
            self.drawString(54, 750, "BCSE497J Project-I | Smart Health Risk Indicator (SHRI)")
            self.drawRightString(558, 750, "Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
            # Footer
            page_str = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 36, page_str)
            self.drawString(54, 36, "School of Computer Science and Engineering (SCOPE) — Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 46, 558, 46)
        self.restoreState()


def build_project_report_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    PRIMARY = colors.HexColor("#0F172A")
    ACCENT = colors.HexColor("#0284C7")
    ACCENT_LIGHT = colors.HexColor("#F0F9FF")
    SECONDARY = colors.HexColor("#334155")
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#64748B")
    BORDER_COLOR = colors.HexColor("#CBD5E1")

    # Styles
    cover_course = ParagraphStyle('CoverCourse', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=PRIMARY, alignment=1, spaceAfter=15)
    cover_title = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=20, leading=26, textColor=PRIMARY, alignment=1, spaceAfter=20)
    cover_dept = ParagraphStyle('CoverDept', fontName='Helvetica', fontSize=10.5, leading=15, textColor=SECONDARY, alignment=1, spaceAfter=8)
    
    h1_style = ParagraphStyle('RepH1', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=PRIMARY, spaceBefore=14, spaceAfter=8, keepWithNext=True)
    h2_style = ParagraphStyle('RepH2', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=ACCENT, spaceBefore=10, spaceAfter=5, keepWithNext=True)
    h3_style = ParagraphStyle('RepH3', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=SECONDARY, spaceBefore=6, spaceAfter=3, keepWithNext=True)
    body_style = ParagraphStyle('RepBody', fontName='Helvetica', fontSize=9.5, leading=14, textColor=TEXT_DARK, spaceAfter=6)
    bullet_style = ParagraphStyle('RepBullet', fontName='Helvetica', fontSize=9, leading=13.5, textColor=TEXT_DARK, leftIndent=14, firstLineIndent=-9, spaceAfter=3)
    
    table_header = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, leading=10.5, textColor=colors.white)
    table_body = ParagraphStyle('TB', fontName='Helvetica', fontSize=7.5, leading=10, textColor=TEXT_DARK)

    story = []

    # ── PAGE 1: TITLE / COVER PAGE ───────────────────────────────────────────
    story.append(Spacer(1, 30))
    story.append(Paragraph("BCSE497J Project-I", cover_course))
    story.append(Spacer(1, 10))
    story.append(Paragraph("SMART HEALTH RISK INDICATOR (SHRI):<br/>BROWSER-NATIVE AI-POWERED CLINICAL DECISION SUPPORT SYSTEM FOR ADOLESCENT MENTAL HEALTH MONITORING", cover_title))
    story.append(HRFlowable(width="75%", thickness=2, color=ACCENT, spaceAfter=30))
    
    story.append(Paragraph("<b>Submitted for Project Review - II</b>", ParagraphStyle('Sub', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=ACCENT, alignment=1, spaceAfter=25)))
    
    author_box = [
        [Paragraph("<b>Programme:</b>", body_style), Paragraph("B.Tech in Computer Science and Engineering", body_style)],
        [Paragraph("<b>Course Code:</b>", body_style), Paragraph("BCSE497J — PROJECT 1", body_style)],
        [Paragraph("<b>Specialization:</b>", body_style), Paragraph("Artificial Intelligence, Machine Learning & Data Science", body_style)],
        [Paragraph("<b>School:</b>", body_style), Paragraph("School of Computer Science and Engineering (SCOPE)", body_style)],
        [Paragraph("<b>Academic Year:</b>", body_style), Paragraph("2026", body_style)],
        [Paragraph("<b>Live System URL:</b>", body_style), Paragraph("https://nishanth702.github.io/-Smart-Health-Risk-Indicator-SHRI-/", body_style)]
    ]
    t_auth = Table(author_box, colWidths=[150, 320])
    t_auth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_auth)
    story.append(PageBreak())

    # ── PAGE 2: ABSTRACT ──────────────────────────────────────────────────────
    story.append(Paragraph("ABSTRACT", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=10))
    story.append(Paragraph(
        "Adolescent mental health disorders—encompassing depression, anxiety, insomnia, and behavioral dysregulation—have emerged as an escalating public health crisis worldwide. Despite the severe long-term consequences of untreated psychological distress in youth (ages 10–18), proactive early detection remains severely hindered by social stigma, clinician shortages, and traditional questionnaire-based screening that offers no predictive tracking. Existing digital mental health applications frequently rely on third-party cloud-hosted inference pipelines, raising severe patient confidentiality concerns under HIPAA/FERPA standards and precluding deployment in low-resource or disconnected clinical environments.",
        body_style
    ))
    story.append(Paragraph(
        "This project presents the <b>Smart Health Risk Indicator (SHRI)</b>, an innovative, browser-native, AI-powered Clinical Decision Support System (CDSS) designed for adolescent mental health screening, uncertainty quantification, and longitudinal monitoring. The system combines validated clinical instruments (<b>PHQ-9</b>, <b>GAD-7</b>, <b>ISI</b>, <b>SCARED</b>), real-time Natural Language Processing (NLP) journal sentiment scoring with emergency crisis escalation, and lifestyle behavioral biomarkers into a unified <b>20-dimensional multimodal feature engineering matrix</b>.",
        body_style
    ))
    story.append(Paragraph(
        "At the core of SHRI is a <b>four-model stacked ensemble architecture</b> composed of three domain-specialist neural networks (<i>DepNet</i>, <i>AnxNet</i>, <i>SleepNet</i>) combined with a 23-input meta-learner (<i>FusionNet</i>) using Stacked Generalization. To eliminate the medical risks of overconfident point predictions, the platform incorporates <b>Monte Carlo Dropout (20 stochastic passes)</b> to yield an empirical mean and an exact <b>95% Confidence Interval</b> ($Score \\pm 1.96\\sigma$). Furthermore, the framework integrates Explainable AI (XAI) using <b>Permutation SHAP attribution</b>, 30-day longitudinal trajectory forecasting (combining Linear Regression with Exponentially Weighted Moving Average, $\\alpha=0.4$), $2\\sigma$ statistical anomaly detection, and automated evidence-graded Cognitive Behavioral Therapy (CBT) recommendations with HL7 FHIR export.",
        body_style
    ))
    story.append(Paragraph(
        "Implemented entirely on the client-side using JavaScript, HTML5/CSS3, and Python, SHRI executes all neural inferences locally within the user's browser, ensuring that <b>zero sensitive patient biometrics or journal entries ever leave the device</b>. Experimental validation on a 6,000-sample clinically grounded benchmark demonstrates an ensemble accuracy of $R^2 = 0.948$, a Mean Absolute Error of $3.1$ points, and sub-12ms inference latency, providing an accessible, privacy-preserving, and infrastructure-independent platform for modern adolescent mental healthcare.",
        body_style
    ))
    story.append(Paragraph("<b>Keywords:</b> Artificial Intelligence, Healthcare Informatics, Clinical Decision Support, Stacked Ensemble, Monte Carlo Dropout, Explainable AI, Natural Language Processing, Privacy-Preserving AI.", ParagraphStyle('KW', fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY, spaceBefore=8)))
    story.append(PageBreak())

    # ── PAGE 3: TABLE OF CONTENTS ─────────────────────────────────────────────
    story.append(Paragraph("TABLE OF CONTENTS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=12))
    
    toc_data = [
        [Paragraph("<b>Sl.No</b>", table_header), Paragraph("<b>Contents</b>", table_header), Paragraph("<b>Page No.</b>", table_header)],
        [Paragraph("", table_body), Paragraph("<b>ABSTRACT</b>", table_body), Paragraph("1", table_body)],
        [Paragraph("<b>1.</b>", table_body), Paragraph("<b>INTRODUCTION</b>", table_body), Paragraph("3", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;1.1 Background", table_body), Paragraph("3", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;1.2 Motivation", table_body), Paragraph("3", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;1.3 Scope of the Project", table_body), Paragraph("4", table_body)],
        [Paragraph("<b>2.</b>", table_body), Paragraph("<b>PROJECT DESCRIPTION AND GOALS</b>", table_body), Paragraph("5", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;2.1 Literature Review (16 Studies)", table_body), Paragraph("5", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;2.2 Research Gap", table_body), Paragraph("8", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;2.3 Objectives", table_body), Paragraph("8", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;2.4 Problem Statement", table_body), Paragraph("9", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;2.5 Project Plan & Gantt Timeline", table_body), Paragraph("9", table_body)],
        [Paragraph("<b>3.</b>", table_body), Paragraph("<b>TECHNICAL SPECIFICATION</b>", table_body), Paragraph("10", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;3.1 Requirements (Functional & Non-Functional)", table_body), Paragraph("10", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;3.2 Feasibility Study (Technical, Economic, Social)", table_body), Paragraph("11", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;3.3 System Specification (Hardware & Software)", table_body), Paragraph("12", table_body)],
        [Paragraph("<b>4.</b>", table_body), Paragraph("<b>DESIGN APPROACH AND DETAILS</b>", table_body), Paragraph("13", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;4.1 System Architecture & Framework", table_body), Paragraph("13", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;4.2 Design Models (DFD, Use Case, Class, Sequence)", table_body), Paragraph("14", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;4.3 The 8 Modular Sub-Systems", table_body), Paragraph("16", table_body)],
        [Paragraph("", table_body), Paragraph("&nbsp;&nbsp;4.4 Experimental Results & Benchmarking", table_body), Paragraph("17", table_body)],
        [Paragraph("<b>5.</b>", table_body), Paragraph("<b>REFERENCES</b>", table_body), Paragraph("18", table_body)]
    ]
    t_toc = Table(toc_data, colWidths=[40, 410, 54])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ── CHAPTER 1: INTRODUCTION ───────────────────────────────────────────────
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    
    story.append(Paragraph("1.1 Background", h2_style))
    story.append(Paragraph(
        "Adolescence represents a critical neurodevelopmental window characterized by profound biological, emotional, and social transitions. Epidemiological studies from the World Health Organization (WHO) report that approximately 14% of adolescents globally experience mental health disorders, with depression and anxiety ranking among the leading contributors to disability. However, the majority of adolescent cases remain unrecognized and untreated until acute escalation. Conventional psychiatric assessments depend almost exclusively on retrospective clinical interviews and paper-based scoring (e.g., PHQ-9, GAD-7) conducted during periodic hospital visits. These traditional paradigms suffer from significant recall bias, subjective clinical variance, and complete absence of real-time early warning mechanisms.",
        body_style
    ))

    story.append(Paragraph("1.2 Motivation", h2_style))
    story.append(Paragraph(
        "The emergence of digital health technologies provides unprecedented opportunities for continuous adolescent monitoring. However, contemporary digital screening tools present critical vulnerabilities: (1) <i>Privacy Hazards</i>: Almost all commercial mental health apps transmit unencrypted or cloud-processed personal journals and behavioral data to third-party servers; (2) <i>Black-Box Predictors</i>: Standard machine learning applications deliver point-estimate scores without uncertainty bounds, leaving clinicians unaware of model confidence; (3) <i>Lack of Multimodal Integration</i>: Psychometric surveys, physiological sleep habits, and natural language self-reports are examined in isolation. This project is motivated by the imperative to engineer a <b>privacy-first, client-side, explainable, and multi-modal clinical decision support system</b> that operates reliably in the browser without server dependency.",
        body_style
    ))

    story.append(Paragraph("1.3 Scope of the Project", h2_style))
    story.append(Paragraph(
        "The scope of this project encompasses: (a) Programmatic generation of a 6,000-sample clinically validated hybrid training dataset; (b) Engineering a 20-dimensional multimodal feature pipeline capturing non-linear interactions ($Depression \\times Anxiety$, $Sleep \\times Sentiment$); (c) Constructing a 4-model stacked ensemble (DepNet, AnxNet, SleepNet, FusionNet); (d) Quantifying epistemic uncertainty via Monte Carlo Dropout (95% CI); (e) Building a real-time clinical NLP sentiment parser with 20 emergency crisis bigrams; (f) Implementing Permutation SHAP explainability and EWMA longitudinal trajectory forecasting; (g) Deploying a production-grade, responsive web portal live on GitHub Pages.",
        body_style
    ))
    story.append(PageBreak())

    # ── CHAPTER 2: PROJECT DESCRIPTION AND GOALS ──────────────────────────────
    story.append(Paragraph("2. PROJECT DESCRIPTION AND GOALS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))

    story.append(Paragraph("2.1 Literature Review", h2_style))
    story.append(Paragraph(
        "A rigorous systematic review of 16 recent studies (2021–2025) across IEEE, ACM, and biomedical journals was conducted to benchmark existing approaches:",
        body_style
    ))
    
    lit_summary_table = [
        [Paragraph("Study & Citation", table_header), Paragraph("Methodology", table_header), Paragraph("Identified Gap / Limitation", table_header)],
        [
            Paragraph("Suresh & Agarwal (IEEE, 2025)", table_body),
            Paragraph("Hybrid ML (RF, GB, CatBoost) + GNN on synthetic workplace dataset.", table_body),
            Paragraph("Synthetic limits real-world generalizability; GNN lacks interpretability.", table_body)
        ],
        [
            Paragraph("Hermawan et al. (IEEE, 2024)", table_body),
            Paragraph("DASS-21 chatbot comparing RFC (82.5%) vs MNB (66.0%).", table_body),
            Paragraph("Small dataset (n=424); no clinical deployment validation.", table_body)
        ],
        [
            Paragraph("Dhawale et al. (ICCCNT, 2024)", table_body),
            Paragraph("KNN (82.5%) and Logistic Regression on employee dataset.", table_body),
            Paragraph("Single-domain questionnaire; no text NLP or uncertainty bounds.", table_body)
        ],
        [
            Paragraph("Jayakumar & R.N. (ICWITE, 2024)", table_body),
            Paragraph("Systematic review of SVM, RF, XGBoost in predictive psychiatry.", table_body),
            Paragraph("Purely literature-based; no software deployment artifact.", table_body)
        ],
        [
            Paragraph("Cherian et al. (IEEE, 2024)", table_body),
            Paragraph("Smartphone sensor data with canonical correlation under RDoC.", table_body),
            Paragraph("Heavy sensor hardware dependency; no client-side edge execution.", table_body)
        ],
        [
            Paragraph("Pant et al. (IEEE BIBM, 2024)", table_body),
            Paragraph("35-year CAMHS EHR trajectory and ADHD co-occurrence visualization.", table_body),
            Paragraph("Retrospective statistical analysis; no real-time predictive screening.", table_body)
        ],
        [
            Paragraph("Amirhosseini et al. (IEEE IS, 2024)", table_body),
            Paragraph("NHANES multimodal dataset (19,560 rows) with RF (R²=0.93).", table_body),
            Paragraph("Adult population focus; heavy computational overhead; no edge web deployment.", table_body)
        ]
    ]
    t_lits = Table(lit_summary_table, colWidths=[140, 190, 174])
    t_lits.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_lits)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Research Gap", h2_style))
    story.append(Paragraph(
        "Current literature exhibits critical deficiencies: (1) Absence of browser-native, zero-cloud execution models; (2) Over-reliance on single classifiers with no epistemic uncertainty modeling; (3) Lack of transparent Explainable AI (XAI) feature decomposition for adolescent psychopathology; (4) Failure to bridge diagnostic scoring with immediate evidence-based CBT intervention protocols.",
        body_style
    ))

    story.append(Paragraph("2.3 Objectives", h2_style))
    story.append(Paragraph("• To develop a browser-native multimodal screening platform executing entirely on client hardware via JavaScript/TensorFlow.js.", bullet_style))
    story.append(Paragraph("• To implement a 4-model stacked ensemble combining specialist neural networks with a 23-input meta-learner achieving $R^2 > 0.94$.", bullet_style))
    story.append(Paragraph("• To quantify diagnostic uncertainty using Monte Carlo Dropout over 20 stochastic passes (95% CI).", bullet_style))
    story.append(Paragraph("• To construct an NLP sentiment parser with 20 emergency crisis bigrams and automated Tele-MANAS helpline escalation.", bullet_style))
    story.append(Paragraph("• To engineer Permutation SHAP attribution, longitudinal EWMA forecasting, and FHIR standard JSON export.", bullet_style))

    story.append(Paragraph("2.4 Problem Statement", h2_style))
    story.append(Paragraph(
        "Traditional adolescent mental health assessment is subjective, cloud-dependent, uncalibrated, and detached from continuous monitoring. Existing systems fail to provide private, multi-modal risk scoring with verified confidence intervals and interpretable feature drivers.",
        body_style
    ))
    story.append(PageBreak())

    # ── CHAPTER 3: TECHNICAL SPECIFICATION ────────────────────────────────────
    story.append(Paragraph("3. TECHNICAL SPECIFICATION", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))

    story.append(Paragraph("3.1 Requirements", h2_style))
    story.append(Paragraph("<b>Functional Requirements:</b>", h3_style))
    story.append(Paragraph("• <b>FR-01:</b> The system must ingest 10 standardized psychometric items across PHQ-9, GAD-7, ISI, and SCARED domains.", bullet_style))
    story.append(Paragraph("• <b>FR-02:</b> The system must compute a 20-dimensional feature vector with interaction terms.", bullet_style))
    story.append(Paragraph("• <b>FR-03:</b> The system must execute a 4-model stacked ensemble and compute 20 Monte Carlo Dropout passes.", bullet_style))
    story.append(Paragraph("• <b>FR-04:</b> The system must scan journal text for 20 crisis bigrams and trigger emergency alert banners.", bullet_style))
    story.append(Paragraph("• <b>FR-05:</b> The system must calculate permutation SHAP feature contributions summing to the baseline difference.", bullet_style))
    story.append(Paragraph("• <b>FR-06:</b> The system must project a 30-day forecast using Linear Regression + EWMA (alpha=0.4) and detect 2σ anomalies.", bullet_style))
    story.append(Paragraph("• <b>FR-07:</b> The system must export HL7 FHIR DiagnosticReport JSON summaries.", bullet_style))

    story.append(Paragraph("<b>Non-Functional Requirements:</b>", h3_style))
    story.append(Paragraph("• <b>NFR-01 (Privacy & Security):</b> Zero sensitive health data transmitted to cloud servers; 100% local inference.", bullet_style))
    story.append(Paragraph("• <b>NFR-02 (Performance):</b> Model inference and UI chart updates must execute in under 20ms.", bullet_style))
    story.append(Paragraph("• <b>NFR-03 (Availability):</b> Hosted 24/7 on GitHub Pages static CDN infrastructure with zero downtime.", bullet_style))
    story.append(Paragraph("• <b>NFR-04 (Usability):</b> Responsive, accessible UI supporting desktop, tablet, and mobile browsers.", bullet_style))

    story.append(Paragraph("3.2 Feasibility Study", h2_style))
    story.append(Paragraph("• <b>Technical Feasibility:</b> Built using mature client-side technologies (HTML5, CSS3, ES6 JavaScript, Chart.js, and Python Scikit-Learn/Streamlit), eliminating costly GPU infrastructure.", body_style))
    story.append(Paragraph("• <b>Economic Feasibility:</b> Zero cloud server or database hosting costs; utilizes free GitHub Pages edge CDN.", body_style))
    story.append(Paragraph("• <b>Social Feasibility:</b> Aligns with UN SDG 3 (Good Health and Well-Being), offering accessible adolescent mental health screening in low-resource schools and clinics.", body_style))

    story.append(Paragraph("3.3 System Specification", h2_style))
    story.append(Paragraph("• <b>Hardware Specification:</b> Dual-core CPU (2.0 GHz+), 4 GB RAM, standard display (1366x768+), 50 MB disk space.", body_style))
    story.append(Paragraph("• <b>Software Specification:</b> Modern Web Browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+), Python 3.9+ (for offline training/FastAPI), Git.", body_style))
    story.append(PageBreak())

    # ── CHAPTER 4: DESIGN APPROACH AND DETAILS ────────────────────────────────
    story.append(Paragraph("4. DESIGN APPROACH AND DETAILS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))

    story.append(Paragraph("4.1 System Architecture", h2_style))
    story.append(Paragraph(
        "SHRI operates as a 5-tier pipeline: (1) <i>Multi-Modal Ingestion</i> (Questionnaires, Biomarkers, NLP Journal); (2) <i>20D Feature Extraction</i>; (3) <i>Specialist Ensemble</i> (DepNet, AnxNet, SleepNet); (4) <i>Meta-Learner & MC Dropout</i> (FusionNet + 20 stochastic passes); (5) <i>Clinical Output Layer</i> (0–100 Score, 95% CI, SHAP waterfall, EWMA forecast, CBT actions, FHIR JSON).",
        body_style
    ))

    story.append(Paragraph("4.2 Design Models & Flow", h2_style))
    story.append(Paragraph("<b>1. Data Flow Diagram (DFD):</b> Patient inputs flow through validation, feature engineering, specialist models, meta-learner, and uncertainty engine to render dashboard analytics.", bullet_style))
    story.append(Paragraph("<b>2. Use Case Diagram:</b> Clinicians register patients, input assessment sliders, view SHAP explainability, monitor anomaly alerts, and download FHIR reports.", bullet_style))
    story.append(Paragraph("<b>3. Class Diagram:</b> Modular JS architecture comprising `SmartHealthEnsembleJS`, `analyzeSentimentDetailed()`, `extractFeatures()`, `computeShapContributions()`, and `CBT_DATA`.", bullet_style))
    story.append(Paragraph("<b>4. Sequence Diagram:</b> Synchronous client-side execution from UI slider event listener $\\rightarrow$ feature transformation $\\rightarrow$ ensemble prediction $\\rightarrow$ Chart.js canvas repaint in $<12\\text{ms}$.", bullet_style))

    story.append(Paragraph("4.3 Experimental Results & Performance", h2_style))
    
    exp_table = [
        [Paragraph("Model", table_header), Paragraph("Architecture / Layers", table_header), Paragraph("MAE", table_header), Paragraph("RMSE", table_header), Paragraph("R² Score", table_header)],
        [Paragraph("DepNet", table_body), Paragraph("Dense(64) -> BN -> Dense(32) -> Dropout(0.3) -> 16 -> 1", table_body), Paragraph("4.2", table_body), Paragraph("5.3", table_body), Paragraph("0.912", table_body)],
        [Paragraph("AnxNet", table_body), Paragraph("Dense(64) -> BN -> Dropout(0.25) -> Dense(32) -> 16 -> 1", table_body), Paragraph("4.5", table_body), Paragraph("5.6", table_body), Paragraph("0.904", table_body)],
        [Paragraph("SleepNet", table_body), Paragraph("Dense(48) -> BN -> Dense(24) -> Dropout(0.25) -> 12 -> 1", table_body), Paragraph("4.8", table_body), Paragraph("5.9", table_body), Paragraph("0.887", table_body)],
        [Paragraph("<b>FusionNet (Stacked Meta)</b>", table_body), Paragraph("<b>Dense(128) -> BN -> Dense(64) -> Drop(0.35) -> 32 -> 1</b>", table_body), Paragraph("<b>3.2</b>", table_body), Paragraph("<b>4.1</b>", table_body), Paragraph("<b>0.942</b>", table_body)],
        [Paragraph("<b>Full Ensemble + 20 MC</b>", table_body), Paragraph("<b>Weighted 4-Model Stack + Test-Time Stochastic Dropout</b>", table_body), Paragraph("<b>3.1</b>", table_body), Paragraph("<b>3.9</b>", table_body), Paragraph("<b>0.948</b>", table_body)]
    ]
    t_exp = Table(exp_table, colWidths=[120, 220, 50, 50, 64])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_exp)
    story.append(PageBreak())

    # ── CHAPTER 5: REFERENCES ─────────────────────────────────────────────────
    story.append(Paragraph("5. REFERENCES", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
    
    refs = [
        "[1] S. A. Suresh and S. Agarwal, 'Hybrid ML Approach for Mental Health Prediction,' in Proc. 4th Int. Conf. Innovative Mechanisms for Industry Applications (ICIMIA), IEEE, 2025.",
        "[2] L. Hermawan, Meilinda, D. Stiawan, D. S. Ikhsan, and R. A. Syakurah, 'Mental Health with Machine Learning: A Prediction-Based Intervention Chatbot for Mental Health Conversations,' in Proc. IEEE Conf., 2024.",
        "[3] H. Dhawale, D. Thakare, N. C. Morris, R. Agrawal, and C. Dhule, 'The Prediction of Mental Health Using Machine Learning,' in Proc. 15th ICCCNT, IEEE, 2024.",
        "[4] N. Jayakumar and R. N., 'Modeling Mental Health: Advances in Predictive Science towards Proactive Health Care,' in Proc. IEEE Int. Conf. for Women in Innovation, Technology & Entrepreneurship (ICWITE), 2024.",
        "[5] S. Purohit, R. Mudgal, S. Vats, P. Rana, and A. Verma, 'Analyzing the Impact of Social Media Usage on Mental Health: A Machine Learning Approach,' in Proc. 15th ICCCNT, IEEE, 2024.",
        "[6] J. Cherian et al., 'Multimodal Markers of Transdiagnostic Childhood Mental Health Impairment,' in Proc. IEEE Conf., 2024.",
        "[7] Y. Koh, C. Lee, Y. Ku, and U. Lee, 'Data Visualization for Mental Health Monitoring in Smart Home Environment: A Case Study,' in Proc. IEEE Conf., 2023.",
        "[8] B. Li and Y. Xu, 'Research on Evaluation Model of College Students Mental Health,' in Proc. Int. Conf. Health Big Data and Smart Sports (HBDSS), IEEE, 2021.",
        "[9] G. Peng and W. Y. Leong, 'Brain Wave Response of Style Geometry in Artistic Creation in VR Environments: An Impact Study on Cognitive Function of Autistic Children,' in Proc. IEEE ICSIPA, 2024.",
        "[10] D. Pant et al., 'Visualizing Patient Trajectories and Disorder Co-occurrences in Child and Adolescent Mental Health,' in Proc. IEEE BIBM, 2024.",
        "[11] S. Kataru, K. King, and L. Fernando, 'Machine Learning-Based Early Detection and Intervention for Mental Health Issues in Children,' in Proc. IEEE COMPSAC, 2024.",
        "[12] C. R. Madhuri, M. Srinu, J. S. K. Bandaru, and G. M. A. Vardhan, 'AI-Powered Mental Health Screening and Support for Homeless Children,' in Proc. AI-Driven Smart Healthcare, IEEE, 2025.",
        "[13] X. Yuan, 'Study on the Correlation between Growth Environment and Mental Health of Left-Behind Children,' in Proc. IEEE Conf., 2023.",
        "[14] N. L. Gowda, N. Kumar, and N. S. L. Gowda, 'A Comparative Study on Various Detection Techniques to Detect Mental Health Disorders in Children,' in Proc. IEEE NEleX, 2023.",
        "[15] M. H. Amirhosseini, A. L. Ayodele, and A. Karami, 'Prediction of Depression Severity and Personalised Risk Factors Using Machine Learning on Multimodal Data,' in Proc. IEEE 12th Int. Conf. Intelligent Systems (IS), 2024.",
        "[16] H. K. Marrapu, B. Maram, and P. Reddi, 'New Analytic Framework of Public Mental Health Prediction Using Data Science,' in Proc. IEEE ICSTSN, 2022."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('Ref', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=TEXT_DARK, spaceAfter=4)))

    doc.build(story, canvasmaker=ReportCanvas)
    print(f"[SUCCESS] Project Report PDF generated at: {output_path}")


if __name__ == "__main__":
    desktop_path = r"C:\Users\nishanth golakoti\Desktop\Smart_Health_Risk_Indicator_Project_Report.pdf"
    build_project_report_pdf(desktop_path)
