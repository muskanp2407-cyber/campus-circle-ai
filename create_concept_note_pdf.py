import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_concept_note(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1E293B')
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("PROJECT CONCEPT NOTE", ParagraphStyle('TopTag', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#EA580C'), leading=12)))
    elements.append(Paragraph("CAMPUS CIRCLE AI", title_style))
    elements.append(Paragraph("Smart Student Skill Exchange & Circular Campus Resource Network", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Program:</b> AICTE | IBM SkillsBuild Internship 2026<br/><b>Organizing Partner:</b> BharatCares (CSRBOX)<br/><b>Domain:</b> Machine Learning & Applied AI", meta_style),
            Paragraph("<b>Author / Intern:</b> Muskan Priyadarshani Patra<br/><b>Internship ID:</b> IBMUEML013863 | <b>Plan ID:</b> PLAN-CD7DED2B108B<br/><b>SDG Focus:</b> SDG 4 (Education) & SDG 8 (Decent Work)", meta_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[260, 255])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 10))

    # Section 1: Executive Summary
    elements.append(Paragraph("1. Executive Summary", h1_style))
    elements.append(Paragraph(
        "<b>Campus Circle AI</b> is an applied Artificial Intelligence and Machine Learning platform engineered to address two systemic challenges across higher education campuses: (1) the financial strain and material waste caused by single-semester physical educational resources, and (2) the accessibility barrier to syllabus-aligned, affordable skill learning. Aligned with <b>UN Sustainable Development Goals (SDG 4, SDG 8, and SDG 12)</b>, Campus Circle AI fuses a <b>Content-Based Skill Recommender System</b> (using TF-IDF vectorization and Cosine Similarity) with a <b>Supervised Fair-Price Machine Learning Regressor</b> (using Random Forest and Decision Tree models) into a unified, verified campus network.",
        body_style
    ))

    # Section 2: Problem Statement
    elements.append(Paragraph("2. Problem Statement & Campus Need", h1_style))
    elements.append(Paragraph(
        "In Indian collegiate ecosystems, university students face three critical hurdles every academic cycle:",
        body_style
    ))
    elements.append(Paragraph("• <b>Resource Waste & High Costs:</b> Academic materials such as engineering drafters, lab aprons, scientific calculators, and reference textbooks are purchased at full retail prices (MRP) but discarded or left idle after a single semester. Junior students in subsequent batches struggle with these recurring expenses.", bullet_style))
    elements.append(Paragraph("• <b>Inaccessible, Impersonal Skill Learning:</b> Students seeking practical industry skills (Python, CAD, Web Development, DSA) often face expensive commercial EdTech courses that lack alignment with college syllabi and internal practical exams.", bullet_style))
    elements.append(Paragraph("• <b>Trust Deficit & Informal Chaos:</b> Present student exchanges rely on unmonitored WhatsApp groups and generic classifieds, which are prone to spam, lack verified campus identity, and suffer from volatile price disputes.", bullet_style))

    # Section 3: UN SDG Alignment
    elements.append(Paragraph("3. UN Sustainable Development Goals (SDG) Alignment", h1_style))
    sdg_table_data = [
        [
            Paragraph("<b>SDG Goal</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white)),
            Paragraph("<b>Target & Direct Relevance to Campus Circle AI</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white))
        ],
        [
            Paragraph("<b>SDG 4:<br/>Quality Education</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#C5192D'))),
            Paragraph("<b>Target 4.4:</b> Democratizes practical technical & vocational skills through peer-to-peer micro-learning. Juniors learn syllabus-matched programming and lab skills directly from experienced seniors at negligible or zero cost (via skill swapping).", body_style)
        ],
        [
            Paragraph("<b>SDG 8:<br/>Decent Work & Economic Growth</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#A21942'))),
            Paragraph("<b>Target 8.6:</b> Prepares students for technical interviews and professional roles by building verified portfolios. Senior mentors gain recognized leadership experience and micro-earning opportunities on campus.", body_style)
        ],
        [
            Paragraph("<b>SDG 12:<br/>Responsible Consumption</b>", ParagraphStyle('TB', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#BF8B2E'))),
            Paragraph("<b>Target 12.5:</b> Establishes a circular campus equipment lifecycle, substantially diverting textbook, calculator, and plastic drafting hardware waste from college landfills through verified peer reuse.", body_style)
        ]
    ]
    t_sdg = Table(sdg_table_data, colWidths=[120, 395])
    t_sdg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_sdg)
    elements.append(Spacer(1, 8))

    # Section 4: Machine Learning Engine
    elements.append(Paragraph("4. Technical Machine Learning Methodology", h1_style))
    elements.append(Paragraph(
        "Directly implementing core competencies from the <b>IBM SkillsBuild Masterclass Series</b> (Masterclass 3: Supervised Learning & Decision Trees; Masterclass 4/5: Applied AI & Recommenders), Campus Circle AI features two algorithmic engines:",
        body_style
    ))
    elements.append(Paragraph("<b>A. Supervised Fair-Price Valuation Regressor (Masterclass 3 Alignment):</b>", body_style))
    elements.append(Paragraph(
        "To eliminate price disputes between student buyers and sellers, we engineered a multi-feature regression model predicting fair depreciated valuation. Features include: (1) <i>Original Retail Price (MRP)</i>, (2) <i>Age in Semesters (1–8)</i>, (3) <i>Condition Rating (1–5 scale)</i>, (4) <i>Category Encoding</i>, and (5) <i>Campus Demand Index</i>. Trained on 300 campus transactions with an 80:20 train/test split, the <b>Random Forest Regressor</b> achieved an <b>R² accuracy of 0.9527</b> (MAE = Rs. 68.23), benchmarked against a <b>Decision Tree Regressor</b> (R² = 0.9133).",
        body_style
    ))

    elements.append(Paragraph("<b>B. Natural Language Semantic Skill Matcher (Masterclass 4/5 Alignment):</b>", body_style))
    elements.append(Paragraph(
        "Rather than relying on rigid keyword lookups, the skill matcher utilizes <b>TF-IDF (Term Frequency-Inverse Document Frequency) N-gram Vectorization</b> coupled with <b>Cosine Similarity</b>. The system converts student natural language learning queries (e.g., <i>'Want to learn Python for data science and model building'</i>) into high-dimensional vector embeddings, measuring the angular similarity against all verified mentor profiles. It ranks mentors by compatibility percentage, highlighting shared interests and zero-cost swap opportunities.",
        body_style
    ))

    # Section 5: System Architecture & Implementation
    elements.append(Paragraph("5. System Implementation & Tech Stack", h1_style))
    elements.append(Paragraph("• <b>Machine Learning & Analytics:</b> Scikit-Learn (RandomForestRegressor, DecisionTreeRegressor, TfidfVectorizer, cosine_similarity), Pandas, NumPy.", bullet_style))
    elements.append(Paragraph("• <b>Interactive Web Interface:</b> Streamlit application with custom responsive CSS styling, real-time KPI metrics, and modular tabs.", bullet_style))
    elements.append(Paragraph("• <b>Conversational Assistant:</b> Integrated Campus Circle AI Agent providing context-aware guidance on learning roadmaps, fair pricing, and platform features.", bullet_style))
    elements.append(Paragraph("• <b>Verification Architecture:</b> Institutional email authentication domain gating ensuring safety and campus accountability.", bullet_style))

    # Section 6: Lean Canvas Highlights
    elements.append(Paragraph("6. Lean Canvas Summary & Business Model", h1_style))
    elements.append(Paragraph("• <b>Unique Value Proposition (UVP):</b> 'One platform. Two solutions. For every student.' Seamlessly unifies peer skill development and secondhand circular exchanges.", bullet_style))
    elements.append(Paragraph("• <b>Unfair Advantage:</b> Closed-loop campus trust backed by institutional email IDs, zero delivery/shipping costs, and hyper-localized syllabus relevance.", bullet_style))
    elements.append(Paragraph("• <b>Revenue Model:</b> 100% free for peer-to-peer swaps; nominal 5%–10% commission on premium paid tutoring sessions; small listing fee (Rs. 10–20) for urgent marketplace banners.", bullet_style))
    elements.append(Paragraph("• <b>Cost Structure:</b> Minimal cloud hosting (Streamlit Community / AWS), low maintenance overhead, and student ambassador marketing.", bullet_style))

    # Section 7: Expected Impact & Metrics
    elements.append(Paragraph("7. Projected Campus Impact & Key Metrics", h1_style))
    elements.append(Paragraph("• <b>Economic Savings:</b> Projected average saving of Rs. 520 per item per student, generating over Rs. 95,000+ in aggregate student savings per semester.", bullet_style))
    elements.append(Paragraph("• <b>Environmental Sustainability:</b> Prevents over 340+ kg of plastic instruments, lab tools, and textbook paper from entering university landfills annually.", bullet_style))
    elements.append(Paragraph("• <b>Peer Educational Hours:</b> Facilitates 400+ hours of localized peer tutoring per semester, boosting practical coding and lab proficiency.", bullet_style))

    # Section 8: Conclusion
    elements.append(Paragraph("8. Conclusion", h1_style))
    elements.append(Paragraph(
        "Campus Circle AI demonstrates how applied machine learning can solve grounded, real-world community problems. By replacing fragmented, inefficient campus exchanges with an intelligent, trustworthy, and sustainable platform, Campus Circle AI fulfills the vision of the <b>IBM SkillsBuild and AICTE</b> applied AI curriculum.",
        body_style
    ))

    doc.build(elements)
    print(f"Concept Note PDF generated successfully at {output_path}")

if __name__ == "__main__":
    out = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Concept_Note.pdf"
    create_concept_note(out)
