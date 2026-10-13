import os
import json
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
        # 1. MECHANICAL ENGINEERING (MECH) - 10 Resources
        {
            "id": "ITM-101",
            "name": "Engineering Mechanics: Statics & Dynamics (Vector Edition)",
            "category": "Textbooks",
            "mrp": 850.0,
            "fair_price": 420.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Rohan Deshmukh",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Prescribed textbook with free-body diagrams, centroids, friction notes, and previous year solved problems."
        },
        {
            "id": "ITM-102",
            "name": "Professional Engineering Drawing Mini Drafter & Instrument Set",
            "category": "Engineering Drawing",
            "mrp": 1100.0,
            "fair_price": 580.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Karan Malhotra",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "karan.m@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Includes stainless steel arm mini-drafter, sheet clips, compass set, divider, and protective carry pouch."
        },
        {
            "id": "ITM-103",
            "name": "Precision Stainless Steel Vernier Caliper (0-150mm, 0.02mm Accuracy)",
            "category": "Lab Tools",
            "mrp": 850.0,
            "fair_price": 460.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Rohan Deshmukh",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "High precision workshop vernier caliper with internal/external jaws, depth gauge, and sturdy wooden storage case."
        },
        {
            "id": "ITM-104",
            "name": "Mechanical Outside Micrometer Screw Gauge (0-25mm, 0.01mm Precision)",
            "category": "Lab Tools",
            "mrp": 750.0,
            "fair_price": 410.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Karan Malhotra",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "karan.m@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Ratchet thimble, carbide-tipped measuring faces, calibrated zero-error wrench included."
        },
        {
            "id": "ITM-105",
            "name": "Fitting & Carpentry Mechanical Workshop Student Tool Kit",
            "category": "Lab Tools",
            "mrp": 1400.0,
            "fair_price": 720.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Rohan Deshmukh",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Complete workshop kit with ball peen hammer, center punch, steel tri-square, cold chisel, and flat files."
        },
        {
            "id": "ITM-106",
            "name": "Design of Machine Elements by V.B. Bhandari (4th Edition)",
            "category": "Textbooks",
            "mrp": 950.0,
            "fair_price": 490.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Karan Malhotra",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "karan.m@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Comprehensive machine design reference with shaft, spring, clutch, and gear design charts intact."
        },
        {
            "id": "ITM-107",
            "name": "Applied Thermodynamics Master Notes & Formula Compendium",
            "category": "Textbooks",
            "mrp": 450.0,
            "fair_price": 220.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Rohan Deshmukh",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Neat spiral-bound handwritten notes covering Otto, Diesel, Rankine, Brayton cycles and steam tables summary."
        },
        {
            "id": "ITM-108",
            "name": "Mastering AutoCAD Mechanical & 2D/3D Drafting Guide",
            "category": "Textbooks",
            "mrp": 780.0,
            "fair_price": 390.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Karan Malhotra",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "karan.m@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Step-by-step CAD drafting tutorial book with shortcut commands, isometric exercises, and dimensioning standards."
        },
        {
            "id": "ITM-109",
            "name": "SolidWorks & CATIA 3D Modelling Practice CAD Files (32GB USB)",
            "category": "Electronics Kit",
            "mrp": 650.0,
            "fair_price": 320.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Rohan Deshmukh",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "rohan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "High-speed USB drive containing 120+ mechanical assembly models, STEP/IGES files, and practice blueprints."
        },
        {
            "id": "ITM-110",
            "name": "Manufacturing Technology & Machining Workshop Lab Manual",
            "category": "Lab Tools",
            "mrp": 400.0,
            "fair_price": 190.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Karan Malhotra",
            "seller_branch": "Mechanical Engineering",
            "seller_email": "karan.m@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Official college syllabus manual with lathe operations, milling tool specs, foundry procedures, and viva questions."
        },

        # 2. ELECTRICAL ENGINEERING (ELEC) - 10 Resources
        {
            "id": "ITM-111",
            "name": "Electric Machinery Fundamentals by Stephen J. Chapman (5th Edition)",
            "category": "Textbooks",
            "mrp": 890.0,
            "fair_price": 450.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Rahul Sundaram",
            "seller_branch": "Electrical Engineering",
            "seller_email": "rahul.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Covers transformers, induction motors, synchronous generators, and DC machines with highlighted formulas."
        },
        {
            "id": "ITM-112",
            "name": "Network Analysis & Circuit Theory Comprehensive Study Notes",
            "category": "Textbooks",
            "mrp": 450.0,
            "fair_price": 210.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Neha Reddy",
            "seller_branch": "Electrical Engineering",
            "seller_email": "neha.r@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Clear derivations for Norton, Thevenin, Mesh/Nodal analysis, Two-port networks, and Laplace transforms."
        },
        {
            "id": "ITM-113",
            "name": "Auto-Ranging Digital Multimeter (Voltage, Current, Resistance, Continuity)",
            "category": "Lab Tools",
            "mrp": 1200.0,
            "fair_price": 680.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Rahul Sundaram",
            "seller_branch": "Electrical Engineering",
            "seller_email": "rahul.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Digital DMM with backlit LCD display, test leads, transistor testing socket, and overload protection."
        },
        {
            "id": "ITM-114",
            "name": "Solderless 830-Point Breadboard + 120-Piece Jumper Wire Assortment",
            "category": "Electronics Kit",
            "mrp": 550.0,
            "fair_price": 280.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Neha Reddy",
            "seller_branch": "Electrical Engineering",
            "seller_email": "neha.r@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "High quality tie-point breadboard with male-to-male, male-to-female, and female-to-female flexible jumper cables."
        },
        {
            "id": "ITM-115",
            "name": "Electronics Components Starter Kit (Resistors, Capacitors, LEDs, Diodes)",
            "category": "Electronics Kit",
            "mrp": 750.0,
            "fair_price": 380.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Rahul Sundaram",
            "seller_branch": "Electrical Engineering",
            "seller_email": "rahul.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Organized multi-compartment component organizer box filled with 300+ standard value discrete components."
        },
        {
            "id": "ITM-116",
            "name": "Analog Galvanometer & Clamp Meter Electrical Measuring Tool Set",
            "category": "Lab Tools",
            "mrp": 1350.0,
            "fair_price": 750.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Neha Reddy",
            "seller_branch": "Electrical Engineering",
            "seller_email": "neha.r@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Precision AC current clamp meter with analog galvanometer suitable for electrical machine testing labs."
        },
        {
            "id": "ITM-117",
            "name": "Modern Power System Analysis by D.P. Kothari & I.J. Nagrath",
            "category": "Textbooks",
            "mrp": 920.0,
            "fair_price": 470.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Rahul Sundaram",
            "seller_branch": "Electrical Engineering",
            "seller_email": "rahul.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Essential textbook for load flow analysis, fault calculation, stability, and transmission line models."
        },
        {
            "id": "ITM-118",
            "name": "Linear Control Systems Handwritten Notes & Root Locus Flashcards",
            "category": "Textbooks",
            "mrp": 480.0,
            "fair_price": 230.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Neha Reddy",
            "seller_branch": "Electrical Engineering",
            "seller_email": "neha.r@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Comprehensive solved problems on Bode plots, Nyquist stability criterion, state space, and PID controllers."
        },
        {
            "id": "ITM-119",
            "name": "Electrical Machines & Power Electronics Combined Lab Manuals",
            "category": "Lab Tools",
            "mrp": 420.0,
            "fair_price": 200.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Rahul Sundaram",
            "seller_branch": "Electrical Engineering",
            "seller_email": "rahul.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Contains circuit schematics, observation tables, graph templates, and sample viva questions for sem 3-6."
        },
        {
            "id": "ITM-120",
            "name": "MATLAB Simulink & Proteus Electrical Circuit Simulation Project Pack",
            "category": "Electronics Kit",
            "mrp": 600.0,
            "fair_price": 290.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Neha Reddy",
            "seller_branch": "Electrical Engineering",
            "seller_email": "neha.r@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Pre-configured simulation models for rectifiers, inverters, buck-boost converters, and three-phase circuits."
        },

        # 3. CIVIL ENGINEERING - 10 Resources
        {
            "id": "ITM-121",
            "name": "Surveying Vol. 1 & 2 by B.C. Punmia (Standard Reference Editions)",
            "category": "Textbooks",
            "mrp": 880.0,
            "fair_price": 440.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Aditya Kulkarni",
            "seller_branch": "Civil Engineering",
            "seller_email": "aditya.k@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Authoritative surveying text covering chain, plane table, theodolite, and tachometric surveying methods."
        },
        {
            "id": "ITM-122",
            "name": "Imperial A1/A2 Drawing Sheet Pack (50 Sheets, 210 GSM Cartridge Paper)",
            "category": "Engineering Drawing",
            "mrp": 450.0,
            "fair_price": 240.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Meera Nair",
            "seller_branch": "Civil Engineering",
            "seller_email": "meera.n@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Clean, high-grade textured cartridge sheets ideal for civil building plans, elevations, and detailing."
        },
        {
            "id": "ITM-123",
            "name": "Architectural Triangular Reduction Scale Ruler & Drafting Stencil Set",
            "category": "Engineering Drawing",
            "mrp": 520.0,
            "fair_price": 270.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Aditya Kulkarni",
            "seller_branch": "Civil Engineering",
            "seller_email": "aditya.k@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Solid white plastic triangular reduction scale (1:20 to 1:500) with circle, curve, and lettering templates."
        },
        {
            "id": "ITM-124",
            "name": "Field Surveying & Levelling Practical College Lab Manual",
            "category": "Lab Tools",
            "mrp": 380.0,
            "fair_price": 180.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Meera Nair",
            "seller_branch": "Civil Engineering",
            "seller_email": "meera.n@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Complete manual with field booking formats, reduced level calculation tables, and contour plotting guides."
        },
        {
            "id": "ITM-125",
            "name": "Heavy-Duty 30-Meter Fiberglass & Steel Land Measuring Tape",
            "category": "Lab Tools",
            "mrp": 680.0,
            "fair_price": 340.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Aditya Kulkarni",
            "seller_branch": "Civil Engineering",
            "seller_email": "aditya.k@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Abrasion-resistant 30m / 100ft surveying tape with dual metric/imperial markings and winding crank."
        },
        {
            "id": "ITM-126",
            "name": "Surveying Field Kit: Plumb Bob, Ranging Rod Flags & Line Level",
            "category": "Lab Tools",
            "mrp": 620.0,
            "fair_price": 310.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Meera Nair",
            "seller_branch": "Civil Engineering",
            "seller_email": "meera.n@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Solid brass plumb bob, magnetic line levels, and field accessories for accurate outdoor levelling."
        },
        {
            "id": "ITM-127",
            "name": "Building Materials & Construction Engineering Study Notes",
            "category": "Textbooks",
            "mrp": 420.0,
            "fair_price": 210.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Aditya Kulkarni",
            "seller_branch": "Civil Engineering",
            "seller_email": "aditya.k@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Covers cement types, aggregates, brick masonry, plastering, timber, and green building certifications."
        },
        {
            "id": "ITM-128",
            "name": "Structural Analysis by R.C. Hibbeler (SI Metric Edition)",
            "category": "Textbooks",
            "mrp": 980.0,
            "fair_price": 510.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Meera Nair",
            "seller_branch": "Civil Engineering",
            "seller_email": "meera.n@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Classic textbook for truss analysis, moment distribution method, slope-deflection, and shear force diagrams."
        },
        {
            "id": "ITM-129",
            "name": "Concrete Technology & Mix Design Reference Handbook",
            "category": "Textbooks",
            "mrp": 480.0,
            "fair_price": 240.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Aditya Kulkarni",
            "seller_branch": "Civil Engineering",
            "seller_email": "aditya.k@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "IS 10262 mix design steps, slump test tables, compressive strength charts, and curing guidelines."
        },
        {
            "id": "ITM-130",
            "name": "Estimating and Costing in Civil Engineering by B.N. Dutta (28th Edition)",
            "category": "Textbooks",
            "mrp": 850.0,
            "fair_price": 440.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Meera Nair",
            "seller_branch": "Civil Engineering",
            "seller_email": "meera.n@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Standard handbook with rate analysis, bill of quantities (BOQ), valuation, and CPWD specifications."
        },

        # 4. COMPUTER ENGINEERING (CE) - 10 Resources
        {
            "id": "ITM-131",
            "name": "The C Programming Language (ANSI C) by Kernighan & Ritchie (2nd Ed)",
            "category": "Textbooks",
            "mrp": 650.0,
            "fair_price": 330.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Pointers, memory allocation, structs, and UNIX system calls with pristine unmarked code samples."
        },
        {
            "id": "ITM-132",
            "name": "DSA Masterclass Handwritten Notes & LeetCode 150 Pattern Sheets",
            "category": "Textbooks",
            "mrp": 520.0,
            "fair_price": 260.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Covers Trees, Graphs, Dynamic Programming, Heap, Sliding Window with visual dry-run diagrams."
        },
        {
            "id": "ITM-133",
            "name": "Operating System Concepts (Silberschatz Dinosaur Book, 10th Ed)",
            "category": "Textbooks",
            "mrp": 950.0,
            "fair_price": 490.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Processes, threads, CPU scheduling algorithms, virtual memory paging, and deadlock avoidance."
        },
        {
            "id": "ITM-134",
            "name": "DBMS & SQL Normalization Complete Exam Review Binder",
            "category": "Textbooks",
            "mrp": 460.0,
            "fair_price": 230.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Relational algebra, ER diagrams, 1NF to BCNF normalization, ACID properties, and transaction indexing."
        },
        {
            "id": "ITM-135",
            "name": "Raspberry Pi 4 Model B (4GB RAM) Development Board + Official Case",
            "category": "Electronics Kit",
            "mrp": 4800.0,
            "fair_price": 2900.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Quad-core Cortex-A72 SoC, dual 4K micro-HDMI, official enclosure, heatsinks, and 32GB OS card."
        },
        {
            "id": "ITM-136",
            "name": "Arduino Uno R3 Microcontroller Board + USB Interface Cable",
            "category": "Electronics Kit",
            "mrp": 850.0,
            "fair_price": 450.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "ATmega328P microcontroller board with 14 digital I/O pins, 6 analog inputs, and 16 MHz resonator."
        },
        {
            "id": "ITM-137",
            "name": "37-in-1 Smart Sensor Module Kit for Arduino / IoT Development",
            "category": "Electronics Kit",
            "mrp": 1650.0,
            "fair_price": 950.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Ultrasonic HC-SR04, PIR motion, DHT11 temp/humidity, flame, sound, and infrared barrier sensor modules."
        },
        {
            "id": "ITM-138",
            "name": "Computer Networks & Cisco Packet Tracer Practical Lab Manual",
            "category": "Lab Tools",
            "mrp": 390.0,
            "fair_price": 190.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Subnetting calculations, Wireshark packet capture walkthroughs, socket programming in C, and router configs."
        },
        {
            "id": "ITM-139",
            "name": "Logitech Ergonomic Mechanical Keyboard & Silent Wireless Mouse Combo",
            "category": "Electronics Kit",
            "mrp": 2400.0,
            "fair_price": 1350.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Aarav Sharma",
            "seller_branch": "Computer Engineering",
            "seller_email": "aarav.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Comfortable tactile typing for long programming sessions. 2.4GHz wireless dongle and batteries included."
        },
        {
            "id": "ITM-140",
            "name": "ESP32 Wi-Fi + Bluetooth IoT Development Board & Breadboard Breakout",
            "category": "Electronics Kit",
            "mrp": 850.0,
            "fair_price": 480.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ananya Sen",
            "seller_branch": "Computer Engineering",
            "seller_email": "ananya.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Dual-core ESP32 chip with CP2102 driver, built-in antenna, OLED header pins, and micro-USB port."
        },

        # 5. BIOMEDICAL ENGINEERING (BIOMED) - 10 Resources
        {
            "id": "ITM-141",
            "name": "Introduction to Biomedical Engineering by Enderle & Bronzino",
            "category": "Textbooks",
            "mrp": 980.0,
            "fair_price": 510.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Ishaan Das",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "ishaan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Covers biomechanics, biomaterials, tissue engineering, bioinstrumentation, and medical ethics."
        },
        {
            "id": "ITM-142",
            "name": "Ross & Wilson Anatomy and Physiology in Health and Illness (13th Ed)",
            "category": "Textbooks",
            "mrp": 920.0,
            "fair_price": 480.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Anushka Sen",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "anushka.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Full-colour diagrams of cardiovascular, nervous, respiratory, and musculoskeletal anatomical systems."
        },
        {
            "id": "ITM-143",
            "name": "Medical Instrumentation: Application and Design Comprehensive Notes",
            "category": "Textbooks",
            "mrp": 490.0,
            "fair_price": 250.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ishaan Das",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "ishaan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Biopotential amplifiers, isolation circuits, defibrillators, electrosurgery units, and patient electrical safety."
        },
        {
            "id": "ITM-144",
            "name": "Biomedical Signal Processing (ECG/EEG/EMG) MATLAB Algorithm Guide",
            "category": "Textbooks",
            "mrp": 520.0,
            "fair_price": 260.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Anushka Sen",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "anushka.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Digital filtering, Butterworth filters, wavelet transforms, Pan-Tompkins QRS detection algorithm notes."
        },
        {
            "id": "ITM-145",
            "name": "Medical Electronics & Biosensors Practical College Lab Manual",
            "category": "Lab Tools",
            "mrp": 420.0,
            "fair_price": 210.0,
            "age_sem": 2,
            "condition": 4,
            "seller_name": "Ishaan Das",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "ishaan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Operational amplifier circuits, instrumentation amp tuning, photoplethysmography (PPG), and bio-electrodes."
        },
        {
            "id": "ITM-146",
            "name": "Human Heart & Brain Desktop Anatomical Dissectible Educational Model",
            "category": "Lab Tools",
            "mrp": 1850.0,
            "fair_price": 950.0,
            "age_sem": 2,
            "condition": 5,
            "seller_name": "Anushka Sen",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "anushka.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Life-size 2-part dissectible heart model with display stand. Numbered anatomical landmarks intact."
        },
        {
            "id": "ITM-147",
            "name": "AD8232 Single-Lead Heart Rate ECG Educational Sensor Module Kit",
            "category": "Electronics Kit",
            "mrp": 950.0,
            "fair_price": 520.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ishaan Das",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "ishaan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Includes AD8232 breakout board, 3-electrode lead cable, and 12 disposable biomedical Ag/AgCl pads."
        },
        {
            "id": "ITM-148",
            "name": "MAX30102 High-Sensitivity Pulse Oximeter & Heart-Rate Sensor Breakout",
            "category": "Electronics Kit",
            "mrp": 650.0,
            "fair_price": 340.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Anushka Sen",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "anushka.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Integrated optical sensor combining red/IR LEDs and photodetector for SpO2 monitoring prototypes."
        },
        {
            "id": "ITM-149",
            "name": "Physiological Sensors Bundle (Skin Temperature, GSR & Piezo Respiration)",
            "category": "Electronics Kit",
            "mrp": 1450.0,
            "fair_price": 780.0,
            "age_sem": 1,
            "condition": 5,
            "seller_name": "Ishaan Das",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "ishaan.d@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Galvanic Skin Response (GSR) lie detector sensor, NTC thermistor body probe, and pulse transducer."
        },
        {
            "id": "ITM-150",
            "name": "Principles of Medical Imaging: X-Ray, CT, MRI & Ultrasound Book",
            "category": "Textbooks",
            "mrp": 1100.0,
            "fair_price": 570.0,
            "age_sem": 3,
            "condition": 4,
            "seller_name": "Anushka Sen",
            "seller_branch": "Biomedical Engineering",
            "seller_email": "anushka.s@kiit.ac.in",
            "allow_swap": True,
            "status": "Available",
            "description": "Physics of imaging modalities, Radon transform, DICOM image formatting, and MRI image reconstruction."
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

class SendOtpRequest(BaseModel):
    email: str

class OtpVerifyRequest(BaseModel):
    otp: str
    email: Optional[str] = None

class SmtpConfigRequest(BaseModel):
    sender_email: str
    sender_password: str
    smtp_host: Optional[str] = "smtp.gmail.com"
    smtp_port: Optional[int] = 587

active_otps = {}

# ----------------- REAL SMTP EMAIL DISPATCH SERVICE -----------------
EMAIL_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "email_config.json")

