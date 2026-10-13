import pandas as pd
import numpy as np

# 1. Peer Mentors Dataset
mentors_data = [
    {
        "mentor_id": "MNT-101",
        "name": "Aarav Sharma",
        "branch": "Computer Engineering",
        "semester": 7,
        "skills_offered": "Python, Machine Learning, Data Science, Scikit-learn, Pandas",
        "skills_wanted": "UI/UX Design, Figma, Public Speaking",
        "experience_years": 2.5,
        "hourly_fee_inr": 0,  # Free peer swap
        "rating": 4.9,
        "total_sessions": 24,
        "bio": "Final year CSE student. IBM SkillsBuild certified in ML. Love teaching Python and model building to juniors.",
        "verified": True
    },
    {
        "mentor_id": "MNT-102",
        "name": "Priya Patel",
        "branch": "Information Technology",
        "semester": 5,
        "skills_offered": "Web Development, React.js, JavaScript, HTML/CSS, Tailwind",
        "skills_wanted": "Competitive Programming, C++",
        "experience_years": 1.5,
        "hourly_fee_inr": 99,
        "rating": 4.8,
        "total_sessions": 18,
        "bio": "Full-stack developer with 3 campus project deployments. Can guide you from zero to full responsive website.",
        "verified": True
    },
    {
        "mentor_id": "MNT-103",
        "name": "Rohan Deshmukh",
        "branch": "Mechanical Engineering",
        "semester": 6,
        "skills_offered": "CAD, AutoCAD, SolidWorks, 3D Modeling, Engineering Drawing",
        "skills_wanted": "Python, Excel Automation",
        "experience_years": 2.0,
        "hourly_fee_inr": 120,
        "rating": 4.7,
        "total_sessions": 15,
        "bio": "Mech 3rd year. Winner of Inter-college CAD design sprint. Practical mechanical drawing and 3D modeling tutor.",
        "verified": True
    },
    {
        "mentor_id": "MNT-104",
        "name": "Ananya Sen",
        "branch": "Computer Engineering",
        "semester": 7,
        "skills_offered": "Data Structures & Algorithms, C++, LeetCode Problem Solving, Java",
        "skills_wanted": "Machine Learning, Deep Learning",
        "experience_years": 3.0,
        "hourly_fee_inr": 150,
        "rating": 5.0,
        "total_sessions": 32,
        "bio": "Candidate Master on Codeforces, 500+ LeetCode solved. Specialized in technical interview prep and DSA.",
        "verified": True
    },
    {
        "mentor_id": "MNT-105",
        "name": "Vikram Singh",
        "branch": "Electronics & Communication",
        "semester": 5,
        "skills_offered": "Arduino, Embedded C, IoT, Circuit Design, Raspberry Pi",
        "skills_wanted": "Flutter, App Development",
        "experience_years": 1.8,
        "hourly_fee_inr": 0,
        "rating": 4.6,
        "total_sessions": 12,
        "bio": "Hardware and robotics enthusiast. Can help with lab practicals, microcontrollers, and IoT sensor circuits.",
        "verified": True
    },
    {
        "mentor_id": "MNT-106",
        "name": "Sneha Mukherjee",
        "branch": "Design & Humanities",
        "semester": 6,
        "skills_offered": "UI/UX Design, Figma, Adobe Illustrator, Canva, Graphic Design",
        "skills_wanted": "Web Development, React.js",
        "experience_years": 2.2,
        "hourly_fee_inr": 100,
        "rating": 4.9,
        "total_sessions": 27,
        "bio": "Design club lead. Specialized in creating wireframes, design systems, and product pitch decks.",
        "verified": True
    },
    {
        "mentor_id": "MNT-107",
        "name": "Kabir Verma",
        "branch": "Computer Science",
        "semester": 4,
        "skills_offered": "Database Systems, SQL, PostgreSQL, MongoDB, Backend APIs",
        "skills_wanted": "Cloud, AWS, Docker",
        "experience_years": 1.0,
        "hourly_fee_inr": 0,
        "rating": 4.5,
        "total_sessions": 9,
        "bio": "Backend developer passionate about schema design and writing performant SQL queries.",
        "verified": True
    },
    {
        "mentor_id": "MNT-108",
        "name": "Tanya Joshi",
        "branch": "Business Administration / MBA",
        "semester": 4,
        "skills_offered": "Public Speaking, Resume Building, Interview Skills, Case Study, Pitching",
        "skills_wanted": "Python for Data Analytics",
        "experience_years": 2.0,
        "hourly_fee_inr": 150,
        "rating": 4.9,
        "total_sessions": 21,
        "bio": "Winner of National Debate Championships. Helping engineering students crack HR interviews & GD rounds.",
        "verified": True
    }
]

