import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_screenshots_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=14
    )

    elements = []

    # Title & Metadata
    elements.append(Paragraph("PROJECT SCREENSHOTS & PROOF OF IMPLEMENTATION", ParagraphStyle('TopTag', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#EA580C'), leading=11)))
    elements.append(Paragraph("CAMPUS CIRCLE AI", title_style))
    elements.append(Paragraph("AICTE | IBM SkillsBuild Machine Learning & Applied AI Internship 2026 | BharatCares", sub_style))
    elements.append(Paragraph("<b>Student:</b> Muskan Priyadarshani Patra | <b>Plan ID:</b> PLAN-CD7DED2B108B | <b>Domain:</b> Applied AI / ML", sub_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceBefore=6, spaceAfter=12))

    screens = [
        (
            "1. Dashboard & SDG Impact Overview",
            "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/screenshots/1_dashboard_impact.png",
            "Figure 1: Live Campus Circle AI dashboard displaying real-time SDG impact metrics (Student Money Saved, Peer Skill Hours Taught, Resources Diverted, Active Campus Users) and core mission highlights."
        ),
        (
            "2. AI Peer Skill Matcher (SDG 4: Quality Education)",
            "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/screenshots/2_skill_matcher.png",
            "Figure 2: Semantic NLP Recommender system using TF-IDF and Cosine Similarity to pair learners with senior peer mentors based on natural language skill requests."
        ),
        (
            "3. Supervised Fair-Price ML Predictor (SDG 8 & 12)",
            "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/screenshots/3_fair_price_predictor.png",
            "Figure 3: Supervised regression engine (Random Forest & Decision Tree) predicting fair secondhand prices, depreciation percentage, and direct student savings."
        ),
        (
            "4. Machine Learning Architecture & Performance Metrics",
            "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/screenshots/4_ml_architecture.png",
            "Figure 4: Model evaluation metrics displaying Random Forest R² score of 95.27%, MAE of Rs. 68.23, and comparison against the baseline Decision Tree regressor."
        )
    ]

    for title, img_path, caption in screens:
        if os.path.exists(img_path):
            elements.append(Paragraph(title, h2_style))
            # Width = 525 pt, maintain aspect ratio
            img = Image(img_path, width=520, height=270)
            elements.append(img)
            elements.append(Paragraph(caption, caption_style))
            elements.append(Spacer(1, 8))

    doc.build(elements)
    print(f"Screenshots PDF generated successfully at {output_path}")

if __name__ == "__main__":
    out = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Screenshots.pdf"
    create_screenshots_pdf(out)