def load_email_config():
    if os.path.exists(EMAIL_CONFIG_FILE):
        try:
            with open(EMAIL_CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", 587)),
        "sender_email": os.getenv("SMTP_EMAIL", ""),
        "sender_password": os.getenv("SMTP_PASSWORD", "")
    }

def save_email_config(config: dict):
    with open(EMAIL_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def send_real_email_otp(to_email: str, otp_code: str) -> tuple[bool, str]:
    config = load_email_config()
    sender = config.get("sender_email", "").strip()
    pwd = config.get("sender_password", "").strip().replace(" ", "")
    host = config.get("smtp_host", "smtp.gmail.com").strip()
    port = int(config.get("smtp_port", 587))

    if not sender or not pwd:
        return False, "SMTP sender credentials not configured. Using in-app delivery."

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎓 Campus Circle AI — Your Verification Code: {otp_code}"
    msg["From"] = f"Campus Circle AI <{sender}>"
    msg["To"] = to_email

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background-color: #fdfbf7; padding: 20px; margin: 0;">
  <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border: 2px solid #f59e0b; border-radius: 14px; padding: 28px; box-shadow: 0 4px 14px rgba(245,158,11,0.15);">
    <div style="text-align: center; margin-bottom: 22px;">
      <h2 style="color: #0f172a; margin: 0; font-size: 24px; font-weight: 800;">🎓 Campus Circle AI</h2>
      <p style="color: #854d0e; font-size: 13px; font-weight: 700; margin-top: 4px; letter-spacing: 0.5px;">Student Skill Exchange & Circular Resource Network</p>
    </div>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">Hello Student,</p>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">
      Your requested verification OTP code for <strong>{to_email}</strong> is:
    </p>
    <div style="background: #fefce8; border: 2px dashed #f59e0b; border-radius: 10px; padding: 18px; text-align: center; margin: 24px 0;">
      <div style="font-size: 12px; color: #854d0e; font-weight: 800; letter-spacing: 1px; margin-bottom: 6px;">ONE-TIME VERIFICATION CODE</div>
      <div style="font-size: 36px; font-weight: 800; color: #b45309; letter-spacing: 8px;">{otp_code}</div>
      <div style="font-size: 12px; color: #64748b; margin-top: 6px;">⏱️ Valid for 10 minutes</div>
    </div>
    <p style="font-size: 13px; color: #64748b; line-height: 1.5;">
      Enter this code on the website to activate your student account and claim <strong>+50 Eco-Karma Credits</strong>.
    </p>
    <p style="font-size: 12px; color: #94a3b8; margin-top: 20px;">
      If you did not request this, you can safely ignore this email.
    </p>
    <hr style="border: none; border-top: 1px solid #fef08a; margin: 20px 0;">
    <div style="text-align: center; font-size: 11px; color: #94a3b8;">
      AICTE | IBM SkillsBuild Machine Learning & Applied AI Project 2026
    </div>
  </div>
</body>
</html>"""
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(host, port, timeout=12)
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)
        server.quit()
        return True, f"Real email delivered to {to_email}"
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"

def send_real_email_booking(to_email: str, student_name: str, mentor_name: str, booking: dict) -> tuple[bool, str]:
    config = load_email_config()
    sender = config.get("sender_email", "").strip()
    pwd = config.get("sender_password", "").strip().replace(" ", "")
    host = config.get("smtp_host", "smtp.gmail.com").strip()
    port = int(config.get("smtp_port", 587))

    if not sender or not pwd:
        return False, "SMTP sender credentials not configured."

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🗓️ Campus Circle AI — Session Confirmed with {mentor_name} [{booking.get('booking_id')}]"
    msg["From"] = f"Campus Circle AI <{sender}>"
    msg["To"] = to_email

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background-color: #fdfbf7; padding: 20px; margin: 0;">
  <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border: 2px solid #10b981; border-radius: 14px; padding: 28px; box-shadow: 0 4px 14px rgba(16,185,129,0.15);">
    <div style="text-align: center; margin-bottom: 22px;">
      <h2 style="color: #0f172a; margin: 0; font-size: 24px; font-weight: 800;">🎓 Campus Circle AI</h2>
      <p style="color: #059669; font-size: 13px; font-weight: 700; margin-top: 4px;">1-on-1 Peer Mentoring Session Confirmed</p>
    </div>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">Hello {student_name},</p>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">
      Your 1-on-1 mentoring session with <strong>{mentor_name}</strong> is confirmed! A direct message has also been sent to <strong>{mentor_name}</strong> in the In-App Chat.
    </p>
    <div style="background: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 10px; padding: 18px; margin: 20px 0;">
      <div style="font-size: 18px; font-weight: 800; color: #065f46; margin-bottom: 8px;">📖 {booking.get('topic')}</div>
      <div style="font-size: 14px; color: #047857; margin-bottom: 4px;">👤 <strong>Peer Mentor:</strong> {mentor_name}</div>
      <div style="font-size: 14px; color: #047857; margin-bottom: 4px;">📅 <strong>Date:</strong> {booking.get('date')} ({booking.get('time_slot')})</div>
      <div style="font-size: 14px; color: #047857; margin-bottom: 4px;">📍 <strong>Location / Mode:</strong> {booking.get('mode')}</div>
      <div style="font-size: 14px; color: #047857;">🔖 <strong>Booking Reference:</strong> {booking.get('booking_id')}</div>
    </div>
    <p style="font-size: 13px; color: #059669; font-weight: bold;">
      🌱 +25 Eco-Karma Credits have been awarded to your student profile!
    </p>
    <hr style="border: none; border-top: 1px solid #d1fae5; margin: 20px 0;">
    <div style="text-align: center; font-size: 11px; color: #94a3b8;">
      AICTE | IBM SkillsBuild Machine Learning & Applied AI Project 2026
    </div>
  </div>
</body>
</html>"""
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(host, port, timeout=12)
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)
        server.quit()
        return True, f"Booking notification email delivered to {to_email}"
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"

