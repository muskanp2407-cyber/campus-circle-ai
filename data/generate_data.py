import pandas as pd
import numpy as np

# 1. Peer Mentors Dataset
mentors_data = [
    {
        "mentor_id": "MNT-101",
        "name": "Aarav Sharma",
        "branch": "Computer Engineering",
        "semester": 7,
        "skills_offered": "Python programming, Web development, React basics, Git and GitHub, Machine Learning fundamentals",
        "skills_wanted": "UI/UX design, Figma, 3D modelling",
        "experience_years": 2.5,
        "hourly_fee_inr": 0,
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
        "skills_offered": "Web development, React basics, JavaScript, HTML/CSS, Database and SQL",
        "skills_wanted": "C/C++ programming, Data Structures",
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
        "skills_offered": "AutoCAD, SolidWorks, CATIA basics, 3D modelling, Engineering drawing",
        "skills_wanted": "Python programming, Excel for civil calculations",
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
        "skills_offered": "C/C++ programming, Java programming, Database and SQL, UI/UX design, Cybersecurity fundamentals",
        "skills_wanted": "Machine Learning fundamentals, Python programming",
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
        "skills_offered": "Arduino-based circuit projects, Embedded C, IoT, Circuit analysis, Raspberry Pi",
        "skills_wanted": "React basics, Web development",
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
        "skills_offered": "UI/UX design, Figma, Adobe Illustrator, Canva, Graphic Design",
        "skills_wanted": "Web development, React basics",
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
        "skills_offered": "Database and SQL, PostgreSQL, MongoDB, Backend APIs, Git and GitHub",
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
        "skills_wanted": "Python programming, Data analysis",
        "experience_years": 2.0,
        "hourly_fee_inr": 150,
        "rating": 4.9,
        "total_sessions": 21,
        "bio": "Winner of National Debate Championships. Helping engineering students crack HR interviews & GD rounds.",
        "verified": True
    },
    {
        "mentor_id": "MNT-109",
        "name": "Aditya Kulkarni",
        "branch": "Civil Engineering",
        "semester": 6,
        "skills_offered": "AutoCAD 2D drafting, Civil 3D basics, Revit/BIM fundamentals, Surveying fundamentals, Quantity estimation",
        "skills_wanted": "Python programming, Excel for civil calculations",
        "experience_years": 2.0,
        "hourly_fee_inr": 0,
        "rating": 4.8,
        "total_sessions": 16,
        "bio": "Civil 3rd year. Site planning, surveying total station handling and BIM drafting tutor.",
        "verified": True
    },
    {
        "mentor_id": "MNT-110",
        "name": "Meera Nair",
        "branch": "Civil Engineering",
        "semester": 5,
        "skills_offered": "Building planning and drawing, Structural analysis basics, Excel for civil calculations, Concrete mix design fundamentals, Project scheduling basics",
        "skills_wanted": "AutoCAD, 3D modelling",
        "experience_years": 1.5,
        "hourly_fee_inr": 80,
        "rating": 4.7,
        "total_sessions": 11,
        "bio": "Specialized in structural design, AutoCAD drawings, and cost estimation.",
        "verified": True
    },
    {
        "mentor_id": "MNT-111",
        "name": "Rahul Sundaram",
        "branch": "Electrical Engineering",
        "semester": 6,
        "skills_offered": "Circuit analysis, MATLAB/Simulink basics, Electrical circuit simulation, Basic electronics, Digital logic design",
        "skills_wanted": "Python programming, Machine Learning fundamentals",
        "experience_years": 2.2,
        "hourly_fee_inr": 0,
        "rating": 4.9,
        "total_sessions": 19,
        "bio": "Electrical 6th sem. Passionate about MATLAB simulation, circuit analysis and digital electronics.",
        "verified": True
    },
    {
        "mentor_id": "MNT-112",
        "name": "Neha Reddy",
        "branch": "Electrical Engineering",
        "semester": 7,
        "skills_offered": "Arduino-based circuit projects, Electrical machines fundamentals, Power system analysis, PCB design basics, Electrical measurement techniques",
        "skills_wanted": "Web development, React basics",
        "experience_years": 2.8,
        "hourly_fee_inr": 110,
        "rating": 4.8,
        "total_sessions": 22,
        "bio": "Hands-on PCB designer, hardware prototype builder, and power systems tutor.",
        "verified": True
    },
    {
        "mentor_id": "MNT-113",
        "name": "Ishaan Das",
        "branch": "Biomedical Engineering",
        "semester": 6,
        "skills_offered": "Biomedical instrumentation fundamentals, Human physiology concepts, ECG signal interpretation for learning, Biomedical signal processing with MATLAB/Python, Medical image processing basics",
        "skills_wanted": "Python programming, Machine Learning fundamentals",
        "experience_years": 2.4,
        "hourly_fee_inr": 0,
        "rating": 4.9,
        "total_sessions": 20,
        "bio": "Biomedical 3rd year. Teaching ECG/EEG signal filtering, biosensor circuits, and MATLAB signal processing.",
        "verified": True
    },
    {
        "mentor_id": "MNT-114",
        "name": "Anushka Sen",
        "branch": "Biomedical Engineering",
        "semester": 5,
        "skills_offered": "Biomedical sensor interfacing, Arduino-based biomedical prototypes, Medical equipment maintenance fundamentals, Medical imaging fundamentals, Biomedical data analysis",
        "skills_wanted": "Circuit analysis, 3D modelling",
        "experience_years": 1.7,
        "hourly_fee_inr": 90,
        "rating": 4.8,
        "total_sessions": 14,
        "bio": "Researcher in patient monitoring sensors, pulse oximetry circuits, and DICOM imaging.",
        "verified": True
    },
    {
        "mentor_id": "MNT-115",
        "name": "Karan Malhotra",
        "branch": "Mechanical Engineering",
        "semester": 7,
        "skills_offered": "CNC machining fundamentals, Workshop safety and tool handling, Thermodynamics concepts, Machine design fundamentals, Manufacturing processes",
        "skills_wanted": "AutoCAD 2D drafting, SolidWorks",
        "experience_years": 2.6,
        "hourly_fee_inr": 0,
        "rating": 4.9,
        "total_sessions": 25,
        "bio": "Workshop captain. Hands-on expert in lathe turning, milling, thermal engineering, and machine design.",
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
