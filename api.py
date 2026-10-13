import os
import datetime
import random
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ml_models import FairPricePredictor, SkillMatcher, calculate_sdg_impact

app = FastAPI(
    title="Campus Circle AI API",
    description="Student Skill Exchange & Circular Resource Network Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- INITIALIZE ML MODELS -----------------
print("Loading Machine Learning Models...")
fair_price_model = FairPricePredictor()
skill_matcher_model = SkillMatcher()
print("ML Models Ready!")

# ----------------- IN-MEMORY DATA STORE (PERSISTENT IN-PROCESS) -----------------
data_store = {
    "user": {
        "name": "Muskan Priyadarshani Patra",
        "email": "muskan.patra@kiit.ac.in",
        "branch": "Computer Science & Engineering",
        "semester": 6,
        "roll_no": "2105128",
        "internship_id": "IBMUEML013863",
        "plan_id": "PLAN-CD7DED2B108B",
        "verified": True,
        "eco_credits": 340,
        "is_pro": False
    },
    "items": [
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
    ],
    "bookings": [
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
    ],
    "chat_channels": {
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
    },
    "reviews": [
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
}

# ----------------- PYDANTIC REQUEST MODELS -----------------
class UserUpdateRequest(BaseModel):
    name: str
    email: str
    branch: str
    semester: int
    roll_no: str

class OtpVerifyRequest(BaseModel):
    otp: str

class PricePredictionRequest(BaseModel):
    category: str
    original_mrp: float
    age_semesters: int
    condition_rating: int
    demand_index: float = 0.85

class ItemCreateRequest(BaseModel):
    name: str
    category: str
    mrp: float
    age_sem: int
    condition: int
    demand_index: float = 0.85
    allow_swap: bool = True
    description: Optional[str] = ""

class ItemActionRequest(BaseModel):
    pickup_point: Optional[str] = "Central Library"
    swap_offer: Optional[str] = ""

class MentorRegisterRequest(BaseModel):
    skills_offered: str
    skills_wanted: str
    hourly_fee_inr: float = 0.0
    bio: str
    experience_years: float = 1.5

class SkillDiscoveryRequest(BaseModel):
    learn_query: str
    teach_query: Optional[str] = ""
    top_k: int = 4

class BookingCreateRequest(BaseModel):
    mentor_name: str
    topic: str
    date: str
    time_slot: str
    mode: str
    notes: Optional[str] = ""

class ChatMessageRequest(BaseModel):
    channel: str
    message: str

class ReviewCreateRequest(BaseModel):
    target: str
    rating: int
    category: str
    comment: str

# ----------------- API ENDPOINTS -----------------

@app.get("/api/user")
def get_user_profile():
    return data_store["user"]

@app.post("/api/user")
def update_user_profile(req: UserUpdateRequest):
    is_valid_domain = any(d in req.email.lower() for d in [".ac.in", ".edu", "college", "univ"])
    data_store["user"].update({
        "name": req.name,
        "email": req.email,
        "branch": req.branch,
        "semester": req.semester,
        "roll_no": req.roll_no,
        "verified": is_valid_domain
    })
    return {"status": "success", "user": data_store["user"]}

@app.post("/api/user/verify-otp")
def verify_otp(req: OtpVerifyRequest):
    if req.otp == "8492":
        data_store["user"]["verified"] = True
        data_store["user"]["eco_credits"] += 50
        return {"status": "success", "message": "Institutional ID Verified! +50 Eco-Credits awarded.", "user": data_store["user"]}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP code. Please use demo OTP: 8492")

@app.get("/api/items")
def get_items(category: Optional[str] = None, search: Optional[str] = None, swap_only: bool = False):
    items = data_store["items"]
    if category and category != "All Categories":
        items = [i for i in items if i["category"].lower() == category.lower()]
    if search:
        s = search.lower()
        items = [i for i in items if s in i["name"].lower() or s in i["description"].lower() or s in i["category"].lower()]
    if swap_only:
        items = [i for i in items if i["allow_swap"]]
    return items

@app.post("/api/predict-price")
def predict_fair_price(req: PricePredictionRequest):
    pred = fair_price_model.predict(
        category=req.category,
        original_mrp=req.original_mrp,
        age_semesters=req.age_semesters,
        condition_rating=req.condition_rating,
        demand_index=req.demand_index
    )
    breakdown = fair_price_model.explain_prediction(
        original_mrp=req.original_mrp,
        age_semesters=req.age_semesters,
        condition_rating=req.condition_rating,
        demand_index=req.demand_index,
        fair_price=pred["suggested_fair_price"]
    )
    return {
        "prediction": pred,
        "attribution_breakdown": breakdown
    }

@app.post("/api/items")
def create_item(req: ItemCreateRequest):
    pred = fair_price_model.predict(
        category=req.category,
        original_mrp=req.mrp,
        age_semesters=req.age_sem,
        condition_rating=req.condition,
        demand_index=req.demand_index
    )
    item_id = f"ITM-{len(data_store['items']) + 101}"
    new_item = {
        "id": item_id,
        "name": req.name,
        "category": req.category,
        "mrp": req.mrp,
        "fair_price": float(pred["suggested_fair_price"]),
        "age_sem": req.age_sem,
        "condition": req.condition,
        "seller_name": data_store["user"]["name"],
        "seller_branch": data_store["user"]["branch"],
        "seller_email": data_store["user"]["email"],
        "allow_swap": req.allow_swap,
        "status": "Available",
        "description": req.description or "Verified student equipment."
    }
    data_store["items"].insert(0, new_item)
    data_store["user"]["eco_credits"] += 30
    return {"status": "success", "item": new_item}

@app.post("/api/items/{item_id}/buy")
def buy_item(item_id: str, action: ItemActionRequest):
    item = next((i for i in data_store["items"] if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data_store["user"]["eco_credits"] += 20
    order_ref = f"ORD-{random.randint(10000, 99999)}"
    return {
        "status": "success",
        "order_reference": order_ref,
        "item_name": item["name"],
        "fair_price": item["fair_price"],
        "pickup_point": action.pickup_point or "Campus Central Library",
        "seller": item["seller_name"],
        "message": f"Order confirmed! Pick up at {action.pickup_point}. +20 Eco-Credits awarded."
    }

@app.post("/api/items/{item_id}/swap")
def propose_swap(item_id: str, action: ItemActionRequest):
    item = next((i for i in data_store["items"] if i["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "status": "success",
        "message": f"Swap proposal sent to {item['seller_name']}! Chat channel updated.",
        "swap_offer": action.swap_offer
    }

@app.get("/api/mentors")
def get_all_mentors():
    return skill_matcher_model.get_all_mentors()

@app.post("/api/mentors")
def register_as_mentor(req: MentorRegisterRequest):
    new_mentor = {
        "mentor_id": f"MNT-{len(skill_matcher_model.df) + 101}",
        "name": data_store["user"]["name"],
        "branch": data_store["user"]["branch"],
        "semester": data_store["user"]["semester"],
        "skills_offered": req.skills_offered,
        "skills_wanted": req.skills_wanted or "None (Volunteer)",
        "experience_years": req.experience_years,
        "hourly_fee_inr": req.hourly_fee_inr,
        "rating": 5.0,
        "total_sessions": 0,
        "bio": req.bio or "Peer mentor.",
        "verified": True
    }
    skill_matcher_model.add_mentor(new_mentor)
    data_store["user"]["eco_credits"] += 40
    return {"status": "success", "mentor": new_mentor}

@app.post("/api/discover-skills")
def discover_skills(req: SkillDiscoveryRequest):
    results = skill_matcher_model.find_two_way_barter(
        learn_query=req.learn_query,
        teach_query=req.teach_query or "",
        top_k=req.top_k
    )
    return {"matches": results}

@app.get("/api/bookings")
def get_bookings():
    return data_store["bookings"]

@app.post("/api/bookings")
def create_booking(req: BookingCreateRequest):
    booking_code = f"BK-{random.randint(1000, 9999)}"
    new_b = {
        "booking_id": booking_code,
        "mentor_name": req.mentor_name,
        "topic": req.topic or "Peer Tutoring Session",
        "date": req.date,
        "time_slot": req.time_slot,
        "mode": req.mode,
        "notes": req.notes,
        "status": "Confirmed ✅",
        "fee": "FREE (Skill Swap)"
    }
    data_store["bookings"].insert(0, new_b)
    data_store["user"]["eco_credits"] += 25
    return {"status": "success", "booking": new_b}

@app.get("/api/chat")
def get_chat_channels():
    return data_store["chat_channels"]

@app.post("/api/chat/send")
def send_chat_message(req: ChatMessageRequest):
    if req.channel not in data_store["chat_channels"]:
        data_store["chat_channels"][req.channel] = []
    
    # Append user message
    data_store["chat_channels"][req.channel].append({"sender": "user", "text": req.message})

    # Auto response logic
    if "AI Bot" in req.channel:
        q = req.message.lower()
        if "sdg" in q:
            reply = "Campus Circle AI directly aligns with **SDG 4 (Quality Education)**, **SDG 8 (Decent Work)**, and **SDG 12 (Responsible Consumption & Circular Economy)**!"
        elif "price" in q or "fair" in q or "cost" in q:
            reply = "Our Supervised **Random Forest Regressor (R² = 0.952)** evaluates condition, semesters of use, and exam demand to eliminate depreciation disputes."
        elif "barter" in q or "swap" in q:
            reply = "With **Two-Way Skill Barter**, students can exchange knowledge 100% free with zero platform fees!"
        else:
            reply = f"Great question regarding '{req.message}'! Campus Circle AI unifies peer tutoring with verified circular campus exchange."
    else:
        peer = req.channel.split(" (")[0]
        reply = f"Hey {data_store['user']['name'].split(' ')[0]}! Got your message: '{req.message}'. That works for me, let's meet up at the campus spot!"

    data_store["chat_channels"][req.channel].append({"sender": "other", "text": reply})
    return {"status": "success", "messages": data_store["chat_channels"][req.channel]}

@app.get("/api/reviews")
def get_reviews():
    return data_store["reviews"]

@app.post("/api/reviews")
def post_review(req: ReviewCreateRequest):
    new_r = {
        "reviewer": data_store["user"]["name"],
        "target": req.target,
        "rating": req.rating,
        "category": req.category,
        "date": str(datetime.date.today()),
        "comment": req.comment
    }
    data_store["reviews"].insert(0, new_r)
    data_store["user"]["eco_credits"] += 15
    return {"status": "success", "review": new_r}

@app.post("/api/upgrade-pro")
def upgrade_pro():
    data_store["user"]["is_pro"] = not data_store["user"]["is_pro"]
    return {"status": "success", "is_pro": data_store["user"]["is_pro"]}

@app.get("/api/sdg-impact")
def get_sdg_impact():
    return calculate_sdg_impact(total_swaps=184, avg_saving_per_item=520, skill_hours=410)

@app.get("/api/ml-metrics")
def get_ml_metrics():
    return fair_price_model.metrics

# ----------------- STATIC FRONTEND SERVING -----------------
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Campus Circle AI API is running. Static frontend mounting in progress."}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print(">>> Campus Circle AI Engine Starting on http://127.0.0.1:8000")
    print("="*60 + "\n")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