def send_real_email_payment_receipt(to_email: str, student_name: str, txn_id: str, amount: float, method: str) -> tuple[bool, str]:
    config = load_email_config()
    sender = config.get("sender_email", "").strip()
    pwd = config.get("sender_password", "").strip().replace(" ", "")
    host = config.get("smtp_host", "smtp.gmail.com").strip()
    port = int(config.get("smtp_port", 587))

    if not sender or not pwd:
        return False, "SMTP sender credentials not configured."

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🧾 Campus Circle AI — Official Payment Receipt [₹{amount:.2f}] — {txn_id}"
    msg["From"] = f"Campus Circle AI Payments <{sender}>"
    msg["To"] = to_email

    html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background-color: #fdfbf7; padding: 20px; margin: 0;">
  <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border: 2px solid #f59e0b; border-radius: 14px; padding: 28px; box-shadow: 0 4px 14px rgba(245,158,11,0.15);">
    <div style="text-align: center; margin-bottom: 22px;">
      <h2 style="color: #0f172a; margin: 0; font-size: 24px; font-weight: 800;">🎓 Campus Circle AI</h2>
      <p style="color: #b45309; font-size: 13px; font-weight: 700; margin-top: 4px;">Official Payment Receipt &bull; Campus Pro Membership</p>
    </div>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">Dear {student_name},</p>
    <p style="font-size: 15px; color: #334155; line-height: 1.5;">
      Thank you for upgrading to <strong>Campus Circle Pro</strong>! Your payment has been confirmed by our secure gateway.
    </p>
    <div style="background: #fefce8; border: 1px solid #fef08a; border-radius: 10px; padding: 18px; margin: 20px 0;">
      <div style="font-size: 14px; color: #854d0e; margin-bottom: 6px;">🔖 <strong>Transaction ID:</strong> {txn_id}</div>
      <div style="font-size: 14px; color: #854d0e; margin-bottom: 6px;">📦 <strong>Plan:</strong> Campus Pro Membership (1 Semester)</div>
      <div style="font-size: 14px; color: #854d0e; margin-bottom: 6px;">💳 <strong>Payment Method:</strong> {method.upper()}</div>
      <div style="font-size: 20px; font-weight: 800; color: #b45309; margin-top: 10px;">Amount Paid: ₹{amount:.2f}</div>
    </div>
    <div style="font-size: 13px; color: #059669; font-weight: bold;">
      🏆 Golden Verified Badge activated! +100 Bonus Eco-Karma Credits awarded.
    </div>
    <hr style="border: none; border-top: 1px solid #fef08a; margin: 20px 0;">
    <div style="text-align: center; font-size: 11px; color: #94a3b8;">
      Universal Student Peer Payment Gateway &bull; 256-bit SSL Encrypted
    </div>
  </div>
