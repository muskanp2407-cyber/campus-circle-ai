import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_lean_canvas(output_path):
    # Landscape A4 is 841.89 x 595.27 points
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=20,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=18,
        textColor=colors.HexColor('#0F172A')
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor('#64748B')
    )

    box_title_style = ParagraphStyle(
        'BoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=3
    )

    box_content_style = ParagraphStyle(
        'BoxContent',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.5,
        textColor=colors.HexColor('#334155')
    )

    subbox_title_style = ParagraphStyle(
        'SubBoxTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor('#0F766E'),
        spaceBefore=4,
        spaceAfter=2
    )

    elements = []

    # Header section
    header_html = """
    <b>CAMPUS CIRCLE AI — LEAN CANVAS</b> 
    <font size="9" color="#2563EB">| AICTE - IBM SkillsBuild Machine Learning & Applied AI Internship 2026 | BharatCares</font><br/>
    <font size="7.5" color="#64748B"><b>Author:</b> Muskan Priyadarshani Patra (IBMUEML013863 | PLAN-CD7DED2B108B) | <b>SDG Alignment:</b> SDG 4 (Quality Education) & SDG 8 (Decent Work) | <b>Date:</b> October 2026</font>
    """
    elements.append(Paragraph(header_html, title_style))
    elements.append(Spacer(1, 8))

    # Grid Dimensions (Total width ~800 points, total height ~480 points)
    # Col widths: 5 columns = [160, 160, 160, 160, 160]
    col_w = 801.89 / 5.0

    # 1. Box content strings
    p_problem = Paragraph("""
    <b>1. PROBLEM</b><br/>
    • Students waste money buying new books, lab drafters, & calculators used for only 1 semester.<br/>
    • Costly, impersonal online courses fail to provide syllabus-matched practical coding/lab tutoring.<br/>
    • Unorganized, unsafe WhatsApp groups with zero accountability.<br/>
    <br/>
    <b>EXISTING ALTERNATIVES</b><br/>
    • Unverified WhatsApp/Telegram groups<br/>
    • OLX / generic marketplaces (no campus trust)<br/>
    • Expensive commercial EdTech platforms
    """, box_content_style)

    p_solution = Paragraph("""
    <b>4. SOLUTION</b><br/>
    • <b>AI Peer Skill Hub:</b> Semantic matching connects learners with senior mentors for micro-learning.<br/>
    • <b>Campus Circular Marketplace:</b> Verified student buy/sell/swap for lab tools & textbooks.<br/>
    • <b>ML Fair-Price Valuation:</b> Transparent AI price calculation to eliminate negotiation disputes.
    """, box_content_style)

    p_uvp = Paragraph("""
    <b>3. UNIQUE VALUE PROPOSITION</b><br/>
    <b>"One platform. Two solutions. For every student."</b><br/>
    Connects peer learning and circular equipment exchange inside the campus with verified college trust.<br/>
    <br/>
    <b>HIGH-LEVEL CONCEPT</b><br/>
    "LinkedIn + Coursera + Circular Swaps — Exclusively verified for University Campuses."
    """, box_content_style)

    p_unfair_adv = Paragraph("""
    <b>9. UNFAIR ADVANTAGE</b><br/>
    • Closed-loop institutional email verification (.edu / @college.ac.in).<br/>
    • Direct syllabus alignment with campus exam & lab requirements.<br/>
    • Zero shipping overhead (hand-to-hand campus handoffs).
    """, box_content_style)

    p_customer_segments = Paragraph("""
    <b>2. CUSTOMER SEGMENTS</b><br/>
    • <b>Primary:</b> Undergraduate students in engineering, science & management residing in hostels & campus.<br/>
    • <b>Secondary:</b> Student mentors, campus tech club leads, and faculty.<br/>
    <br/>
    <b>EARLY ADOPTERS</b><br/>
    • 1st & 2nd year students needing lab equipment & coding guidance from seniors.
    """, box_content_style)

    p_key_metrics = Paragraph("""
    <b>8. KEY METRICS</b><br/>
    • Monthly Active Campus Users (MAU)<br/>
    • Successful resource swaps & items listed<br/>
    • Peer tutoring hours completed & rating avg<br/>
    • Total student rupees saved (INR) & kg waste diverted
    """, box_content_style)

    p_channels = Paragraph("""
    <b>5. CHANNELS</b><br/>
    • Campus orientation sessions & student council<br/>
    • College WhatsApp/Discord communities<br/>
    • Campus posters & QR code flyers in labs/hostels<br/>
    • Word of mouth & peer referral rewards
    """, box_content_style)

    p_cost_structure = Paragraph("""
    <b>7. COST STRUCTURE</b><br/>
    • Cloud hosting & database infrastructure (AWS/Vercel/Heroku): <b>Low fixed cost</b><br/>
    • Campus domain verification & security API tokens: <b>Variable</b><br/>
    • Offline campus marketing, banners & sticker promotional packs.<br/>
    • Ongoing platform maintenance & open-source ML model retraining.
    """, box_content_style)

    p_revenue_streams = Paragraph("""
    <b>6. REVENUE STREAMS</b><br/>
    • <b>Skill Tutoring Commission:</b> 5%–10% platform facilitation on paid senior-junior masterclasses (free swaps remain 100% free).<br/>
    • <b>Promoted Campus Listings:</b> Small Rs. 10–20 fee for urgent sale banner placements.<br/>
    • <b>Campus Vendor Partnerships:</b> Exclusive student discount sponsorships from local bookstores & printing shops.
    """, box_content_style)

    # Table layout:
    # Row 0: Top row of 5 boxes (Problem, Solution, UVP, Unfair Adv, Customer Segments)
    # Row 1: Middle split (Problem continues / Key Metrics, UVP continues, Channels, Cust Segments continues)
    # Row 2: Bottom row (Cost Structure spanning 2.5 cols, Revenue Streams spanning 2.5 cols)

    table_data = [
        [p_problem, p_solution, p_uvp, p_unfair_adv, p_customer_segments],
        ['', p_key_metrics, '', p_channels, ''],
        [p_cost_structure, '', '', p_revenue_streams, '']
    ]

    # Grid styling
    t_style = TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        
        # Spanning for row 0 & 1:
        # Col 0 (Problem) spans row 0 to 1
        ('SPAN', (0,0), (0,1)),
        # Col 2 (UVP) spans row 0 to 1
        ('SPAN', (2,0), (2,1)),
        # Col 4 (Customer Segments) spans row 0 to 1
        ('SPAN', (4,0), (4,1)),
        
        # Spanning for row 2 (Bottom):
        # Cost structure spans col 0, 1, and part of 2 (first 2 or 3 cols)
        ('SPAN', (0,2), (2,2)),
        # Revenue streams spans col 3 and 4
        ('SPAN', (3,2), (4,2)),
        
        ('BACKGROUND', (0,2), (2,2), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (3,2), (4,2), colors.HexColor('#F8FAFC')),
    ])

    # Row heights: Top = 230, Mid = 120, Bot = 140 -> Total = 490 pt
    t = Table(table_data, colWidths=[col_w]*5, rowHeights=[220, 120, 130])
    t.setStyle(t_style)
    elements.append(t)

    doc.build(elements)
    print(f"Lean Canvas PDF created successfully at {output_path}")

if __name__ == "__main__":
    out = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Lean_Canvas.pdf"
    create_lean_canvas(out)
