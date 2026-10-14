import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count: 'Page X of Y'
    along with running header and footer.
    """
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
        self.setFillColor(colors.HexColor('#64748B'))

        # Running header (pages 2 and 3)
        if self._pageNumber > 1:
            self.drawString(40, 805, "Campus Circle AI — Project Concept Note | AICTE - IBM SkillsBuild 2026")
            self.drawRightString(555, 805, "Muskan Priyadarshani Patra (ID: IBMUEML013863)")
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(40, 798, 555, 798)

        # Running footer (all pages)
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.5)
        self.line(40, 40, 555, 40)

        self.drawString(40, 28, "AICTE | IBM SkillsBuild Applied AI & ML Internship • Partner: BharatCares")
        self.drawRightString(555, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def generate_concept_note(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F62FE'), # IBM Blue
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#161616'),
        spaceAfter=8
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#393939')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0F62FE'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#161616'),
        spaceBefore=6,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor('#262626'),
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.6,
        leading=12,
        textColor=colors.HexColor('#262626'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    table_th = ParagraphStyle(
        'TableTH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_td = ParagraphStyle(
        'TableTD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor('#262626')
    )

    table_td_bold = ParagraphStyle(
        'TableTDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=10.5,
        textColor=colors.HexColor('#161616')
    )

    elements = []

    # =========================================================================
    # PAGE 1: EXECUTIVE FOUNDATION, PROBLEM & SDG ALIGNMENT
    # =========================================================================
    elements.append(Paragraph("AICTE - IBM SKILLSBUILD INTERNSHIP 2026 • PROJECT CONCEPT NOTE", ParagraphStyle('Tag', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#DA1E28'), leading=10)))
    elements.append(Spacer(1, 2))
    elements.append(Paragraph("CAMPUS CIRCLE AI", title_style))
    elements.append(Paragraph("Smart Student Skill Exchange & Circular Campus Resource Network", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F62FE'), spaceAfter=6))

    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Program:</b> AICTE | IBM SkillsBuild Internship 2026<br/><b>Domain:</b> Machine Learning & Applied AI<br/><b>Partner:</b> BharatCares (CSRBOX)", meta_label),
            Paragraph("<b>Student / Intern:</b> Muskan Priyadarshani Patra<br/><b>Internship ID:</b> IBMUEML013863 | <b>Plan ID:</b> PLAN-CD7DED2B108B<br/><b>SDG Focus:</b> SDG 4 (Education), SDG 8 (Decent Work), SDG 12 (Consumption)", meta_label)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 255])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F4F4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E0E0E0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 4))

    # 1. Executive Summary
    elements.append(Paragraph("1. Executive Summary & Vision", h1_style))
    elements.append(Paragraph(
        "<b>Campus Circle AI</b> is an applied Artificial Intelligence and Machine Learning platform engineered to resolve two persistent inefficiencies within collegiate ecosystems: <b>(1) the single-semester educational equipment waste and expense crisis</b>, and <b>(2) the lack of syllabus-aligned, affordable peer technical mentoring</b>. Grounded in the <b>UN Sustainable Development Goals (SDG 4, SDG 8, and SDG 12)</b>, Campus Circle AI fuses a <b>Supervised Fair-Price Regressor</b> (Masterclass 3: Random Forest and Decision Tree) with an <b>NLP Semantic Skill Recommender</b> (Masterclass 4/5: TF-IDF Vectorization and Cosine Similarity) into an authenticated, closed-loop university environment.",
        body_style
    ))

    # 2. Problem Statement
    elements.append(Paragraph("2. Campus Problem Statement & Ground Need", h1_style))
    elements.append(Paragraph("University students across Indian higher education institutions face three structural bottlenecks each academic term:", body_style))
    elements.append(Paragraph("• <b>Resource Cost & Single-Term Waste (SDG 12):</b> Academic hardware such as mini drafters, scientific calculators, multimeter tools, drawing instruments, and reference textbooks are purchased at full retail price (MRP) but become idle after one semester. Incoming junior batches bear these recurring costs while older assets gather dust or end up in campus trash.", bullet_style))
    elements.append(Paragraph("• <b>Inaccessible, Impersonal Skill Learning (SDG 4):</b> Commercial EdTech courses charge prohibitive fees and fail to address college-specific lab assignments, viva examinations, and internal syllabi. Juniors lack a structured, safe bridge to learn practical skills from experienced seniors.", bullet_style))
    elements.append(Paragraph("• <b>Trust Deficit & Informal Chaos:</b> Present campus exchanges rely on unmoderated WhatsApp and Telegram groups plagued by spam, volatile negotiation friction, absent price transparency, and identity ambiguity.", bullet_style))

    # 3. UN SDG Alignment Table
    elements.append(Paragraph("3. UN Sustainable Development Goals (SDG) Alignment", h1_style))
    sdg_table = [
        [Paragraph("<b>SDG Goal</b>", table_th), Paragraph("<b>Target & Direct Operational Mechanism in Campus Circle AI</b>", table_th)],
        [
            Paragraph("<b>SDG 4:<br/>Quality Education</b>", ParagraphStyle('G4', parent=table_td_bold, textColor=colors.HexColor('#C5192D'))),
            Paragraph("<b>Target 4.4:</b> Substantially increases technical and vocational skills via peer-to-peer micro-learning. Juniors master coding (Python, DSA, Web) and engineering tools (AutoCAD, MATLAB, PCB design) directly from senior mentors at zero or micro cost.", table_td)
        ],
        [
            Paragraph("<b>SDG 8:<br/>Decent Work & Growth</b>", ParagraphStyle('G8', parent=table_td_bold, textColor=colors.HexColor('#A21942'))),
            Paragraph("<b>Target 8.6:</b> Enhances youth employability and interview readiness through hands-on technical teaching portfolios. Enables senior students to earn fair on-campus micro-income while fostering campus leadership.", table_td)
        ],
        [
            Paragraph("<b>SDG 12:<br/>Responsible Consumption</b>", ParagraphStyle('G12', parent=table_td_bold, textColor=colors.HexColor('#BF8B2E'))),
            Paragraph("<b>Target 12.5:</b> Substantially reduces campus solid waste by establishing a closed-loop circular exchange for textbooks, drafting tools, calculators, and lab components, keeping hardware out of local landfills.", table_td)
        ]
    ]
    t_sdg = Table(sdg_table, colWidths=[120, 395])
    t_sdg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#161616')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t_sdg)

    # 4. Target Customer Segments
    elements.append(Paragraph("4. Target Beneficiaries & Customer Segments", h1_style))
    elements.append(Paragraph("• <b>Primary Users:</b> Undergraduate students across engineering disciplines residing in campus hostels, PGs, and local student housing needing cost-effective lab tools and academic mentorship.", bullet_style))
    elements.append(Paragraph("• <b>Secondary Users:</b> Senior student mentors, university technical club coordinators, and student council leads seeking structured tutoring recognition.", bullet_style))
    elements.append(Paragraph("• <b>Early Adopters:</b> 1st and 2nd-year engineering students needing immediate lab equipment (mini drafters, calculators) and practical orientation for introductory programming and CAD practicals.", bullet_style))

    # END OF PAGE 1
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: MACHINE LEARNING ENGINES & CROSS-DISCIPLINARY MATRIX
    # =========================================================================
    elements.append(Paragraph("5. Technical Machine Learning Methodology", h1_style))
    elements.append(Paragraph(
        "Directly translating the core curriculum of the <b>IBM SkillsBuild Masterclass Series</b> (Masterclass 3: Supervised Learning & Regression; Masterclasses 4 & 5: Applied AI & Recommenders), Campus Circle AI integrates two production-ready Machine Learning engines:",
        body_style
    ))

    elements.append(Paragraph("<b>A. Supervised Fair-Price Regressor (Masterclass 3 Alignment):</b>", h2_style))
    elements.append(Paragraph(
        "To replace subjective haggling with transparent algorithmic valuation, we engineered a multi-feature regression model predicting fair depreciated asset pricing. Features include: <i>Original MRP (Rs.)</i>, <i>Age in Semesters (1–8)</i>, <i>Physical Condition Rating (1–5)</i>, <i>Item Category One-Hot Encoding</i>, and <i>Campus Demand Index</i>. Trained on 300 campus transactions with an 80:20 train/test split, models performed as follows:",
        body_style
    ))

    # ML Benchmark Table
    ml_table = [
        [Paragraph("<b>Model Architecture</b>", table_th), Paragraph("<b>Evaluation Task</b>", table_th), Paragraph("<b>R² Score</b>", table_th), Paragraph("<b>MAE (Mean Absolute Error)</b>", table_th), Paragraph("<b>Curriculum Alignment</b>", table_th)],
        [
            Paragraph("<b>Random Forest Regressor</b>", table_td_bold),
            Paragraph("Fair Depreciated Price", table_td),
            Paragraph("<b>0.9527</b>", table_td_bold),
            Paragraph("<b>Rs.68.23</b>", table_td),
            Paragraph("Production Ensemble ML", table_td)
        ],
        [
            Paragraph("<b>Decision Tree Regressor</b>", table_td_bold),
            Paragraph("Fair Depreciated Price", table_td),
            Paragraph("0.9133", table_td),
            Paragraph("Rs.96.25", table_td),
            Paragraph("IBM Masterclass 3 Baseline", table_td)
        ]
    ]
    t_ml = Table(ml_table, colWidths=[120, 105, 65, 105, 120])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F62FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_ml)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("<b>B. Natural Language Semantic Skill Recommender (Masterclasses 4 & 5 Alignment):</b>", h2_style))
    elements.append(Paragraph(
        "Rather than relying on brittle keyword filtering, the Skill Recommender implements <b>TF-IDF (Term Frequency-Inverse Document Frequency) N-gram Vectorization</b> coupled with <b>Cosine Angular Similarity</b>. Student natural language intent strings (e.g., <i>'Want to learn Python for data science and model building'</i>) are projected into a high-dimensional vector space, calculating mathematical cosine similarity against all verified campus mentor skill embeddings to output ranked compatibility scores (0%–100%).",
        body_style
    ))

    # 6. Cross-Disciplinary Academic Matrix
    elements.append(Paragraph("6. Cross-Disciplinary Academic Matrix (5 Core Engineering Branches)", h1_style))
    elements.append(Paragraph("Campus Circle AI delivers campus-wide inclusivity covering <b>50 Academic Lab Resources</b> and <b>50 Technical Skills</b> across 5 core engineering streams:", body_style))

    branch_table = [
        [Paragraph("<b>Engineering Stream</b>", table_th), Paragraph("<b>Marketplace Resources (10 Cataloged per Branch)</b>", table_th), Paragraph("<b>Skill Hub Modules (10 Skills per Branch)</b>", table_th)],
        [
            Paragraph("<b>Mechanical (MECH)</b>", table_td_bold),
            Paragraph("Mechanics textbooks, Drawing tools, Vernier caliper, Screw gauge, Workshop kits, Machine Design notes, Thermodynamics books, AutoCAD guides, 3D modelling files, Manufacturing manuals", table_td),
            Paragraph("AutoCAD, SolidWorks, CATIA, 3D Printing, Ansys FEA, Engineering Drawing, CNC Programming, GD&T, MATLAB for Mechanics, Fluid Simulation", table_td)
        ],
        [
            Paragraph("<b>Electrical (ELEC)</b>", table_td_bold),
            Paragraph("Circuit kits, Breadboards & components, Digital Multimeter, Basic Electrical books, Power Electronics notes, Arduino starter kits, Control Systems books, Signal cables, Microcontroller boards, Transformer manuals", table_td),
            Paragraph("Arduino prototyping, MATLAB/Simulink, Circuit design, PCB Design (EasyEDA), IoT systems, Proteus simulation, PLC basics, Power system analysis, Sensor interfacing, Embedded C", table_td)
        ],
        [
            Paragraph("<b>Civil (CIVIL)</b>", table_td_bold),
            Paragraph("Surveying instruments, Drawing boards & clips, Mini drafters, Building Materials books, Structural Analysis manuals, Ranging rods & tape, Concrete Tech textbooks, Soil Mechanics guides, Fluid Mechanics manuals, Highway Engg references", table_td),
            Paragraph("AutoCAD Civil 3D, Revit Architecture, Total Station surveying, STAAD Pro, Estimating & Costing, GIS basics, Structural detailing, Blueprint reading, Construction management, Site inspection", table_td)
        ],
        [
            Paragraph("<b>Computer (CE/CSE)</b>", table_td_bold),
            Paragraph("Programming books, DSA textbooks, Raspberry Pi, Network crimping tools, Computer Architecture guides, OS references, Web development books, AI/ML study guides, DBMS manuals, Linux cheat sheets", table_td),
            Paragraph("Python, Web Development, DSA, Git & GitHub, Machine Learning, Database SQL, Java, Android App dev, Cloud computing (GCP/AWS), Cyber security basics", table_td)
        ],
        [
            Paragraph("<b>Biomedical (BIOMED)</b>", table_td_bold),
            Paragraph("Biomedical textbooks, Medical instrumentation manuals, Physiology atlases, Biomechanics guides, Sensor experiment kits, Biosignal processing notes, Biomaterials references, Lab coats & safety gear, Clinical equipment guides, Imaging handbooks", table_td),
            Paragraph("Biosignal analysis, MATLAB for Healthcare, Medical image processing, Biomechanics analysis, LabVIEW basics, Arduino for Medical sensors, Healthcare IoT, Prosthetics 3D design, Bio-instrumentation, Regulatory standards", table_td)
        ]
    ]
    t_branch = Table(branch_table, colWidths=[110, 205, 200])
    t_branch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#161616')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t_branch)

    # 7. System Architecture
    elements.append(Paragraph("7. System Implementation & Tech Stack", h1_style))
    elements.append(Paragraph("• <b>Machine Learning & Analytics:</b> Scikit-Learn (RandomForestRegressor, DecisionTreeRegressor, TfidfVectorizer, cosine_similarity), Pandas, NumPy, Matplotlib.", bullet_style))
    elements.append(Paragraph("• <b>Full-Stack Interfaces:</b> Interactive Streamlit analytical application (port 8501) with custom glassmorphism styles, coupled with an asynchronous FastAPI REST engine (port 8000) and vanilla JS/HTML5 frontend.", bullet_style))
    elements.append(Paragraph("• <b>Verification Architecture:</b> Institutional college email domain gating (.edu / @college.ac.in) establishing closed-loop campus trust.", bullet_style))

    # END OF PAGE 2
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 3: LEAN CANVAS, ROADMAP, IMPACT & CONCLUSION
    # =========================================================================
    elements.append(Paragraph("8. Lean Canvas Business Framework Summary", h1_style))

    canvas_table = [
        [Paragraph("<b>Lean Canvas Dimension</b>", table_th), Paragraph("<b>Strategic Specification for Campus Circle AI</b>", table_th)],
        [
            Paragraph("<b>Unique Value Proposition (UVP)</b>", table_td_bold),
            Paragraph("<b>'One platform. Two solutions. For every student.'</b> Fuses circular hardware reuse and peer technical tutoring into one authenticated campus platform.", table_td)
        ],
        [
            Paragraph("<b>Unfair Advantage</b>", table_td_bold),
            Paragraph("Closed-loop institutional email authentication; zero delivery or shipping fees (hand-to-hand campus handoffs); exact alignment with university syllabi and lab evaluations.", table_td)
        ],
        [
            Paragraph("<b>Channels</b>", table_td_bold),
            Paragraph("College orientation sessions, Student Council & Tech Club partnerships, official campus Discord/WhatsApp communities, physical QR code flyers in labs and hostels.", table_td)
        ],
        [
            Paragraph("<b>Revenue Streams</b>", table_td_bold),
            Paragraph("100% free for peer-to-peer swaps; nominal 5%–10% platform facilitation on paid senior-junior masterclasses; small listing fee (Rs.10–Rs.20) for urgent marketplace banners; bookstore sponsorships.", table_td)
        ],
        [
            Paragraph("<b>Cost Structure</b>", table_td_bold),
            Paragraph("Low fixed cloud hosting (Streamlit Community / AWS / Vercel), negligible domain upkeep, campus student ambassador kits.", table_td)
        ],
        [
            Paragraph("<b>Key Metrics</b>", table_td_bold),
            Paragraph("Monthly Active Campus Users (MAU), successful resource swaps, peer tutoring hours completed, total student rupees saved (INR), kilograms of waste diverted.", table_td)
        ]
    ]
    t_canvas = Table(canvas_table, colWidths=[140, 375])
    t_canvas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F62FE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_canvas)

    # 9. Phased Roadmap
    elements.append(Paragraph("9. Phased Implementation & Scalability Roadmap", h1_style))
    elements.append(Paragraph("• <b>Phase 1 — Campus Pilot (Months 1–3):</b> Launch within host university hostels, labs, and academic departments. Target 500+ active student users, catalog 150+ academic assets, and facilitate 200+ peer tutoring hours.", bullet_style))
    elements.append(Paragraph("• <b>Phase 2 — Regional College Expansion (Months 4–8):</b> Expand to neighboring colleges in Daman, Vapi, and surrounding university clusters. Introduce inter-campus technical skill workshops and verified cross-college equipment swaps.", bullet_style))
    elements.append(Paragraph("• <b>Phase 3 — Pan-India Scalability (Months 9–18):</b> Scale across India's 40M+ higher education student population. Even a 5% adoption rate represents a thriving ecosystem of 2,000,000+ active student users.", bullet_style))

    # 10. Projected Impact Metrics
    elements.append(Paragraph("10. Projected Societal, Economic & Environmental Impact", h1_style))
    elements.append(Paragraph("• <b>Direct Economic Savings:</b> Projected average saving of Rs.520 per item per student, yielding an estimated aggregate student community savings of <b>Rs.95,000+ per semester</b> in a single college.", bullet_style))
    elements.append(Paragraph("• <b>Landfill Waste Diversion:</b> Diverts over <b>340+ kg</b> of plastic drafting tools, lab instruments, electronic kits, and discarded paper textbooks annually from local municipal landfills.", bullet_style))
    elements.append(Paragraph("• <b>Practical Learning Velocity:</b> Facilitates <b>400+ peer mentoring hours</b> per semester, elevating student pass rates and practical exam readiness in core engineering disciplines.", bullet_style))

    # 11. Conclusion
    elements.append(Paragraph("11. Conclusion & Alignment with IBM SkillsBuild Mission", h1_style))
    elements.append(Paragraph(
        "Campus Circle AI represents an authentic synthesis of applied artificial intelligence and community-driven social impact. By transforming fragmented, unverified campus exchanges into an intelligent, equitable, and sustainable circular network, this project directly embodies the ethos of the <b>AICTE | IBM SkillsBuild Internship 2026</b>: leveraging real-world machine learning to solve tangible everyday challenges.",
        body_style
    ))
    elements.append(Spacer(1, 6))

    # Sign-off box
    sign_data = [
        [
            Paragraph("<b>Submitted by:</b> Muskan Priyadarshani Patra<br/><b>Internship ID:</b> IBMUEML013863<br/><b>Plan ID:</b> PLAN-CD7DED2B108B", meta_label),
            Paragraph("<b>Domain:</b> Machine Learning & Applied AI<br/><b>Program:</b> AICTE | IBM SkillsBuild Internship 2026<br/><b>Date of Submission:</b> October 2026", meta_label)
        ]
    ]
    t_sign = Table(sign_data, colWidths=[260, 255])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F4F4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F62FE')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_sign)

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Concept Note PDF generated successfully at {output_path}")

if __name__ == "__main__":
    out_file = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Concept_Note.pdf"
    generate_concept_note(out_file)
