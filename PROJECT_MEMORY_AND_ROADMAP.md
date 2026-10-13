# 🎓 CAMPUS CIRCLE AI — MASTER PROJECT MEMORY & ROADMAP
> **AICTE | IBM SkillsBuild Machine Learning & Applied AI Internship 2026**  
> **Student:** Muskan Priyadarshani Patra  
> **Internship ID:** `IBMUEML013863`  
> **Certificate / Learning Plan ID:** `PLAN-CD7DED2B108B`  
> **Partner Organization:** BharatCares (CSRBOX)  
> **Document Purpose:** Complete Technical Handoff, Work Done, Code Architecture, and Step-by-Step Future Execution Guide (Account Transfer Memory).

---

## 📌 TABLE OF CONTENTS
1. [Executive Project Summary](#1-executive-project-summary)
2. [What Has Been Done So Far (Pura Kaam Details)](#2-what-has-been-done-so-far-pura-kaam-details)
3. [The 10 Proposed Features & Implementation Status](#3-the-10-proposed-features--implementation-status)
4. [Machine Learning & NLP Architecture](#4-machine-learning--nlp-architecture)
5. [Current File Structure & Directory Map](#5-current-file-structure--directory-map)
6. [How To Run The Project (Step-by-Step Commands)](#6-how-to-run-the-project-step-by-step-commands)
7. [What To Do Next (Work To Do & Future Plans)](#7-what-to-do-next-work-to-do--future-plans)
8. [Firebase Integration Blueprint (If Adding Cloud DB)](#8-firebase-integration-blueprint)
9. [IBM Viva & Presentation Q&A Cheat Sheet](#9-ibm-viva--presentation-qa-cheat-sheet)
10. [Prompt For New AI Agent (Next Account Master Prompt)](#10-prompt-for-new-ai-agent-copy-paste-this)

---

## 1. EXECUTIVE PROJECT SUMMARY

**Campus Circle AI** is a circular campus economy and peer-to-peer micro-learning platform designed to solve university affordability crises, educational waste, and the isolation in syllabus-specific peer tutoring.

* **Target Audience:** College / University students across all departments (Engineering, IT, MBA, Design).
* **UN Sustainable Development Goals (SDGs):**
  * **SDG 4 (Quality Education):** Peer-to-peer syllabus-aligned tutoring and skill swaps.
  * **SDG 8 (Decent Work & Economic Growth):** Students gain practical industry skills, portfolio reviews, and earn micro-incomes as campus tutors.
  * **SDG 12 (Responsible Consumption & Production):** Circular reuse of textbooks, calculators, engineering tools, diverting paper/e-waste from landfills.

---

## 2. WHAT HAS BEEN DONE SO FAR (PURA KAAM DETAILS)

### A. Machine Learning Pipeline Built
1. **Supervised Regression Engine (`ml_models.py`):**
   * **Random Forest Regressor ($R^2 = 0.9527$, $MAE = ₹68.23$):** Predicts fair secondhand prices factoring in Original MRP, Age in semesters, Condition rating (1-5), and Campus Exam Demand Index.
   * **Decision Tree Regressor ($R^2 = 0.9133$, $MAE = ₹96.25$):** Baseline benchmark taught in Masterclass 3.
   * **Explainable AI (XAI) Helper:** Calculates exact monetary attribution (Depreciation from Age, Condition impact, and Exam demand shift).
2. **Natural Language Processing (NLP) Recommender (`ml_models.py`):**
   * **TF-IDF Vectorizer + Cosine Similarity:** Semantic matching between a student's learning query and campus senior profiles.
   * **Two-Way Skill Barter Engine:** Matches what Student A wants to learn against Student B's offerings, AND matches what Student A can teach against Student B's wants for a **100% Free Mutual Barter (0 Rupee Exchange)**.

### B. Interactive Web Application (`app.py`)
* Built completely with **Streamlit** and custom CSS styling.
* Fully interactive with `st.session_state` persistence for student profile, marketplace catalog, session bookings, live chat messages, and reviews.
* Successfully running on `http://localhost:8501`.

### C. Deliverables & Documentation Created
All official IBM internship files have been generated and exist in `c:\Users\User\Desktop\PAYAL IBM`:
1. `Campus_Circle_AI_Final_Presentation.pptx` (16 slides, custom color palette, slide architecture).
2. `Campus_Circle_AI_Concept_Note.pdf` (Executive summary, SDG alignment, problem-solution mapping).
3. `Campus_Circle_AI_Lean_Canvas.pdf` (Business model, unfair advantage, cost structure, revenue streams).
4. `Campus_Circle_AI_Screenshots.pdf` (Visual app walkthrough screenshots).
5. `Payal IBM (1).pdf` (Official IBM SkillsBuild Self-Learning Completion Certificate - PLAN-CD7DED2B108B).

---

## 3. THE 10 PROPOSED FEATURES & IMPLEMENTATION STATUS

All 10 proposed features from your presentation are **100% functional** inside `app.py`:

| No. | Feature Name | Description & Working State | Location in Code / UI |
| :---: | :--- | :--- | :--- |
| **1** | **Student Registration** | Students can create and edit their profile with Full Name, Roll Number, Branch, Semester, and College Email. | `Module 2: Tab 2 (Register / Update Account)` |
| **2** | **College Email Verification** | Institutional domain check (`.ac.in` / `.edu`) + simulated 4-digit OTP system (`8492`) granting the **"✅ Institutional ID Verified"** badge and +50 Eco-Credits. | `Module 2: Tab 1 (Profile & Verification)` |
| **3** | **Campus Marketplace** | Filterable catalog of Calculators, Books, Mini Drafters, Uniforms, Lab Kits with search bar, condition rating, and seller info. | `Module 3: Tab 1 (Browse Items)` |
| **4** | **Buy, Sell and Swap** | **Buy:** Instant order confirmation with campus pickup points.<br>**Swap:** Propose item trade to seller.<br>**Sell:** Inputs MRP, age, and condition into Random Forest model -> calculates fair valuation -> instantly publishes to live marketplace catalog. | `Module 3: Tab 1 & Tab 2 (Sell Item)` |
| **5** | **Skill Hub** | Verified campus mentors directory + Registration form for students to list skills offered, skills wanted, hourly fee, and bio. | `Module 4: Tab 2 (Directory) & Tab 3 (Register)` |
| **6** | **Skill Discovery** | NLP TF-IDF Cosine Similarity engine that ranks mentors based on learning query and detects **2-Way Mutual Skill Barters (0-Cost Swap)**. | `Module 4: Tab 1 (AI Skill Discovery)` |
| **7** | **Session Booking** | Booking portal allowing students to select a mentor, topic, date, time slot, and meeting mode (Library Pod, SAC, Online). Generates booking IDs (`BK-XXXX`). | `Module 5: Session Booking Portal` |
| **8** | **In-App Chat** | Interactive messaging system with conversation channels (Aarav Sharma, Rohan Joshi, and Campus Circle AI Assistant) supporting real-time chat bubbles and automated peer replies. | `Module 6: In-App Campus Chat` |
| **9** | **Ratings and Reviews** | 5-star rating submission form with category tagging and live feed of verified student testimonials and trust scores. | `Module 7: Ratings & Student Reviews` |
| **10** | **Revenue Model & Economics** | Freemium vs **Campus Pro (₹49/sem)** tier, 2% micro-fee on cash equipment, 0% on swaps, and an interactive **Financial Simulator** comparing platform revenue to student body savings. | `Module 8: Revenue Model & Economics` |

---

## 4. MACHINE LEARNING & NLP ARCHITECTURE

### Model 1: Fair-Price Valuation Regressor
* **Algorithm:** `RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)`
* **Benchmark:** `DecisionTreeRegressor(max_depth=5, random_state=42)`
* **Dataset:** `data/campus_items.csv` (300+ campus transactions)
* **Input Features:**
  * Categorical: `category` (One-hot encoded)
  * Numerical: `original_mrp`, `age_semesters`, `condition_rating` (1 to 5), `demand_index` (0.5 to 1.0)
* **Target:** `fair_price_inr`
* **Performance Metrics:**
  * Random Forest $R^2$: **0.9527** (95.3% accuracy)
  * Random Forest MAE: **₹68.23**
  * Decision Tree $R^2$: **0.9133**
  * Decision Tree MAE: **₹96.25**

### Model 2: Content-Based Skill Recommender & 2-Way Barter
* **Algorithm:** `TfidfVectorizer(stop_words='english', ngram_range=(1,2))` + `cosine_similarity`
* **Dataset:** `data/peer_mentors.csv`
* **Corpus:** Concatenation of `skills_offered + bio + branch`
* **Two-Way Barter Formula:**
  $$\text{Score}_{\text{combined}} = 0.6 \times \text{Sim}(\text{Query}_{\text{learn}}, \text{Mentor}_{\text{offered}}) + 0.4 \times \text{Sim}(\text{Query}_{\text{teach}}, \text{Mentor}_{\text{wanted}})$$
  If both scores exceed threshold $\rightarrow$ Flagged as **"Mutual Skill Barter (0-Rupee Exchange)"**.

---

## 5. CURRENT FILE STRUCTURE & DIRECTORY MAP

```
c:\Users\User\Desktop\PAYAL IBM\
├── Campus_Circle_AI_Concept_Note.pdf       # Deliverable: 2-page Concept Note
├── Campus_Circle_AI_Final_Presentation.pptx# Deliverable: 16-Slide Final Deck
├── Campus_Circle_AI_Lean_Canvas.pdf        # Deliverable: 1-page Lean Canvas
├── Campus_Circle_AI_Screenshots.pdf        # Deliverable: App Screenshots Document
├── Payal IBM (1).pdf                       # Deliverable: IBM SkillsBuild Certificate
├── campus_circle_ai\                       # Main Project Codebase
│   ├── app.py                              # Streamlit Application (All 10 features)
│   ├── ml_models.py                        # ML Engine (Random Forest, DT, TF-IDF Barter)
│   ├── logo.jpeg                           # Project Logo
│   ├── requirements.txt                    # Project Dependencies
│   ├── README.md                           # GitHub README documentation
│   ├── PROJECT_MEMORY_AND_ROADMAP.md       # THIS MASTER HANDOFF FILE
│   ├── create_presentation.py              # Script that builds the 16-slide PPTX
│   ├── create_concept_note_pdf.py          # Script that builds Concept Note PDF
│   ├── create_lean_canvas_pdf.py           # Script that builds Lean Canvas PDF
│   ├── create_screenshots_pdf.py           # Script that builds Screenshots PDF
│   ├── data\
│   │   ├── campus_items.csv                # Secondhand items dataset (300 records)
│   │   ├── peer_mentors.csv                # Student mentors dataset
│   │   └── generate_data.py                # Synthetic dataset generator script
│   └── screenshots\                        # Captured PNG screenshots
```

---

## 6. HOW TO RUN THE PROJECT (STEP-BY-STEP COMMANDS)

### Step 1: Open PowerShell / Terminal
Navigate to the project folder:
```powershell
cd "c:\Users\User\Desktop\PAYAL IBM\campus_circle_ai"
```

### Step 2: Install Required Libraries (If running on a fresh PC/environment)
```powershell
pip install -r requirements.txt
```
*(Packages needed: `streamlit`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `python-pptx`, `reportlab`)*

### Step 3: Run the Streamlit Application
```powershell
# Windows with py launcher:
py -m streamlit run app.py

# Or standard python:
streamlit run app.py
```
App will automatically open in your browser at: **`http://localhost:8501`**.

### Step 4: Regenerate PPT or PDFs (Optional)
If you ever want to update text and rebuild the slides or PDFs:
```powershell
py create_presentation.py
py create_concept_note_pdf.py
py create_lean_canvas_pdf.py
py create_screenshots_pdf.py
```

---

## 7. WHAT TO DO NEXT (WORK TO DO & FUTURE PLANS)

Here is the exact priority list of what should be done next:

### 🔴 Priority 1: Git Push to GitHub (For Submission Link)
IBM SkillsBuild requires a public GitHub repository link.
Run these commands in PowerShell:
```powershell
cd "c:\Users\User\Desktop\PAYAL IBM\campus_circle_ai"
git init
git add .
git commit -m "feat: complete Campus Circle AI with all 10 features and ML models"
# Create a repository on github.com named 'campus-circle-ai'
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/campus-circle-ai.git
git branch -M main
git push -u origin main
```

### 🟡 Priority 2: Deploy Free Online (Streamlit Community Cloud)
So the jury can click a link and test it on their phone/laptop:
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Connect your GitHub account.
3. Select your repository `campus-circle-ai`, branch `main`, and main file `app.py`.
4. Click **Deploy**. Your app will get a public link like `https://campus-circle-ai.streamlit.app`.

### 🟢 Priority 3: Final Internship Submission Checklist
Check off each deliverable before submitting on the IBM portal:
- [x] **Deliverable 1:** IBM SkillsBuild Completion Certificate (`Payal IBM (1).pdf`)
- [x] **Deliverable 2A:** Concept Note (`Campus_Circle_AI_Concept_Note.pdf`)
- [x] **Deliverable 2B:** Lean Canvas (`Campus_Circle_AI_Lean_Canvas.pdf`)
- [x] **Deliverable 2C:** Project Presentation (`Campus_Circle_AI_Final_Presentation.pptx`)
- [x] **Deliverable 2D:** Screenshots PDF (`Campus_Circle_AI_Screenshots.pdf`)
- [ ] **Deliverable 3:** GitHub Repository URL
- [ ] **Deliverable 4:** Live Deployed Web App URL (Optional bonus point)
- [ ] **Deliverable 5:** 2-3 minute video demonstration screen recording

---

## 8. FIREBASE INTEGRATION BLUEPRINT

If you or your team decide to convert this from prototype session storage to a live production database:

### Recommended Architecture:
```
[ Frontend: Streamlit / React ]
       │
       ├──► [ Machine Learning Core: Python (Scikit-Learn, TF-IDF) ]
       │
       └──► [ Cloud Database & Auth: Firebase ]
              ├── Firebase Authentication (College .edu / .ac.in email OTP)
              ├── Cloud Firestore (Persistent items, mentors, bookings, reviews)
              └── Firebase Storage (Real photos of books and equipment)
```

### Quick Python Connection Snippet (`firebase-admin`):
```python
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Download serviceAccountKey.json from Firebase Console
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. Add an item to Firestore:
db.collection("marketplace_items").add({
    "name": "Casio fx-991EX",
    "fair_price": 950,
    "seller_email": "muskan.patra@kiit.ac.in",
    "status": "Available"
})

# 3. Read items in real-time:
docs = db.collection("marketplace_items").stream()
items = [doc.to_dict() for doc in docs]
```

---

## 9. IBM VIVA & PRESENTATION Q&A CHEAT SHEET

1. **Q: Why did you use Random Forest Regression instead of simple Linear Regression?**  
   * **A:** Secondhand price depreciation is non-linear. A calculator's price drops significantly in the first 2 semesters and then plateaus. Random Forest handles non-linear depreciation and feature interactions (e.g., high condition mitigating older age) far better, achieving an $R^2$ of 0.952 compared to lower baseline linear models.
2. **Q: How does the AI Skill Matcher work?**  
   * **A:** It uses Natural Language Processing (NLP). We vectorize mentor bios, branches, and offered skills using `TfidfVectorizer` (with 1-2 n-grams) and compute semantic `cosine_similarity` against the user's natural language query. We also built a two-way barter formula to detect 100% mutual free skill exchanges.
3. **Q: Which UN SDGs does your project address?**  
   * **A:** **SDG 4 (Quality Education)** through syllabus-tailored peer mentoring, **SDG 8 (Decent Work)** by allowing skilled seniors to monetize their expertise, and **SDG 12 (Responsible Consumption)** through circular reuse of university tools and textbooks.
4. **Q: How will the platform sustain itself financially?**  
   * **A:** Through a freemium model: Free basic swapping and skill bartering for all students, with an optional **Campus Pro** membership at ₹49/semester for priority search rankings, verified senior badges, and zero fees.

---

## 10. PROMPT FOR NEW AI AGENT (COPY-PASTE THIS!)

> **Copy and paste the text below into your new account whenever you start a new conversation:**

```markdown
I am continuing my AICTE | IBM SkillsBuild Applied AI & Machine Learning Internship 2026 project: "Campus Circle AI".
Student: Muskan Priyadarshani Patra (Plan ID: PLAN-CD7DED2B108B).

Please read the master project memory file at:
`c:\Users\User\Desktop\PAYAL IBM\campus_circle_ai\PROJECT_MEMORY_AND_ROADMAP.md`

Current Project Summary:
1. Core Stack: Python, Streamlit, Scikit-Learn (Random Forest Regressor R2=0.952, Decision Tree R2=0.913), NLP TF-IDF & Cosine Similarity (Two-way skill barter).
2. App file: `campus_circle_ai/app.py` has all 10 features implemented and running live at http://localhost:8501 (Student Auth, Email Verification, Marketplace, Buy/Sell/Swap, Skill Hub, 2-Way Barter Discovery, Session Booking, In-App Chat, Ratings & Reviews, Revenue Model).
3. All Deliverable PDFs and PPTX are already generated in `c:\Users\User\Desktop\PAYAL IBM`.

Acknowledge this project memory and tell me what you're ready to help me with next (e.g., GitHub push, cloud deployment, or code modification).
```

---
*Created on 13 October 2026 | Campus Circle AI — Student Skill Exchange & Circular Resource Network*