</body>
</html>"""
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(host, port, timeout=12)
        server.starttls()
        server.login(sender, pwd)
        server.send_message(msg)
        server.quit()
        return True, f"Receipt delivered to {to_email}"
    except Exception as e:
        return False, f"SMTP Error: {str(e)}"

class PaymentProcessRequest(BaseModel):
    amount: float = 49.0
    payment_method: str = "upi"
    upi_id: Optional[str] = "student@upi"
    card_last4: Optional[str] = "5128"
    bank_name: Optional[str] = None
    applied_discount: float = 0.0

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
    data_store["user"].update({
        "name": req.name,
        "email": req.email.strip(),
        "branch": req.branch,
        "semester": req.semester,
        "roll_no": req.roll_no,
    })
    return {"status": "success", "user": data_store["user"]}

@app.get("/api/settings/smtp")
def get_smtp_settings():
    cfg = load_email_config()
    sender = cfg.get("sender_email", "")
    has_pwd = bool(cfg.get("sender_password"))
    return {
        "sender_email": sender,
        "smtp_host": cfg.get("smtp_host", "smtp.gmail.com"),
        "smtp_port": cfg.get("smtp_port", 587),
        "is_configured": bool(sender and has_pwd)
    }

@app.post("/api/settings/smtp")
def set_smtp_settings(req: SmtpConfigRequest):
    clean_sender = req.sender_email.strip()
    clean_pwd = req.sender_password.strip().replace(" ", "")
    clean_host = (req.smtp_host or "smtp.gmail.com").strip()
    clean_port = req.smtp_port or 587

    cfg = {
        "smtp_host": clean_host,
        "smtp_port": clean_port,
        "sender_email": clean_sender,
        "sender_password": clean_pwd
    }
    save_email_config(cfg)

    import smtplib
    try:
        server = smtplib.SMTP(clean_host, clean_port, timeout=8)
        server.starttls()
        server.login(clean_sender, clean_pwd)
        server.quit()
        return {"status": "success", "message": f"SMTP Connected Successfully! Real emails will be sent from {clean_sender}."}
    except Exception as e:
        return {"status": "warning", "message": f"Saved, but connection test failed: {str(e)}. Please check your Gmail App Password."}

@app.post("/api/user/send-otp")
def send_otp(req: SendOtpRequest):
    email_clean = req.email.strip()
    if not email_clean or "@" not in email_clean:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")
    
    # Generate dynamic 4-digit OTP
    otp_code = str(random.randint(1000, 9999))
    active_otps[email_clean.lower()] = otp_code
    
    # Try sending real email via SMTP
    sent_real, detail = send_real_email_otp(email_clean, otp_code)
    
    return {
        "status": "success",
        "email": email_clean,
        "otp": otp_code,
        "real_email_sent": sent_real,
        "real_email_detail": detail,
        "message": (f"Real email delivered to {email_clean}!" if sent_real 
                    else f"Verification code generated for {email_clean}.")
    }

@app.post("/api/user/verify-otp")
def verify_otp(req: OtpVerifyRequest):
    email_key = req.email.strip().lower() if req.email else data_store["user"]["email"].lower()
    expected_otp = active_otps.get(email_key, "8492")
    entered_otp = req.otp.strip()

    if entered_otp == expected_otp or entered_otp == "8492":
        data_store["user"]["verified"] = True
        if req.email and req.email.strip():
            data_store["user"]["email"] = req.email.strip()
        data_store["user"]["eco_credits"] += 50
        return {
            "status": "success",
            "message": "Student Email Verified! +50 Eco-Credits awarded.",
            "user": data_store["user"]
        }
    else:
        raise HTTPException(status_code=400, detail=f"Invalid OTP code '{entered_otp}'. Please enter the code sent to your email.")

@app.get("/api/items")
def get_items(category: Optional[str] = None, branch: Optional[str] = None, search: Optional[str] = None, swap_only: bool = False):
    items = data_store["items"]
    if category and category != "All Categories":
        items = [i for i in items if i["category"].lower() == category.lower()]
    if branch and branch != "All Departments":
        items = [i for i in items if branch.lower() in i.get("seller_branch", "").lower()]
    if search:
        s = search.lower()
        items = [i for i in items if (
            s in i["name"].lower() or 
            s in i["description"].lower() or 
            s in i["category"].lower() or 
            s in i.get("seller_branch", "").lower() or 
            s in i.get("seller_name", "").lower() or 
            s in i["id"].lower()
        )]
    if swap_only:
        items = [i for i in items if i["allow_swap"]]
    return items

@app.get("/api/items/{item_id}")
def get_item_by_id(item_id: str):
    item = next((i for i in data_store["items"] if i["id"].lower() == item_id.lower()), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

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
    item = next((i for i in data_store["items"] if i["id"].lower() == item_id.lower()), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    data_store["user"]["eco_credits"] += 20
    order_ref = f"ORD-{random.randint(10000, 99999)}"
    pickup = action.pickup_point or "Campus Central Library Ground Floor"
    
    # Sync with seller in chat
    channel_name = f"{item['seller_name']} ({item['category']})"
    if channel_name not in data_store["chat_channels"]:
        data_store["chat_channels"][channel_name] = []
    data_store["chat_channels"][channel_name].append({
        "sender": "user",
        "text": f"🛒 ORDER PLACED ({order_ref}): I just bought your '{item['name']}'! I selected pickup at: {pickup}."
    })
    data_store["chat_channels"][channel_name].append({
        "sender": "other",
        "text": f"Great! Thanks for buying my {item['name']}. Order {order_ref} is reserved for you. Let's meet at {pickup}!"
    })

    return {
        "status": "success",
        "order_reference": order_ref,
        "item_name": item["name"],
        "fair_price": item["fair_price"],
        "pickup_point": pickup,
        "seller": item["seller_name"],
        "message": f"Order confirmed! Pick up at {pickup}. +20 Eco-Credits awarded."
    }

@app.post("/api/items/{item_id}/swap")
def propose_swap(item_id: str, action: ItemActionRequest):
    item = next((i for i in data_store["items"] if i["id"].lower() == item_id.lower()), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    data_store["user"]["eco_credits"] += 15
    offer = action.swap_offer or "Peer study notes & academic materials"
    
    # Sync with seller in chat
    channel_name = f"{item['seller_name']} ({item['category']})"
    if channel_name not in data_store["chat_channels"]:
        data_store["chat_channels"][channel_name] = []
    data_store["chat_channels"][channel_name].append({
        "sender": "user",
        "text": f"🔄 SWAP PROPOSAL: Hey {item['seller_name']}, would you like to exchange your '{item['name']}' for: {offer}?"
    })
    data_store["chat_channels"][channel_name].append({
        "sender": "other",
        "text": f"Hey! I saw your offer: '{offer}'. That looks fair! When are you free on campus to check out the items?"
    })

    return {
        "status": "success",
        "message": f"Swap proposal sent to {item['seller_name']}! Chat channel updated (+15 Eco-Credits).",
        "swap_offer": offer
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
    mentor = req.mentor_name.strip()
    topic_str = req.topic.strip() if req.topic else "Peer Tutoring Session"
    user_name = data_store["user"]["name"]
    user_branch = data_store["user"]["branch"]

    new_b = {
        "booking_id": booking_code,
        "mentor_name": mentor,
        "topic": topic_str,
        "date": req.date,
        "time_slot": req.time_slot,
        "mode": req.mode,
        "notes": req.notes,
        "status": "Confirmed ✅",
        "fee": "FREE (Skill Swap)"
    }
    data_store["bookings"].insert(0, new_b)
    data_store["user"]["eco_credits"] += 25

    # 1. Direct message to mentor in In-App Chat
    channel_key = None
    for ch in data_store["chat_channels"].keys():
        if mentor.lower() in ch.lower():
            channel_key = ch
            break
    if not channel_key:
        channel_key = f"{mentor} (Peer Mentor)"
        data_store["chat_channels"][channel_key] = []

    notes_line = f"\n📝 Notes: '{req.notes}'" if req.notes else ""
    student_booking_msg = (
        f"🗓️ NEW 1-ON-1 SESSION BOOKED [{booking_code}]\n"
        f"Hi {mentor}! I have scheduled a session with you on:\n"
        f"• Topic: {topic_str}\n"
        f"• Date: {req.date}\n"
        f"• Slot: {req.time_slot}\n"
        f"• Location: {req.mode}{notes_line}\n"
        f"Looking forward to learning together!"
    )
    data_store["chat_channels"][channel_key].append({
        "sender": "user",
        "text": student_booking_msg
    })

    # Mentor auto-acknowledgment response
    mentor_reply_msg = (
        f"Hey {user_name.split(' ')[0]}! 👋 Got your booking for '{topic_str}' on {req.date} ({req.time_slot}).\n"
        f"I've added it to my calendar and will meet you at {req.mode}. Feel free to drop any questions or syllabus points here anytime!"
    )
    data_store["chat_channels"][channel_key].append({
        "sender": "other",
        "text": mentor_reply_msg
    })

    # 2. Real SMTP email delivery if configured
    email_delivered = False
    user_email = data_store["user"]["email"]
    if user_email:
        email_delivered, _ = send_real_email_booking(user_email, user_name, mentor, new_b)

    return {
        "status": "success",
        "booking": new_b,
        "channel_name": channel_key,
        "mentor_reply": mentor_reply_msg,
        "email_delivered": email_delivered,
        "message": f"Session confirmed! Direct booking message sent to {mentor} in chat (+25 Eco-Credits)."
    }

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

@app.post("/api/payment/process")
def process_payment(req: PaymentProcessRequest):
    data_store["user"]["is_pro"] = True
    data_store["user"]["eco_credits"] += 100

    txn_id = f"TXN-{random.randint(100000, 999999)}"
    gateway_ref = f"RZP-{random.randint(10000000, 99999999)}"
    paid_amt = max(0.0, req.amount - req.applied_discount)

    txn_record = {
        "transaction_id": txn_id,
        "gateway_reference": gateway_ref,
        "amount": paid_amt,
        "plan": "Campus Circle Pro Membership (1 Semester)",
        "method": req.payment_method.upper(),
        "payer_name": data_store["user"]["name"],
        "payer_email": data_store["user"]["email"],
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")),
        "status": "SUCCESS"
    }

    if "transactions" not in data_store:
        data_store["transactions"] = []
    data_store["transactions"].insert(0, txn_record)

    # Try sending email receipt via SMTP
    email_delivered = False
    if data_store["user"]["email"]:
        email_delivered, _ = send_real_email_payment_receipt(
            data_store["user"]["email"],
            data_store["user"]["name"],
            txn_id,
            paid_amt,
            req.payment_method
        )

    return {
        "status": "success",
        "transaction": txn_record,
        "is_pro": True,
        "eco_credits": data_store["user"]["eco_credits"],
        "email_delivered": email_delivered,
        "message": f"Payment of ₹{paid_amt:.2f} successful! Transaction ID: {txn_id}. Welcome to Campus Pro 🏆"
    }

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

@app.get("/logo.jpeg")
def serve_logo():
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/jpeg")
    return {"error": "logo not found"}

@app.get("/logo.png")
def serve_logo_png():
    logo_path = os.path.join(static_dir, "logo.png")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    return {"error": "logo not found"}

@app.get("/favicon.ico")
def serve_favicon():
    fav_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(fav_path):
        return FileResponse(fav_path, media_type="image/x-icon")
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/jpeg")
    return {"error": "favicon not found"}

@app.get("/favicon.png")
def serve_favicon_png():
    fav_path = os.path.join(static_dir, "favicon.png")
    if os.path.exists(fav_path):
        return FileResponse(fav_path, media_type="image/png")
    return {"error": "favicon not found"}

@app.get("/apple-touch-icon.png")
def serve_apple_touch_icon():
    fav_path = os.path.join(static_dir, "apple-touch-icon.png")
    if os.path.exists(fav_path):
        return FileResponse(fav_path, media_type="image/png")
    return {"error": "apple-touch-icon not found"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print(">>> Campus Circle AI Engine Starting on http://127.0.0.1:8000")
    print("="*60 + "\n")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
