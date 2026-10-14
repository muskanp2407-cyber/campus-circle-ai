import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_lean_canvas(output_paths):
    # A4 Landscape: 841.89 x 595.27 points
    # Printable width: 841.89 - 48 = 793.89 pt
    # Total margins: 24 pt left/right, 18 pt top/bottom
    doc_margin = 24
    total_w = 841.89 - (2 * doc_margin) # 793.89 pt

    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=22,
        textColor=colors.HexColor('#0F172A')
    )

    # Metadata styles
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#475569')
    )
    meta_val_style = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0F172A')
    )

    # Box Headers
    header_style = ParagraphStyle(
        'BoxHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=1
    )

    header_hint_style = ParagraphStyle(
        'BoxHint',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=6.2,
        leading=7.8,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=3
    )

    # Content text
    body_style = ParagraphStyle(
        'BoxBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.6,
        leading=8.6,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=2
    )

    body_bold_style = ParagraphStyle(
        'BoxBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.6,
        leading=8.6,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=2
    )

    footer_style = ParagraphStyle(
        'FooterText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=8.0,
        textColor=colors.HexColor('#64748B')
    )

    # Helper function to create a boxed cell with title, hint, and content
    def make_box(title, hint, content_html, padding_bottom=2):
        text = f"<b>{title}</b><br/><font size='6.0' color='#64748B'><i>{hint}</i></font><br/>{content_html}"
        return Paragraph(text, body_style)

    # =========================================================================
    # 1. HEADER SECTION
    # =========================================================================
    p_title = Paragraph("<b>The Lean Canvas</b>", title_style)

    # Metadata table (Designed for, Designed by, Date, Version)
    meta_table_data = [
        [
            Paragraph("<b>Designed for:</b>", meta_label_style),
            Paragraph("<b>Campus Circle AI</b>", meta_val_style),
            Paragraph("<b>Designed by:</b>", meta_label_style),
            Paragraph("<b>Muskan Priyadarshani Patra</b>", meta_val_style),
            Paragraph("<b>Date:</b>", meta_label_style),
            Paragraph("14/10/2026", meta_val_style),
            Paragraph("<b>Version:</b>", meta_label_style),
            Paragraph("1.0", meta_val_style)
        ],
        [
            Paragraph("<b>Program:</b>", meta_label_style),
            Paragraph("AICTE | IBM SkillsBuild", meta_val_style),
            Paragraph("<b>Internship ID:</b>", meta_label_style),
            Paragraph("IBMUEML013863", meta_val_style),
            Paragraph("<b>Domain:</b>", meta_label_style),
            Paragraph("Applied AI & ML", meta_val_style),
            Paragraph("<b>Plan ID:</b>", meta_label_style),
            Paragraph("PLAN-CD7DED2B108B", meta_val_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[65, 95, 65, 125, 45, 55, 45, 75])
    t_meta.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))

    header_table = Table([[p_title, t_meta]], colWidths=[223.89, 570])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    # =========================================================================
    # 2. COLUMN DATA PREPARATION
    # =========================================================================
    # Width of each of the 5 main columns: 793.89 / 5 = 158.78 pt
    col_w = total_w / 5.0
    half_w = total_w / 2.0

    # Total height for top grid = 368 pt
    # Col 1: Problem (240 pt) + Existing Alternatives (128 pt) = 368 pt
    # Col 2: Solution (220 pt) + Key Metrics (148 pt) = 368 pt
    # Col 3: Unique Value Prop (265 pt) + High-Level Concept (103 pt) = 368 pt
    # Col 4: Unfair Advantage (184 pt) + Channels (184 pt) = 368 pt
    # Col 5: Customer Segments (240 pt) + Early Adopters (128 pt) = 368 pt
    # Bottom Row: Cost Structure (110 pt) + Revenue Streams (110 pt)

    # --- COLUMN 1: PROBLEM & EXISTING ALTERNATIVES ---
    c1_top = make_box(
        "Problem",
        "List your top 1-3 problems.",
        """
        <b>1. Single-Semester Asset Waste:</b> Engineering students (MECH, ELEC, CIVIL, CE, BIOMED) spend Rs. 6,000–Rs. 10,000 annually buying new lab kits, mini drafters, calculators, and reference textbooks that become idle after just 4 months of use.<br/>
        <b>2. Inaccessible Practical Mentoring:</b> Juniors lack 1-on-1 guidance for college lab exams, coding assignments, and viva questions. Costly commercial EdTech courses are generic and disconnected from university syllabi.<br/>
        <b>3. Chaotic & Unsafe Informal Trades:</b> Student trades rely on unmoderated WhatsApp/Telegram groups plagued by spam, persistent price haggling, absent safety, and identity fraud.
        """
    )
    c1_bot = make_box(
        "Existing Alternatives",
        "List how these problems are solved today.",
        """
        • <b>Unverified WhatsApp/Telegram groups:</b> Noisy, unorganized, zero campus verification.<br/>
        • <b>OLX / Generic Marketplaces:</b> No campus trust, high shipping fees, stranger risk.<br/>
        • <b>Commercial EdTech (Coursera/Udemy):</b> Expensive & detached from college practicals.<br/>
        • <b>Buying New at Full MRP:</b> High recurring burden on student/hostel budgets every semester.
        """
    )
    t_col1 = Table([[c1_top], [c1_bot]], colWidths=[col_w], rowHeights=[240, 128])
    t_col1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # --- COLUMN 2: SOLUTION & KEY METRICS ---
    c2_top = make_box(
        "Solution",
        "Outline a possible solution for each problem.",
        """
        <b>1. Circular Campus Marketplace:</b> Verified student buy, sell, and swap portal for textbooks, lab tools, and drafting kits with zero delivery fees via campus handoffs.<br/>
        <b>2. AI Peer Skill-Sharing Hub:</b> Semantic matching engine pairing juniors with experienced senior mentors for practical micro-learning and zero-cost skill swaps.<br/>
        <b>3. Supervised ML Fair-Price Valuation:</b> Automated depreciation pricing (Random Forest, R²=0.952) providing transparent pricing to eliminate bargaining disputes.<br/>
        <b>4. Institutional Domain Gating:</b> Access strictly restricted to verified @college.ac.in emails.
        """
    )
    c2_bot = make_box(
        "Key Metrics",
        "List the key numbers that tell you how your business is doing.",
        """
        • <b>Monthly Active Users (MAU) & Signups</b><br/>
        • <b>Total Student Rupees Saved (INR Rs.):</b> Target Rs. 95,000+ per campus/sem.<br/>
        • <b>Equipment Diverted from Landfills:</b> Target 340+ kg plastic/paper annually.<br/>
        • <b>Peer Tutoring Hours Completed:</b> 400+ hrs.<br/>
        • <b>Successful Swaps & Transaction Count</b><br/>
        • <b>Average Mentor Session Rating (out of 5.0)</b>
        """
    )
    t_col2 = Table([[c2_top], [c2_bot]], colWidths=[col_w], rowHeights=[220, 148])
    t_col2.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # --- COLUMN 3: UNIQUE VALUE PROP & HIGH-LEVEL CONCEPT ---
    c3_top = make_box(
        "Unique Value Prop.",
        "Single, clear, compelling message that states why you are different and worth paying attention.",
        """
        <b>“One platform. Two solutions. For every student.”</b><br/>
        <b>1. Unified Campus Ecosystem:</b> Seamlessly connects circular equipment exchange and peer skill development inside one verified college hub.<br/>
        <b>2. Algorithmic Fair Pricing:</b> AI-driven valuation trained on real student depreciation patterns removes pricing exploitation.<br/>
        <b>3. Zero Friction & Zero Waste:</b> Immediate on-campus handoffs with zero shipping fees, zero delivery delays, and zero packaging waste.<br/>
        <b>4. Hyper-Localized Syllabus Relevance:</b> Mentors and resources aligned with internal college exams, practicals, and professor assignments.<br/>
        <b>5. UN SDG Alignment:</b> Champions Quality Education (SDG 4), Decent Work (SDG 8), and Responsible Consumption (SDG 12).
        """
    )
    c3_bot = make_box(
        "High-Level Concept",
        "List your X for Y analogy, e.g. YouTube = Flickr for videos.",
        """
        <b>“LinkedIn + Coursera + Circular Swaps — Exclusively verified for University Campuses.”</b><br/>
        • Campus Circle = Circular Equipment Lifecycle + Peer Knowledge Exchange.<br/>
        • Micro-tutoring + verified second-life lab hardware network.
        """
    )
    t_col3 = Table([[c3_top], [c3_bot]], colWidths=[col_w], rowHeights=[265, 103])
    t_col3.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # --- COLUMN 4: UNFAIR ADVANTAGE & CHANNELS ---
    c4_top = make_box(
        "Unfair Advantage",
        "Something that cannot easily be bought or copied.",
        """
        <b>1. Closed-Loop Campus Trust:</b> Strict college institutional email domain verification (.edu / @college.ac.in) guarantees safety and accountability.<br/>
        <b>2. Hyper-Localized Academic Relevance:</b> Mentors and materials mapped directly to university course codes, labs, and faculty notes.<br/>
        <b>3. Proprietary Campus Pricing Engine:</b> Multi-feature ML regression trained on campus transaction history.<br/>
        <b>4. Zero Logistical Cost:</b> Zero shipping overhead through on-campus peer handoffs.
        """
    )
    c4_bot = make_box(
        "Channels",
        "List your path to customers (inbound or outbound).",
        """
        • <b>Campus Orientation & Freshers Induction:</b> Direct reach to incoming 1st-year students.<br/>
        • <b>Student Council & Tech Club Partnerships:</b> Coding clubs, robotics & design societies.<br/>
        • <b>College WhatsApp / Discord communities:</b> Direct student engagement & peer referrals.<br/>
        • <b>Physical QR Code Posters:</b> Labs, libraries, notice boards, and hostels.<br/>
        • <b>Campus Tech Fests & Hackathons:</b> Workshop sponsorships & live demo booths.
        """
    )
    t_col4 = Table([[c4_top], [c4_bot]], colWidths=[col_w], rowHeights=[184, 184])
    t_col4.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # --- COLUMN 5: CUSTOMER SEGMENTS & EARLY ADOPTERS ---
    c5_top = make_box(
        "Customer Segments",
        "List your target customers and users.",
        """
        <b>1. Undergraduate Students (Primary):</b> Hostelers, day-scholars & PG residents across 5 engineering disciplines (MECH, ELEC, CIVIL, CE, BIOMED) seeking affordable lab tools and textbooks.<br/>
        <b>2. Senior Student Mentors:</b> 3rd & 4th-year high-performing students wanting recognized leadership portfolios, teaching experience, and micro-income.<br/>
        <b>3. Campus Tech Clubs & Student Chapters:</b> IEEE, CSI, SAE seeking structured platforms for peer workshops.<br/>
        <b>4. University Administration:</b> Seeking quantifiable metrics for NIRF / NAAC Green Campus rankings.
        """
    )
    c5_bot = make_box(
        "Early Adopters",
        "List the characteristics of your ideal customers.",
        """
        • <b>1st & 2nd Year Juniors:</b> Urgent need for expensive lab tools (drafters, calculators, aprons, component kits) and introductory coding mentorship.<br/>
        • <b>Hostel Residents:</b> High density of shared living, peer networking, and immediate physical handoffs.<br/>
        • <b>Technical Society Leads:</b> Senior students passionate about sharing engineering design and coding skills.
        """
    )
    t_col5 = Table([[c5_top], [c5_bot]], colWidths=[col_w], rowHeights=[240, 128])
    t_col5.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('LINEBELOW', (0,0), (0,0), 0.75, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # Combine 5 columns into top main grid
    top_grid = Table([[t_col1, t_col2, t_col3, t_col4, t_col5]], colWidths=[col_w]*5)
    top_grid.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 0),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    # =========================================================================
    # 3. BOTTOM ROW: COST STRUCTURE & REVENUE STREAMS
    # =========================================================================
    c_cost = make_box(
        "Cost Structure",
        "List your fixed and variable costs.",
        """
        <b>1. Fixed Costs:</b><br/>
        • <b>Cloud Servers & Database:</b> AWS / Streamlit / Vercel hosting infrastructure.<br/>
        • <b>Domain & Security:</b> Annual domain registration, SSL certificates & code upkeep.<br/>
        • <b>ML Engine Maintenance:</b> Ongoing model retraining, Scikit-Learn pipeline updates.<br/>
        <b>2. Variable Costs:</b><br/>
        • <b>Campus Offline Marketing:</b> QR code flyers, lab posters, and hostel sticker packs.<br/>
        • <b>Student Ambassador Incentives:</b> Campus referral perks & ambassador starter kits.<br/>
        • <b>API Gateway Usage:</b> Email authentication tokens & college tech fest demo booths.
        """
    )

    c_rev = make_box(
        "Revenue Streams",
        "List your sources of revenue.",
        """
        • <b>Skill Tutoring Facilitation Fee:</b> Nominal 5%–10% platform commission on paid senior-junior masterclasses (skill swaps remain 100% free).<br/>
        • <b>Promoted Marketplace Listings:</b> Small Rs. 10–Rs. 20 micro-fee for featured urgent-sale banners on the homepage.<br/>
        • <b>Campus Vendor Partnerships:</b> Affiliate sponsorships from local academic bookstores & stationery shops.<br/>
        • <b>Institutional University SaaS (Future):</b> Annual campus subscription for universities to track verified sustainability & peer learning KPIs for NAAC/NIRF accreditation.
        """
    )

    bot_grid = Table([[c_cost, c_rev]], colWidths=[half_w, half_w], rowHeights=[108])
    bot_grid.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.HexColor('#0F172A')),
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))

    # =========================================================================
    # 4. FOOTER ATTRIBUTION SECTION
    # =========================================================================
    p_foot_left = Paragraph(
        "<b>Fill Order:</b> 1. Problem ➔ 2. Customer Segments ➔ 3. Unique Value Prop ➔ 4. Solution ➔ 5. Channels ➔ 6. Revenue Streams ➔ 7. Cost Structure ➔ 8. Key Metrics ➔ 9. Unfair Advantage",
        footer_style
    )
    p_foot_right = Paragraph(
        "Lean Canvas is adapted from The Business Model Canvas (www.businessmodelgeneration.com/canvas). Licensed under CC BY-SA 3.0",
        ParagraphStyle('FootR', parent=footer_style, alignment=2) # right align
    )
    footer_table = Table([[p_foot_left, p_foot_right]], colWidths=[493.89, 300])
    footer_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    # Build Elements list
    elements = [
        header_table,
        Spacer(1, 3),
        top_grid,
        bot_grid,
        Spacer(1, 2),
        footer_table
    ]

    for p in output_paths:
        doc = SimpleDocTemplate(
            p,
            pagesize=landscape(A4),
            leftMargin=doc_margin,
            rightMargin=doc_margin,
            topMargin=16,
            bottomMargin=14
        )
        doc.build(elements)
        print(f"Lean Canvas PDF created successfully at {p}")

if __name__ == "__main__":
    out1 = "c:/Users/User/Desktop/PAYAL IBM/Campus_Circle_AI_Lean_Canvas.pdf"
    out2 = "c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/Campus_Circle_AI_Lean_Canvas.pdf"
    create_lean_canvas([out1, out2])