df_mentors = pd.DataFrame(mentors_data)
df_mentors.to_csv("c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/data/peer_mentors.csv", index=False)
print("Created peer_mentors.csv with", len(df_mentors), "records.")

# 2. Campus Marketplace Items Dataset (Historical data for Fair Price ML Training)
np.random.seed(42)
categories = ["Textbooks", "Calculators", "Lab Tools", "Electronics Kit", "Engineering Drawing", "College Uniform/Coat"]

samples = []
for i in range(1, 301):
    cat = np.random.choice(categories, p=[0.35, 0.15, 0.15, 0.15, 0.10, 0.10])
    
    if cat == "Textbooks":
        mrp = np.random.randint(350, 1200)
        age_sem = np.random.randint(1, 7)
        condition = np.random.randint(2, 6) # 2 to 5 stars
        demand_index = np.random.uniform(0.6, 1.0)
    elif cat == "Calculators":
        mrp = np.random.choice([800, 1100, 1400, 1800])
        age_sem = np.random.randint(1, 6)
        condition = np.random.randint(3, 6)
        demand_index = np.random.uniform(0.8, 1.0)
    elif cat == "Lab Tools":
        mrp = np.random.randint(400, 1500)
        age_sem = np.random.randint(1, 5)
        condition = np.random.randint(2, 6)
        demand_index = np.random.uniform(0.5, 0.9)
    elif cat == "Electronics Kit":
        mrp = np.random.randint(800, 3000)
        age_sem = np.random.randint(1, 4)
        condition = np.random.randint(3, 6)
        demand_index = np.random.uniform(0.7, 1.0)
    elif cat == "Engineering Drawing":
        mrp = np.random.randint(500, 1200)
        age_sem = np.random.randint(1, 5)
        condition = np.random.randint(2, 5)
        demand_index = np.random.uniform(0.7, 0.95)
    else:
        mrp = np.random.randint(300, 700)
        age_sem = np.random.randint(1, 4)
        condition = np.random.randint(3, 6)
        demand_index = np.random.uniform(0.4, 0.8)
    
    # Fair price formula logic with noise:
    # Depreciates with age, improves with condition (1-5) and demand index
    base_factor = 0.85 - (age_sem * 0.08) + ((condition - 3) * 0.07) + ((demand_index - 0.7) * 0.15)
    base_factor = max(0.25, min(0.85, base_factor))
    fair_price = round(mrp * base_factor + np.random.normal(0, mrp * 0.03))
    fair_price = max(50, fair_price)
    
    samples.append({
        "item_id": f"ITM-{1000 + i}",
        "category": cat,
        "original_mrp": mrp,
        "age_semesters": age_sem,
        "condition_rating": condition, # 1-5 scale
        "demand_index": round(demand_index, 2),
        "fair_price_inr": fair_price
    })

df_items = pd.DataFrame(samples)
df_items.to_csv("c:/Users/User/Desktop/PAYAL IBM/campus_circle_ai/data/campus_items.csv", index=False)
print("Created campus_items.csv with", len(df_items), "records.")
