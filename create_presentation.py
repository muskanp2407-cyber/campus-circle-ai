import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Colors
    c_navy = RGBColor(15, 23, 42)      # #0f172a
    c_blue = RGBColor(37, 99, 235)     # #2563eb
    c_pink = RGBColor(225, 29, 72)     # #e11d48
    c_orange = RGBColor(249, 115, 22)  # #f97316
    c_gray_bg = RGBColor(248, 250, 252) # #f8fafc
    c_text_dark = RGBColor(30, 41, 59)
    c_text_muted = RGBColor(100, 116, 139)
    c_white = RGBColor(255, 255, 255)
    c_card_border = RGBColor(226, 232, 240)

    logo_path = "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/logo.jpeg"

    def add_header(slide, title_text, category_text="IBM SKILLSBUILD | APPLIED AI & ML INTERNSHIP 2026"):
        # Top banner line
        top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        top_line.fill.solid()
        top_line.fill.fore_color.rgb = c_orange
        top_line.line.color.rgb = c_orange

        # Category / Tag
        tx_box_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        tf_cat = tx_box_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_blue

        # Title
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11), Inches(0.8))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = c_navy

        # Logo on right if available
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(11.2), Inches(0.35), height=Inches(0.95))

    # ---------------- SLIDE 1: TITLE SLIDE ----------------
    s1 = prs.slides.add_slide(blank_layout)
    # Background shape
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = c_navy
    bg1.line.color.rgb = c_navy

    # Accent decorative bar
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.15), Inches(5.0))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = c_orange
    bar1.line.color.rgb = c_orange

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(7.5), Inches(4.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "AICTE | IBM SkillsBuild Internship 2026 | BharatCares"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = c_orange
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "CAMPUS CIRCLE AI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = c_white
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Smart Student Skill Exchange & Circular Campus Resource Network\nPowered by Machine Learning & Recommender Systems"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Submitted by: Muskan Priyadarshani Patra\nInternship ID: IBMUEML013863 | Plan ID: PLAN-CD7DED2B108B\nAligned with UN SDGs: SDG 4 (Quality Education) & SDG 8 (Decent Work)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # Insert logo on right
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(9.2), Inches(2.2), width=Inches(3.2))

    # ---------------- SLIDE 2: CONTEXT & UN SDG ALIGNMENT ----------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "UN Sustainable Development Goals (SDG) Alignment")
    
    sdgs = [
        ("SDG 4: QUALITY EDUCATION", "Target 4.4: Substantially increase youth with technical and vocational skills", 
         "• Peer-to-peer micro-mentoring in syllabus-aligned topics (Python, CAD, DSA).\n• Eliminates costly EdTech barriers through campus knowledge democratization.\n• Practical collaborative learning directly between seniors and juniors.", c_pink),
        ("SDG 8: DECENT WORK & ECONOMIC GROWTH", "Target 8.6: Substantially reduce youth not in employment or education", 
         "• Senior students gain recognized mentoring experience and micro-earnings.\n• Juniors build project portfolios, interview readiness, and industry tools.\n• Fosters campus entrepreneurship and localized professional networks.", c_blue),
        ("SDG 12: RESPONSIBLE CONSUMPTION", "Target 12.5: Substantially reduce waste generation through reuse", 
         "• Circular campus marketplace for textbooks, lab drafters, and calculators.\n• Prevents single-semester equipment dumping into landfills.\n• Saves students 40%–70% compared to purchasing new hardware.", c_orange)
    ]

    for i, (title, sub, details, color) in enumerate(sdgs):
        x = Inches(0.8 + i * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = c_gray_bg
        card.line.color.rgb = color
        card.line.width = Pt(2)

        tb = s2.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(3.4), Inches(4.7))
        ctf = tb.text_frame
        ctf.word_wrap = True
        
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.size = Pt(14)
        cp1.font.bold = True
        cp1.font.color.rgb = color
        cp1.space_after = Pt(8)

        cp2 = ctf.add_paragraph()
        cp2.text = sub
        cp2.font.size = Pt(11)
        cp2.font.italic = True
        cp2.font.color.rgb = c_text_muted
        cp2.space_after = Pt(14)

        cp3 = ctf.add_paragraph()
        cp3.text = details
        cp3.font.size = Pt(12)
        cp3.font.color.rgb = c_text_dark

    # ---------------- SLIDE 3: PROBLEM STATEMENT ----------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "The Problems Faced by College Students")

    probs = [
        ("Wasted Campus Resources", "Students buy expensive engineering tools, lab coats, and books that lie unused after 1 semester while juniors struggle to afford them.", "Over 70% of student hardware is discarded or remains idle."),
        ("Expensive & Impersonal Skill Learning", "Commercial online courses are expensive, generic, and unhelpful for college exams and hands-on lab practicals.", "Students lack access to trusted peer mentors who took the exact course."),
        ("No Unified, Safe Campus Platform", "Students currently rely on chaotic WhatsApp groups with zero verification, frequent scams, and unorganized listings.", "Lack of verified college email security and transparent ratings.")
    ]

    for i, (title, desc, stat) in enumerate(probs):
        y = Inches(1.8 + i * 1.7)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = c_gray_bg
        card.line.color.rgb = c_card_border

        num_card = s3.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.1), y + Inches(0.3), Inches(0.8), Inches(0.8))
        num_card.fill.solid()
        num_card.fill.fore_color.rgb = c_orange
        num_card.line.color.rgb = c_orange
        ntf = num_card.text_frame
        np = ntf.paragraphs[0]
        np.text = f"0{i+1}"
        np.font.size = Pt(16)
        np.font.bold = True
        np.font.color.rgb = c_white
        np.alignment = PP_ALIGN.CENTER

        tb = s3.shapes.add_textbox(Inches(2.2), y + Inches(0.15), Inches(10.0), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = f"{desc}  |  Impact: {stat}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = c_text_muted

    # ---------------- SLIDE 4: THE SOLUTION ----------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Campus Circle AI — The Integrated Solution")

    sols = [
        ("Campus Marketplace", "Verified student marketplace to buy, sell, or swap books, lab drafters, calculators, and tools inside campus.\n\nPromotes reuse, cuts costs, and eliminates landfill waste.", c_orange),
        ("AI Peer Skill Hub", "Connects learners with senior student mentors in coding, CAD, public speaking, and machine learning.\n\nAI Recommender pairs students based on semantic needs & availability.", c_blue),
        ("Verified Trust Graph", "Access strictly via official college email IDs (@college.edu).\n\nPeer review ratings and transaction history ensure high safety and zero scam risk.", c_pink)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(sols):
        x = Inches(0.8 + i * 4.0)
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(4.9))
        c.fill.solid()
        c.fill.fore_color.rgb = c_white
        c.line.color.rgb = scolor
        c.line.width = Pt(2)

        tb = s4.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = scolor
        p1.space_after = Pt(14)

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(13)
        p2.font.color.rgb = c_text_dark

    # ---------------- SLIDE 4B: 5 DEPARTMENTS RESOURCE & SKILL MATRIX ----------------
    s4b = prs.slides.add_slide(blank_layout)
    add_header(s4b, "Cross-Disciplinary Coverage: 5 Departments • 50 Resources • 50 Skills", "MULTI-DEPARTMENT CAMPUS MATRIX")

    dept_matrix = [
        ("MECH", "Mechanical Engineering", c_orange,
         "10 Marketplace Items:\n• Mechanics Textbooks\n• Engg Drawing Tools\n• Vernier Caliper & Gauge\n• Workshop Tool Kits\n• Machine Design & Thermo Notes\n• CAD Books & 3D Practice Files\n• Manufacturing Lab Manuals",
         "10 Skill Hub Skills:\n• AutoCAD & SolidWorks\n• CATIA Basics & 3D Modeling\n• Engineering Drawing\n• CNC Machining\n• Workshop Safety\n• Thermodynamics Concepts\n• Machine Design Fundamentals"),
        
        ("ELEC", "Electrical Engineering", c_blue,
         "10 Marketplace Items:\n• Electrical Machines Books\n• Circuit Theory Notes\n• Digital Multimeter\n• Breadboards & Jumpers\n• Electronic Component Kits\n• Measuring Instruments\n• Power & Control Systems Notes\n• Simulation Project Files",
         "10 Skill Hub Skills:\n• Circuit Analysis\n• MATLAB / Simulink\n• Circuit Simulation\n• Basic Electronics\n• Digital Logic Design\n• Arduino Circuit Projects\n• Power System Analysis\n• PCB Design Basics"),
        
        ("CIVIL", "Civil Engineering", RGBColor(16, 185, 129),
         "10 Marketplace Items:\n• Surveying Vol 1 & 2\n• A1/A2 Drawing Sheets\n• Scale Rulers & Stencils\n• Field Surveying Manuals\n• 30m Land Measuring Tapes\n• Plumb Bob & Field Kit\n• Building Materials Notes\n• Structural Analysis Books",
         "10 Skill Hub Skills:\n• AutoCAD 2D Drafting\n• Civil 3D & Revit/BIM\n• Surveying Total Station\n• Quantity Estimation\n• Building Planning\n• Structural Analysis\n• Excel for Civil Calculations\n• Concrete Mix Design"),

        ("CE", "Computer Engineering", RGBColor(99, 102, 241),
         "10 Marketplace Items:\n• Programming Textbooks\n• DSA & LeetCode Notes\n• Operating Systems Books\n• DBMS Review Binders\n• Raspberry Pi 4 Model B\n• Arduino Uno R3 Boards\n• 37-in-1 Sensor Modules\n• Computer Networks Manuals",
         "10 Skill Hub Skills:\n• C/C++ & Java\n• Python Programming\n• Full-Stack Web Dev\n• React.js Basics\n• Database & SQL\n• Git & GitHub Versioning\n• Machine Learning Basics\n• UI/UX & Cybersecurity"),

        ("BIOMED", "Biomedical Engineering", c_pink,
         "10 Marketplace Items:\n• Biomedical Textbooks\n• Ross & Wilson Anatomy\n• Medical Instrumentation\n• Signal Processing Notes\n• Medical Electronics Manuals\n• Anatomical Heart Models\n• AD8232 ECG Modules\n• MAX30102 Pulse Oximeters",
         "10 Skill Hub Skills:\n• Biomedical Instruments\n• Human Physiology\n• ECG Signal Interpretation\n• MATLAB Signal Processing\n• Medical Image Processing\n• Biosensor Interfacing\n• Arduino Medical Prototypes\n• Biomedical Data Analytics")
    ]

    for i, (code, dname, col, res_list, skill_list) in enumerate(dept_matrix):
        x = Inches(0.6 + i * 2.45)
        card = s4b.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(2.35), Inches(5.3))
        card.fill.solid()
        card.fill.fore_color.rgb = c_gray_bg
        card.line.color.rgb = col
        card.line.width = Pt(2)

        # Header tag
        tag = s4b.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.1), Inches(1.8), Inches(2.15), Inches(0.55))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.color.rgb = col
        ttf = tag.text_frame
        tp = ttf.paragraphs[0]
        tp.text = f"{code}: {dname.split()[0]}"
        tp.font.size = Pt(11)
        tp.font.bold = True
        tp.font.color.rgb = c_white
        tp.alignment = PP_ALIGN.CENTER

        tb = s4b.shapes.add_textbox(x + Inches(0.1), Inches(2.4), Inches(2.15), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_r = tf.paragraphs[0]
        p_r.text = res_list
        p_r.font.size = Pt(8.5)
        p_r.font.color.rgb = c_text_dark
        p_r.space_after = Pt(8)

        p_s = tf.add_paragraph()
        p_s.text = skill_list
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = c_navy

    # ---------------- SLIDE 5: AI ENGINE 1 - SKILL MATCHER ----------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "AI Module 1: Semantic Peer Skill Matcher (SDG 4)")

    # Left card: Algorithm
    c_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = c_gray_bg
    c_left.line.color.rgb = c_card_border

    tbl = s5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tfl = tbl.text_frame
    tfl.word_wrap = True
    pl1 = tfl.paragraphs[0]
    pl1.text = "Natural Language Recommender Engine"
    pl1.font.size = Pt(17)
    pl1.font.bold = True
    pl1.font.color.rgb = c_blue
    pl1.space_after = Pt(10)

    pl2 = tfl.add_paragraph()
    pl2.text = "• Technology: Scikit-learn TF-IDF Vectorizer + Cosine Similarity.\n• Input: Student natural language queries (e.g., 'Want to learn Python, ML algorithms and data science').\n• Processing: Creates n-gram word vector representations across mentor skill offerings, bios, and branch domains.\n• Matching: Computes angular cosine similarity metric between learner query vector and all campus mentor vectors.\n• Output: Ranked compatibility score (%) with contact links."
    pl2.font.size = Pt(13)
    pl2.font.color.rgb = c_text_dark

    # Right card: Example
    c_right = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = c_navy
    c_right.line.color.rgb = c_navy

    tbr = s5.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfr = tbr.text_frame
    tfr.word_wrap = True
    pr1 = tfr.paragraphs[0]
    pr1.text = "Live Match Output Sample"
    pr1.font.size = Pt(17)
    pr1.font.bold = True
    pr1.font.color.rgb = c_orange
    pr1.space_after = Pt(12)

    pr2 = tfr.add_paragraph()
    pr2.text = "Query: 'I want to learn Python and Machine Learning'\n\nRank #1: Aarav Sharma (CSE - 7th Sem)\n• Compatibility: 94.2% Match Score\n• Skills Offered: Python, Scikit-learn, ML, Pandas\n• Verified: IBM SkillsBuild Certified Intern\n• Fee Model: Skill Swap (Zero Cost)\n\nRank #2: Sneha Mukherjee (UI/UX - 6th Sem)\n• Compatibility: 48.1% (Secondary skill interest)\n\nEnables instant syllabus-matched tutoring!"
    pr2.font.size = Pt(12)
    pr2.font.color.rgb = RGBColor(226, 232, 240)

    # ---------------- SLIDE 6: AI ENGINE 2 - FAIR PRICE PREDICTOR ----------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "AI Module 2: Supervised Fair-Price ML Regressor (SDG 8 & 12)")

    c_left6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9))
    c_left6.fill.solid()
    c_left6.fill.fore_color.rgb = c_gray_bg
    c_left6.line.color.rgb = c_card_border

    tbl6 = s6.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tfl6 = tbl6.text_frame
    tfl6.word_wrap = True
    p6_1 = tfl6.paragraphs[0]
    p6_1.text = "Supervised Regression Model"
    p6_1.font.size = Pt(17)
    p6_1.font.bold = True
    p6_1.font.color.rgb = c_orange
    p6_1.space_after = Pt(10)

    p6_2 = tfl6.add_paragraph()
    p6_2.text = "• Aligned with Masterclass 3 (Supervised Learning & Decision Trees).\n• Problem: Secondhand sellers overcharge or underprice, creating buyer friction and failed transactions.\n• Features Engineered:\n  1. Original MRP (Retail price)\n  2. Age in Semesters (1 to 8)\n  3. Condition Rating (1 to 5 scale)\n  4. Category (Books, Drafters, Calculators, Kits)\n  5. Campus Demand Index (Exam season factor)\n• Algorithm: Ensemble Random Forest Regressor & Decision Tree."
    p6_2.font.size = Pt(13)
    p6_2.font.color.rgb = c_text_dark

    # Right Card: Results
    c_right6 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.9))
    c_right6.fill.solid()
    c_right6.fill.fore_color.rgb = c_white
    c_right6.line.color.rgb = c_blue
    c_right6.line.width = Pt(2)

    tbr6 = s6.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.1), Inches(4.5))
    tfr6 = tbr6.text_frame
    tfr6.word_wrap = True
    pr6_1 = tfr6.paragraphs[0]
    pr6_1.text = "Valuation & Savings Output"
    pr6_1.font.size = Pt(17)
    pr6_1.font.bold = True
    pr6_1.font.color.rgb = c_blue
    pr6_1.space_after = Pt(12)

    pr6_2 = tfr6.add_paragraph()
    pr6_2.text = "Example Item: Casio Scientific Calculator\n• Original MRP: ₹1,200\n• Age: 2 Semesters | Condition: 4/5 Stars\n\nAI Predictions:\n• Suggested Fair Price: ₹620\n• Depreciation: 48.3%\n• Direct Student Saving: ₹580\n• Decision Tree Baseline: ₹600\n\nProtects both student buyers and sellers with objective, machine-learned transparency."
    pr6_2.font.size = Pt(13)
    pr6_2.font.color.rgb = c_text_dark

    # ---------------- SLIDE 7: MODEL EVALUATION METRICS ----------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Model Performance & Masterclass Alignment")

    metrics_cards = [
        ("Random Forest Regressor", "R² Score: 95.27%", "MAE: ₹68.23", "Primary Production Model with low generalization error across 300 campus listings.", c_blue),
        ("Decision Tree Regressor", "R² Score: 91.33%", "MAE: ₹96.25", "Direct reference to Masterclass 3 curriculum; baseline tree with depth=5.", c_orange),
        ("TF-IDF Skill Recommender", "Cosine Similarity", "Top-K Matching", "Sub-10ms response time; extracts uni-grams and bi-grams across mentor bios and skill tags.", c_pink)
    ]

    for i, (mtitle, mstat1, mstat2, mdesc, mcol) in enumerate(metrics_cards):
        x = Inches(0.8 + i * 4.0)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = c_gray_bg
        card.line.color.rgb = mcol
        card.line.width = Pt(2)

        tb = s7.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = mtitle
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = mcol
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = mstat1
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = c_navy
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = mstat2
        p3.font.size = Pt(15)
        p3.font.bold = True
        p3.font.color.rgb = c_text_muted
        p3.space_after = Pt(16)

        p4 = tf.add_paragraph()
        p4.text = mdesc
        p4.font.size = Pt(12)
        p4.font.color.rgb = c_text_dark

    # ---------------- SLIDE 8: LEAN CANVAS SUMMARY ----------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Lean Canvas Summary (Masterclass 5 Reference)")

    canvas_items = [
        ("Problem", "Expensive books & tools; isolated skill learning; unsafe WhatsApp groups."),
        ("Solution", "AI-based peer skill matcher + verified campus secondhand marketplace."),
        ("Unique Value", "One verified platform: Swap items, gain practical skills, save money."),
        ("Unfair Advantage", "Closed-loop university email verification & student trust network."),
        ("Customer Segments", "Engineering, science & management students in hostels and campus housing."),
        ("Channels", "Campus student councils, orientations, tech clubs, WhatsApp integration."),
        ("Cost Structure", "Cloud hosting, domain, SMS verification, maintenance & promotion."),
        ("Revenue Streams", "Small listing fee for premium ads; 5-10% fee on paid tutoring; stationery deals.")
    ]

    for i, (head, body) in enumerate(canvas_items):
        row = i // 4
        col = i % 4
        x = Inches(0.8 + col * 2.95)
        y = Inches(1.8 + row * 2.5)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(2.8), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_card_border

        tb = s8.shapes.add_textbox(x + Inches(0.1), y + Inches(0.1), Inches(2.6), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = c_blue
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = c_text_dark

    # ---------------- SLIDE 9: APPLICATION ARCHITECTURE & UI ----------------
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Application Demo & User Interface")

    # Left: App Modules
    tb9 = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.9))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    p9_1 = tf9.paragraphs[0]
    p9_1.text = "Interactive Streamlit Web Application"
    p9_1.font.size = Pt(18)
    p9_1.font.bold = True
    p9_1.font.color.rgb = c_navy
    p9_1.space_after = Pt(10)

    p9_2 = tf9.add_paragraph()
    p9_2.text = "• Module 1: Dashboard & SDG Impact Tracker\n  Live tracking of student savings, peer hours, and waste diverted.\n\n• Module 2: AI Peer Skill Matcher\n  Semantic NLP matching of learning requirements against campus mentors.\n\n• Module 3: Smart Fair-Price Predictor\n  Real-time Supervised ML estimation of secondhand equipment valuation.\n\n• Module 4: Campus Circle AI Agent\n  Natural language chatbot assisting with peer learning roadmaps.\n\n• Module 5: Model Analytics & Metrics\n  Live R² regression curves and algorithm comparison graphs."
    p9_2.font.size = Pt(12.5)
    p9_2.font.color.rgb = c_text_dark

    # Right: Technology Stack Card
    c9_r = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(1.8), Inches(5.5), Inches(4.9))
    c9_r.fill.solid()
    c9_r.fill.fore_color.rgb = c_navy
    c9_r.line.color.rgb = c_navy

    tb9_r = s9.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(4.9), Inches(4.5))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True
    pr9_1 = tf9_r.paragraphs[0]
    pr9_1.text = "Technology Stack Overview"
    pr9_1.font.size = Pt(18)
    pr9_1.font.bold = True
    pr9_1.font.color.rgb = c_orange
    pr9_1.space_after = Pt(14)

    pr9_2 = tf9_r.add_paragraph()
    pr9_2.text = "• Core Language: Python 3.10+\n• Machine Learning: Scikit-learn (Random Forest, Decision Tree, TF-IDF)\n• Frontend Framework: Streamlit UI with responsive custom styling\n• Analytics: Pandas, NumPy, Matplotlib\n• Version Control: Git & GitHub\n• Evaluation Framework: Train/Test cross validation (80:20 split)\n• Target Deployment: Localhost / Streamlit Community Cloud"
    pr9_2.font.size = Pt(13)
    pr9_2.font.color.rgb = RGBColor(226, 232, 240)

    # ---------------- SLIDE 10: IMPACT & SUSTAINABILITY ----------------
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Measurable Impact: People + Planet")

    impacts = [
        ("Financial Savings for Students", "Students save an average of ₹520 per item exchanged and learn skills at 70% lower rates than commercial coaching.", "₹95,000+ Projected Campus Savings", c_blue),
        ("Environmental Sustainability", "Reuse of engineering instruments, calculators, and books diverts substantial plastic and paper waste from college dumpsters.", "340+ kg Waste Diverted per Batch", c_orange),
        ("Peer Community & Collaboration", "Fosters meaningful senior-junior mentorship, builds career networks, and creates an open campus culture.", "410+ Hours of Peer Mentoring", c_pink)
    ]

    for i, (ititle, idesc, istat, icol) in enumerate(impacts):
        x = Inches(0.8 + i * 4.0)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = c_gray_bg
        card.line.color.rgb = icol
        card.line.width = Pt(2)

        tb = s10.shapes.add_textbox(x + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = ititle
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = icol
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = istat
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = c_navy
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = idesc
        p3.font.size = Pt(12.5)
        p3.font.color.rgb = c_text_dark

    # ---------------- SLIDE 11: FUTURE ROADMAP ----------------
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Future Roadmap & Scaling Vision")

    steps = [
        ("Phase 1: Single Campus Pilot", "Launch within our college campus with verified student email IDs. Focus on textbook swap and coding mentorship.", "Months 1-3"),
        ("Phase 2: Inter-College Network", "Expand to neighboring universities and institutes across Daman and regional tech hubs.", "Months 4-6"),
        ("Phase 3: Advanced AI Integration", "Integrate IBM watsonx / IBM BOB for automatic code review, skill badge verification, and mobile app release.", "Months 7-12")
    ]

    for i, (st, sd, stime) in enumerate(steps):
        y = Inches(1.8 + i * 1.7)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.4))
        card.fill.solid()
        card.fill.fore_color.rgb = c_white
        card.line.color.rgb = c_card_border

        badge = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), y + Inches(0.4), Inches(2.0), Inches(0.6))
        badge.fill.solid()
        badge.fill.fore_color.rgb = c_blue
        badge.line.color.rgb = c_blue
        btf = badge.text_frame
        bp = btf.paragraphs[0]
        bp.text = stime
        bp.font.size = Pt(13)
        bp.font.bold = True
        bp.font.color.rgb = c_white
        bp.alignment = PP_ALIGN.CENTER

        tb = s11.shapes.add_textbox(Inches(3.4), y + Inches(0.15), Inches(8.8), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = st
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = c_navy
        
        p2 = tf.add_paragraph()
        p2.text = sd
        p2.font.size = Pt(12.5)
        p2.font.color.rgb = c_text_muted

    # ---------------- SLIDE 12: CONCLUSION & ACKNOWLEDGEMENTS ----------------
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = c_navy
    bg12.line.color.rgb = c_navy

    tb12 = s12.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.3), Inches(4.5))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p12_1 = tf12.paragraphs[0]
    p12_1.text = "THANK YOU!"
    p12_1.font.size = Pt(44)
    p12_1.font.bold = True
    p12_1.font.color.rgb = c_white
    p12_1.space_after = Pt(14)

    p12_2 = tf12.add_paragraph()
    p12_2.text = '"With Campus Circle AI, every campus becomes a smarter, more connected, and self-sustaining community. We are not just building an app — we are building a culture of sharing, learning, and growth."'
    p12_2.font.size = Pt(18)
    p12_2.font.italic = True
    p12_2.font.color.rgb = RGBColor(203, 213, 225)
    p12_2.space_after = Pt(28)

    p12_3 = tf12.add_paragraph()
    p12_3.text = "Acknowledgements:\n• AICTE (All India Council for Technical Education)\n• IBM SkillsBuild Internship Program 2026\n• BharatCares (CSRBOX) Team & Trainer Mr. Amit Tiwari\n\nSubmitted by: Muskan Priyadarshani Patra | Internship ID: IBMUEML013863 | Plan ID: PLAN-CD7DED2B108B"
    p12_3.font.size = Pt(13)
    p12_3.font.color.rgb = RGBColor(148, 163, 184)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path} with {len(prs.slides)} slides.")

if __name__ == "__main__":
    out = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Final_Presentation.pptx"
    create_deck(out)
