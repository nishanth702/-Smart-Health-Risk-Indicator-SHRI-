"""
Generate high-resolution UML and System Diagrams for Smart Health Risk Indicator (SHRI)
1. Data Flow Diagram (DFD Level 0 & Level 1) -> Fig. 3
2. Use Case Diagram -> Fig. 4
3. Class Diagram -> Fig. 5
4. Sequence Diagram -> Fig. 6
5. System Architecture Diagram -> Fig. 2
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, BoxStyle, ArrowStyle, FancyArrowPatch, Circle

DIAGRAMS_DIR = r"c:\Users\nishanth golakoti\Downloads\ADMRI-main\report_diagrams"
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. DATA FLOW DIAGRAM (DFD LEVEL 1) - FIG. 3
# -----------------------------------------------------------------------------
def generate_dfd():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 900)
    ax.axis('off')
    
    # Title
    ax.text(700, 865, "DATA FLOW DIAGRAM (DFD LEVEL 1) - SMART HEALTH RISK INDICATOR (SHRI)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1E3A8A', fontfamily='sans-serif')
    
    # Palette
    ENTITY_BG = '#EFF6FF'
    ENTITY_BORDER = '#2563EB'
    PROC_BG = '#F0FDF4'
    PROC_BORDER = '#059669'
    STORE_BG = '#FFFBEB'
    STORE_BORDER = '#D97706'
    ARROW_COLOR = '#334155'

    def draw_entity(x, y, w, h, text):
        box = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", ec=ENTITY_BORDER, fc=ENTITY_BG, lw=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#1E3A8A', multialignment='center')

    def draw_process(x, y, w, h, num, text):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=16", ec=PROC_BORDER, fc=PROC_BG, lw=2)
        ax.add_patch(box)
        ax.plot([x, x+w], [y+h-24, y+h-24], color=PROC_BORDER, lw=1)
        ax.text(x + w/2, y + h - 12, f"Process {num}", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#065F46')
        ax.text(x + w/2, y + (h-24)/2, text, fontsize=9, fontweight='bold', ha='center', va='center', color='#1F2937', multialignment='center')

    def draw_store(x, y, w, h, num, text):
        # Open ended rectangle (data store)
        ax.plot([x, x+w], [y+h, y+h], color=STORE_BORDER, lw=2)
        ax.plot([x, x+w], [y, y], color=STORE_BORDER, lw=2)
        ax.plot([x, x], [y, y+h], color=STORE_BORDER, lw=2)
        ax.plot([x+45, x+45], [y, y+h], color=STORE_BORDER, lw=1)
        # Background fill
        rect = patches.Rectangle((x, y), w, h, fc=STORE_BG, ec='none', zorder=1)
        ax.add_patch(rect)
        ax.text(x + 22.5, y + h/2, num, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#92400E', zorder=2)
        ax.text(x + 45 + (w-45)/2, y + h/2, text, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1F2937', zorder=2, multialignment='center')

    def draw_flow(x1, y1, x2, y2, label, label_pos=(0.5, 0.5), rad=0.0):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                connectionstyle=f"arc3,rad={rad}",
                                arrowstyle="->,head_length=6,head_width=4",
                                lw=1.5, color=ARROW_COLOR)
        ax.add_patch(arrow)
        lx = x1 + (x2 - x1) * label_pos[0]
        ly = y1 + (y2 - y1) * label_pos[1]
        ax.text(lx, ly, label, fontsize=7.5, ha='center', va='center', color='#0F172A',
                bbox=dict(boxstyle="round,pad=0.2", fc='#FFFFFF', ec='#CBD5E1', lw=0.8, alpha=0.9))

    # Entities
    draw_entity(40, 680, 160, 90, "Adolescent Patient\n(User / Screened)")
    draw_entity(40, 180, 160, 90, "Attending Clinician\n/ Psychologist")
    draw_entity(1180, 440, 180, 90, "Emergency Crisis Care\n& Health Registry")

    # Processes
    draw_process(280, 680, 210, 90, "1.0", "Intake & Psychometric\nData Capture (PHQ/GAD)")
    draw_process(280, 440, 210, 90, "2.0", "NLP Sentiment &\nCrisis Keyword Scanner")
    draw_process(580, 560, 220, 90, "3.0", "Multimodal Feature\nPipeline & Encoding (23D)")
    draw_process(880, 560, 230, 90, "4.0", "4-Model Stacked Ensemble\n(DepNet, AnxNet, SleepNet)")
    draw_process(880, 320, 230, 90, "5.0", "Uncertainty (MC Dropout)\n& SHAP Explainability")
    draw_process(580, 180, 220, 90, "6.0", "Clinical Dashboard &\nCBT Triage Generator")

    # Data Stores
    draw_store(580, 740, 220, 50, "D1", "Local Secure Patient Cache\n(IndexedDB / No-Cloud)")
    draw_store(580, 430, 220, 50, "D2", "Psychiatric Norms &\nSeverity Cutoffs")
    draw_store(880, 180, 230, 50, "D3", "Evidence-Based CBT\nIntervention Library")

    # Flows
    draw_flow(200, 725, 280, 725, "PHQ-9, GAD-7, PSQI, Bio Data", (0.5, 0.5))
    draw_flow(120, 680, 280, 485, "Free-Text Journal Entries", (0.45, 0.3), rad=-0.1)
    
    draw_flow(490, 725, 580, 625, "Normalized Psychometrics", (0.5, 0.5))
    draw_flow(490, 485, 580, 585, "Sentiment Polarity & Lexical Features", (0.5, 0.5))
    
    # Store D1 connections
    draw_flow(690, 650, 690, 740, "Write Session Vector", (0.5, 0.5))
    draw_flow(720, 740, 720, 650, "Read Baseline", (0.5, 0.5))

    # Flow 3 -> 4
    draw_flow(800, 605, 880, 605, "23D Engineered Feature Vector", (0.5, 0.5))
    
    # Flow 4 -> 5
    draw_flow(995, 560, 995, 410, "Raw Predictions & Embeddings", (0.5, 0.5))
    
    # Flow 2 -> Crisis Entity
    draw_flow(490, 460, 1180, 470, "CRISIS KEYWORD ALERT (Immediate Tripwire)", (0.6, 0.6), rad=0.15)

    # Flow 5 -> 6
    draw_flow(880, 365, 800, 245, "95% CI Bounds & SHAP Attributions", (0.5, 0.5))
    
    # Flow D3 -> 6
    draw_flow(880, 205, 800, 205, "Matching CBT Protocols", (0.5, 0.5))

    # Flow 6 -> Clinician & Patient
    draw_flow(580, 225, 200, 225, "Risk Score, Radar Chart, SHAP Waterfall, CBT Plan", (0.5, 0.5))
    draw_flow(580, 200, 120, 680, "Personalized Coping Exercises & Confidence Bounds", (0.4, 0.6), rad=-0.35)
    
    # Flow 6 -> FHIR
    draw_flow(800, 225, 1180, 460, "FHIR-Compliant Patient Record JSON", (0.6, 0.4), rad=-0.1)

    out_path = os.path.join(DIAGRAMS_DIR, "dfd_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved DFD:", out_path)
    return out_path

# -----------------------------------------------------------------------------
# 2. USE CASE DIAGRAM - FIG. 4
# -----------------------------------------------------------------------------
def generate_use_case():
    fig, ax = plt.subplots(figsize=(14, 9.5), dpi=300)
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Title
    ax.text(700, 915, "USE CASE DIAGRAM - SMART HEALTH RISK INDICATOR (SHRI)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1E3A8A', fontfamily='sans-serif')

    # System Boundary Box
    sys_box = FancyBboxPatch((300, 40), 800, 830, boxstyle="round,pad=0,rounding_size=12", ec='#3B82F6', fc='#F8FAFC', lw=2.5, ls='--')
    ax.add_patch(sys_box)
    ax.text(700, 845, "Smart Health Risk Indicator (SHRI) - Browser-Native Boundary", 
            fontsize=12, fontweight='bold', ha='center', va='center', color='#1E3A8A')

    # Actor Drawing function
    def draw_actor(x, y, name, role):
        # Head
        circle = Circle((x, y + 45), 18, fc='#EFF6FF', ec='#1E3A8A', lw=2)
        ax.add_patch(circle)
        # Body
        ax.plot([x, x], [y + 27, y - 15], color='#1E3A8A', lw=2)
        # Arms
        ax.plot([x - 28, x + 28], [y + 12, y + 12], color='#1E3A8A', lw=2)
        # Legs
        ax.plot([x, x - 22], [y - 15, y - 55], color='#1E3A8A', lw=2)
        ax.plot([x, x + 22], [y - 15, y - 55], color='#1E3A8A', lw=2)
        # Label
        ax.text(x, y - 72, name, fontsize=10, fontweight='bold', ha='center', va='top', color='#1E3A8A')
        ax.text(x, y - 88, f"({role})", fontsize=8, ha='center', va='top', color='#4B5563')

    # Draw Actors
    draw_actor(140, 680, "Adolescent\nPatient", "Primary Actor")
    draw_actor(140, 240, "Attending\nClinician", "Primary Actor")
    draw_actor(1260, 680, "School\nCounselor", "Secondary")
    draw_actor(1260, 240, "Emergency\nCrisis Care", "System Service")

    # Use Cases (Ellipses)
    use_cases = [
        (1, 480, 780, "Complete Psychometric\nIntake (PHQ/GAD/PSQI)", '#EFF6FF', '#2563EB'),
        (2, 880, 780, "Submit Daily Free-Text\nJournal Narrative", '#EFF6FF', '#2563EB'),
        (3, 480, 660, "View Privacy-Preserving\nRisk Score & Severity", '#F0FDF4', '#059669'),
        (4, 880, 660, "Execute Real-Time NLP &\nCrisis Tripwire Scan", '#FEF2F2', '#DC2626'),
        (5, 480, 530, "Inspect 95% Confidence\nIntervals (MC Dropout)", '#FFFBEB', '#D97706'),
        (6, 880, 530, "Compute Permutation SHAP\nFeature Attributions", '#FAF5FF', '#7C3AED'),
        (7, 480, 400, "Access Personalized CBT\nIntervention Modules", '#F0FDF4', '#059669'),
        (8, 880, 400, "Track Longitudinal Trends\n& Anomaly Trajectories", '#EFF6FF', '#2563EB'),
        (9, 480, 270, "Clinician Authentication\n& Multi-Patient Registry", '#F8FAFC', '#475569'),
        (10, 880, 270, "Export Automated Clinical\nPDF & FHIR Records", '#EFF6FF', '#2563EB'),
        (11, 680, 130, "Trigger Acute Self-Harm\nEmergency Protocol", '#FEF2F2', '#DC2626'),
    ]

    uc_centers = {}
    for num, ux, uy, ulabel, ufc, uec in use_cases:
        ellipse = patches.Ellipse((ux, uy), 280, 70, fc=ufc, ec=uec, lw=1.8)
        ax.add_patch(ellipse)
        ax.text(ux, uy, f"UC{num}: {ulabel}", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1F2937', multialignment='center')
        uc_centers[num] = (ux, uy)

    # Actor Connections
    def connect_actor(ax_coord, uc_num, is_dashed=False):
        ux, uy = uc_centers[uc_num]
        ls = '--' if is_dashed else '-'
        ax.plot([ax_coord[0], ux], [ax_coord[1], uy], color='#64748B', lw=1.3, ls=ls)

    # Patient links
    connect_actor((180, 710), 1)
    connect_actor((180, 700), 2)
    connect_actor((180, 680), 3)
    connect_actor((180, 660), 7)

    # Clinician links
    connect_actor((180, 280), 3)
    connect_actor((180, 260), 5)
    connect_actor((180, 240), 6)
    connect_actor((180, 220), 8)
    connect_actor((180, 200), 9)
    connect_actor((180, 180), 10)

    # Counselor links
    connect_actor((1220, 680), 7)
    connect_actor((1220, 660), 8)
    connect_actor((1220, 640), 10)

    # Emergency Care links
    connect_actor((1220, 240), 11)

    # <<include>> and <<extend>> relationships between use cases
    def draw_relationship(uc_src, uc_dst, rel_type):
        x1, y1 = uc_centers[uc_src]
        x2, y2 = uc_centers[uc_dst]
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle="->,head_length=5,head_width=3",
                                lw=1.2, ls='--', color='#DC2626' if 'extend' in rel_type else '#2563EB')
        ax.add_patch(arrow)
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ax.text(mx, my, f"<<{rel_type}>>", fontsize=7.5, fontweight='bold', ha='center', va='center', 
                color='#DC2626' if 'extend' in rel_type else '#2563EB',
                bbox=dict(boxstyle="round,pad=0.15", fc='#FFFFFF', ec='#CBD5E1', lw=0.5))

    draw_relationship(2, 4, "include")
    draw_relationship(4, 11, "extend")
    draw_relationship(1, 3, "include")
    draw_relationship(3, 5, "include")
    draw_relationship(3, 6, "include")

    out_path = os.path.join(DIAGRAMS_DIR, "use_case_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Use Case:", out_path)
    return out_path

# -----------------------------------------------------------------------------
# 3. CLASS DIAGRAM - FIG. 5
# -----------------------------------------------------------------------------
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 1000)
    ax.axis('off')

    # Title
    ax.text(750, 965, "UML CLASS DIAGRAM - SMART HEALTH RISK INDICATOR (SHRI)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1E3A8A', fontfamily='sans-serif')

    def draw_class(x, y, w, h, name, attrs, methods, color_hdr='#1E3A8A'):
        # Outer box
        box = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", ec='#64748B', fc='#FFFFFF', lw=1.5)
        ax.add_patch(box)
        # Header box
        hdr = FancyBboxPatch((x, y + h - 30), w, 30, boxstyle="square,pad=0", ec='#64748B', fc=color_hdr, lw=1.5)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 15, name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#FFFFFF')
        
        # Attrs section
        attr_h = (len(attrs) + 1) * 14
        ax.plot([x, x + w], [y + h - 30 - attr_h, y + h - 30 - attr_h], color='#94A3B8', lw=1)
        cur_y = y + h - 45
        for a in attrs:
            ax.text(x + 10, cur_y, a, fontsize=8, ha='left', va='center', color='#1E293B', fontfamily='monospace')
            cur_y -= 14
            
        # Methods section
        cur_y = y + h - 35 - attr_h - 10
        for m in methods:
            ax.text(x + 10, cur_y, m, fontsize=8, ha='left', va='center', color='#0F172A', fontfamily='monospace')
            cur_y -= 14

    # Classes definitions
    draw_class(40, 680, 270, 230, "PatientProfile", 
               ["- patientId: String", "- age: int", "- gender: String", "- registrationDate: Date", "- history: List<AssessmentRecord>"],
               ["+ createAssessment(): AssessmentRecord", "+ getTrajectory(): List<float>", "+ exportFHIR(): JSON", "+ flagAnomaly(score: float): bool"])

    draw_class(360, 680, 310, 230, "AssessmentInput", 
               ["- phq9Scores: int[9]", "- gad7Scores: int[7]", "- psqiScores: int[7]", "- journalText: String", "- sleepHours: float", "- screenTime: float"],
               ["+ validateInput(): bool", "+ computeClinicalTotals(): Map", "+ sanitizeJournalText(): String", "+ getRawVector(): float[23]"])

    draw_class(720, 680, 340, 230, "FeatureEngineer", 
               ["- zMean: float[23]", "- zStd: float[23]", "- engineeredVector: float[23]"],
               ["+ normalizeZScore(raw: float[23]): float[23]", "+ extractLexicalSentiment(): float[3]", "+ assembleTensor(): Tensor", "+ getFeatureNames(): String[23]"],
               color_hdr='#065F46')

    draw_class(1110, 680, 340, 230, "NLPSentimentEngine", 
               ["- vaderLexicon: Map<String, float>", "- crisisKeywords: List<String>", "- sentimentPolarity: float"],
               ["+ analyzeSentiment(text: String): float", "+ detectCrisisKeywords(text): List<String>", "+ extractNegationModifiers(): float"],
               color_hdr='#991B1B')

    draw_class(40, 370, 310, 230, "StackedEnsembleCore", 
               ["- depNet: BiLSTMSpecialist", "- anxNet: Conv1DSpecialist", "- sleepNet: TemporalCNNSpecialist", "- fusionNet: MetaLearner"],
               ["+ predictSubRisks(feat: float[23]): float[3]", "+ predictComposite(feat): float", "+ getLayerEmbeddings(): Tensor", "+ forwardPass(dropout: bool): float"],
               color_hdr='#5B21B6')

    draw_class(400, 370, 320, 230, "UncertaintyEngine", 
               ["- mcPasses: int = 20", "- dropoutRate: float = 0.2", "- confidenceLevel: float = 0.95"],
               ["+ sampleMCDropout(model, feat): float[20]", "+ computeEmpiricalStd(samples): float", "+ compute95CI(): float[2]", "+ evaluateReliability(): String"],
               color_hdr='#B45309')

    draw_class(770, 370, 330, 230, "SHAPExplainer", 
               ["- baselineVector: float[23]", "- numPermutations: int = 100", "- featureAttributions: Map"],
               ["+ computeShapleyValues(model, x): Map", "+ getTopPositiveDrivers(k: int): List", "+ getTopMitigatingDrivers(k: int): List", "+ generateWaterfallData(): JSON"],
               color_hdr='#7C3AED')

    draw_class(1150, 370, 300, 230, "CBTRecommender", 
               ["- cbtLibrary: Map<String, List<Exercise>>", "- severityTier: String"],
               ["+ matchInterventions(dominant: String): List", "+ getBehavioralPlan(): CBTPlan", "+ getSleepHygieneGuide(): CBTPlan"],
               color_hdr='#047857')

    draw_class(400, 60, 340, 240, "ClinicalDashboardController", 
               ["- activePatient: PatientProfile", "- currentSession: AssessmentRecord", "- chartInstances: Map"],
               ["+ renderRadarChart(subRisks: float[3])", "+ renderSHAPWaterfall(attributions: Map)", "+ renderGauge(score: float, ci: float[2])", "+ triggerCrisisModal(alerts: List)"],
               color_hdr='#1E3A8A')

    draw_class(800, 60, 320, 240, "ClinicalReportGenerator", 
               ["- clinicHeader: ClinicMeta", "- reportFormat: String = 'PDF'"],
               ["+ compileClinicalSummary(record): Document", "+ exportFHIRBundle(patient): JSON", "+ downloadClientPDF(): void"],
               color_hdr='#1E3A8A')

    # Association / Composition Lines
    def draw_link(x1, y1, x2, y2, label="", mult1="", mult2=""):
        ax.plot([x1, x2], [y1, y2], color='#475569', lw=1.5)
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my + 8, label, fontsize=7.5, ha='center', va='bottom', color='#334155',
                    bbox=dict(boxstyle="round,pad=0.1", fc='#FFFFFF', ec='none'))
        if mult1:
            ax.text(x1 + 10, y1 - 12, mult1, fontsize=8, fontweight='bold', color='#1E293B')
        if mult2:
            ax.text(x2 - 15, y2 - 12, mult2, fontsize=8, fontweight='bold', color='#1E293B')

    draw_link(310, 795, 360, 795, "submits", "1", "1..*")
    draw_link(670, 795, 720, 795, "normalizes", "1", "1")
    draw_link(1060, 795, 1110, 795, "extracts", "1", "1")
    draw_link(890, 680, 890, 600, "feeds vector", "1", "1")
    draw_link(195, 680, 195, 600, "evaluates", "1", "1")
    draw_link(350, 485, 400, 485, "samples", "1", "1")
    draw_link(720, 485, 770, 485, "explains", "1", "1")
    draw_link(1100, 485, 1150, 485, "triages", "1", "1")
    draw_link(570, 370, 570, 300, "controls", "1", "1")
    draw_link(740, 180, 800, 180, "generates", "1", "1")

    out_path = os.path.join(DIAGRAMS_DIR, "class_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Class Diagram:", out_path)
    return out_path

# -----------------------------------------------------------------------------
# 4. SEQUENCE DIAGRAM - FIG. 6
# -----------------------------------------------------------------------------
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 950)
    ax.axis('off')

    # Title
    ax.text(750, 920, "UML SEQUENCE DIAGRAM - SMART HEALTH RISK INDICATOR (SHRI)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1E3A8A', fontfamily='sans-serif')

    # Lifeline objects
    lifelines = [
        (120, "User / Clinician\n(Actor)", '#EFF6FF', '#2563EB'),
        (380, "UI: Clinical Portal\n(Browser Client)", '#F8FAFC', '#475569'),
        (650, "Feature Pipeline\n& NLP Engine", '#F0FDF4', '#059669'),
        (920, "4-Model Ensemble\n(Dep/Anx/Sleep/Fusion)", '#FAF5FF', '#7C3AED'),
        (1180, "UQ & XAI Engine\n(MC Dropout + SHAP)", '#FFFBEB', '#D97706'),
        (1400, "Local Storage\n(IndexedDB Cache)", '#FEF2F2', '#DC2626')
    ]

    for lx, lname, lbg, lborder in lifelines:
        # Header Box
        box = FancyBboxPatch((lx - 75, 830), 150, 50, boxstyle="round,pad=0,rounding_size=6", ec=lborder, fc=lbg, lw=1.5)
        ax.add_patch(box)
        ax.text(lx, 855, lname, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1E3A8A', multialignment='center')
        # Dashed Lifeline
        ax.plot([lx, lx], [830, 60], color='#94A3B8', lw=1.2, ls='--')

    # Step messages
    steps = [
        (1, 120, 380, 790, "1: Enter Questionnaire (PHQ/GAD/PSQI) & Journal Text", False, '#2563EB'),
        (2, 380, 650, 745, "2: processInputs(rawAnswers, journalText)", False, '#059669'),
        (3, 650, 650, 705, "3: computeSentiment() & scanCrisisKeywords()", True, '#059669'),
        (4, 650, 380, 665, "4: return {featureVector_23D, crisisFlag}", False, '#059669', True),
        (5, 380, 920, 620, "5: predictEnsemble(featureVector_23D)", False, '#7C3AED'),
        (6, 920, 920, 575, "6: executeDepNet(), AnxNet(), SleepNet() -> FusionNet()", True, '#7C3AED'),
        (7, 920, 380, 535, "7: return {compositeRisk: 0-100, subScores: [3]}", False, '#7C3AED', True),
        (8, 380, 1180, 490, "8: computeUQAndSHAP(featureVector_23D, models)", False, '#D97706'),
        (9, 1180, 1180, 445, "9: execute 20 MC Dropout Passes -> μ̂, σ̂, 95% CI", True, '#D97706'),
        (10, 1180, 1180, 405, "10: computePermutationSHAP(23 features) -> Φ", True, '#D97706'),
        (11, 1180, 380, 365, "11: return {ci_95: [low, high], shapValues: Map}", False, '#D97706', True),
        (12, 380, 1400, 320, "12: saveAssessmentRecord(encryptedPayload)", False, '#DC2626'),
        (13, 1400, 380, 275, "13: confirmStorageSuccess()", False, '#DC2626', True),
        (14, 380, 120, 230, "14: renderDashboard(Gauge, RadarChart, SHAP, CBTPlan)", False, '#1E3A8A'),
        (15, 120, 380, 180, "15: clickExportReport('PDF' | 'FHIR')", False, '#2563EB'),
        (16, 380, 120, 135, "16: downloadClientGeneratedPDF()", False, '#1E3A8A', True),
    ]

    for item in steps:
        snum, x1, x2, y, text, is_self, col = item[0:7]
        is_reply = len(item) > 7 and item[7]
        
        if is_self:
            # Self call loop
            ax.plot([x1, x1 + 35], [y + 10, y + 10], color=col, lw=1.4)
            ax.plot([x1 + 35, x1 + 35], [y + 10, y - 10], color=col, lw=1.4)
            ax.plot([x1 + 35, x1], [y - 10, y - 10], color=col, lw=1.4)
            # Arrow head
            ax.plot([x1 + 6, x1], [y - 7, y - 10], color=col, lw=1.4)
            ax.plot([x1 + 6, x1], [y - 13, y - 10], color=col, lw=1.4)
            ax.text(x1 + 42, y, text, fontsize=7.5, fontweight='bold', ha='left', va='center', color=col)
        else:
            ls = '--' if is_reply else '-'
            arrow = FancyArrowPatch((x1, y), (x2, y),
                                    arrowstyle="->,head_length=5,head_width=3.5",
                                    lw=1.4, ls=ls, color=col)
            ax.add_patch(arrow)
            mx = (x1 + x2) / 2
            ax.text(mx, y + 7, text, fontsize=7.5, fontweight='bold', ha='center', va='bottom', color=col,
                    bbox=dict(boxstyle="round,pad=0.15", fc='#FFFFFF', ec='#E2E8F0', lw=0.6))

    out_path = os.path.join(DIAGRAMS_DIR, "sequence_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Sequence Diagram:", out_path)
    return out_path

# -----------------------------------------------------------------------------
# 5. SYSTEM ARCHITECTURE DIAGRAM - FIG. 2
# -----------------------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 850)
    ax.axis('off')

    # Title
    ax.text(700, 815, "SYSTEM ARCHITECTURE - SMART HEALTH RISK INDICATOR (SHRI)", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#1E3A8A', fontfamily='sans-serif')

    # Layer 1: Ingestion
    box1 = FancyBboxPatch((40, 560), 380, 210, boxstyle="round,pad=0,rounding_size=8", ec='#2563EB', fc='#EFF6FF', lw=1.8)
    ax.add_patch(box1)
    ax.text(230, 745, "1. MULTIMODAL INTAKE LAYER", fontsize=11, fontweight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(60, 705, "• PHQ-9 (9 Depression Items)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(60, 675, "• GAD-7 (7 Anxiety Items)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(60, 645, "• PSQI (7 Sleep Architecture Items)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(60, 615, "• Free-Text Adolescent Journal Narratives", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(60, 585, "• Lifestyle Biomarkers (Sleep, Screen, Exercise)", fontsize=9, ha='left', va='center', color='#1E293B')

    # Layer 2: Preprocessing & NLP
    box2 = FancyBboxPatch((510, 560), 380, 210, boxstyle="round,pad=0,rounding_size=8", ec='#059669', fc='#F0FDF4', lw=1.8)
    ax.add_patch(box2)
    ax.text(700, 745, "2. PREPROCESSING & NLP PIPELINE", fontsize=11, fontweight='bold', ha='center', va='center', color='#065F46')
    ax.text(530, 705, "• Z-Score Standardization & Normalization", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(530, 675, "• VADER Sentiment & Lexical Scoring", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(530, 645, "• Acute Crisis Keyword Tripwire Scanner", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(530, 615, "• 23-Dimensional Vector Assembly", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(530, 585, "• Client-Side Tensor Conversion", fontsize=9, ha='left', va='center', color='#1E293B')

    # Layer 3: AI Ensemble Core
    box3 = FancyBboxPatch((980, 560), 380, 210, boxstyle="round,pad=0,rounding_size=8", ec='#7C3AED', fc='#FAF5FF', lw=1.8)
    ax.add_patch(box3)
    ax.text(1170, 745, "3. 4-MODEL STACKED ENSEMBLE", fontsize=11, fontweight='bold', ha='center', va='center', color='#5B21B6')
    ax.text(1000, 705, "• DepNet: BiLSTM + Attention (Depression)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(1000, 675, "• AnxNet: 1D-CNN + Residuals (Anxiety)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(1000, 645, "• SleepNet: Temporal CNN (Circadian Debt)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(1000, 615, "• FusionNet: Meta-Learner (23 Context Inputs)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(1000, 585, "• Huber Loss Robust Optimization (δ = 1.0)", fontsize=9, ha='left', va='center', color='#1E293B')

    # Arrows Row 1
    ax.add_patch(FancyArrowPatch((420, 665), (510, 665), arrowstyle="->,head_length=6,head_width=4", lw=2, color='#2563EB'))
    ax.add_patch(FancyArrowPatch((890, 665), (980, 665), arrowstyle="->,head_length=6,head_width=4", lw=2, color='#059669'))

    # Layer 4: UQ & XAI
    box4 = FancyBboxPatch((200, 280), 450, 190, boxstyle="round,pad=0,rounding_size=8", ec='#D97706', fc='#FFFBEB', lw=1.8)
    ax.add_patch(box4)
    ax.text(425, 440, "4. UNCERTAINTY QUANTIFICATION & XAI", fontsize=11, fontweight='bold', ha='center', va='center', color='#92400E')
    ax.text(220, 400, "• Monte Carlo Dropout (T = 20 Stochastic Passes)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(220, 370, "• Empirical Variance σ̂² & 95% Confidence Interval", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(220, 340, "• Permutation SHAP Additive Feature Attribution (Φ)", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(220, 310, "• Directional Risk Factor Ranking & Decomposition", fontsize=9, ha='left', va='center', color='#1E293B')

    # Layer 5: Clinical Decision Support & UI
    box5 = FancyBboxPatch((750, 280), 450, 190, boxstyle="round,pad=0,rounding_size=8", ec='#047857', fc='#ECFDF5', lw=1.8)
    ax.add_patch(box5)
    ax.text(975, 440, "5. CLINICAL DECISION SUPPORT & UI", fontsize=11, fontweight='bold', ha='center', va='center', color='#065F46')
    ax.text(770, 400, "• Dynamic Risk Gauge & Domain Radar Charts", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(770, 370, "• Evidence-Based CBT Coping Intervention Plans", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(770, 340, "• Longitudinal Trajectory Tracking & Anomaly Alerts", fontsize=9, ha='left', va='center', color='#1E293B')
    ax.text(770, 310, "• Automated PDF Summary & FHIR-Compliant Export", fontsize=9, ha='left', va='center', color='#1E293B')

    # Arrows Downward
    ax.add_patch(FancyArrowPatch((1170, 560), (425, 470), connectionstyle="arc3,rad=-0.2", arrowstyle="->,head_length=6,head_width=4", lw=2, color='#7C3AED'))
    ax.add_patch(FancyArrowPatch((650, 375), (750, 375), arrowstyle="->,head_length=6,head_width=4", lw=2, color='#D97706'))

    # Layer 6: Browser Execution Guarantee Box
    box6 = FancyBboxPatch((150, 50), 1100, 150, boxstyle="round,pad=0,rounding_size=10", ec='#1E3A8A', fc='#F8FAFC', lw=2)
    ax.add_patch(box6)
    ax.text(700, 165, "6. 100% BROWSER-NATIVE EXECUTION GUARANTEE (ZERO-SERVER DEPENDENCY)", fontsize=11.5, fontweight='bold', ha='center', va='center', color='#1E3A8A')
    ax.text(700, 130, "• Pure Client-Side JavaScript & WebAssembly Engine   • 100% Protected Health Information (PHI) On-Device Privacy", fontsize=9.5, ha='center', va='center', color='#1E293B')
    ax.text(700, 100, "• Sub-20ms Real-Time Inference Latency   • Zero Cloud Hosting or API Subscription Costs (GitHub Pages Ready)", fontsize=9.5, ha='center', va='center', color='#1E293B')
    ax.text(700, 70, "• Works Completely Offline After Initial Static Asset Load   • HIPAA & GDPR Compliant Privacy-by-Design Architecture", fontsize=9.5, ha='center', va='center', color='#1E293B')

    ax.add_patch(FancyArrowPatch((975, 280), (975, 200), arrowstyle="->,head_length=6,head_width=4", lw=2, color='#047857'))

    out_path = os.path.join(DIAGRAMS_DIR, "architecture_diagram.png")
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved Architecture Diagram:", out_path)
    return out_path

if __name__ == "__main__":
    generate_dfd()
    generate_use_case()
    generate_class_diagram()
    generate_sequence_diagram()
    generate_system_architecture()
    print("All 5 diagrams successfully generated in:", DIAGRAMS_DIR)
