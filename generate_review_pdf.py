"""
Generate a professional, polished PDF for the 75% Review & Remaining 25% Roadmap
Smart Health Risk Indicator (SHRI)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Smart Health Risk Indicator (SHRI) — 75% Review & 25% Roadmap")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL — College Major Project Review & Defense")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def create_pdf(output_filename="Smart_Health_Risk_Indicator_Review_Document.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#0F172A")    # Deep Slate
    ACCENT = colors.HexColor("#0284C7")     # Medical Cyan/Blue
    ACCENT_LIGHT = colors.HexColor("#F0F9FF")
    SECONDARY = colors.HexColor("#334155")
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#64748B")
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    ALERT_BG = colors.HexColor("#FEF2F2")
    ALERT_BORDER = colors.HexColor("#EF4444")
    SUCCESS_BG = colors.HexColor("#F0FDF4")
    SUCCESS_BORDER = colors.HexColor("#10B981")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'SectionH3',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'DocBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'DocBullet',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    quote_style = ParagraphStyle(
        'DocQuote',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0369A1"),
        leftIndent=14,
        rightIndent=14,
        spaceBefore=4,
        spaceAfter=6
    )
    table_text = ParagraphStyle(
        'TableText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=TEXT_DARK
    )
    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # ── HEADER & COVER BANNER ──────────────────────────────────────────────────
    story.append(Paragraph("SMART HEALTH RISK INDICATOR (SHRI)", title_style))
    story.append(Paragraph("AI-Powered Multi-Domain Clinical Decision Support System | Major Project Review Document", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=2, spaceAfter=12))

    # Executive Metadata Box
    meta_data = [
        [
            Paragraph("<b>Project Phase:</b> 75% Review Completed & 25% Final Defense Roadmap", table_text),
            Paragraph("<b>Team Size:</b> 3 Engineering Members", table_text)
        ],
        [
            Paragraph("<b>Core Stack:</b> Python, Streamlit, Scikit-Learn, Plotly, NLP", table_text),
            Paragraph("<b>Local Web Portal:</b> http://localhost:8501", table_text)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[250, 254])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BAE6FD")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ── SECTION 1: 75% REVIEW MILESTONE & 3-MEMBER DIVISION ───────────────────
    story.append(Paragraph("1. 75% Review Milestone: 3-Member Team Contribution Breakdown", h1_style))
    story.append(Paragraph(
        "For the 75% project review, the engineering workload was split into three modular, non-overlapping domains ensuring each team member has substantial technical ownership.",
        body_style
    ))

    # Table of Team Distribution
    team_table_data = [
        [Paragraph("Team Member", table_header), Paragraph("Role & Core Deliverable", table_header), Paragraph("Key Technical Modules", table_header)],
        [
            Paragraph("<b>👤 Member 1</b>", table_text),
            Paragraph("<b>ML & Ensemble Lead</b><br/>Core Machine Learning & Uncertainty Engine", table_text),
            Paragraph("• 6,000 Hybrid Clinical Dataset Generator<br/>• 20D Multimodal Feature Matrix<br/>• DepNet, AnxNet, SleepNet (Specialists)<br/>• FusionNet Meta-Learner (23 Inputs)<br/>• Monte Carlo Dropout (95% CI, 20 passes)", table_text)
        ],
        [
            Paragraph("<b>👤 Member 2</b>", table_text),
            Paragraph("<b>NLP & XAI Lead</b><br/>Clinical NLP, Crisis Alerting & Explainability", table_text),
            Paragraph("• Real-Time Clinical NLP Sentiment Engine<br/>• 90-Word Clinical Lexicon & Bigrams<br/>• Negation & Intensifier Multipliers<br/>• Permutation SHAP Feature Attribution<br/>• Immediate Crisis UI Escalation Modal", table_text)
        ],
        [
            Paragraph("<b>👤 Member 3</b>", table_text),
            Paragraph("<b>Full-Stack Lead</b><br/>Web Platform, Forecasting & Interoperability", table_text),
            Paragraph("• Interactive Streamlit Web Application<br/>• Longitudinal Trajectory (LR + EWMA)<br/>• Statistical Anomaly Detector (2σ)<br/>• Evidence-Graded CBT Planner<br/>• JSON / FHIR Diagnostic Export", table_text)
        ]
    ]
    t_team = Table(team_table_data, colWidths=[80, 180, 244])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 14))

    # ── INDIVIDUAL SPEECH SCRIPTS ─────────────────────────────────────────────
    story.append(Paragraph("2. Individual Viva Speech Scripts for 75% Review", h1_style))
    
    # Member 1 Script Box
    m1_content = [
        Paragraph("<b>👤 Member 1 (ML & Ensemble Architecture Lead):</b>", h3_style),
        Paragraph(
            "<i>\"Respected Examiners, my primary contribution is the core Machine Learning Pipeline, 20-dimensional Feature Engineering, and the 4-Model Stacked Ensemble with Uncertainty Quantification. Rather than a single monolithic classifier, I designed 3 specialized sub-networks: DepNet (PHQ-9), AnxNet (GAD-7), and SleepNet (ISI/lifestyle), fused by FusionNet—a 23-input meta-learner. To eliminate overconfidence, I implemented Monte Carlo Dropout with 20 stochastic test-time passes, yielding a verified 95% Confidence Interval.\"</i>",
            quote_style
        )
    ]
    t_m1 = Table([[m1_content]], colWidths=[504])
    t_m1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_m1)
    story.append(Spacer(1, 8))

    # Member 2 Script Box
    m2_content = [
        Paragraph("<b>👤 Member 2 (Clinical NLP & Explainable AI Lead):</b>", h3_style),
        Paragraph(
            "<i>\"Respected Examiners, I developed the Real-Time Clinical NLP Sentiment Engine, Crisis Keyword Escalation, and Explainable AI (XAI) using SHAP. Adolescent self-reports contain unstructured emotional signals; I built a sentiment parser with a 90-word clinical dictionary, negation handling, and 20 high-risk bigrams that immediately trigger crisis hotlines like Tele-MANAS. Furthermore, I built a permutation SHAP module that explains to doctors exactly which features drove the score up or down relative to baseline.\"</i>",
            quote_style
        )
    ]
    t_m2 = Table([[m2_content]], colWidths=[504])
    t_m2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_m2)
    story.append(Spacer(1, 8))

    # Member 3 Script Box
    m3_content = [
        Paragraph("<b>👤 Member 3 (Full-Stack Platform, Forecasting & CBT Lead):</b>", h3_style),
        Paragraph(
            "<i>\"Respected Examiners, I engineered the interactive Web Application, Longitudinal Forecasting, Anomaly Detection, and CBT Interventions. I built the Streamlit clinician portal with real-time Plotly charts and gauge indicators. To track recovery, I created a 30-day trajectory forecast combining Linear Regression with Exponentially Weighted Moving Average (EWMA, alpha=0.4) to flag statistical spikes (|z| >= 2σ), and added automated CBT recommendations with FHIR/JSON export.\"</i>",
            quote_style
        )
    ]
    t_m3 = Table([[m3_content]], colWidths=[504])
    t_m3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_m3)
    story.append(Spacer(1, 14))

    # ── LIVE DEMONSTRATION CHECKLIST ──────────────────────────────────────────
    story.append(Paragraph("3. Five-Step Live Demonstration Protocol for Review", h1_style))
    demo_steps = [
        ("Step 1: Patient Assessment", "Load 'Pooja Patel (High Risk)' preset in the web portal. Show the composite score (74/100, Tier 4) and the 95% Confidence Interval badge."),
        ("Step 2: 4-Model & MC Dropout", "Open Ensemble tab. Show the Plotly Gauge Chart and the 20-pass Monte Carlo density histogram with shaded 95% CI region."),
        ("Step 3: SHAP Explainability", "Open SHAP tab. Show the horizontal waterfall chart decomposing score into positive risk factors (+18.2) vs mitigating habits (-6.1)."),
        ("Step 4: Longitudinal & Anomaly", "Open Trajectory tab. Show the 30-day projected forecast line and the 2σ statistical anomaly alert box."),
        ("Step 5: Crisis NLP Escalation", "Type 'I can't cope anymore and want to end it all' in journal text. Show the instant red crisis escalation alert with emergency helplines.")
    ]
    for s_title, s_desc in demo_steps:
        story.append(Paragraph(f"<b>• {s_title}:</b> {s_desc}", bullet_style))
    story.append(Spacer(1, 14))

    # Page Break for Clean Roadmap Section
    story.append(PageBreak())

    # ── SECTION 4: THE REMAINING 25% ROADMAP ──────────────────────────────────
    story.append(Paragraph("4. The Remaining 25% Roadmap: Taking Project to 100%", h1_style))
    story.append(Paragraph(
        "To achieve 100% final defense readiness, the remaining 25% is partitioned into four concrete engineering deliverables with clear technical specifications:",
        body_style
    ))

    roadmap_table_data = [
        [Paragraph("Module", table_header), Paragraph("Scope & Weight", table_header), Paragraph("Technical Deliverable & Method", table_header)],
        [
            Paragraph("<b>1. Clinical Validation</b>", table_text),
            Paragraph("<b>10% Weight</b><br/>Real-world benchmarking", table_text),
            Paragraph("• Generate multi-class ROC-AUC curves for all 5 tiers.<br/>• Compute Sensitivity (Target >92%) & Specificity (>88%).<br/>• 10-Fold Stratified Cross-Validation across age cohorts.<br/>• Brier Score & Platt Calibration curve calculation.", table_text)
        ],
        [
            Paragraph("<b>2. Audio Biomarkers</b>", table_text),
            Paragraph("<b>5% Weight</b><br/>Acoustic speech prosody", table_text),
            Paragraph("• Audio check-in ingestion widget via Python librosa.<br/>• Pitch jitter, shimmer & vocal micro-tremor extraction.<br/>• Speech cadence, pause latency & 13 MFCC coefficients.<br/>• Fuse audio score as 5th input branch into FusionNet.", table_text)
        ],
        [
            Paragraph("<b>3. Production API</b>", table_text),
            Paragraph("<b>5% Weight</b><br/>FastAPI & Docker", table_text),
            Paragraph("• Asynchronous FastAPI REST microservice (/predict, /shap).<br/>• Dockerfile & docker-compose containerization.<br/>• Interactive OpenAPI / Swagger documentation (/docs).<br/>• HL7 FHIR DiagnosticReport JSON interchange.", table_text)
        ],
        [
            Paragraph("<b>4. Regional Localization</b>", table_text),
            Paragraph("<b>5% Weight</b><br/>Multi-language & Offline", table_text),
            Paragraph("• Translate questionnaires into Hindi, Telugu, and Tamil.<br/>• Multi-lingual sentiment lexicon & transliteration.<br/>• Offline Progressive Web App (PWA) sync for rural PHCs.", table_text)
        ]
    ]
    t_road = Table(roadmap_table_data, colWidths=[110, 110, 284])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 14))

    # ── EXAMINER DEFENSE SCRIPT ───────────────────────────────────────────────
    story.append(Paragraph("5. Examiner Defense Script for the Pending 25%", h1_style))
    defense_box = [
        Paragraph("<b>Question from Examiner:</b> <i>\"Your 75% is working. What is pending in the remaining 25% and how will you finish it?\"</i>", h3_style),
        Paragraph(
            "<b>Team Answer:</b> <i>\"Respected Examiners, our 75% milestone proves the mathematical validity, ensemble architecture, explainability, and interactive UI of our system. For the final 25%, our work is divided into 4 clear engineering milestones: (1) Generating full ROC-AUC curves and sensitivity/specificity matrices across all 5 risk tiers; (2) Integrating acoustic prosody extraction using librosa for complete tri-modal scoring; (3) Containerizing the backend into FastAPI microservices with Docker for hospital EHR integration; and (4) Expanding the questionnaire and crisis lexicon into Hindi and Telugu for rural health accessibility. All 3 members have their modules assigned and we are on track for 100% completion for final defense.\"</i>",
            quote_style
        )
    ]
    t_def = Table([[defense_box]], colWidths=[504])
    t_def.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SUCCESS_BG),
        ('BOX', (0, 0), (-1, -1), 1, SUCCESS_BORDER),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_def)
    story.append(Spacer(1, 14))

    # ── SECTION 5: TOP 5 VIVA QUESTIONS & ANSWERS ─────────────────────────────
    story.append(Paragraph("6. Top 5 Viva Questions & Fast Technical Answers", h1_style))
    viva_qa = [
        ("Q1: Why is this system named 'Smart Health Risk Indicator'?",
         "It dynamically synthesizes psychometric assessments, physiological sleep habits, lifestyle screen/exercise data, and natural language journal entries into an adaptive 0–100 risk score with built-in uncertainty bounds."),
        ("Q2: Why use Monte Carlo Dropout instead of standard predictions?",
         "Standard neural networks give overconfident point estimates. MC Dropout keeps dropout active at test-time over 20 passes to sample model epistemic uncertainty, yielding a clinical 95% Confidence Interval."),
        ("Q3: How does Stacked Generalization differ from simple ensemble averaging?",
         "Simple averaging assigns static weights. FusionNet is a meta-learner trained on 23 inputs (20 base features + 3 specialist outputs) that dynamically learns non-linear cross-model weighting based on patient context."),
        ("Q4: How does your NLP engine handle linguistic negation?",
         "The NLP parser inspects preceding tokens for negators ('not', 'never', 'can't'). If a positive word like 'happy' is preceded by 'not', it inverts polarity to elevate distress appropriately."),
        ("Q5: How does the system protect patient data privacy?",
         "All neural network scoring runs locally within the client environment. Raw patient reflections and questionnaire responses do not leave the device for inference.")
    ]
    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h3_style))
        story.append(Paragraph(f"<b>Ans:</b> {a}", body_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF successfully generated at: {os.path.abspath(output_filename)}")


if __name__ == "__main__":
    create_pdf()
