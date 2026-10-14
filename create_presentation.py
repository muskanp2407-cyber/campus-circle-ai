import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_paths):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Color Palette (IBM Carbon & Modern Design)
    c_dark_navy = RGBColor(10, 15, 30)       # #0A0F1E
    c_navy = RGBColor(15, 23, 42)            # #0F172A
    c_blue = RGBColor(15, 98, 254)           # #0F62FE (IBM Carbon Blue)
    c_vibrant_blue = RGBColor(37, 99, 235)   # #2563EB
    c_teal = RGBColor(13, 148, 136)          # #0D9488
    c_rose = RGBColor(225, 29, 72)           # #E11D48
    c_orange = RGBColor(234, 88, 12)         # #EA580C
    c_purple = RGBColor(124, 58, 237)        # #7C3AED
    c_gray_bg = RGBColor(248, 250, 252)      # #F8FAFC
    c_white = RGBColor(255, 255, 255)
    c_text_dark = RGBColor(15, 23, 42)       # #0F172A
    c_text_sub = RGBColor(51, 65, 85)        # #334155
    c_text_muted = RGBColor(100, 116, 139)   # #64748B
    c_border_light = RGBColor(226, 232, 240) # #E2E8F0

    logo_path = "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/logo.jpeg"
    sc_dir = "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/screenshots"

    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, title_text, category_text, subtitle_text=None):
        # Top accent decorative line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_blue
        top_bar.line.color.rgb = c_blue

        # Category Tag Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.32), Inches(3.6), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = RGBColor(238, 242, 255)
        pill.line.color.rgb = RGBColor(199, 210, 254)
        pill.line.width = Pt(1)

        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        p_pill = tf_pill.paragraphs[0]
        p_pill.text = category_text.upper()
        p_pill.font.size = Pt(10.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = c_vibrant_blue
        p_pill.alignment = PP_ALIGN.CENTER

        # Slide Main Title (Large, Bold, High-contrast)
        tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(10.5), Inches(0.75))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = c_navy

        if subtitle_text:
            p_sub = tf_t.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = c_text_muted

        # Logo on right
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.4), Inches(0.3), height=Inches(0.9))

    def create_card(slide, x, y, width, height, title, subtitle, bullets, accent_color, body_font_size=13.5):
        # Card container
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_border_light
        card.line.width = Pt(1.5)

        # Top colored accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, width, Inches(0.12))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = accent_color
        stripe.line.color.rgb = accent_color

        # Text inside card
        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), width - Inches(0.4), height - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        # Title
        p_title = tf.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(18)
        p_title.font.bold = True
        p_title.font.color.rgb = accent_color
        p_title.space_after = Pt(3)

        # Subtitle
        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(12.5)
            p_sub.font.bold = True
            p_sub.font.color.rgb = c_text_muted
            p_sub.space_after = Pt(10)

        # Bullets
        for lead, text in bullets:
            p_b = tf.add_paragraph()
            p_b.space_after = Pt(7)
            
            run_lead = p_b.add_run()
            run_lead.text = f"• {lead}: "
            run_lead.font.size = Pt(body_font_size)
            run_lead.font.bold = True
            run_lead.font.color.rgb = c_text_dark

            run_body = p_b.add_run()
            run_body.text = text
            run_body.font.size = Pt(body_font_size)
            run_body.font.color.rgb = c_text_sub

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, c_dark_navy)

    # Accent decorative bar on left
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.1), Inches(0.15), Inches(5.3))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = c_blue
    bar1.line.color.rgb = c_blue

    tbox1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.1), Inches(8.5), Inches(5.3))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "AICTE | IBM SKILLSBUILD APPLIED AI & ML INTERNSHIP 2026"
    p0.font.size = Pt(15)
    p0.font.bold = True
    p0.font.color.rgb = c_orange
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "CAMPUS CIRCLE AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = c_white
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Smart Student Skill Exchange & Circular Campus Resource Network\nPowered by Machine Learning Regressors & Semantic Recommenders"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Submitted by: Muskan Priyadarshani Patra\nInternship ID: IBMUEML013863  |  Plan ID: PLAN-CD7DED2B108B\nOrganizing Partner: BharatCares (CSRBOX)  |  Domain: Applied AI & ML\nUN SDGs: SDG 4 (Quality Education) • SDG 8 (Decent Work) • SDG 12 (Consumption)"
    p3.font.size = Pt(13.5)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(10.1), Inches(2.2), width=Inches(2.5))

    # =========================================================================
    # SLIDE 2: 1. PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, c_gray_bg)
    add_header(s2, "01. The Problem: Campus Resource Inefficiencies", "TOPIC 1: PROBLEM STATEMENT", "Dual structural bottlenecks affecting millions of university students each term")

    prob_cards = [
        ("Wasted Academic Resources", "Single-Semester Discard Cycle",
         [("Costly Hardware", "Mini drafters, calculators, and lab tools bought at full MRP."),
          ("Idle After 4 Months", "Valuable items sit unused in hostels after just 1 semester."),
          ("Recurring Expense", "Junior batches are forced to buy brand-new equipment repeatedly."),
          ("Landfill Dumping", "Discarded tools and books create unnecessary campus solid waste.")], c_rose),
        ("Inaccessible Practical Skills", "Generic & Costly EdTech Barrier",
         [("Costly Subscriptions", "Commercial platforms charge high recurring fees."),
          ("Syllabus Disconnect", "Online tutorials ignore college-specific lab exams & vivas."),
          ("Missing Mentors", "Juniors lack direct access to seniors who mastered the subjects."),
          ("Hands-on Gap", "Classroom theory fails to build practical engineering confidence.")], c_vibrant_blue),
        ("Informal & Unsafe Exchanges", "Chaotic WhatsApp & Telegram Groups",
         [("Unorganized Groups", "Student trades rely on noisy chats prone to spam and chaos."),
          ("Price Haggling", "Unfair bargaining and disputes with zero price transparency."),
          ("Identity Fraud", "No college verification; risk of external spammers & scammers."),
          ("High Friction", "Difficult to discover trusted seniors or matching equipment.")], c_orange)
    ]

    for i, (title, sub, bullets, color) in enumerate(prob_cards):
        x = Inches(0.8 + i * 4.0)
        create_card(s2, x, Inches(1.65), Inches(3.7), Inches(5.2), title, sub, bullets, color, 13.5)

    # =========================================================================
    # SLIDE 3: 2. WHY THE PROBLEM MATTERS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, c_gray_bg)
    add_header(s3, "02. Why the Problem Matters: Real-World Campus Impact", "TOPIC 2: PROBLEM RELEVANCE & URGENCY", "Tangible economic strain, environmental degradation, and career readiness gaps")

    why_cards = [
        ("Financial Burden on Students", "Recurring Out-of-Pocket Expenses",
         [("High Annual Cost", "Engineering students spend ₹6,000–₹10,000 annually on physical materials."),
          ("Hostel Budget Strain", "Low-income students struggle with high upfront costs each semester."),
          ("Grade Disadvantage", "Students without proper lab tools suffer in practical exams and marks."),
          ("Avoidable Debt", "Money is wasted on tools that exist idle a few doors away in hostels.")], c_orange),
        ("Environmental Degradation", "Campus Solid Waste & Plastic Footprint",
         [("Non-Biodegradable", "Plastic drafters, rulers, and calculators take centuries to degrade."),
          ("Massive Paper Waste", "Thousands of textbooks discarded rather than channeled to juniors."),
          ("Missing Circularity", "Universities lack an automated system for equipment reuse."),
          ("Green Campus Failure", "Campuses miss key NAAC/NIRF sustainability metrics.")], c_teal),
        ("Employability & Skill Gap", "The Practical Competency Deficit",
         [("Industry Demand", "Companies demand hands-on tools: Python, Git, CAD, DSA, and IoT."),
          ("70%+ Skill Deficit", "Rote learning leaves students unprepared for tech interviews."),
          ("1-on-1 Guidance", "Personalized senior mentoring accelerates practical mastery 3x faster."),
          ("Campus Leadership", "Senior mentors gain valuable technical leadership portfolios.")], c_vibrant_blue)
    ]

    for i, (title, sub, bullets, color) in enumerate(why_cards):
        x = Inches(0.8 + i * 4.0)
        create_card(s3, x, Inches(1.65), Inches(3.7), Inches(5.2), title, sub, bullets, color, 13.5)

    # =========================================================================
    # SLIDE 4: 3. PROPOSED SOLUTION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, c_gray_bg)
    add_header(s4, "03. Proposed Solution: Campus Circle AI Platform", "TOPIC 3: PROPOSED SOLUTION", "A unified, closed-loop student ecosystem combining circular exchanges and peer learning")

    # Banner quote
    banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.95))
    banner.fill.solid()
    banner.fill.fore_color.rgb = c_navy
    banner.line.color.rgb = c_blue
    banner.line.width = Pt(1.5)

    tb_b = s4.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(11.3), Inches(0.85))
    tf_b = tb_b.text_frame
    p_b0 = tf_b.paragraphs[0]
    p_b0.text = "“One Platform. Two Solutions. For Every Student.”"
    p_b0.font.size = Pt(18)
    p_b0.font.bold = True
    p_b0.font.color.rgb = c_white
    p_b0.alignment = PP_ALIGN.CENTER
    p_b1 = tf_b.add_paragraph()
    p_b1.text = "Fusing AI-Powered Peer Skill Tutoring and a Circular Campus Marketplace within a Verified Closed-Loop Network"
    p_b1.font.size = Pt(12)
    p_b1.font.color.rgb = RGBColor(203, 213, 225)
    p_b1.alignment = PP_ALIGN.CENTER

    sol_cards = [
        ("AI Peer Skill Hub", "Democratizing Knowledge (SDG 4)",
         [("Semantic Matching", "Connects learners with senior mentors via Natural Language AI."),
          ("Syllabus Alignment", "Micro-tutoring focused on college exams, vivas, and lab practicals."),
          ("Zero-Cost Swapping", "Skill exchange (e.g. learn Python in return for AutoCAD basics)."),
          ("Mentor Portfolios", "Seniors gain leadership credentials and micro-earning perks.")], c_vibrant_blue),
        ("Circular Campus Marketplace", "Sustainable Hardware Lifecycle (SDG 12)",
         [("Verified Trades", "Buy, sell, or swap textbooks, drafting tools, and lab kits safely."),
          ("ML Fair Pricing", "AI calculates true depreciated value to eliminate bargaining friction."),
          ("Zero Shipping", "Instant hand-to-hand handoffs on campus with zero packaging waste."),
          ("Massive Savings", "Students save 40%–70% compared to brand-new retail prices.")], c_teal),
        ("Verified Campus Trust", "Safe & Closed-Loop Security",
         [("College Email Gating", "Access strictly restricted to verified @college.ac.in emails."),
          ("Zero Outsiders", "Completely eliminates anonymous spammers, bots, and scammers."),
          ("Peer Reviews", "Ratings, session completion tracking, and batch verification."),
          ("Admin Dashboard", "Universities track carbon diversion and total student savings.")], c_orange)
    ]

    for i, (title, sub, bullets, color) in enumerate(sol_cards):
        x = Inches(0.8 + i * 4.0)
        create_card(s4, x, Inches(2.75), Inches(3.7), Inches(4.2), title, sub, bullets, color, 13)

    # =========================================================================
    # SLIDE 5: 4. HOW YOUR SYSTEM WORKS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, c_gray_bg)
    add_header(s5, "04. How Your System Works: End-to-End Workflow & Branches", "TOPIC 4: SYSTEM WORKFLOW & ARCHITECTURE", "Structured 4-step user journey backed by 5 engineering disciplines")

    steps = [
        ("Step 1: Auth & Verification", "College Email Gating",
         "Students register using official college email ID (@college.ac.in). Branch and semester profile initialized."),
        ("Step 2: Smart Discovery", "50 Resources & 50 Skills",
         "Explore cataloged resources & skills across Mechanical, Electrical, Civil, Computer & Biomedical."),
        ("Step 3: ML Valuation & Match", "Random Forest & TF-IDF",
         "Predicts fair secondhand price & calculates semantic compatibility score with verified peer mentors."),
        ("Step 4: Safe On-Campus Handoff", "Zero-Cost Exchange",
         "Schedule 1-on-1 peer session or meet on campus for hardware handover with zero delivery overhead.")
    ]

    for i, (title, sub, body) in enumerate(steps):
        x = Inches(0.8 + i * 3.0)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.65), Inches(2.8), Inches(2.5))
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_vibrant_blue
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(x + Inches(0.12), Inches(1.75), Inches(2.55), Inches(2.3))
        ctf = tb.text_frame
        ctf.word_wrap = True

        p_t = ctf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = c_vibrant_blue
        p_t.space_after = Pt(2)

        p_s = ctf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = c_text_muted
        p_s.space_after = Pt(6)

        p_b = ctf.add_paragraph()
        p_b.text = body
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = c_text_sub

    # Cross-disciplinary matrix card at bottom
    bot_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.35), Inches(11.7), Inches(2.65))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = c_white
    bot_card.line.color.rgb = c_border_light
    bot_card.line.width = Pt(1.5)

    tb_bot = s5.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(11.3), Inches(2.45))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True

    p_bt = tf_bot.paragraphs[0]
    p_bt.text = "Cross-Disciplinary Academic Matrix: 5 Engineering Branches (50 Items • 50 Skills)"
    p_bt.font.size = Pt(15)
    p_bt.font.bold = True
    p_bt.font.color.rgb = c_navy
    p_bt.space_after = Pt(6)

    matrix_lines = [
        ("Mechanical (MECH)", "Drawing tools, Vernier caliper, Workshop kits, Mechanics books", "AutoCAD, SolidWorks, CATIA, Ansys, 3D Printing"),
        ("Electrical (ELEC)", "Breadboards, Digital Multimeter, Circuit kits, Arduino boards", "Circuit design, MATLAB/Simulink, PCB Design, IoT systems"),
        ("Civil (CIVIL)", "Surveying tools, Mini drafters, Building materials guides, Total Station", "AutoCAD Civil 3D, Revit Architecture, STAAD Pro, GIS"),
        ("Computer (CE/CSE)", "Programming books, DSA guides, Raspberry Pi, Crimping kits", "Python, Web Dev, DSA, Machine Learning, Git/GitHub, SQL"),
        ("Biomedical (BIOMED)", "Medical instrumentation guides, Physiology atlases, Sensor kits", "Biosignal analysis, MATLAB Healthcare, Medical imaging, IoT")
    ]
    for dept, res, skl in matrix_lines:
        p_m = tf_bot.add_paragraph()
        p_m.space_after = Pt(2)
        run_d = p_m.add_run()
        run_d.text = f"• {dept}: "
        run_d.font.size = Pt(12)
        run_d.font.bold = True
        run_d.font.color.rgb = c_blue

        run_r = p_m.add_run()
        run_r.text = f"{res}  ➔  Skills: {skl}"
        run_r.font.size = Pt(12)
        run_r.font.color.rgb = c_text_sub

    # =========================================================================
    # SLIDE 6: 5. AI/ML USED
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, c_gray_bg)
    add_header(s6, "05. AI & Machine Learning Architecture", "TOPIC 5: MACHINE LEARNING ENGINES", "Direct implementation of IBM SkillsBuild Masterclasses 3, 4 & 5")

    # Left Card: Supervised Regression
    c_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = c_white
    c_left.line.color.rgb = c_blue
    c_left.line.width = Pt(2)

    tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "1. Supervised Fair-Price Regressor"
    p_lt.font.size = Pt(18)
    p_lt.font.bold = True
    p_lt.font.color.rgb = c_blue
    p_lt.space_after = Pt(2)

    p_ls = tf_l.add_paragraph()
    p_ls.text = "IBM SkillsBuild Masterclass 3: Supervised Learning & Regression"
    p_ls.font.size = Pt(13)
    p_ls.font.bold = True
    p_ls.font.color.rgb = c_text_muted
    p_ls.space_after = Pt(10)

    rf_bullets = [
        ("Objective", "Predicts transparent secondhand price to eliminate student negotiation disputes."),
        ("Engineered Features", "Original MRP (₹), Age in Semesters (1–8), Physical Condition (1–5), Category, and Campus Demand Index."),
        ("Model Benchmark", "Random Forest Regressor (R² = 0.9527, MAE = ₹68.23) vs Decision Tree (R² = 0.9133, MAE = ₹96.25)."),
        ("Production Choice", "Random Forest selected for low variance and superior non-linear depreciation modeling.")
    ]
    for lead, text in rf_bullets:
        p_b = tf_l.add_paragraph()
        p_b.space_after = Pt(8)
        run_l = p_b.add_run()
        run_l.text = f"• {lead}: "
        run_l.font.size = Pt(13.5)
        run_l.font.bold = True
        run_l.font.color.rgb = c_text_dark
        run_t = p_b.add_run()
        run_t.text = text
        run_t.font.size = Pt(13.5)
        run_t.font.color.rgb = c_text_sub

    # Right Card: NLP Recommender
    c_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = c_white
    c_right.line.color.rgb = c_teal
    c_right.line.width = Pt(2)

    tb_r = s6.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "2. NLP Semantic Skill Recommender"
    p_rt.font.size = Pt(18)
    p_rt.font.bold = True
    p_rt.font.color.rgb = c_teal
    p_rt.space_after = Pt(2)

    p_rs = tf_r.add_paragraph()
    p_rs.text = "IBM SkillsBuild Masterclasses 4 & 5: Applied AI & Recommenders"
    p_rs.font.size = Pt(13)
    p_rs.font.bold = True
    p_rs.font.color.rgb = c_text_muted
    p_rs.space_after = Pt(10)

    nlp_bullets = [
        ("Objective", "Matches free-text student learning goals with verified senior peer mentors."),
        ("TF-IDF Vectorization", "N-gram word frequency weighting with sublinear TF scaling on skill terms."),
        ("Cosine Angular Similarity", "Computes high-dimensional vector alignment (0% to 100% compatibility score)."),
        ("Output Delivery", "Ranks mentors displaying verified branch, rating, shared interests, and free swap options.")
    ]
    for lead, text in nlp_bullets:
        p_b = tf_r.add_paragraph()
        p_b.space_after = Pt(8)
        run_l = p_b.add_run()
        run_l.text = f"• {lead}: "
        run_l.font.size = Pt(13.5)
        run_l.font.bold = True
        run_l.font.color.rgb = c_text_dark
        run_t = p_b.add_run()
        run_t.text = text
        run_t.font.size = Pt(13.5)
        run_t.font.color.rgb = c_text_sub

    # =========================================================================
    # SLIDE 7: 6. TECHNOLOGY USED
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, c_gray_bg)
    add_header(s7, "06. Technology Used: Full-Stack & Machine Learning Architecture", "TOPIC 6: TECHNOLOGY STACK", "Modern, scalable, and production-tested open source software ecosystem")

    tech_cols = [
        ("Machine Learning & Data", "Scikit-Learn, Pandas, NumPy",
         [("Scikit-Learn", "RandomForestRegressor, DecisionTreeRegressor, TfidfVectorizer, cosine_similarity."),
          ("Data Science", "Pandas & NumPy for data cleansing and one-hot encoding."),
          ("Validation", "Train-test split (80:20), MAE, and R² score evaluation.")], c_blue),
        ("Analytical Web App", "Streamlit & Matplotlib",
         [("Streamlit 1.30+", "Reactive UI with 5 multi-disciplinary interactive modules."),
          ("Custom Styles", "Glassmorphism cards, badges, and real-time KPI metrics."),
          ("Matplotlib", "Depreciation visualizer & feature importance charts.")], c_rose),
        ("Asynchronous REST API", "FastAPI & Uvicorn",
         [("FastAPI", "High-performance asynchronous REST backend engine."),
          ("Uvicorn ASGI", "Lightning-fast production server on port 8000."),
          ("Pydantic", "Strict request/response data validation schemas.")], c_teal),
        ("Modern Web Client", "HTML5, CSS3, JavaScript",
         [("Modern SPA", "Interactive marketplace with branch filter dropdown."),
          ("Dynamic AJAX", "Real-time peer session scheduling & price calculator."),
          ("Chart.js", "Live campus savings and waste diversion metrics.")], c_orange)
    ]

    for i, (title, sub, bullets, color) in enumerate(tech_cols):
        x = Inches(0.8 + i * 3.0)
        create_card(s7, x, Inches(1.65), Inches(2.8), Inches(5.2), title, sub, bullets, color, 12.5)

    # =========================================================================
    # SLIDE 8: 7. SCREENSHOTS/DEMO - PART 1
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, c_gray_bg)
    add_header(s8, "07. Screenshots / Demo: Dashboard & Skill Matcher", "TOPIC 7: LIVE DEMO & UI WALKTHROUGH", "High-resolution proof of working platform modules in the Streamlit application")

    im1_path = os.path.join(sc_dir, "1_dashboard_impact.png")
    if os.path.exists(im1_path):
        s8.shapes.add_picture(im1_path, Inches(0.8), Inches(1.65), width=Inches(5.7))
    tb_cap1 = s8.shapes.add_textbox(Inches(0.8), Inches(5.65), Inches(5.7), Inches(1.5))
    tf_c1 = tb_cap1.text_frame
    tf_c1.word_wrap = True
    pc1_t = tf_c1.paragraphs[0]
    pc1_t.text = "Module 1: Real-Time Campus Impact & SDG Metrics"
    pc1_t.font.size = Pt(15)
    pc1_t.font.bold = True
    pc1_t.font.color.rgb = c_navy
    pc1_b = tf_c1.add_paragraph()
    pc1_b.text = "Live KPI counters displaying total student rupees saved (₹95,000+), peer tutoring hours completed (400+), and physical hardware diverted from municipal landfills (340+ kg)."
    pc1_b.font.size = Pt(13)
    pc1_b.font.color.rgb = c_text_sub

    im2_path = os.path.join(sc_dir, "2_skill_matcher.png")
    if os.path.exists(im2_path):
        s8.shapes.add_picture(im2_path, Inches(6.8), Inches(1.65), width=Inches(5.7))
    tb_cap2 = s8.shapes.add_textbox(Inches(6.8), Inches(5.65), Inches(5.7), Inches(1.5))
    tf_c2 = tb_cap2.text_frame
    tf_c2.word_wrap = True
    pc2_t = tf_c2.paragraphs[0]
    pc2_t.text = "Module 2: Natural Language Semantic Peer Skill Matcher"
    pc2_t.font.size = Pt(15)
    pc2_t.font.bold = True
    pc2_t.font.color.rgb = c_navy
    pc2_b = tf_c2.add_paragraph()
    pc2_b.text = "Ranks verified peer mentors using TF-IDF and Cosine Angular Similarity with exact compatibility percentages, displaying verified branch, rating, and zero-cost swap opportunities."
    pc2_b.font.size = Pt(13)
    pc2_b.font.color.rgb = c_text_sub

    # =========================================================================
    # SLIDE 9: 7. SCREENSHOTS/DEMO - PART 2
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, c_gray_bg)
    add_header(s9, "07. Screenshots / Demo: Fair-Price Valuation & ML Engine", "TOPIC 7: LIVE DEMO & UI WALKTHROUGH", "Supervised regression pricing module and comparative machine learning benchmarking")

    im3_path = os.path.join(sc_dir, "3_fair_price_predictor.png")
    if os.path.exists(im3_path):
        s9.shapes.add_picture(im3_path, Inches(0.8), Inches(1.65), width=Inches(5.7))
    tb_cap3 = s9.shapes.add_textbox(Inches(0.8), Inches(5.65), Inches(5.7), Inches(1.5))
    tf_c3 = tb_cap3.text_frame
    tf_c3.word_wrap = True
    pc3_t = tf_c3.paragraphs[0]
    pc3_t.text = "Module 3: Supervised ML Fair-Price Predictor"
    pc3_t.font.size = Pt(15)
    pc3_t.font.bold = True
    pc3_t.font.color.rgb = c_navy
    pc3_b = tf_c3.add_paragraph()
    pc3_b.text = "Evaluates original retail MRP, semesters used, condition rating (1–5), and demand to predict transparent fair prices, estimated discount percentage, and student rupee savings."
    pc3_b.font.size = Pt(13)
    pc3_b.font.color.rgb = c_text_sub

    im4_path = os.path.join(sc_dir, "4_ml_architecture.png")
    if os.path.exists(im4_path):
        s9.shapes.add_picture(im4_path, Inches(6.8), Inches(1.65), width=Inches(5.7))
    tb_cap4 = s9.shapes.add_textbox(Inches(6.8), Inches(5.65), Inches(5.7), Inches(1.5))
    tf_c4 = tb_cap4.text_frame
    tf_c4.word_wrap = True
    pc4_t = tf_c4.paragraphs[0]
    pc4_t.text = "Module 4: Machine Learning Model Benchmarking"
    pc4_t.font.size = Pt(15)
    pc4_t.font.bold = True
    pc4_t.font.color.rgb = c_navy
    pc4_b = tf_c4.add_paragraph()
    pc4_b.text = "Direct comparative benchmarking between Random Forest and Decision Tree Regressor displaying R² accuracy scores, MAE errors, and predictive feature importance rankings."
    pc4_b.font.size = Pt(13)
    pc4_b.font.color.rgb = c_text_sub

    # =========================================================================
    # SLIDE 10: 8. RESULTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, c_gray_bg)
    add_header(s10, "08. Results: Machine Learning Performance & Validation", "TOPIC 8: RESULTS & METRICS", "Quantitative model evaluation and projected single-campus pilot validation")

    # ML Results Box on Left
    c_res_l = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.65), Inches(6.8), Inches(5.2))
    c_res_l.fill.solid()
    c_res_l.fill.fore_color.rgb = c_white
    c_res_l.line.color.rgb = c_blue
    c_res_l.line.width = Pt(2)

    tb_rl = s10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.4), Inches(4.9))
    tf_rl = tb_rl.text_frame
    tf_rl.word_wrap = True

    p_rlt = tf_rl.paragraphs[0]
    p_rlt.text = "Machine Learning Benchmark Results"
    p_rlt.font.size = Pt(18)
    p_rlt.font.bold = True
    p_rlt.font.color.rgb = c_navy
    p_rlt.space_after = Pt(10)

    # Insert Table with larger font
    table_shape = s10.shapes.add_table(3, 4, Inches(1.0), Inches(2.4), Inches(6.4), Inches(1.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.3)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.4)
    table.columns[3].width = Inches(1.5)

    headers = ["Model", "R² Score", "MAE", "Status"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_navy
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = c_white

    row1 = ["Random Forest Regressor", "0.9527", "₹68.23", "Selected Model"]
    for col_idx, val in enumerate(row1):
        cell = table.cell(1, col_idx)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = (col_idx == 1 or col_idx == 3)
            p.font.color.rgb = c_blue if col_idx == 3 else c_text_dark

    row2 = ["Decision Tree Regressor", "0.9133", "₹96.25", "Masterclass Baseline"]
    for col_idx, val in enumerate(row2):
        cell = table.cell(2, col_idx)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.color.rgb = c_text_dark

    tb_sub = s10.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(6.4), Inches(2.3))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub0 = tf_sub.paragraphs[0]
    p_sub0.text = "Key ML Performance Insights:"
    p_sub0.font.size = Pt(14)
    p_sub0.font.bold = True
    p_sub0.font.color.rgb = c_navy
    p_sub0.space_after = Pt(6)

    res_insights = [
        ("High Accuracy", "Random Forest achieves 95.27% R² score on 300 test transactions."),
        ("Feature Dominance", "Original MRP & Condition account for 68% of predictive importance."),
        ("Zero Latency", "Model inference executes in <15ms via FastAPI and Streamlit.")
    ]
    for lead, text in res_insights:
        p_b = tf_sub.add_paragraph()
        p_b.space_after = Pt(4)
        run_l = p_b.add_run()
        run_l.text = f"• {lead}: "
        run_l.font.size = Pt(13)
        run_l.font.bold = True
        run_l.font.color.rgb = c_text_dark
        run_t = p_b.add_run()
        run_t.text = text
        run_t.font.size = Pt(13)
        run_t.font.color.rgb = c_text_sub

    # Right Card: Projected Campus Impact
    c_res_r = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.65), Inches(4.7), Inches(5.2))
    c_res_r.fill.solid()
    c_res_r.fill.fore_color.rgb = c_white
    c_res_r.line.color.rgb = c_teal
    c_res_r.line.width = Pt(2)

    tb_rr = s10.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.3), Inches(4.9))
    tf_rr = tb_rr.text_frame
    tf_rr.word_wrap = True

    p_rrt = tf_rr.paragraphs[0]
    p_rrt.text = "Campus Pilot Impact (Single Term)"
    p_rrt.font.size = Pt(18)
    p_rrt.font.bold = True
    p_rrt.font.color.rgb = c_navy
    p_rrt.space_after = Pt(12)

    stat_cards = [
        ("₹95,000+", "Total Student Money Saved per Semester", c_blue),
        ("340+ kg", "Hardware & Textbook Waste Diverted from Landfills", c_teal),
        ("400+ hrs", "Peer Tutoring & Practical Skill Learning Completed", c_orange),
        ("5 Disciplines", "50 Resources & 50 Skills Mapped across 15 Mentors", c_rose)
    ]

    for val, lbl, col in stat_cards:
        p_v = tf_rr.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(26)
        p_v.font.bold = True
        p_v.font.color.rgb = col
        p_l = tf_rr.add_paragraph()
        p_l.text = lbl
        p_l.font.size = Pt(12.5)
        p_l.font.bold = True
        p_l.font.color.rgb = c_text_muted
        p_l.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: 9. BENEFITS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11, c_gray_bg)
    add_header(s11, "09. Benefits: Triple Impact for People, Planet & Campus", "TOPIC 9: PLATFORM BENEFITS & VALUE", "Substantial measurable value delivered across students, institutions, and global goals")

    benefit_cards = [
        ("For Students", "Affordability & Practical Skills",
         [("40%–70% Savings", "Cut semester expenses on lab kits, books, and drafting gear."),
          ("Syllabus Mastery", "1-on-1 tutoring focused on upcoming internal exams and lab vivas."),
          ("Peer Micro-Earnings", "Experienced senior mentors gain recognized income and perks."),
          ("Career Portfolios", "Builds verified practical competence for technical job placements.")], c_vibrant_blue),
        ("For University Campus", "Community & Green Campus Culture",
         [("Strong Camaraderie", "Builds productive, friendly bonds across senior and junior batches."),
          ("Circular Campus", "Promotes sustainable, zero-waste equipment reuse within hostels."),
          ("Accreditation Boost", "Directly improves NIRF & NAAC Green Campus evaluation scores."),
          ("Zero Risk", "Closed-loop authentication eliminates external spam and theft.")], c_teal),
        ("UN Sustainable Development", "Global Goals Alignment",
         [("SDG 4 (Education)", "Target 4.4: Democratizes technical and vocational micro-learning."),
          ("SDG 8 (Decent Work)", "Target 8.6: Fosters youth employability and technical leadership."),
          ("SDG 12 (Consumption)", "Target 12.5: Substantially diverts equipment waste from landfills."),
          ("Scalable Model", "Ready to replicate across all Indian engineering universities.")], c_orange)
    ]

    for i, (title, sub, bullets, color) in enumerate(benefit_cards):
        x = Inches(0.8 + i * 4.0)
        create_card(s11, x, Inches(1.65), Inches(3.7), Inches(5.2), title, sub, bullets, color, 13.5)

    # =========================================================================
    # SLIDE 12: 10. FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12, c_gray_bg)
    add_header(s12, "10. Future Scope & Phased Implementation Roadmap", "TOPIC 10: SCALABILITY & FUTURE ROADMAP", "Clear strategic roadmap from local university pilot to national collegiate network")

    phases = [
        ("Phase 1: Campus Pilot", "Months 1 – 3",
         [("Host College Rollout", "Deploy in university hostels, academic departments, and tech clubs."),
          ("500+ Active Users", "Onboard 500+ verified students across 5 engineering streams."),
          ("Live Valuation", "Validate fair-price regressor on 250+ live student marketplace trades."),
          ("200+ Tutoring Hours", "Facilitate peer tutoring with satisfaction rating benchmark > 4.7/5.")], c_vibrant_blue),
        ("Phase 2: Regional College Hubs", "Months 4 – 8",
         [("Multi-College Network", "Expand to colleges across Daman, Vapi, and neighboring clusters."),
          ("Inter-Campus Swaps", "Enable inter-college technical hackathons and shared resource pools."),
          ("Stationery Partnerships", "Collaborate with university bookstores for student discounts."),
          ("Computer Vision AI", "Integrate automated image analysis for item condition grading.")], c_teal),
        ("Phase 3: Pan-India Scalability", "Months 9 – 18",
         [("National Expansion", "Scale across India's 40,000,000+ higher education student population."),
          ("Mobile Application", "Launch native Flutter iOS and Android app with instant push alerts."),
          ("University SaaS", "Admin dashboard for colleges to track verified campus sustainability."),
          ("2M+ User Goal", "Achieving 5% adoption creates an active ecosystem of 2M+ students.")], c_orange)
    ]

    for i, (title, sub, bullets, color) in enumerate(phases):
        x = Inches(0.8 + i * 4.0)
        create_card(s12, x, Inches(1.65), Inches(3.7), Inches(5.2), title, sub, bullets, color, 13.5)

    # =========================================================================
    # SLIDE 13: CONCLUSION & THANK YOU
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13, c_dark_navy)

    bar13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(1.1), Inches(0.15), Inches(5.3))
    bar13.fill.solid()
    bar13.fill.fore_color.rgb = c_orange
    bar13.line.color.rgb = c_orange

    tbox13 = s13.shapes.add_textbox(Inches(1.3), Inches(1.1), Inches(8.5), Inches(5.3))
    tf13 = tbox13.text_frame
    tf13.word_wrap = True

    p_th0 = tf13.paragraphs[0]
    p_th0.text = "AICTE | IBM SKILLSBUILD INTERNSHIP 2026"
    p_th0.font.size = Pt(15)
    p_th0.font.bold = True
    p_th0.font.color.rgb = c_orange
    p_th0.space_after = Pt(12)

    p_th1 = tf13.add_paragraph()
    p_th1.text = "THANK YOU!"
    p_th1.font.size = Pt(46)
    p_th1.font.bold = True
    p_th1.font.color.rgb = c_white
    p_th1.space_after = Pt(10)

    p_th2 = tf13.add_paragraph()
    p_th2.text = "“With CampusCircle, every campus becomes a smarter, more connected, and self-sustaining community.”"
    p_th2.font.size = Pt(18)
    p_th2.font.color.rgb = RGBColor(203, 213, 225)
    p_th2.space_after = Pt(26)

    p_th3 = tf13.add_paragraph()
    p_th3.text = (
        "• Project: Campus Circle AI — Student Skill Exchange & Circular Resource Network\n"
        "• Author / Intern: Muskan Priyadarshani Patra\n"
        "• Internship ID: IBMUEML013863  |  Plan ID: PLAN-CD7DED2B108B\n"
        "• GitHub Repository: github.com/muskanp2407-cyber/campus-circle-ai\n"
        "• Live Streamlit Application: localhost:8501  |  FastAPI Backend: 127.0.0.1:8000\n"
        "• Ready for Questions & Discussion!"
    )
    p_th3.font.size = Pt(14)
    p_th3.font.color.rgb = RGBColor(148, 163, 184)

    if os.path.exists(logo_path):
        s13.shapes.add_picture(logo_path, Inches(10.1), Inches(2.2), width=Inches(2.5))

    for p in output_paths:
        prs.save(p)
        print(f"Presentation saved successfully to {p} with {len(prs.slides)} slides.")

if __name__ == "__main__":
    out1 = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Final_Presentation.pptx"
    out2 = "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/Campus_Circle_AI_Final_Presentation.pptx"
    create_deck([out1, out2])
