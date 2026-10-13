import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from ml_models import FairPricePredictor, SkillMatcher, calculate_sdg_impact

# ----------------- PAGE CONFIGURATION -----------------
st.set_page_config(
    page_title="Campus Circle AI - Student Exchange & Skill Network",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS DESIGN SYSTEM -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF5E62, #FF9966, #6A11CB, #2575FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #475569;
        font-size: 1.05rem;
        font-weight: 500;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.03);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.6px;
    }
    .sdg-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        color: white;
        margin-right: 4px;
    }
    .sdg-4 { background-color: #C5192D; }
    .sdg-8 { background-color: #A21942; }
    .sdg-12 { background-color: #BF8B2E; }
    
    .card-box {
        background: white;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .card-box:hover {
        border-color: #6366f1;
        box-shadow: 0 6px 20px rgba(99,102,241,0.1);
    }
    .tag-pill {
        display: inline-block;
        background: #f1f5f9;
        color: #334155;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 12px;
        margin-right: 6px;
    }
    .tag-pro {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
    }
    .tag-verified {
        background: #ecfdf5;
        color: #059669;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        border: 1px solid #a7f3d0;
    }
    .chat-bubble-user {
        background: #e0e7ff;
        color: #1e1b4b;
        padding: 10px 14px;
        border-radius: 14px 14px 2px 14px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        text-align: right;
        font-size: 0.92rem;
    }
    .chat-bubble-other {
        background: #f1f5f9;
        color: #0f172a;
        padding: 10px 14px;
        border-radius: 14px 14px 14px 2px;
        margin: 6px auto 6px 0;
        max-width: 80%;
        text-align: left;
        font-size: 0.92rem;
        border-left: 3px solid #6366f1;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- INITIALIZE SESSION STATE -----------------
if "student_user" not in st.session_state:
    st.session_state["student_user"] = {
        "name": "Muskan Priyadarshani Patra",
        "email": "muskan.patra@kiit.ac.in",
        "branch": "Computer Science & Engineering",
        "semester": 6,
        "roll_no": "2105128",
        "verified": True,
        "eco_credits": 320,
        "is_pro": False
    }

if "marketplace_items" not in st.session_state:
    st.session_state["marketplace_items"] = [
        {
            "id": "ITM-101",
            "name": "Casio fx-991EX ClassWiz Scientific Calculator",
            "category": "Calculators",
            "mrp": 1400.0,
            "fair_price": 950.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Rohan Joshi",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.j@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Mint condition, original solar dual-power with battery. Box included."
        },
        {
            "id": "ITM-102",
            "name": "Higher Engineering Mathematics by B.S. Grewal (44th Edition)",
            "category": "Textbooks",
            "mrp": 850.0,
            "fair_price": 420.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Clean pages, formula sheet intact. Essential for Sem 1 to 4 syllabus."
        },
        {
            "id": "ITM-103",
            "name": "Omega Steel Mini Drafter & Engineering Sheet Holder",
            "category": "Engineering Drawing",
            "mrp": 950.0,
            "fair_price": 520.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Sneha Patel",
            "seller_branch": "Civil Engineering",
            "seller_email": "sneha.p@kiit.ac.in",
            "allow_swap": False,
            "status": "Available",
            "description": "Unbreakable steel arm. Calibrated scales for ED sheets."
        },
        {
            "id": "ITM-104",
            "name": "Arduino Uno R3 Starter Kit + Sensor Bundle + Breadboard",
            "category": "Electronics Kit",
            "mrp": 1850.0,
            "fair_price": 1100.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Vikram Singh",
            "seller_branch": "Electronics & Communication",
            "seller_email": "vikram.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Complete sensor kit with ultrasonic, DHT11, servo motor, and jumper wires."
        },
        {
            "id": "ITM-105",
            "name": "College Chemistry Lab Apron (Pure White Cotton - Size M)",
            "category": "College Uniform/Coat",
            "mrp": 550.0,
            "fair_price": 280.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Priya Sen",
            "seller_branch": "Biotechnology",
            "seller_email": "priya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Washed, no acid stains. Double pocket with embroidered college emblem."
        },
        {
            "id": "ITM-106",
            "name": "GATE CSE 2026 Made Easy Theory Notes & Formula Flashcards",
            "category": "Textbooks",
            "mrp": 1200.0,
            "fair_price": 600.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Handwritten crisp summary notes covering OS, DBMS, TOC, and Algorithms."
        }
    ]

if "session_bookings" not in st.session_state:
    st.session_state["session_bookings"] = [
        {
            "booking_id": "BK-7021",
            "mentor_name": "Aarav Sharma",
            "topic": "Python & Scikit-Learn Model Building",
            "date": str(datetime.date.today() + datetime.timedelta(days=1)),
            "time_slot": "04:30 PM - 05:30 PM",
            "mode": "Campus Central Library (Room 204)",
            "status": "Confirmed ✅",
            "fee": "FREE (Skill Swap)"
        }
    ]

if "chat_channels" not in st.session_state:
    st.session_state["chat_channels"] = {
        "Aarav Sharma (Python Mentor)": [
            {"sender": "other", "text": "Hi Muskan! Looking forward to our peer ML session tomorrow."},
            {"sender": "user", "text": "Hi Aarav, thanks! I have prepared questions on TF-IDF and Decision Trees."},
            {"sender": "other", "text": "Perfect! We will cover practical scikit-learn coding together at the library."}
        ],
        "Rohan Joshi (Casio Calculator Seller)": [
            {"sender": "other", "text": "Hey! Yes, the fx-991EX calculator is available."},
            {"sender": "user", "text": "Great! Can we inspect it today at the Student Cafeteria?"},
            {"sender": "other", "text": "Sure, I will be there around 3:30 PM after my fluid mechanics lab."}
        ],
        "Campus Circle AI Bot": [
            {"sender": "other", "text": "Hello! I am your Campus Circle AI Assistant. How can I help you navigate campus resource swaps or find mentors today?"}
        ]
    }

if "reviews" not in st.session_state:
    st.session_state["reviews"] = [
        {
            "reviewer": "Tushar M.",
            "target": "Aarav Sharma (Peer Mentor)",
            "rating": 5,
            "category": "Peer Mentoring",
            "date": "2026-10-10",
            "comment": "Explained DSA and recursion concepts 10x better than YouTube tutorials. Saved me before the mid-term exams!"
        },
        {
            "reviewer": "Pooja Roy",
            "target": "Rohan Joshi (Calculators)",
            "rating": 5,
            "category": "Item Purchase",
            "date": "2026-10-11",
            "comment": "Casio calculator was in mint condition. Fair price predictor matched the exact reasonable college rate."
        },
        {
            "reviewer": "Deepak K.",
            "target": "Sneha Mukherjee (UI/UX Design)",
            "rating": 4,
            "category": "Skill Barter",
            "date": "2026-10-12",
            "comment": "Great mutual swap! She taught me Figma components and I helped her debug her React state hooks."
        }
    ]

# ----------------- LOAD ML MODELS -----------------
@st.cache_resource
def load_models():
    fp = FairPricePredictor()
    sm = SkillMatcher()
    return fp, sm

fair_price_model, skill_matcher_model = load_models()

# ----------------- SIDEBAR NAVIGATION -----------------
logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.title("🎓 Campus Circle AI")

# Student Profile Mini Banner in Sidebar
u = st.session_state["student_user"]
st.sidebar.markdown(f"""
<div style="background:white; border-radius:10px; border:1px solid #cbd5e1; padding:12px; margin-bottom:12px;">
    <div style="font-weight:700; color:#0f172a; font-size:0.95rem;">👤 {u['name']}</div>
    <div style="font-size:0.8rem; color:#64748b;">{u['branch']} (Sem {u['semester']})</div>
    <div style="margin-top:6px; display:flex; gap:6px; align-items:center;">
        <span class="{'tag-verified' if u['verified'] else 'tag-pill'}">{'✅ ID Verified' if u['verified'] else '⚠️ Unverified'}</span>
        <span class="{'tag-pro' if u['is_pro'] else 'tag-pill'}">{'🏆 Campus Pro' if u['is_pro'] else 'Free Tier'}</span>
    </div>
    <div style="font-size:0.78rem; color:#059669; margin-top:6px; font-weight:600;">🌱 {u['eco_credits']} Eco-Karma Points</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "All 10 Proposed Project Features:",
    [
        "📊 1. Overview & SDG Impact Dashboard",
        "🔐 2. Student Registration & Email Verification (Features 1 & 2)",
        "🛒 3. Campus Marketplace — Buy, Sell & Swap (Features 3 & 4)",
        "🧠 4. Skill Hub & AI Skill Discovery (Features 5 & 6)",
        "📅 5. 1-on-1 Session Booking (Feature 7)",
        "💬 6. In-App Campus Chat (Feature 8)",
        "⭐ 7. Ratings & Student Reviews (Feature 9)",
        "💰 8. Revenue Model & Economics (Feature 10)",
        "📈 9. ML Architecture & Performance"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("AICTE | IBM SkillsBuild Applied AI Internship 2026\nBharatCares (CSRBOX)")

# ----------------- HEADER BANNER -----------------
col_h1, col_h2 = st.columns([4, 1.2])
with col_h1:
    st.markdown('<div class="main-title">CAMPUS CIRCLE AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Student Skill Exchange, Circular Resource Network & Fair Valuation Engine</div>', unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style="padding-top: 8px; text-align:right;">
        <span class="sdg-badge sdg-4">SDG 4: Quality Edu</span><br style="line-height:20px;">
        <span class="sdg-badge sdg-8">SDG 8: Decent Work</span><br style="line-height:20px;">
        <span class="sdg-badge sdg-12">SDG 12: Circular Economy</span>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: OVERVIEW & SDG IMPACT DASHBOARD
# ==============================================================================
if menu == "📊 1. Overview & SDG Impact Dashboard":
    st.markdown("### 🌍 Real-Time Campus Impact & Circular Economy Overview")
    st.write("Campus Circle AI empowers students to eliminate educational waste, combat exorbitant resource costs, and bridge skill gaps through an institutional peer network.")

    impact = calculate_sdg_impact(total_swaps=184, avg_saving_per_item=520, skill_hours=410)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Student Money Saved</div>
            <div class="metric-val">₹{impact['total_monetary_saved_inr']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Peer Skill Hours Taught</div>
            <div class="metric-val">{impact['peer_skill_hours']} hrs</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Plastic & Paper Saved</div>
            <div class="metric-val">{impact['waste_diverted_kg']} kg</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Active Campus Students</div>
            <div class="metric-val">{impact['active_students']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    col_prob, col_sol = st.columns(2)
    with col_prob:
        st.markdown("""
        #### 🛑 Critical Campus Problems Solved
        * **Expensive Educational Equipment**: Calculators, mini-drafters, lab coats, and engineering textbooks are purchased at 100% MRP, used for one semester, and discarded.
        * **Impersonal & Costly EdTech**: Generic tutorials don't match college syllabus or university lab exam patterns.
        * **Chaos & Fraud in WhatsApp Groups**: Campus trading in informal chats lacks price transparency, identity verification, and accountability.
        """)
    with col_sol:
        st.markdown("""
        #### 💡 The Campus Circle AI Solution
        * **Verified Campus Graph**: Authentication restricted to verified college institutional domains (`.ac.in` / `.edu`).
        * **Supervised ML Regressor**: Random Forest and Decision Tree models predict transparent, non-exploitative fair prices.
        * **AI Two-Way Skill Barter**: NLP Content-based TF-IDF recommender enabling 100% free peer mentoring via mutual skill swaps.
        """)

# ==============================================================================
# MODULE 2: STUDENT REGISTRATION & EMAIL VERIFICATION (FEATURES 1 & 2)
# ==============================================================================
elif menu == "🔐 2. Student Registration & Email Verification (Features 1 & 2)":
    st.markdown("### 🔐 Feature 1 & 2: Student Registration & Institutional Email Verification")
    st.write("Ensure a trusted, safe campus environment by authenticating student accounts with verified institutional domain emails.")

    tab_profile, tab_register = st.tabs(["👤 My Student Profile & Identity", "📝 Register / Update Account"])

    with tab_profile:
        col_id, col_ver = st.columns([1.5, 1])
        with col_id:
            u = st.session_state["student_user"]
            st.markdown(f"""
            <div class="card-box" style="border-left: 6px solid #6366f1;">
                <h3 style="margin:0 0 10px 0; color:#1e293b;">🎓 Institutional Student Card</h3>
                <p style="margin:4px 0;"><strong>Full Name:</strong> {u['name']}</p>
                <p style="margin:4px 0;"><strong>College Email:</strong> <code>{u['email']}</code></p>
                <p style="margin:4px 0;"><strong>Roll Number:</strong> {u['roll_no']}</p>
                <p style="margin:4px 0;"><strong>Department:</strong> {u['branch']}</p>
                <p style="margin:4px 0;"><strong>Current Semester:</strong> Semester {u['semester']}</p>
                <p style="margin:4px 0;"><strong>Membership Tier:</strong> {'🏆 Campus Pro' if u['is_pro'] else 'Free Basic Student'}</p>
                <div style="margin-top:12px;">
                    <span class="{'tag-verified' if u['verified'] else 'tag-pill'}">
                        {'✅ Institutional Email Verified' if u['verified'] else '⚠️ Email Verification Pending'}
                    </span>
                    <span class="tag-pill">🌱 {u['eco_credits']} Eco-Karma Credits</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_ver:
            st.markdown("#### 📧 College Email Verification Portal")
            if u['verified']:
                st.success(f"✅ Your institutional email (`{u['email']}`) is fully verified! You have complete access to the Marketplace, Skill Hub, and Session Bookings.")
                if st.button("Simulate Re-verification"):
                    st.session_state["student_user"]["verified"] = False
                    st.rerun()
            else:
                st.warning("⚠️ Your email is currently unverified. Please verify with your college email ending in `.edu` or `.ac.in`.")
                demo_otp = "8492"
                st.info(f"💡 Demo Institutional Mail System: A 4-digit OTP has been sent to `{u['email']}`: **{demo_otp}**")
                entered_otp = st.text_input("Enter 4-Digit OTP", max_chars=4, placeholder="e.g. 8492")
                if st.button("Verify OTP & Activate Badge", type="primary"):
                    if entered_otp == demo_otp:
                        st.session_state["student_user"]["verified"] = True
                        st.session_state["student_user"]["eco_credits"] += 50
                        st.balloons()
                        st.success("🎉 Email Verified Successfully! +50 Eco-Karma Credits awarded!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Please enter 8492 for the simulation.")

    with tab_register:
        st.markdown("#### 📝 Register a New Student / Edit Information")
        with st.form("student_registration_form"):
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                r_name = st.text_input("Full Name", value=st.session_state["student_user"]["name"])
                r_email = st.text_input("Institutional Email (.ac.in / .edu)", value=st.session_state["student_user"]["email"])
                r_roll = st.text_input("University Roll / Enrollment No.", value=st.session_state["student_user"]["roll_no"])
            with c_f2:
                r_branch = st.selectbox(
                    "Branch / Department",
                    [
                        "Computer Science & Engineering",
                        "Information Technology",
                        "Electronics & Communication",
                        "Mechanical Engineering",
                        "Civil Engineering",
                        "Electrical Engineering",
                        "Biotechnology",
                        "Business Administration / MBA"
                    ],
                    index=0
                )
                r_sem = st.slider("Current Semester", min_value=1, max_value=8, value=int(st.session_state["student_user"]["semester"]))

            submit_reg = st.form_submit_button("Save & Update Profile", type="primary")
            if submit_reg:
                is_valid_domain = any(domain in r_email.lower() for domain in [".ac.in", ".edu", "college", "univ"])
                st.session_state["student_user"].update({
                    "name": r_name,
                    "email": r_email,
                    "roll_no": r_roll,
                    "branch": r_branch,
                    "semester": r_sem,
                    "verified": is_valid_domain
                })
                st.success("✅ Profile updated successfully!")
                if not is_valid_domain:
                    st.warning("⚠️ Note: Your email did not contain `.ac.in` or `.edu`. Please use your official college domain for full verification.")
                st.rerun()

# ==============================================================================
# MODULE 3: CAMPUS MARKETPLACE — BUY, SELL & SWAP (FEATURES 3 & 4)
# ==============================================================================
elif menu == "🛒 3. Campus Marketplace — Buy, Sell & Swap (Features 3 & 4)":
    st.markdown("### 🛒 Feature 3 & 4: Campus Marketplace & Supervised ML Fair-Price Engine")
    st.write("Browse secondhand educational tools, purchase directly from verified seniors, or list your items with instant **Random Forest Fair-Price Valuation**.")

    tab_browse, tab_sell = st.tabs(["🛍️ Browse, Buy & Swap Items (Feature 3 & 4)", "🏷️ Sell / List Item with ML Valuation Engine"])

    with tab_browse:
        f_col1, f_col2, f_col3 = st.columns([2, 1.5, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search items by title or keywords...", placeholder="e.g. Casio, Grewal, Drafter, Arduino")
        with f_col2:
            cat_filter = st.selectbox("Filter Category", ["All Categories"] + fair_price_model.categories)
        with f_col3:
            swap_only = st.checkbox("🔄 Swap Available Only", value=False)

        # Filter items
        filtered = st.session_state["marketplace_items"]
        if search_query:
            filtered = [i for i in filtered if search_query.lower() in i["name"].lower() or search_query.lower() in i["description"].lower()]
        if cat_filter != "All Categories":
            filtered = [i for i in filtered if i["category"] == cat_filter]
        if swap_only:
            filtered = [i for i in filtered if i["allow_swap"]]

        st.caption(f"Showing **{len(filtered)} items** available on campus.")

        # Display Grid
        for idx in range(0, len(filtered), 2):
            g_col1, g_col2 = st.columns(2)
            cols = [g_col1, g_col2]
            for j in range(2):
                if idx + j < len(filtered):
                    item = filtered[idx + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="card-box">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <h4 style="margin:0 0 4px 0; color:#1e293b;">{item['name']}</h4>
                                <span style="background:#ecfdf5; color:#047857; font-weight:800; font-size:1.1rem; padding:4px 10px; border-radius:8px;">
                                    ₹{int(item['fair_price'])}
                                </span>
                            </div>
                            <div style="margin-bottom:8px;">
                                <span class="tag-pill">{item['category']}</span>
                                <span class="tag-pill">⭐ {item['condition']}/5 Condition</span>
                                <span class="tag-pill">Used {item['age_sem']} Semesters</span>
                                {'<span class="tag-pill" style="background:#fef3c7; color:#b45309; font-weight:700;">🔄 Swap Eligible</span>' if item['allow_swap'] else ''}
                            </div>
                            <p style="font-size:0.86rem; color:#475569; margin:6px 0;">{item['description']}</p>
                            <p style="font-size:0.8rem; color:#64748b; margin:4px 0;">
                                <strong>Seller:</strong> {item['seller_name']} ({item['seller_branch']}) | Original MRP: <del>₹{int(item['mrp'])}</del>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        c_btn1, c_btn2 = st.columns(2)
                        with c_btn1:
                            if st.button(f"🛒 Buy for ₹{int(item['fair_price'])}", key=f"buy_{item['id']}"):
                                st.session_state["student_user"]["eco_credits"] += 20
                                st.success(f"🎉 Order Confirmed for {item['name']}! Meet seller {item['seller_name']} at Central Library. +20 Eco-Credits awarded!")
                        with c_btn2:
                            if item['allow_swap']:
                                if st.button(f"🔄 Propose Swap", key=f"swap_{item['id']}"):
                                    st.info(f"📩 Swap request sent to {item['seller_name']} (`{item['seller_email']}`). Check In-App Chat to finalize trade!")

    with tab_sell:
        st.markdown("#### 🏷️ List an Item with ML-Assisted Fair Pricing")
        st.write("Our **Random Forest Regression model ($R^2 = 0.952$)** calculates fair market valuation to eliminate seller-buyer price disputes.")

        c_s1, c_s2 = st.columns(2)
        with c_s1:
            n_title = st.text_input("Item Title", placeholder="e.g. Casio Scientific Calculator fx-82MS")
            n_cat = st.selectbox("Category", fair_price_model.categories)
            n_mrp = st.number_input("Original Retail MRP (₹)", min_value=100.0, max_value=25000.0, value=1200.0, step=50.0)
            n_desc = st.text_area("Item Description / Notes", placeholder="e.g. Barely used during 2nd sem physics lab. No scratches.")
        with c_s2:
            n_age = st.slider("Item Age (in Semesters used)", min_value=1, max_value=8, value=2)
            n_cond = st.slider("Physical Condition (1 = Heavy Wear, 5 = Like New)", min_value=1, max_value=5, value=4)
            n_demand = st.slider("Campus Exam Demand Index", min_value=0.5, max_value=1.0, value=0.85, step=0.05)
            n_swap = st.checkbox("Allow Skill / Item Swap for this item", value=True)

        pred_res = fair_price_model.predict(n_cat, n_mrp, n_age, n_cond, n_demand)

        # Valuation Cards
        v1, v2, v3 = st.columns(3)
        with v1:
            st.metric("Suggested Fair Price", f"₹{pred_res['suggested_fair_price']}", delta=f"-{pred_res['depreciation_percent']}% Depreciation")
        with v2:
            st.metric("Buyer Savings", f"₹{pred_res['student_saving_inr']}", "vs Purchasing New")
        with v3:
            st.metric("Decision Tree Baseline", f"₹{pred_res['decision_tree_estimate']}")

        # Feature Importance / Price Breakdown
        st.markdown("##### 🔍 Explainable AI (XAI): Price Depreciation Breakdown")
        breakdown = fair_price_model.explain_prediction(n_mrp, n_age, n_cond, n_demand, pred_res['suggested_fair_price'])
        
        b_df = pd.DataFrame(list(breakdown.items()), columns=["Factor", "Amount (₹)"])
        fig_xai, ax_xai = plt.subplots(figsize=(6, 2.4))
        colors = ['#3b82f6', '#ef4444', '#f97316', '#10b981', '#6366f1']
        ax_xai.barh(b_df["Factor"], b_df["Amount (₹)"], color=colors, height=0.45)
        ax_xai.set_title("Machine Learning Depreciation Factor Attribution", fontsize=10)
        ax_xai.set_xlabel("Value in INR (₹)")
        st.pyplot(fig_xai)

        if st.button("🚀 Publish Item to Live Marketplace", type="primary"):
            if not n_title.strip():
                st.error("Please enter an item title before publishing.")
            else:
                new_item = {
                    "id": f"ITM-{len(st.session_state['marketplace_items']) + 101}",
                    "name": n_title,
                    "category": n_cat,
                    "mrp": float(n_mrp),
                    "fair_price": float(pred_res['suggested_fair_price']),
                    "age_sem": int(n_age),
                    "condition": int(n_cond),
                    "seller_name": st.session_state["student_user"]["name"],
                    "seller_branch": st.session_state["student_user"]["branch"],
                    "seller_email": st.session_state["student_user"]["email"],
                    "allow_swap": n_swap,
                    "status": "Available",
                    "description": n_desc if n_desc.strip() else "Verified student listing."
                }
                st.session_state["marketplace_items"].insert(0, new_item)
                st.session_state["student_user"]["eco_credits"] += 30
                st.success(f"🎉 Item '{n_title}' listed live on the marketplace at ₹{pred_res['suggested_fair_price']}! Check the 'Browse' tab to view it.")

# ==============================================================================
# MODULE 4: SKILL HUB & AI SKILL DISCOVERY (FEATURES 5 & 6)
# ==============================================================================
elif menu == "🧠 4. Skill Hub & AI Skill Discovery (Features 5 & 6)":
    st.markdown("### 🧠 Feature 5 & 6: Campus Skill Hub & AI Two-Way Skill Barter")
    st.write("Connect with campus seniors who took the exact same courses. Find 100% free peer mentoring via mutual skill swaps powered by **TF-IDF & Cosine Similarity**.")

    tab_disc, tab_dir, tab_reg_mentor = st.tabs([
        "🔍 AI Skill Discovery & 2-Way Barter (Feature 6)",
        "👥 Campus Mentors Directory (Feature 5)",
        "➕ Register as Peer Mentor (Feature 5)"
    ])

    with tab_disc:
        st.markdown("#### 🎯 AI Peer Skill Matcher with Mutual Barter Matching")
        c_in1, c_in2 = st.columns(2)
        with c_in1:
            want_to_learn = st.text_input(
                "1. What skill or subject do you want to learn?",
                value="I want to learn Python programming, Machine Learning, and Scikit-learn algorithms."
            )
        with c_in2:
            can_teach = st.text_input(
                "2. What skill can you teach in exchange? (Optional for 0-Cost Barter)",
                value="UI/UX Design, Figma wireframing, and Public Speaking"
            )

        top_k = st.slider("Number of mentor recommendations", min_value=2, max_value=6, value=3)

        if st.button("🔍 Run AI Semantic Matching", type="primary"):
            matches = skill_matcher_model.find_two_way_barter(want_to_learn, can_teach, top_k=top_k)

            st.success(f"Matched {len(matches)} peer mentors based on TF-IDF semantic similarity!")

            for m in matches:
                is_barter = m.get("is_mutual_barter", False)
                fee_badge = "FREE (Mutual Skill Barter 🔄)" if is_barter or m['hourly_fee_inr'] == 0 else f"₹{m['hourly_fee_inr']}/hr"
                
                st.markdown(f"""
                <div class="card-box" style="{'border: 2px solid #10b981;' if is_barter else ''}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="margin:0; color:#1e293b;">{m['name']} ({m['mentor_id']})</h4>
                        <div>
                            {f'<span class="tag-pill" style="background:#ecfdf5; color:#047857; font-weight:700;">🎉 2-Way Barter Match ({m.get("barter_score_pct", 0)}%)</span>' if is_barter else ''}
                            <span style="background:#e0e7ff; color:#4338ca; padding:4px 10px; border-radius:12px; font-weight:700; font-size:0.85rem;">
                                ⚡ {m['match_score_pct']}% Learn Match
                            </span>
                        </div>
                    </div>
                    <p style="margin:4px 0; color:#64748b; font-size:0.88rem;">
                        <strong>Branch:</strong> {m['branch']} | <strong>Semester:</strong> {m['semester']} | <strong>Rating:</strong> ⭐ {m['rating']}/5.0 ({m['total_sessions']} sessions)
                    </p>
                    <p style="margin:6px 0; font-size:0.92rem;"><strong>Skills Offered:</strong> <span style="color:#0f766e;">{m['skills_offered']}</span></p>
                    <p style="margin:4px 0; font-size:0.92rem;"><strong>Skills Wanted:</strong> <span style="color:#b45309;">{m['skills_wanted']}</span></p>
                    <p style="margin:4px 0; font-size:0.85rem; color:#475569;"><em>"{m['bio']}"</em></p>
                    <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:700; color:#b45309; font-size:0.95rem;">Fee: {fee_badge}</span>
                        <span style="font-size:0.8rem; color:#059669; font-weight:600;">✅ Campus ID Verified</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_dir:
        st.markdown("#### 👥 All Verified Campus Peer Mentors")
        all_mentors = skill_matcher_model.get_all_mentors()
        for mentor in all_mentors:
            st.markdown(f"""
            <div class="card-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h5 style="margin:0; color:#1e293b;">{mentor['name']} — {mentor['branch']} (Sem {mentor['semester']})</h5>
                    <span style="color:#f59e0b; font-weight:700;">⭐ {mentor['rating']} / 5.0</span>
                </div>
                <p style="margin:4px 0; font-size:0.88rem;"><strong>Offers:</strong> {mentor['skills_offered']}</p>
                <p style="margin:4px 0; font-size:0.88rem;"><strong>Seeking:</strong> {mentor['skills_wanted']}</p>
                <div style="margin-top:8px;">
                    <span class="tag-pill">{f'₹{mentor['hourly_fee_inr']}/hr' if mentor['hourly_fee_inr'] > 0 else 'Free Barter'}</span>
                    <span class="tag-verified">Verified Senior</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_reg_mentor:
        st.markdown("#### ➕ Register as a Peer Mentor in Campus Circle")
        with st.form("mentor_reg_form"):
            m_skills_offered = st.text_input("Skills You Can Teach", placeholder="e.g. C++, Object Oriented Programming, DSA")
            m_skills_wanted = st.text_input("Skills You Want to Learn (for Barter)", placeholder="e.g. Cloud Computing, AWS, UI/UX")
            m_fee = st.number_input("Hourly Fee (₹) [Set 0 for Free Peer Barter]", min_value=0, max_value=500, value=0, step=25)
            m_bio = st.text_area("Short Bio & Academic Experience", placeholder="e.g. 3rd year CSE student, scored 9.4 SGPA in DSA. Ready to help juniors.")
            m_submit = st.form_submit_button("Join Mentor Network", type="primary")

            if m_submit:
                if not m_skills_offered.strip():
                    st.error("Please enter at least one skill you can teach.")
                else:
                    new_mentor = {
                        "mentor_id": f"MNT-{len(skill_matcher_model.df) + 101}",
                        "name": st.session_state["student_user"]["name"],
                        "branch": st.session_state["student_user"]["branch"],
                        "semester": st.session_state["student_user"]["semester"],
                        "skills_offered": m_skills_offered,
                        "skills_wanted": m_skills_wanted if m_skills_wanted.strip() else "None (Paid/Volunteer)",
                        "experience_years": 1.5,
                        "hourly_fee_inr": m_fee,
                        "rating": 5.0,
                        "total_sessions": 0,
                        "bio": m_bio if m_bio.strip() else "Verified peer tutor.",
                        "verified": True
                    }
                    skill_matcher_model.add_mentor(new_mentor)
                    st.session_state["student_user"]["eco_credits"] += 40
                    st.success("🎉 You are now registered as a campus peer mentor! +40 Eco-Credits awarded!")

# ==============================================================================
# MODULE 5: 1-ON-1 SESSION BOOKING (FEATURE 7)
# ==============================================================================
elif menu == "📅 5. 1-on-1 Session Booking (Feature 7)":
    st.markdown("### 📅 Feature 7: Peer Mentoring Session Booking Portal")
    st.write("Schedule 1-on-1 tutoring or skill-swap sessions with campus seniors at verified locations or online.")

    tab_book, tab_my_sessions = st.tabs(["🗓️ Schedule a New Session", "📋 My Booked Sessions"])

    with tab_book:
        mentors = skill_matcher_model.get_all_mentors()
        mentor_names = [f"{m['name']} ({m['branch']}) - Fee: ₹{m['hourly_fee_inr']}" for m in mentors]

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            selected_mentor_str = st.selectbox("Select Peer Mentor", mentor_names)
            session_topic = st.text_input("Specific Topic / Chapter to Cover", placeholder="e.g. Dynamic Programming & Recursion")
            session_date = st.date_input("Preferred Date", min_value=datetime.date.today(), value=datetime.date.today() + datetime.timedelta(days=1))
        with col_b2:
            session_slot = st.selectbox(
                "Time Slot",
                [
                    "03:30 PM - 04:30 PM",
                    "04:30 PM - 05:30 PM",
                    "05:30 PM - 06:30 PM",
                    "07:00 PM - 08:00 PM (Hostel / Online)"
                ]
            )
            session_mode = st.selectbox(
                "Meeting Mode / Location",
                [
                    "Campus Central Library (2nd Floor Discussion Pod)",
                    "Student Activity Centre (SAC Room 102)",
                    "Campus Cafeteria Corner",
                    "Online (Google Meet / Microsoft Teams)"
                ]
            )
            notes_for_mentor = st.text_input("Notes / Doubts for Mentor", placeholder="e.g. Please bring notes for syllabus unit 3")

        if st.button("✅ Confirm & Book Session", type="primary"):
            mentor_clean_name = selected_mentor_str.split(" (")[0]
            booking_code = f"BK-{np.random.randint(1000, 9999)}"
            new_booking = {
                "booking_id": booking_code,
                "mentor_name": mentor_clean_name,
                "topic": session_topic if session_topic.strip() else "General Peer Mentoring",
                "date": str(session_date),
                "time_slot": session_slot,
                "mode": session_mode,
                "status": "Confirmed ✅",
                "fee": "FREE (Skill Swap)"
            }
            st.session_state["session_bookings"].insert(0, new_booking)
            st.session_state["student_user"]["eco_credits"] += 25
            st.balloons()
            st.success(f"🎉 Session Successfully Booked with **{mentor_clean_name}**! Booking ID: **{booking_code}**. +25 Eco-Credits awarded!")

    with tab_my_sessions:
        st.markdown("#### 📋 My Active Mentoring Sessions")
        for b in st.session_state["session_bookings"]:
            st.markdown(f"""
            <div class="card-box" style="border-left: 5px solid #10b981;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#1e293b;">{b['topic']} — with {b['mentor_name']}</h4>
                    <span class="tag-verified">{b['status']}</span>
                </div>
                <p style="margin:6px 0; color:#475569; font-size:0.9rem;">
                    <strong>Date:</strong> {b['date']} | <strong>Time:</strong> {b['time_slot']} | <strong>Booking Ref:</strong> <code>{b['booking_id']}</code>
                </p>
                <p style="margin:4px 0; color:#334155; font-size:0.88rem;"><strong>Location:</strong> {b['mode']}</p>
                <p style="margin:4px 0; color:#b45309; font-weight:700; font-size:0.85rem;">Fee Terms: {b['fee']}</p>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# MODULE 6: IN-APP CAMPUS CHAT (FEATURE 8)
# ==============================================================================
elif menu == "💬 6. In-App Campus Chat (Feature 8)":
    st.markdown("### 💬 Feature 8: In-App Campus Messaging & Conversation Hub")
    st.write("Communicate directly with buyers, sellers, peer mentors, or the AI Assistant in a secured college network.")

    channel_list = list(st.session_state["chat_channels"].keys())
    active_channel = st.selectbox("Select Active Conversation Channel:", channel_list)

    st.markdown(f"#### Conversation with: **{active_channel}**")
    chat_container = st.container()

    with chat_container:
        msgs = st.session_state["chat_channels"][active_channel]
        for m in msgs:
            if m["sender"] == "user":
                st.markdown(f'<div class="chat-bubble-user"><strong>You:</strong><br>{m["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-other"><strong>{active_channel.split(" (")[0]}:</strong><br>{m["text"]}</div>', unsafe_allow_html=True)

    with st.form("chat_input_form", clear_on_submit=True):
        col_msg, col_snd = st.columns([4, 1])
        with col_msg:
            user_text = st.text_input("Type your message here...", placeholder="e.g. Is the item available? Can we meet at the library?", label_visibility="collapsed")
        with col_snd:
            send_btn = st.form_submit_button("Send 📤", type="primary")

        if send_btn and user_text.strip():
            # Append user message
            st.session_state["chat_channels"][active_channel].append({"sender": "user", "text": user_text})

            # Automated peer reply or AI reply
            if "AI Bot" in active_channel:
                q = user_text.lower()
                if "sdg" in q:
                    bot_reply = "Campus Circle AI supports **SDG 4 (Quality Education)** via peer mentoring, **SDG 8 (Decent Work)** via practical skills, and **SDG 12 (Responsible Consumption)** through circular reuse!"
                elif "price" in q or "fair" in q or "cost" in q:
                    bot_reply = "Our Fair-Price Predictor uses a **Random Forest Regressor (95.2% R²)** that factors in MRP, age, and condition to prevent price gouging."
                elif "barter" in q or "swap" in q:
                    bot_reply = "You can use the AI Skill Matcher to perform a 2-way barter: enter what you want to learn AND what you can teach to unlock 0-rupee tutoring!"
                else:
                    bot_reply = f"Thanks for asking about '{user_text}'! Campus Circle AI facilitates verified campus peer learning and circular equipment exchange."
                st.session_state["chat_channels"][active_channel].append({"sender": "other", "text": bot_reply})
            else:
                peer_name = active_channel.split(" (")[0]
                auto_reply = f"Hey Muskan! Got your message: '{user_text}'. That works for me, let's meet up at the designated campus spot."
                st.session_state["chat_channels"][active_channel].append({"sender": "other", "text": auto_reply})

            st.rerun()

# ==============================================================================
# MODULE 7: RATINGS & STUDENT REVIEWS (FEATURE 9)
# ==============================================================================
elif menu == "⭐ 7. Ratings & Student Reviews (Feature 9)":
    st.markdown("### ⭐ Feature 9: Peer Accountability, Ratings & Verified Reviews")
    st.write("Transparent student ratings ensure high mentoring quality and honest secondhand item descriptions.")

    tab_view_rev, tab_submit_rev = st.tabs(["🌟 Verified Campus Feedback Feed", "✍️ Submit a Rating & Review"])

    with tab_view_rev:
        st.markdown("#### 🌟 Recent Verified Campus Reviews")
        for r in st.session_state["reviews"]:
            stars_display = "⭐" * r["rating"]
            st.markdown(f"""
            <div class="card-box">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#1e293b;">{r['target']}</h4>
                    <span style="color:#f59e0b; font-size:1.1rem; font-weight:700;">{stars_display} ({r['rating']}/5)</span>
                </div>
                <div style="margin:4px 0;">
                    <span class="tag-pill">{r['category']}</span>
                    <span class="tag-verified">Verified Transaction</span>
                    <span style="font-size:0.8rem; color:#64748b;">Reviewed on {r['date']} by <strong>{r['reviewer']}</strong></span>
                </div>
                <p style="margin:8px 0 0 0; color:#334155; font-size:0.92rem;"><em>"{r['comment']}"</em></p>
            </div>
            """, unsafe_allow_html=True)

    with tab_submit_rev:
        st.markdown("#### ✍️ Rate a Peer Mentor or Item Seller")
        with st.form("review_form"):
            targets = [
                "Aarav Sharma (Python Peer Mentor)",
                "Priya Patel (Web Dev Mentor)",
                "Rohan Joshi (Casio Calculator Seller)",
                "Sneha Patel (Engineering Mini Drafter)",
                "Vikram Singh (Arduino Sensor Kit)"
            ]
            r_target = st.selectbox("Select Student to Review", targets)
            r_cat = st.selectbox("Interaction Category", ["Peer Mentoring", "Item Purchase", "Skill Barter", "Item Swap"])
            r_stars = st.slider("Rating (1 to 5 Stars)", min_value=1, max_value=5, value=5)
            r_comment = st.text_area("Your Review & Feedback", placeholder="e.g. Very patient tutor, cleared my doubt on recursion within 30 minutes!")
            
            sub_rev = st.form_submit_button("Post Verified Review", type="primary")
            if sub_rev:
                if not r_comment.strip():
                    st.error("Please provide review text.")
                else:
                    new_r = {
                        "reviewer": st.session_state["student_user"]["name"],
                        "target": r_target,
                        "rating": r_stars,
                        "category": r_cat,
                        "date": str(datetime.date.today()),
                        "comment": r_comment
                    }
                    st.session_state["reviews"].insert(0, new_r)
                    st.session_state["student_user"]["eco_credits"] += 15
                    st.success("🎉 Thank you! Your review has been added to the campus trust graph! +15 Eco-Credits awarded!")

# ==============================================================================
# MODULE 8: REVENUE MODEL & ECONOMICS (FEATURE 10)
# ==============================================================================
elif menu == "💰 8. Revenue Model & Economics (Feature 10)":
    st.markdown("### 💰 Feature 10: Platform Revenue Model & Campus Economics")
    st.write("Campus Circle AI employs a **sustainable, zero-exploitation freemium model** designed specifically for university students.")

    rev_col1, rev_col2 = st.columns([1.5, 1])

    with rev_col1:
        st.markdown("#### 🏛️ Three Core Monetization Streams")
        st.markdown("""
        <div class="card-box">
            <h4 style="margin:0 0 6px 0; color:#1e293b;">1. 🏆 Campus Pro Student Membership (₹49 / Semester)</h4>
            <p style="font-size:0.88rem; color:#475569; margin:0;">
                Students unlock unlimited priority listing badges, verified star on profile, zero convenience fees on paid item sales, and priority search visibility for peer tutoring.
            </p>
        </div>
        <div class="card-box">
            <h4 style="margin:0 0 6px 0; color:#1e293b;">2. 🏷️ 2% Micro-Platform Fee on High-Value Equipment</h4>
            <p style="font-size:0.88rem; color:#475569; margin:0;">
                Free basic students pay a minimal 2% convenience fee on items sold above ₹500 (e.g. ₹10 on a ₹500 drafter). <strong>100% Free on all Skill Swaps & Resource Barters.</strong>
            </p>
        </div>
        <div class="card-box">
            <h4 style="margin:0 0 6px 0; color:#1e293b;">3. 🏢 Institutional Partnerships & Sustainable Brand Deals</h4>
            <p style="font-size:0.88rem; color:#475569; margin:0;">
                Colleges license the verified campus graph to track institutional ESG / SDG compliance scores for NAAC and NIRF accreditation rankings.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with rev_col2:
        st.markdown("#### 🌟 Upgrade Account")
        is_pro = st.session_state["student_user"]["is_pro"]
        if is_pro:
            st.success("🏆 You are an active **Campus Pro Member**! Enjoy zero platform fees and priority search rankings.")
            if st.button("Downgrade to Free Tier"):
                st.session_state["student_user"]["is_pro"] = False
                st.rerun()
        else:
            st.markdown("""
            <div class="card-box" style="border: 2px solid #f59e0b; background:#fffbeb;">
                <h4 style="margin:0; color:#b45309;">Campus Pro Membership</h4>
                <p style="font-size:1.5rem; font-weight:800; color:#b45309; margin:6px 0;">₹49 <span style="font-size:0.85rem; font-weight:500;">/ semester</span></p>
                <ul style="font-size:0.85rem; color:#78350f; padding-left:18px;">
                    <li>Zero commission on all sales</li>
                    <li>Golden Verified Senior Badge</li>
                    <li>Top-of-search Mentor Placement</li>
                    <li>Priority Item Barter Alerts</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ Upgrade to Campus Pro (₹49)", type="primary"):
                st.session_state["student_user"]["is_pro"] = True
                st.balloons()
                st.success("🎉 Welcome to Campus Pro!")
                st.rerun()

    st.markdown("---")
    st.markdown("#### 📊 Interactive Campus Financial & Sustainability Simulator")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        camp_students = st.slider("Total Campus Students", min_value=1000, max_value=20000, value=6000, step=500)
    with s_col2:
        pro_rate = st.slider("Campus Pro Adoption Rate (%)", min_value=2, max_value=25, value=10)
    with s_col3:
        avg_items_per_stu = st.slider("Avg Resource Swaps per Student/Year", min_value=1, max_value=6, value=3)

    pro_subscribers = int(camp_students * (pro_rate / 100))
    pro_revenue = pro_subscribers * 49 * 2 # 2 semesters
    total_trades = camp_students * avg_items_per_stu
    commission_rev = int(total_trades * 0.4 * 600 * 0.02) # 40% cash items at avg 600 with 2% fee
    total_rev = pro_revenue + commission_rev
    total_savings = int(total_trades * 480) # avg 480 saved per swap

    sim1, sim2, sim3 = st.columns(3)
    sim1.metric("Projected Platform Revenue", f"₹{total_rev:,} / yr", f"₹{pro_revenue:,} from Pro Tier")
    sim2.metric("Total Student Body Savings", f"₹{total_savings:,} / yr", f"{total_savings // total_rev if total_rev > 0 else 0}x ROI for Students")
    sim3.metric("Waste Diverted from Landfills", f"{int(total_trades * 1.85):,} kg", "Circular SDG 12 Impact")

# ==============================================================================
# MODULE 9: ML ARCHITECTURE & PERFORMANCE
# ==============================================================================
elif menu == "📈 9. ML Architecture & Performance":
    st.markdown("### 📈 Machine Learning Architecture & Evaluation Metrics")
    st.write("Technical implementation directly reflects the curriculum of the **IBM SkillsBuild Machine Learning Masterclasses**.")

    m = fair_price_model.metrics
    c_m1, c_m2, c_m3 = st.columns(3)
    c_m1.metric("Random Forest R² Score", f"{m['RandomForest_R2'] * 100:.1f}%", "Ensemble Regressor")
    c_m2.metric("Random Forest MAE", f"₹{m['RandomForest_MAE']}", "Mean Absolute Error")
    c_m3.metric("Decision Tree Baseline R²", f"{m['DecisionTree_R2'] * 100:.1f}%", "Masterclass 3 Benchmark")

    st.markdown("#### Supervised Regression Model Comparison")
    fig, ax = plt.subplots(figsize=(7, 2.8))
    models = ['Decision Tree (Baseline)', 'Random Forest (Ensemble)']
    r2_vals = [m['DecisionTree_R2'], m['RandomForest_R2']]
    colors = ['#f59e0b', '#10b981']
    bars = ax.barh(models, r2_vals, color=colors, height=0.45)
    ax.set_xlim(0.8, 1.0)
    ax.set_xlabel('R² Goodness of Fit Score')
    ax.set_title('Supervised Regression Accuracy on Campus Exchange Pricing')
    for bar in bars:
        ax.text(bar.get_width() - 0.04, bar.get_y() + 0.15, f"{bar.get_width():.3f}", color='white', fontweight='bold')
    st.pyplot(fig)

    st.markdown("""
    #### 🛠️ Masterclass Alignment Summary
    * **Masterclass 1 & 2**: Exploratory Data Analysis (EDA) on student living expenses, data cleaning, and one-hot encoding.
    * **Masterclass 3**: Supervised Learning (Decision Trees & Random Forest Regression) for objective fair price valuation.
    * **Masterclass 4**: Unsupervised / Content-Based Recommendation using **TF-IDF Vectorization** and **Cosine Similarity** for two-way skill barter.
    * **Masterclass 5**: Model deployment, Streamlit application architecture, and UN SDG alignment.
    """)
