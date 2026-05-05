"""
data/hospital_data.py - Hospital Knowledge Base
================================================
This is the "database" for the RAG system. It contains all
the information the chatbot can answer questions about.

In a production system, this would be replaced by:
  - A SQL/PostgreSQL database with a query interface
  - PDF documents (patient handbooks, brochures) loaded via PyPDF2
  - A CMS or hospital information system API
  - A combination of all the above

Each document chunk has:
  - text:     The actual content the LLM will use as context
  - source:   Label shown to users as citation
  - category: Used for optional filtering

The chunks are designed to be self-contained paragraphs
(not too short, not too long — ~100-300 words each).
"""

from typing import List, Dict


def get_all_documents() -> List[Dict]:
    """Return all hospital knowledge chunks."""
    docs = []
    docs.extend(_timings())
    docs.extend(_departments())
    docs.extend(_fees())
    docs.extend(_doctors())
    docs.extend(_emergency())
    docs.extend(_diagnostics())
    docs.extend(_diseases())
    docs.extend(_pharmacy())
    docs.extend(_insurance())
    docs.extend(_appointments())
    docs.extend(_general_info())
    docs.extend(_hospital_kb())
    docs.extend(_doctor_profiles_kb())
    docs.extend(medical_info_kb())
    docs.extend(patient_programs_kb() )
    docs.extend(health_packages_kb())
    docs.extend(fee_structure_kb())
    docs.extend(emergency_services_kb())
    docs.extend(diagnostic_services_kb())
    docs.extend(inpatient_services_kb())    
    docs.extend(maternity_pediatrics_kb())
    docs.extend(mental_health_kb())
    return docs


# ─────────────────────────────────────────────
# TIMINGS
# ─────────────────────────────────────────────
def _timings():
    return [
        {
            "text": """City General Hospital operating hours:
- Main Hospital Building: Open 24 hours, 7 days a week (including public holidays)
- OPD (Outpatient Department): Monday to Saturday, 8:00 AM – 8:00 PM
- Emergency Department: Open 24/7, no appointment needed
- ICU and NICU: Visiting hours are 10:00 AM–12:00 PM and 5:00 PM–7:00 PM daily
- Administrative Office: Monday to Friday, 9:00 AM – 5:00 PM
- Billing & Accounts: Monday to Saturday, 8:00 AM – 6:00 PM""",
            "source": "Hospital Timings",
            "category": "timings"
        },
        {
            "text": """Department-specific OPD timings at City General Hospital:
- Cardiology OPD: Monday, Wednesday, Friday – 9:00 AM to 1:00 PM
- Orthopedics OPD: Tuesday, Thursday, Saturday – 9:00 AM to 2:00 PM
- Pediatrics OPD: Daily (Mon–Sat) – 9:00 AM to 12:00 PM and 4:00 PM to 6:00 PM
- Neurology OPD: Monday, Wednesday, Friday – 2:00 PM to 5:00 PM
- Gynecology & Obstetrics OPD: Daily – 9:00 AM to 1:00 PM
- Dermatology OPD: Tuesday, Thursday – 10:00 AM to 1:00 PM
- ENT OPD: Monday, Wednesday, Saturday – 9:00 AM to 12:00 PM
- Ophthalmology OPD: Tuesday, Thursday, Saturday – 9:00 AM to 1:00 PM
- Psychiatry OPD: Monday to Friday – 10:00 AM to 1:00 PM (by appointment only)
- General Surgery OPD: Monday to Saturday – 8:00 AM to 10:00 AM""",
            "source": "Department OPD Timings",
            "category": "timings"
        },
        {
            "text": """Lab and Diagnostic timings at City General Hospital:
- Pathology Laboratory: 24/7 for emergency tests; Routine tests: 6:00 AM to 8:00 PM
- Radiology (X-Ray, CT Scan, MRI): 7:00 AM to 10:00 PM daily; Emergency imaging 24/7
- Ultrasound: Monday to Saturday, 8:00 AM to 6:00 PM; Sunday 8:00 AM to 12:00 PM
- Echocardiography (ECG/Echo): Monday to Friday, 8:00 AM to 5:00 PM
- Blood Collection Center: 6:00 AM to 8:00 PM daily (fasting samples preferred before 10 AM)
- Pharmacy (Main): 24 hours, 7 days a week
- Pharmacy (Outpatient Branch): 8:00 AM to 9:00 PM daily""",
            "source": "Lab & Diagnostic Timings",
            "category": "timings"
        },
        {
            "text": """Visiting hours policy at City General Hospital:
- General Wards: 10:00 AM – 12:00 PM and 4:00 PM – 7:00 PM
- Private Rooms: Flexible visiting, attendant allowed 24/7 (one at a time)
- ICU/CCU: 10:00 AM – 11:00 AM and 5:00 PM – 6:00 PM (immediate family only)
- NICU (Newborn ICU): Parents may visit anytime; others restricted to 10 AM–12 PM
- COVID/Isolation Ward: No visitors allowed; video calls can be arranged through nursing station
- Children's Ward: Parents allowed 24/7; other visitors from 4 PM–6 PM only
Note: All visitors must register at the reception and wear visitor badges.""",
            "source": "Visiting Hours Policy",
            "category": "timings"
        }
    ]


# ─────────────────────────────────────────────
# DEPARTMENTS
# ─────────────────────────────────────────────
def _departments():
    return [
        {
            "text": """City General Hospital Departments Overview:
The hospital has the following clinical departments:
1. Cardiology – Heart conditions, ECG, stress tests, angiography
2. Neurology – Brain, spine, and nervous system disorders
3. Orthopedics – Bones, joints, fractures, spine surgery
4. Pediatrics – Child healthcare from newborn to 18 years
5. Gynecology & Obstetrics – Women's health, pregnancy, delivery
6. General Medicine – Internal medicine, fevers, infections
7. General Surgery – Appendix, hernia, gallbladder, laparoscopy
8. Oncology – Cancer diagnosis and treatment
9. Urology – Kidney, bladder, prostate conditions
10. Dermatology – Skin, hair, nail disorders
11. ENT (Ear, Nose, Throat) – Hearing, sinus, throat issues
12. Ophthalmology – Eye care, cataract, LASIK
13. Psychiatry & Psychology – Mental health, counseling
14. Endocrinology – Diabetes, thyroid, hormonal disorders
15. Pulmonology – Lungs, asthma, COPD
16. Gastroenterology – Digestive system, liver disorders
17. Nephrology – Kidney disease, dialysis
18. Rheumatology – Arthritis, autoimmune conditions
19. Anesthesiology – Surgical anesthesia, pain management
20. Radiology & Imaging – Diagnostic imaging services""",
            "source": "Hospital Departments",
            "category": "departments"
        },
        {
            "text": """Emergency and Critical Care at City General Hospital:
- Emergency Department (ED): Available 24/7 with trauma bays, resuscitation rooms
- Ambulance Services: Dial 108 or our hospital line +1-800-HOSPITAL for ambulance
- ICU (Intensive Care Unit): 20-bed unit with ventilator support, cardiac monitoring
- CCU (Cardiac Care Unit): Specialized 10-bed unit for heart patients
- NICU (Neonatal ICU): For premature and critically ill newborns
- PICU (Pediatric ICU): For critically ill children
- Trauma Center: Level II trauma center; handles road accidents, burns, major injuries
- Stroke Unit: Dedicated unit with rapid response within 60 minutes of symptom onset""",
            "source": "Emergency & Critical Care",
            "category": "departments"
        }
    ]


# ─────────────────────────────────────────────
# FEES
# ─────────────────────────────────────────────
def _fees():
    return [
        {
            "text": """OPD Consultation Fees at City General Hospital:
- General Physician / GP: ₹300 (new patient), ₹200 (follow-up within 7 days)
- Specialist Consultation (Cardiology, Neurology, Orthopedics, etc.): ₹600 (new), ₹400 (follow-up)
- Senior Consultant / HOD: ₹900 (new), ₹600 (follow-up)
- Pediatrics: ₹500 (new), ₹300 (follow-up)
- Gynecology & Obstetrics: ₹500 (new), ₹350 (follow-up)
- Psychiatry: ₹700 per session (approx. 45–60 minutes)
- Physiotherapy: ₹400 per session; package of 10 sessions ₹3,500
- Dietician: ₹300 per consultation
- Emergency OPD Visit: ₹500 (includes initial assessment)
Note: Above fees are subject to change. Senior citizens (60+) get 15% discount on OPD fees.""",
            "source": "OPD Consultation Fees",
            "category": "fees"
        },
        {
            "text": """Diagnostic Test Fees at City General Hospital:
- Complete Blood Count (CBC): ₹200
- Blood Sugar (Fasting/PP): ₹100 each
- HbA1c (Diabetes monitoring): ₹350
- Lipid Profile: ₹400
- Thyroid Profile (T3, T4, TSH): ₹500
- Liver Function Test (LFT): ₹450
- Kidney Function Test (KFT/RFT): ₹450
- Urine Routine: ₹100
- ECG (Electrocardiogram): ₹200
- 2D Echocardiography: ₹2,500
- Chest X-Ray: ₹350
- Ultrasound Abdomen: ₹800
- CT Scan (without contrast): ₹3,500 – ₹5,000 (depends on body part)
- MRI (without contrast): ₹5,000 – ₹8,000 (depends on body part)
- COVID RT-PCR Test: ₹500
- Pregnancy Test (urine): ₹100""",
            "source": "Diagnostic Test Fees",
            "category": "fees"
        },
        {
            "text": """Inpatient / Admission Charges at City General Hospital:
Room Types and Per-Day Charges:
- General Ward (6-bed): ₹1,500/day (includes nursing, meals, basic monitoring)
- Semi-Private Room (2-bed): ₹3,000/day
- Private Room: ₹5,000/day (includes AC, attached bathroom, TV, attendant cot)
- Deluxe Room: ₹7,500/day (includes enhanced amenities, mini-fridge)
- ICU: ₹8,000–₹15,000/day (depending on level of care and ventilator use)
- NICU: ₹6,000–₹12,000/day
- Surgery Packages (approximate, all-inclusive):
  * Appendectomy: ₹40,000–₹60,000
  * Cataract (per eye): ₹25,000–₹40,000
  * Hip Replacement: ₹1,20,000–₹1,80,000
  * Cardiac Bypass (CABG): ₹2,50,000–₹4,00,000
  * Normal Delivery: ₹20,000–₹30,000
  * C-Section Delivery: ₹35,000–₹50,000
Note: Surgery packages are approximate. Actual cost depends on surgeon, complexity, and stay duration.""",
            "source": "Inpatient & Surgery Fees",
            "category": "fees"
        }
    ]


# ─────────────────────────────────────────────
# DOCTORS
# ─────────────────────────────────────────────
def _doctors():
    return [
        {
            "text": """Senior Doctors at City General Hospital - Cardiology Department:
- Dr. Rajesh Sharma, MD, DM Cardiology – Head of Cardiology
  Specialization: Interventional Cardiology, Angioplasty, Pacemakers
  OPD: Monday, Wednesday, Friday – 9:00 AM to 12:00 PM
  Consultation Fee: ₹900

- Dr. Priya Nair, MD, DM Cardiology – Senior Cardiologist
  Specialization: Heart Failure, Echocardiography, Women's Heart Health
  OPD: Tuesday, Thursday – 9:00 AM to 1:00 PM
  Consultation Fee: ₹700

- Dr. Arun Kumar, MD – General Cardiologist
  OPD: Monday to Saturday – 9:00 AM to 11:00 AM
  Consultation Fee: ₹600""",
            "source": "Cardiology Doctors",
            "category": "doctors"
        },
        {
            "text": """Senior Doctors at City General Hospital - Orthopedics & Neurology:
Orthopedics:
- Dr. Suresh Patel, MS Orthopedics – HOD Orthopedics
  Specialization: Joint Replacement (Hip, Knee), Spine Surgery
  OPD: Tuesday, Thursday – 9:00 AM to 12:00 PM | Fee: ₹800

- Dr. Meena Rao, MS Orthopedics
  Specialization: Sports Injuries, Arthroscopy, Pediatric Orthopedics
  OPD: Wednesday, Saturday – 10:00 AM to 1:00 PM | Fee: ₹650

Neurology:
- Dr. Vikram Singh, DM Neurology – Head of Neurology
  Specialization: Stroke, Epilepsy, Parkinson's, Multiple Sclerosis
  OPD: Monday, Wednesday, Friday – 2:00 PM to 5:00 PM | Fee: ₹900

- Dr. Ananya Desai, DM Neurology
  Specialization: Headache Disorders, Dementia, Neuropathy
  OPD: Tuesday, Thursday – 2:00 PM to 5:00 PM | Fee: ₹700""",
            "source": "Orthopedics & Neurology Doctors",
            "category": "doctors"
        },
        {
            "text": """Senior Doctors at City General Hospital - Pediatrics & Gynecology:
Pediatrics:
- Dr. Kavitha Menon, MD Pediatrics – HOD Pediatrics
  Specialization: Neonatology, Pediatric Infections, Growth Disorders
  OPD: Monday to Friday – 9:00 AM to 12:00 PM | Fee: ₹700

- Dr. Ravi Joshi, DCH, MD Pediatrics
  Specialization: Childhood Asthma, Nutrition, Developmental Pediatrics
  OPD: Saturday – 9:00 AM to 1:00 PM; Weekdays 4:00 PM–6:00 PM | Fee: ₹500

Gynecology & Obstetrics:
- Dr. Sunita Agarwal, MS OB-GYN – HOD
  Specialization: High-risk Pregnancy, Laparoscopic Gynecology, Infertility
  OPD: Monday, Wednesday, Friday – 9:00 AM to 1:00 PM | Fee: ₹800

- Dr. Leela Thomas, MD OB-GYN
  Specialization: Normal & C-Section Delivery, PCOS, Menstrual Disorders
  OPD: Tuesday, Thursday, Saturday – 9:00 AM to 1:00 PM | Fee: ₹600""",
            "source": "Pediatrics & Gynecology Doctors",
            "category": "doctors"
        }
    ]


# ─────────────────────────────────────────────
# EMERGENCY
# ─────────────────────────────────────────────
def _emergency():
    return [
        {
            "text": """Emergency Contact Numbers - City General Hospital:
- Main Emergency Line: +1-800-HOSPITAL (24/7)
- Ambulance: 108 (toll-free) or +1-800-AMB-HELP
- Emergency Department Direct: +91-80-2234-5678
- Cardiac Emergency Hotline: +91-80-2234-5699
- Poison Control: +91-80-2234-5700
- Police (in case of accident): 100
- Fire: 101
- Women's Helpline: 1091

For cardiac arrest, stroke symptoms, major trauma, difficulty breathing, or unconsciousness — 
call 108 immediately or come to the Emergency entrance (Gate 2, open 24/7).

Do NOT wait for an OPD appointment in case of chest pain, severe headache, paralysis symptoms, 
high fever with stiff neck, heavy bleeding, or any life-threatening emergency.""",
            "source": "Emergency Contacts",
            "category": "emergency"
        }
    ]


# ─────────────────────────────────────────────
# DIAGNOSTIC SERVICES
# ─────────────────────────────────────────────
def _diagnostics():
    return [
        {
            "text": """Diagnostic Services available at City General Hospital:
Blood Tests:
- Routine blood work (CBC, ESR, blood group, blood sugar, lipid panel)
- Hormone panels (thyroid, insulin, cortisol, LH/FSH, testosterone)
- Tumour markers (PSA, CA-125, CEA, AFP)
- Infectious disease testing (HIV, Hepatitis B/C, Dengue, Malaria, Typhoid)
- COVID-19 RT-PCR and Rapid Antigen Test
- Genetic testing and chromosomal analysis (by referral)

Imaging Services:
- Digital X-Ray (all body parts)
- Ultrasound (abdomen, pelvis, obstetric, neck, small parts)
- Doppler Ultrasound (vascular)
- CT Scan (head, chest, abdomen, spine, angiography)
- MRI (brain, spine, joints, abdomen, cardiac MRI)
- PET Scan (available through referral to affiliated center)
- Mammography (for breast cancer screening)
- Bone Density Scan (DEXA)

Cardiac Diagnostics:
- ECG (Electrocardiogram)
- 24-hour Holter Monitoring
- Treadmill Test (TMT) / Stress Test
- 2D Echocardiography
- Cardiac Catheterization (in cath lab)

Endoscopy:
- Upper GI Endoscopy (gastroscopy)
- Colonoscopy
- Bronchoscopy
- Cystoscopy""",
            "source": "Diagnostic Services",
            "category": "diagnostics"
        }
    ]


# ─────────────────────────────────────────────
# DISEASES & MEDICAL INFO
# ─────────────────────────────────────────────
def _diseases():
    return [
        {
            "text": """Diabetes Mellitus - Information from City General Hospital:
What is Diabetes?
Diabetes is a chronic condition where the body cannot properly regulate blood sugar (glucose) levels.

Types:
- Type 1 Diabetes: Autoimmune condition; pancreas produces little/no insulin. Requires insulin injections.
- Type 2 Diabetes: Most common type; body doesn't use insulin effectively. Managed by diet, exercise, oral medication, or insulin.
- Gestational Diabetes: Occurs during pregnancy; increases risk of Type 2 diabetes later.
- Prediabetes: Blood sugar higher than normal but not yet diabetic range.

Common Symptoms:
Frequent urination, excessive thirst, unexplained weight loss, blurred vision, slow-healing wounds, numbness/tingling in hands/feet, frequent infections.

Diagnosis Tests Available at Our Hospital:
- Fasting Blood Sugar (normal: <100 mg/dL)
- HbA1c (normal: <5.7%; diabetic: ≥6.5%)
- Oral Glucose Tolerance Test (OGTT)

Consultation: Visit our Endocrinology or General Medicine OPD.
Department: Endocrinology – Dr. Neha Gupta, DM Endocrinology
OPD: Monday, Wednesday, Friday – 11:00 AM to 2:00 PM | Fee: ₹700""",
            "source": "Medical Info - Diabetes",
            "category": "diseases"
        },
        {
            "text": """Hypertension (High Blood Pressure) - Medical Information:
What is Hypertension?
Hypertension is when blood pressure consistently reads 130/80 mmHg or higher.

Categories:
- Normal: <120/80 mmHg
- Elevated: 120–129/<80 mmHg
- Stage 1 Hypertension: 130–139 / 80–89 mmHg
- Stage 2 Hypertension: ≥140/90 mmHg
- Hypertensive Crisis: >180/120 mmHg (medical emergency)

Risk Factors:
Age, obesity, smoking, excessive salt intake, lack of exercise, family history, chronic stress, kidney disease, diabetes.

Symptoms:
Often called the "silent killer" – most people have NO symptoms. Severe cases may cause headache, nosebleeds, shortness of breath, chest pain, or vision changes.

Complications if Untreated:
Heart attack, stroke, kidney failure, vision loss, heart failure.

Treatment:
Lifestyle changes (diet, exercise, weight loss) + medications (ACE inhibitors, beta-blockers, diuretics, etc.)

At Our Hospital: Visit Cardiology or General Medicine OPD for diagnosis and management.""",
            "source": "Medical Info - Hypertension",
            "category": "diseases"
        },
        {
            "text": """Heart Disease - Cardiology Information:
Common heart conditions treated at City General Hospital:

1. Coronary Artery Disease (CAD):
   Blockage of arteries supplying heart muscle. Symptoms: chest pain (angina), shortness of breath.
   Treatment: Lifestyle changes, medications, angioplasty, or bypass surgery (CABG).

2. Heart Failure:
   Heart cannot pump blood efficiently. Symptoms: swelling in legs, breathlessness, fatigue.
   Treatment: Medications, diet restrictions (low sodium), pacemaker, or transplant in severe cases.

3. Arrhythmia:
   Irregular heartbeat. Symptoms: palpitations, dizziness, fainting.
   Treatment: Medications, cardioversion, ablation, or pacemaker.

4. Heart Attack (Myocardial Infarction):
   EMERGENCY – blocked blood flow causes heart muscle death.
   Symptoms: Severe chest pain radiating to left arm, sweating, nausea.
   Action: Call 108 immediately. Every minute matters.

5. Valvular Heart Disease:
   Damaged heart valves affecting blood flow. May require valve repair or replacement surgery.

Available Tests: ECG, Echo, Stress Test, Angiography, Holter Monitor
Department: Cardiology – Available Monday to Saturday""",
            "source": "Medical Info - Heart Disease",
            "category": "diseases"
        },
        {
            "text": """Common Conditions Treated in General Medicine OPD:
- Fever (viral, bacterial infections, dengue, malaria, typhoid)
- Common Cold, Flu, Upper Respiratory Infections
- Urinary Tract Infections (UTI)
- Gastroenteritis (food poisoning, stomach infections)
- Anemia (low hemoglobin)
- Jaundice (Hepatitis A, B, C; liver disease)
- Dengue Fever: Symptoms include high fever, severe headache, joint pain, rash. Requires platelet monitoring.
- Malaria: Cyclical fever with chills; diagnosed by blood smear; treated with antimalarials.
- Typhoid: Prolonged fever with abdominal pain; treated with antibiotics.
- COVID-19: Respiratory symptoms, fever, loss of taste/smell; testing and treatment available.

When to seek emergency care:
- Fever >104°F / 40°C
- Difficulty breathing
- Altered consciousness
- Severe dehydration
- Rash with fever in children

General Medicine OPD: Monday to Saturday, 9:00 AM to 6:00 PM""",
            "source": "Medical Info - General Medicine",
            "category": "diseases"
        },
        {
            "text": """Bone and Joint Conditions - Orthopedics Information:
Common conditions treated at our Orthopedics Department:

1. Fractures: Treatment includes casting, splinting, or surgical fixation (ORIF) depending on severity.

2. Osteoarthritis: Wear-and-tear of joint cartilage. Common in knees, hips. Treatment: physiotherapy, pain medication, joint replacement for severe cases.

3. Rheumatoid Arthritis: Autoimmune joint inflammation. Treated by Rheumatology with DMARDs (Disease-Modifying Drugs).

4. Lower Back Pain:
   - Most common cause: Muscle strain or disc problems (herniated disc, spondylosis)
   - Treatment: Rest, physiotherapy, pain medication, rarely surgery
   - Red flags requiring immediate attention: Pain with fever, numbness in legs, bladder/bowel dysfunction

5. Osteoporosis: Brittle bones due to low bone density. Diagnosed by DEXA scan. Treated with calcium, Vitamin D, bisphosphonates. Common in postmenopausal women.

6. Sports Injuries: Sprains, ligament tears (ACL/PCL), rotator cuff injuries. Treatment: RICE method, physiotherapy, arthroscopic surgery if needed.

Orthopedics OPD: Tuesday, Thursday, Saturday – 9:00 AM to 2:00 PM
Physiotherapy Center: Monday to Saturday, 8:00 AM to 6:00 PM""",
            "source": "Medical Info - Orthopedics",
            "category": "diseases"
        },
        {
            "text": """Neurological Conditions - Information from Neurology Department:
Common conditions treated:

1. Stroke:
   EMERGENCY – occurs when blood supply to part of the brain is cut off.
   Warning signs (FAST): Face drooping, Arm weakness, Speech difficulty, Time to call 108.
   Treatment: Clot-busting drugs (within 4.5 hours) or endovascular procedure.
   Our hospital has a dedicated Stroke Unit with 24/7 CT scan.

2. Epilepsy / Seizures:
   Recurrent unprovoked seizures. Managed with antiepileptic medications.
   First seizure should be evaluated urgently.

3. Migraines:
   Severe throbbing headaches, often with nausea, light/sound sensitivity.
   Treatment: Triptan medications, preventive therapy, lifestyle changes.

4. Parkinson's Disease:
   Progressive movement disorder. Symptoms: tremors, stiffness, slow movement.
   Managed with levodopa and other medications; physiotherapy important.

5. Multiple Sclerosis (MS):
   Autoimmune disease affecting brain and spinal cord. Treated with disease-modifying therapies.

6. Dementia / Alzheimer's:
   Progressive memory and cognitive decline. No cure; management focuses on quality of life.

Neurology OPD: Monday–Friday, 2:00 PM to 5:00 PM
MRI and EEG services available on-site.""",
            "source": "Medical Info - Neurology",
            "category": "diseases"
        },
        {
            "text": """Children's Health - Pediatrics Information:
Common conditions in children treated at City General Hospital:

Newborn Care:
- Jaundice in newborns (phototherapy available)
- Low birth weight / Premature birth (NICU available)
- Feeding difficulties

Infections (very common in children):
- Viral Fever, Hand-Foot-Mouth Disease, Chicken Pox
- Ear Infections (Otitis Media)
- Strep Throat, Tonsillitis
- Pneumonia and Bronchiolitis

Chronic Conditions:
- Childhood Asthma: Managed with inhalers, avoiding triggers
- Allergies (food, environmental)
- Type 1 Diabetes
- ADHD and Developmental Delays (assessed by Developmental Pediatrician + Psychologist)

Vaccinations:
City General Hospital follows the Indian National Immunization Schedule.
Vaccines available: BCG, OPV, Pentavalent, Rotavirus, PCV, MMR, Typhoid, Hepatitis A, Chicken Pox, HPV (for girls 9–14 years).
Vaccination clinic: Monday, Wednesday, Friday – 9:00 AM to 12:00 PM

When to bring your child immediately:
- Fever >101°F in infants <3 months
- Difficulty breathing, bluish lips
- Severe dehydration, not urinating
- Seizures, loss of consciousness""",
            "source": "Medical Info - Pediatrics",
            "category": "diseases"
        }
    ]


# ─────────────────────────────────────────────
# PHARMACY
# ─────────────────────────────────────────────
def _pharmacy():
    return [
        {
            "text": """Pharmacy Services at City General Hospital:
Main Pharmacy (24/7):
- Located at Ground Floor, near Emergency Exit
- Dispenses all prescribed medications
- Stocks generic and branded medicines
- Chemotherapy drugs available (by prescription)

Outpatient Pharmacy Branch:
- Hours: 8:00 AM to 9:00 PM
- Located near OPD Block, Building B

Services:
- Prescription dispensing
- Medication counseling (speak to hospital pharmacist)
- Home delivery for inpatients' families: Available on request
- Compounding (special preparations): Available for specific cases

Drug Return Policy:
- Sealed/unopened medicines can be returned within 3 days with receipt
- Schedule H/H1 drugs require valid prescription
- Emergency medications available without prior appointment (billed to patient account)

Contact: pharmacy@citygeneralhospital.com | Ext: 105""",
            "source": "Pharmacy Services",
            "category": "pharmacy"
        }
    ]


# ─────────────────────────────────────────────
# INSURANCE
# ─────────────────────────────────────────────
def _insurance():
    return [
        {
            "text": """Health Insurance & Cashless Treatment at City General Hospital:
We are empanelled with the following insurance providers:
- Ayushman Bharat (PMJAY) – Government scheme for below poverty line patients
- CGHS (Central Government Health Scheme)
- ECHS (Ex-servicemen Contributory Health Scheme)
- Star Health Insurance
- HDFC ERGO Health
- New India Assurance
- United India Insurance
- Bajaj Allianz Health Insurance
- Religare (Care) Health Insurance
- Max Bupa (now Niva Bupa)
- ICICI Lombard Health Insurance

Cashless Process:
1. Present your insurance card and policy document at the Insurance Desk (Ground Floor)
2. Our TPA (Third Party Administrator) team will process pre-authorization
3. Processing time: 2–4 hours for planned admissions, 30 minutes for emergencies
4. Co-payment (if applicable) will be collected at discharge

Insurance Helpdesk Timings: Monday to Saturday, 8:00 AM to 6:00 PM
Contact: insurance@citygeneralhospital.com | Ext: 210""",
            "source": "Insurance & Cashless",
            "category": "insurance"
        }
    ]


# ─────────────────────────────────────────────
# APPOINTMENTS
# ─────────────────────────────────────────────
def _appointments():
    return [
        {
            "text": """How to Book an Appointment at City General Hospital:
Online Booking:
- Website: www.citygeneralhospital.com/appointments
- Mobile App: City General Hospital app (available on iOS and Android)
- WhatsApp: Send "APPOINTMENT" to +91-98765-43210

Phone Booking:
- Call: +1-800-HOSPITAL (Mon–Sat, 8 AM–8 PM)
- Our team will confirm doctor availability and slot

Walk-in:
- OPD Registration Counter: Open Mon–Sat, 7:30 AM (before OPD starts)
- Token-based system; arrive 30 minutes early for first-come-first-served departments

What to Bring:
- Government ID proof
- Previous medical records, reports, prescriptions
- Insurance card (if applicable)
- Referral letter (if referred by another doctor)

Cancellation Policy:
- Cancel at least 2 hours before appointment to avoid non-refundable booking fee
- Rescheduling available up to 3 times per appointment""",
            "source": "Appointment Booking",
            "category": "appointments"
        }
    ]


# ─────────────────────────────────────────────
# GENERAL INFO
# ─────────────────────────────────────────────
def _general_info():
    return [
        {
            "text": """About City General Hospital:
City General Hospital is a 500-bed multi-specialty tertiary care hospital established in 1985.
We are accredited by NABH (National Accreditation Board for Hospitals) and ISO 9001:2015 certified.

Location:
123, Healthcare Avenue, Medical District, New Delhi – 110001
Landmark: Opposite Central Metro Station, Exit Gate 4

Parking: Multi-level parking available (₹20/hour); free for ambulances and emergency vehicles

Facilities:
- Cafeteria (Ground Floor): 7:00 AM to 10:00 PM
- ATM: Available 24/7 at main entrance
- Wheelchair and porter services: Available at all entrances
- Chapel / Prayer Room: Second floor, open all day
- Wi-Fi: Complimentary in OPD and waiting areas (Network: CGH-Guest)
- Helpdesk: Main entrance, Ground Floor – available 8 AM to 8 PM

Telemedicine:
- Video consultations available for follow-up appointments
- Platform: Available through our website and app
- Timings: 6:00 PM to 9:00 PM (evening hours for working patients)
- Fee: 80% of regular consultation fee""",
            "source": "About the Hospital",
            "category": "general"
        },
        {
            "text": """Patient Rights and Hospital Policies:
Patient Rights:
- Right to receive respectful, non-discriminatory care
- Right to be informed about diagnosis, treatment options, and costs
- Right to refuse treatment (with consequences explained)
- Right to privacy and confidentiality of medical records
- Right to access your medical records (written request required, 3–5 working days)

Grievance Redressal:
- Patient Relations Officer: Available Mon–Fri, 9 AM–5 PM (Room 14, Admin Block)
- Complaint/Suggestion Box: Near OPD registration
- Email: feedback@citygeneralhospital.com
- Expected response time: Within 72 hours

Hospital Policies:
- No smoking anywhere on hospital premises
- Maintain silence in clinical areas
- Attendants must carry valid ID
- Food from outside allowed in private rooms only
- Mobile phones on silent mode in clinical areas
- Children under 12 not permitted in ICU/OT areas""",
            "source": "Patient Rights & Policies",
            "category": "general"
        }
    ]
    
    
def _hospital_kb():
    return [
        {
            "text": "The Cardiology Department provides comprehensive care for heart-related conditions, including Coronary Artery Disease (CAD), arrhythmias, heart failure, and hypertension. Our facility is equipped with a state-of-the-art flat-panel Cath Lab, 3D Echocardiography, and TMT machines. Available procedures include angiography, angioplasty, pacemaker implantation, and bypass surgery consults. Location: 1st Floor, Block A. OPD timings: Monday to Saturday, 9:00 AM - 2:00 PM. Emergency availability: Yes, 24/7 cardiac emergency and chest pain clinic. Consultation Fee: ₹1500. Head of Department: Dr. Arvind Patel, MD, DM (Cardiology).",
            "source": "Department - Cardiology",
            "category": "departments"
        },
 {
        "text": "The Neurology Department specializes in the diagnosis and management of disorders affecting the brain, spinal cord, and nerves. We treat conditions such as stroke, epilepsy, Parkinson's disease, multiple sclerosis, and complex migraines. Available technologies include 3T MRI, EEG, EMG, and Nerve Conduction Velocity (NCV) testing. Procedures encompass stroke thrombolysis and botox therapy for movement disorders. Location: 2nd Floor, Block A. OPD timings: Monday, Wednesday, and Friday, 10:00 AM - 4:00 PM. Emergency availability: Yes, acute stroke ready. Consultation Fee: ₹1800. Head of Department: Dr. Meena Subramaniam, MD, DM (Neurology).",
        "source": "Department - Neurology",
        "category": "departments"
    },
    {
        "text": "The Orthopedics Department is dedicated to musculoskeletal health, treating bone fractures, osteoarthritis, sports injuries, and spinal disorders. Our advanced technologies include a NAVIO Robotic joint replacement system, minimally invasive arthroscopy suites, and high-frequency C-arm fluoroscopy. We routinely perform total knee and hip replacements, ACL reconstructions, and complex trauma surgeries. Location: Ground Floor, Block B. OPD timings: Monday to Saturday, 8:00 AM - 1:00 PM. Emergency availability: Yes, 24/7 dedicated trauma care. Consultation Fee: ₹1200. Head of Department: Dr. Vikram Sharma, MS (Orthopedics), DNB.",
        "source": "Department - Orthopedics",
        "category": "departments"
    },
    {
        "text": "The Oncology Department offers multidisciplinary cancer care, treating solid tumors (breast, lung, GI) and hematological malignancies (leukemia, lymphoma). We feature a TrueBeam Linear Accelerator (LINAC) for precise radiation therapy, PET-CT imaging, and a dedicated 20-bed chemotherapy daycare suite. Treatments include chemotherapy, targeted therapy, immunotherapy, and palliative care. Location: Basement 1, Cancer Wing. OPD timings: Tuesday, Thursday, and Saturday, 9:00 AM - 3:00 PM. Emergency availability: No (On-call support for registered patients only). Consultation Fee: ₹2000. Head of Department: Dr. Rajeev Menon, MD, DM (Medical Oncology).",
        "source": "Department - Oncology",
        "category": "departments"
    },
    {
        "text": "The Nephrology Department focuses on kidney health, managing Chronic Kidney Disease (CKD), Acute Kidney Injury (AKI), kidney stones, and hypertensive nephropathy. Our state-of-the-art 30-bed dialysis unit features reverse osmosis water purification and hemodiafiltration capability. We offer in-center hemodialysis, Continuous Renal Replacement Therapy (CRRT), and kidney transplant workup/post-op care. Location: 3rd Floor, Block B. OPD timings: Monday to Friday, 10:00 AM - 2:00 PM. Emergency availability: Yes, 24/7 emergency dialysis. Consultation Fee: ₹1600. Head of Department: Dr. Sunita Agarwal, MD, DM (Nephrology).",
        "source": "Department - Nephrology",
        "category": "departments"
    },
    {
        "text": "The Gastroenterology Department treats digestive system and liver disorders, including Irritable Bowel Syndrome (IBS), liver cirrhosis, peptic ulcers, and acute pancreatitis. Our endoscopy suite is equipped with high-definition optical systems. Available procedures include diagnostic and therapeutic Upper GI Endoscopy, Colonoscopy, ERCP for bile duct issues, and FibroScan for liver staging. Location: 1st Floor, Block C. OPD timings: Monday, Tuesday, Thursday, and Friday, 9:00 AM - 1:00 PM. Emergency availability: Yes, GI bleed protocol active. Consultation Fee: ₹1500. Head of Department: Dr. Anil Deshmukh, MD, DM (Gastroenterology).",
        "source": "Department - Gastroenterology",
        "category": "departments"
    },
    {
        "text": "The Pulmonology Department provides specialized care for respiratory tract diseases, including severe asthma, COPD, tuberculosis, pneumonia, and Interstitial Lung Disease (ILD). Our respiratory lab is equipped with advanced Pulmonary Function Testing (PFT), a Level 1 Sleep Lab for sleep apnea studies, and rigid/flexible bronchoscopy video systems. Location: 2nd Floor, Block C. OPD timings: Wednesday, Friday, and Saturday, 10:00 AM - 3:00 PM. Emergency availability: Yes, dedicated respiratory ICU access. Consultation Fee: ₹1400. Head of Department: Dr. Sneha Reddy, MD (Pulmonology/Respiratory Medicine).",
        "source": "Department - Pulmonology",
        "category": "departments"
    },
    {
        "text": "The Rheumatology Department manages systemic autoimmune and inflammatory conditions affecting the joints and connective tissues. We actively treat Rheumatoid Arthritis, Systemic Lupus Erythematosus (SLE), Ankylosing Spondylitis, and gout. We utilize high-resolution musculoskeletal ultrasound for early detection of joint inflammation and an advanced immunology lab for precise autoantibody profiling. Infusion therapies are administered in our dedicated lounge. Location: 3rd Floor, Block A. OPD timings: Tuesday and Thursday, 11:00 AM - 4:00 PM. Emergency availability: No. Consultation Fee: ₹1800. Head of Department: Dr. Kiran Gupta, MD, DM (Rheumatology).",
        "source": "Department - Rheumatology",
        "category": "departments"
    }
]

def _doctor_profiles_kb():
    return [
    
    {
        "text": "Dr. Arvind Patel is the Head of Department (HOD) for Cardiology. Qualifications: MBBS, MD (General Medicine), DM (Cardiology). He has 25 years of experience specializing in Interventional Cardiology, Complex Angioplasties, and Heart Failure Management. He holds a prestigious fellowship in structural heart diseases from the UK. OPD Schedule: Monday to Friday, 9:00 AM - 1:00 PM. Room Number: 101. Languages spoken: English, Hindi, Gujarati. Consultation Fee: ₹1500 (New), ₹1000 (Follow-up).",
        "source": "Doctor Profile - Dr. Arvind Patel",
        "category": "doctors"
    },
    {
        "text": "Dr. Sunita Rao is a Senior Consultant in the Cardiology department. Qualifications: MBBS, MD (Medicine), DNB (Cardiology). With 18 years of experience, her specific areas of expertise include Echocardiography, Preventive Cardiology, and Women's Cardiovascular Health. She was awarded the Young Cardiologist Award by the Cardiological Society of India. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 4:00 PM. Room Number: 104. Languages spoken: English, Hindi, Kannada, Telugu. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Sunita Rao",
        "category": "doctors"
    },
    {
        "text": "Dr. Vivek Sharma is a Consultant in Cardiology. Qualifications: MBBS, MD, DM (Cardiology). He brings 10 years of experience, focusing on Electrophysiology, Arrhythmia Management, and Pacemaker Implantation. He recently completed specialized training in leadless pacemaker insertion. OPD Schedule: Monday, Wednesday, Friday, 2:00 PM - 6:00 PM. Room Number: 107. Languages spoken: English, Hindi, Marathi. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Vivek Sharma",
        "category": "doctors"
    },
    {
        "text": "Dr. Kavita Desai is a Consultant in the Cardiology department. Qualifications: MBBS, MD, Fellowship in Non-Invasive Cardiology. With 8 years of experience, she specializes in Pediatric Cardiology, Fetal Echocardiography, and Congenital Heart Defects. She authored a textbook chapter on pediatric murmurs. OPD Schedule: Monday to Thursday, 9:00 AM - 1:00 PM. Room Number: 109. Languages spoken: English, Hindi, Gujarati, Marathi. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Kavita Desai",
        "category": "doctors"
    },
    {
        "text": "Dr. Meena Subramaniam is the Head of Department (HOD) for Neurology. Qualifications: MBBS, MD (Medicine), DM (Neurology). She has 22 years of experience and specializes in Stroke Management, Epilepsy, and Parkinson's Disease. She established the hospital's first comprehensive stroke center. OPD Schedule: Monday, Wednesday, Friday, 10:00 AM - 3:00 PM. Room Number: 201. Languages spoken: English, Hindi, Tamil, Kannada. Consultation Fee: ₹1800 (New), ₹1200 (Follow-up).",
        "source": "Doctor Profile - Dr. Meena Subramaniam",
        "category": "doctors"
    },
    {
        "text": "Dr. Rakesh Kadam is a Senior Consultant in Neurology. Qualifications: MBBS, MD, DNB (Neurology). With 15 years of experience, he focuses on Neuromuscular Disorders, Migraine management, and Dementia. He underwent advanced training in Botulinum Toxin therapy for movement disorders in Germany. OPD Schedule: Tuesday, Thursday, Saturday, 9:00 AM - 2:00 PM. Room Number: 203. Languages spoken: English, Hindi, Marathi. Consultation Fee: ₹1400 (New), ₹900 (Follow-up).",
        "source": "Doctor Profile - Dr. Rakesh Kadam",
        "category": "doctors"
    },
    {
        "text": "Dr. Neha Joshi is a Consultant in the Neurology department. Qualifications: MBBS, MD (Medicine), DM (Neurology). She brings 12 years of experience, specializing in Multiple Sclerosis, Autoimmune Encephalitis, and Neuro-immunology. She has published over 20 peer-reviewed papers on demyelinating diseases. OPD Schedule: Monday to Saturday, 2:00 PM - 5:00 PM. Room Number: 205. Languages spoken: English, Hindi, Marathi. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Neha Joshi",
        "category": "doctors"
    },
    {
        "text": "Dr. Imran Khan is a Consultant in Neurology. Qualifications: MBBS, MD, DM (Neurology). With 9 years of experience, he specializes in Sleep Disorders, Restless Leg Syndrome, and Neurophysiology (EEG/EMG). He completed a fellowship in sleep medicine at AIIMS. OPD Schedule: Monday, Wednesday, Friday, 4:00 PM - 8:00 PM. Room Number: 208. Languages spoken: English, Hindi, Urdu. Consultation Fee: ₹1100 (New), ₹750 (Follow-up).",
        "source": "Doctor Profile - Dr. Imran Khan",
        "category": "doctors"
    },
    {
        "text": "Dr. Vikram Sharma is the Head of Department (HOD) for Orthopedics. Qualifications: MBBS, MS (Orthopedics), MCh (Orthopedics). With 28 years of experience, his specialties include Robotic Joint Replacement, Complex Trauma Surgery, and Pelvic Acetabular fractures. He is a pioneer in computer-navigated knee replacements in the region. OPD Schedule: Monday to Friday, 8:00 AM - 1:00 PM. Room Number: 301. Languages spoken: English, Hindi, Punjabi. Consultation Fee: ₹1600 (New), ₹1100 (Follow-up).",
        "source": "Doctor Profile - Dr. Vikram Sharma",
        "category": "doctors"
    },
    {
        "text": "Dr. Anil Shetty is a Senior Consultant in Orthopedics. Qualifications: MBBS, MS (Orthopedics), Fellowship in Sports Medicine. He has 20 years of experience, specializing in Arthroscopy, ACL Reconstruction, and Sports Injuries. He serves as the official medical consultant for the state cricket association. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 4:00 PM. Room Number: 305. Languages spoken: English, Hindi, Kannada, Tulu. Consultation Fee: ₹1300 (New), ₹900 (Follow-up).",
        "source": "Doctor Profile - Dr. Anil Shetty",
        "category": "doctors"
    },
    {
        "text": "Dr. Priya Rajan is a Consultant in the Orthopedics department. Qualifications: MBBS, MS (Orthopedics). With 14 years of experience, she focuses on Pediatric Orthopedics, Clubfoot correction, and Scoliosis management. She has specialized training in Ponseti casting for clubfoot. OPD Schedule: Monday, Wednesday, Friday, 9:00 AM - 2:00 PM. Room Number: 308. Languages spoken: English, Hindi, Tamil. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Priya Rajan",
        "category": "doctors"
    },
    {
        "text": "Dr. Rohan Kapoor is a Consultant in Orthopedics. Qualifications: MBBS, MS (Orthopedics), Fellowship in Hand Surgery. He brings 7 years of experience, specializing in Hand and Microvascular Surgery, Carpal Tunnel Syndrome, and Tendon repairs. He was awarded the best paper at the Indian Orthopedic Association conference. OPD Schedule: Tuesday, Thursday, Saturday, 2:00 PM - 6:00 PM. Room Number: 310. Languages spoken: English, Hindi. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Rohan Kapoor",
        "category": "doctors"
    },
    {
        "text": "Dr. Anjali Mehta is the Director of the Gynecology department. Qualifications: MBBS, MD (Obstetrics & Gynecology), FRCOG (UK). She has 30 years of experience, specializing in High-Risk Pregnancies, Infertility Management (IVF), and Minimally Invasive Gynecological Surgeries. She is a recognized national board examiner. OPD Schedule: Monday, Wednesday, Friday, 10:00 AM - 2:00 PM. Room Number: 401. Languages spoken: English, Hindi, Gujarati. Consultation Fee: ₹2000 (New), ₹1500 (Follow-up).",
        "source": "Doctor Profile - Dr. Anjali Mehta",
        "category": "doctors"
    },
    {
        "text": "Dr. Shilpa Bhat is a Senior Consultant in Gynecology. Qualifications: MBBS, MS (OBG), Diploma in Reproductive Medicine. With 16 years of experience, her areas of expertise include Laparoscopic Hysterectomy, Endometriosis management, and PCOS. She holds advanced certification in advanced pelvic endoscopy. OPD Schedule: Tuesday, Thursday, Saturday, 9:00 AM - 3:00 PM. Room Number: 404. Languages spoken: English, Hindi, Kannada, Konkani. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Shilpa Bhat",
        "category": "doctors"
    },
    {
        "text": "Dr. Radhika Nair is a Consultant in the Gynecology department. Qualifications: MBBS, DNB (OBG). She has 11 years of experience, specializing in Urogynecology, Pelvic Floor Prolapse, and Maternal-Fetal Medicine. She completed an intensive fellowship in urogynecology in Chennai. OPD Schedule: Monday to Friday, 4:00 PM - 8:00 PM. Room Number: 406. Languages spoken: English, Hindi, Malayalam. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Radhika Nair",
        "category": "doctors"
    },
    {
        "text": "Dr. Snehal Kulkarni is a Consultant in Gynecology. Qualifications: MBBS, MS (OBG). With 9 years of experience, she focuses on Adolescent Gynecology, Menopause Management, and Preventive Cervical Cancer Screening. She runs the hospital's dedicated adolescent health clinic. OPD Schedule: Monday, Wednesday, Friday, 9:00 AM - 1:00 PM. Room Number: 408. Languages spoken: English, Hindi, Marathi. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Snehal Kulkarni",
        "category": "doctors"
    },
    {
        "text": "Dr. Rajesh Iyer is the Head of Department (HOD) for Pediatrics. Qualifications: MBBS, MD (Pediatrics), Fellowship in Neonatology. With 24 years of experience, he specializes in Neonatal Intensive Care (NICU), Extreme Prematurity, and Pediatric Asthma. He was instrumental in upgrading the hospital's Level 3 NICU. OPD Schedule: Monday to Saturday, 9:00 AM - 12:00 PM. Room Number: 501. Languages spoken: English, Hindi, Tamil. Consultation Fee: ₹1500 (New), ₹1000 (Follow-up).",
        "source": "Doctor Profile - Dr. Rajesh Iyer",
        "category": "doctors"
    },
    {
        "text": "Dr. Farah Ahmed is a Senior Consultant in the Pediatrics department. Qualifications: MBBS, MD (Pediatrics), DCH. She has 17 years of experience, focusing on Pediatric Infectious Diseases, Growth & Development Assessment, and Immunization protocols. She previously worked with WHO on regional polio eradication campaigns. OPD Schedule: Monday, Wednesday, Friday, 2:00 PM - 6:00 PM. Room Number: 503. Languages spoken: English, Hindi, Urdu, Kannada. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Farah Ahmed",
        "category": "doctors"
    },
    {
        "text": "Dr. Aditya Verma is a Consultant in Pediatrics. Qualifications: MBBS, MD (Pediatrics), Fellowship in Pediatric Endocrinology. He brings 12 years of experience, specializing in Type 1 Diabetes in children, Short Stature, and Thyroid Disorders. He established the first specialized pediatric endocrine clinic in the district. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 2:00 PM. Room Number: 505. Languages spoken: English, Hindi. Consultation Fee: ₹1100 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Aditya Verma",
        "category": "doctors"
    },
    {
        "text": "Dr. Rajeev Menon is the Head of Department (HOD) for Oncology. Qualifications: MBBS, MD (Medicine), DM (Medical Oncology). With 26 years of experience, his specialties include Breast Cancer, Gastrointestinal Malignancies, and Targeted Immunotherapy. He is a primary investigator in several international clinical trials for targeted cancer drugs. OPD Schedule: Monday, Wednesday, Friday, 10:00 AM - 3:00 PM. Room Number: 601. Languages spoken: English, Hindi, Malayalam. Consultation Fee: ₹2000 (New), ₹1400 (Follow-up).",
        "source": "Doctor Profile - Dr. Rajeev Menon",
        "category": "doctors"
    },
    {
        "text": "Dr. Pooja Reddy is a Senior Consultant in Oncology. Qualifications: MBBS, MS (General Surgery), MCh (Surgical Oncology). She has 19 years of experience, focusing on Head and Neck Cancers, Breast Conservation Surgery, and Gynecological Oncology. She holds a prestigious robotic surgery certification from the USA. OPD Schedule: Tuesday, Thursday, Saturday, 9:00 AM - 2:00 PM. Room Number: 604. Languages spoken: English, Hindi, Telugu. Consultation Fee: ₹1800 (New), ₹1200 (Follow-up).",
        "source": "Doctor Profile - Dr. Pooja Reddy",
        "category": "doctors"
    },
    {
        "text": "Dr. Suresh Pillai is a Consultant in the Oncology department. Qualifications: MBBS, MD (Radiotherapy), DNB. With 13 years of experience, he specializes in Radiation Oncology, Brachytherapy, and Stereotactic Body Radiation Therapy (SBRT). He was crucial in implementing the TrueBeam LINAC system at the hospital. OPD Schedule: Monday to Friday, 2:00 PM - 6:00 PM. Room Number: 607 (Radiation Wing). Languages spoken: English, Hindi, Tamil. Consultation Fee: ₹1500 (New), ₹1000 (Follow-up).",
        "source": "Doctor Profile - Dr. Suresh Pillai",
        "category": "doctors"
    },
    {
        "text": "Dr. Kiran Gupta is a Consultant in Oncology. Qualifications: MBBS, MD (Medicine), DM (Medical Oncology). He brings 8 years of experience, specializing in Hematological Malignancies (Leukemia/Lymphoma) and Bone Marrow Transplants. He trained extensively at Tata Memorial Hospital. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 4:00 PM. Room Number: 609. Languages spoken: English, Hindi. Consultation Fee: ₹1400 (New), ₹900 (Follow-up).",
        "source": "Doctor Profile - Dr. Kiran Gupta",
        "category": "doctors"
    },
    {
        "text": "Dr. Mahesh Jha is the Head of Department (HOD) for Urology. Qualifications: MBBS, MS (Surgery), MCh (Urology). With 27 years of experience, his expertise covers Renal Transplants, Advanced Endourology, and Prostate Surgeries (TURP/HoLEP). He has performed over 500 successful kidney transplants. OPD Schedule: Monday to Friday, 9:00 AM - 1:00 PM. Room Number: 701. Languages spoken: English, Hindi, Maithili. Consultation Fee: ₹1600 (New), ₹1200 (Follow-up).",
        "source": "Doctor Profile - Dr. Mahesh Jha",
        "category": "doctors"
    },
    {
        "text": "Dr. Amit Bansal is a Senior Consultant in Urology. Qualifications: MBBS, MS, DNB (Urology). He has 15 years of experience, specializing in Uro-oncology (Kidney, Bladder, Prostate cancers) and Robotic Urology. He won the best video presentation for robotic partial nephrectomy at the Urological Society of India. OPD Schedule: Monday, Wednesday, Friday, 2:00 PM - 6:00 PM. Room Number: 704. Languages spoken: English, Hindi, Punjabi. Consultation Fee: ₹1400 (New), ₹1000 (Follow-up).",
        "source": "Doctor Profile - Dr. Amit Bansal",
        "category": "doctors"
    },
    {
        "text": "Dr. Swati Patil is a Consultant in the Urology department. Qualifications: MBBS, MS, MCh (Urology). With 10 years of experience, she focuses on Female Urology, Overactive Bladder management, and Laser Stone Surgeries (RIRS). She is one of the few female urologists in the region specializing in urinary incontinence. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 2:00 PM. Room Number: 706. Languages spoken: English, Hindi, Marathi, Kannada. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Swati Patil",
        "category": "doctors"
    },
    {
        "text": "Dr. Sangeeta Das is the Head of Department (HOD) for Dermatology. Qualifications: MBBS, MD (Dermatology, Venereology & Leprosy). With 21 years of experience, she specializes in Clinical Dermatology, Psoriasis management, and Autoimmune skin disorders. She is an executive committee member of the Indian Association of Dermatologists. OPD Schedule: Monday to Saturday, 9:00 AM - 1:00 PM. Room Number: 801. Languages spoken: English, Hindi, Bengali. Consultation Fee: ₹1200 (New), ₹800 (Follow-up).",
        "source": "Doctor Profile - Dr. Sangeeta Das",
        "category": "doctors"
    },
    {
        "text": "Dr. Tarun Balakrishnan is a Senior Consultant in Dermatology. Qualifications: MBBS, MD (DVL), Fellowship in Aesthetic Medicine. He has 14 years of experience, focusing on Cosmetology, Laser Hair Reduction, and Acne Scar Revisions. He holds an international diploma in lasers from the American Academy of Aesthetic Medicine. OPD Schedule: Monday, Wednesday, Friday, 3:00 PM - 7:00 PM. Room Number: 803. Languages spoken: English, Hindi, Tamil, Malayalam. Consultation Fee: ₹1000 (New), ₹700 (Follow-up).",
        "source": "Doctor Profile - Dr. Tarun Balakrishnan",
        "category": "doctors"
    },
    {
        "text": "Dr. Nandini Sen is a Consultant in the Dermatology department. Qualifications: MBBS, DNB (Dermatology). With 9 years of experience, her areas of expertise include Pediatric Dermatology, Eczema, and Hair Loss (Alopecia) treatments. She runs a specialized vitiligo clinic utilizing targeted phototherapy. OPD Schedule: Tuesday, Thursday, Saturday, 10:00 AM - 3:00 PM. Room Number: 805. Languages spoken: English, Hindi, Bengali. Consultation Fee: ₹900 (New), ₹600 (Follow-up).",
        "source": "Doctor Profile - Dr. Nandini Sen",
        "category": "doctors"
    },
    {
        "text": "Dr. Deepak Chawla is a Consultant in Dermatology. Qualifications: MBBS, MD (Dermatology). He brings 6 years of experience, specializing in Dermatosurgery, Vitiligo grafting, and Nail surgeries. He recently published a study on the efficacy of novel biologics in severe psoriasis. OPD Schedule: Monday to Friday, 4:00 PM - 8:00 PM. Room Number: 808. Languages spoken: English, Hindi, Punjabi. Consultation Fee: ₹800 (New), ₹500 (Follow-up).",
        "source": "Doctor Profile - Dr. Deepak Chawla",
        "category": "doctors"
    }
]

    
def medical_info_kb():
    return [
    {
        "text": "Asthma is a chronic lung condition where your airways narrow and swell, making it hard to breathe. Types include allergic asthma (triggered by dust or pollen) and exercise-induced asthma. Common causes include genetics, air pollution, and respiratory infections. Early symptoms are mild wheezing and a lingering cough, while advanced symptoms include severe shortness of breath and chest tightness.",
        "source": "Medical Info - Asthma",
        "category": "diseases"
    },
    {
        "text": "For Asthma diagnosis, our hospital uses a Pulmonary Function Test (Spirometry). A normal result shows an FEV1 score of 80% or higher. We may also do a Chest X-ray to rule out other issues. Please visit the Pulmonology Department. Approximate fees: Consultation ₹1200, Spirometry Test ₹800, Chest X-ray ₹400.",
        "source": "Medical Info - Asthma",
        "category": "diseases"
    },
    {
        "text": "Asthma treatment includes daily controller inhalers and rescue inhalers for sudden attacks. Lifestyle changes like avoiding dust and smoke are crucial. Visit the OPD for regular check-ups and prescription refills. Go to the Emergency instantly if your lips turn blue, you are gasping for air, or your rescue inhaler isn't working. Prevention tips: Wear a mask in pollution and identify your triggers.",
        "source": "Medical Info - Asthma",
        "category": "diseases"
    },
    {
        "text": "Kidney Stones are hard deposits made of minerals and salts that form inside your kidneys. The main types are calcium stones and uric acid stones. Common causes include drinking too little water, high salt intake, and obesity. Early symptoms include a mild ache in the lower back, while advanced symptoms feature agonizing pain in the side and back, blood in the urine, and vomiting.",
        "source": "Medical Info - Kidney Stones",
        "category": "diseases"
    },
    {
        "text": "To diagnose Kidney Stones, we use an Ultrasound KUB (Kidney, Ureters, Bladder) and a Routine Urine Test. Normal urine pH is around 6.0, and a normal ultrasound shows no stones or swelling. Visit the Urology or Nephrology Department. Approximate fees: Consultation ₹1400, Ultrasound KUB ₹1200, Urine Routine ₹200.",
        "source": "Medical Info - Kidney Stones",
        "category": "diseases"
    },
    {
        "text": "Small kidney stones are treated by drinking lots of water and taking pain medication to pass them naturally. Larger stones may need laser lithotripsy (a minimally invasive surgery). Visit the OPD for mild back pain. Rush to the Emergency if the pain is unbearable, accompanied by high fever, or if you cannot pass urine at all. Prevention tips: Drink 3-4 liters of water daily and reduce salt.",
        "source": "Medical Info - Kidney Stones",
        "category": "diseases"
    },
    {
        "text": "Thyroid Disorders happen when the butterfly-shaped thyroid gland in your neck produces too much or too little hormone. Types: Hypothyroidism (underactive) and Hyperthyroidism (overactive). Causes include autoimmune diseases, iodine deficiency, or stress. Symptoms of Hypothyroidism include weight gain, feeling cold, and tiredness. Hyperthyroidism causes weight loss, fast heartbeat, and anxiety.",
        "source": "Medical Info - Thyroid Disorders",
        "category": "diseases"
    },
    {
        "text": "Thyroid disorders are diagnosed using a Thyroid Profile blood test (T3, T4, and TSH). The normal range for TSH is 0.4 to 4.0 mIU/L. Abnormal levels confirm the disease. Please consult the Endocrinology or General Medicine Department. Approximate fees: Consultation ₹1000, Thyroid Profile Blood Test ₹600.",
        "source": "Medical Info - Thyroid Disorders",
        "category": "diseases"
    },
    {
        "text": "Treatment for Hypothyroidism involves taking daily synthetic hormone pills. Hyperthyroidism is treated with anti-thyroid medications, radioactive iodine, or rarely, surgery. Visit the OPD for routine monitoring. Go to the Emergency only if you experience an extremely fast, irregular heartbeat or extreme confusion/fainting. Prevention tips: Consume iodized salt and manage stress levels.",
        "source": "Medical Info - Thyroid Disorders",
        "category": "diseases"
    },
    {
        "text": "Liver Cirrhosis is late-stage scarring (fibrosis) of the liver, which prevents it from working properly. It is generally categorized by its cause: Alcoholic Cirrhosis or Viral Cirrhosis. Causes include chronic alcohol abuse, Hepatitis B or C, and fatty liver disease. Early symptoms are fatigue and loss of appetite. Advanced symptoms include jaundice (yellow eyes/skin), fluid buildup in the belly, and confusion.",
        "source": "Medical Info - Liver Cirrhosis",
        "category": "diseases"
    },
    {
        "text": "Liver Cirrhosis is diagnosed via a Liver Function Test (LFT) and a FibroScan. Normal total bilirubin in an LFT is 0.1 to 1.2 mg/dL. A FibroScan checks liver stiffness (normal is below 7 kPa). Please visit the Gastroenterology Department. Approximate fees: Consultation ₹1500, LFT ₹700, FibroScan ₹2500.",
        "source": "Medical Info - Liver Cirrhosis",
        "category": "diseases"
    },
    {
        "text": "Cirrhosis damage cannot be reversed, but treatment can stop it from getting worse. This includes quitting alcohol completely, antiviral drugs, and eating a low-sodium diet. Severe cases require a liver transplant. Visit the OPD for fatigue or mild swelling. Go to the Emergency immediately if you vomit blood or your skin turns deep yellow. Prevention tips: Avoid alcohol abuse and get vaccinated for Hepatitis B.",
        "source": "Medical Info - Liver Cirrhosis",
        "category": "diseases"
    },
    {
        "text": "Anemia is a condition where you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues. The most common types are Iron-deficiency anemia and Vitamin B12 deficiency anemia. Causes include poor diet, heavy menstrual bleeding, or internal ulcers. Early symptoms include tiredness, pale skin, and cold hands. Advanced symptoms are dizziness, chest pain, and shortness of breath.",
        "source": "Medical Info - Anemia",
        "category": "diseases"
    },
    {
        "text": "Anemia is diagnosed with a Complete Blood Count (CBC) test. The normal hemoglobin range is 13.5-17.5 g/dL for men and 12.0-15.5 g/dL for women. Anything lower indicates anemia. Please consult the General Medicine or Hematology Department. Approximate fees: Consultation ₹1000, CBC Test ₹300, Vitamin B12 Test ₹800.",
        "source": "Medical Info - Anemia",
        "category": "diseases"
    },
    {
        "text": "Anemia treatment depends on the cause but usually involves iron tablets, Vitamin B12 injections, and eating iron-rich foods like spinach and meat. Visit the OPD if you feel constantly tired or look pale. Go to the Emergency if you experience sudden chest pain or fainting. Prevention tips: Eat a balanced diet rich in green leafy vegetables, lentils, and citrus fruits.",
        "source": "Medical Info - Anemia",
        "category": "diseases"
    },
    {
        "text": "PCOS (Polycystic Ovary Syndrome) is a hormonal imbalance in women of reproductive age, often causing small cysts to form on the ovaries. Causes are linked to genetics, insulin resistance, and high levels of male hormones (androgens). Early symptoms include irregular periods, excess facial hair, and acne. Advanced symptoms can include severe weight gain, hair thinning, and difficulty getting pregnant (infertility).",
        "source": "Medical Info - PCOS",
        "category": "diseases"
    },
    {
        "text": "PCOS is diagnosed using a Pelvic Ultrasound to look for cysts, and hormonal blood tests. A normal fasting insulin level is below 25 mIU/L, and normal testosterone levels in women are 15-70 ng/dL. Higher levels suggest PCOS. Please visit the Gynecology or Endocrinology Department. Approximate fees: Consultation ₹1200, Pelvic Ultrasound ₹1000, Hormonal Profile ₹1500.",
        "source": "Medical Info - PCOS",
        "category": "diseases"
    },
    {
        "text": "PCOS cannot be cured but is managed with lifestyle changes, birth control pills to regulate periods, and medications like Metformin for insulin resistance. Visit the OPD for irregular periods or acne. Go to the Emergency if you experience sudden, agonizing pelvic pain, which could be a ruptured cyst. Prevention tips: Maintain a healthy weight and exercise for 30 minutes daily.",
        "source": "Medical Info - PCOS",
        "category": "diseases"
    },
    {
        "text": "Dengue Fever is a painful, mosquito-borne viral disease. It ranges from mild Classic Dengue to severe Dengue Hemorrhagic Fever. It is caused by the bite of an infected Aedes mosquito. Early symptoms include high fever (up to 104F), severe body/joint ache (breakbone fever), and a skin rash. Advanced, severe symptoms include bleeding gums, severe abdominal pain, and constant vomiting.",
        "source": "Medical Info - Dengue Fever",
        "category": "diseases"
    },
    {
        "text": "Dengue is diagnosed using a Dengue NS1 Antigen blood test and a Complete Blood Count to check platelets. A normal platelet count is 1.5 to 4.5 lakhs/mcL. In Dengue, this drops rapidly. Please visit the General Medicine or Infectious Diseases Department. Approximate fees: Consultation ₹1000, Dengue NS1 & Serology ₹1200, CBC ₹300.",
        "source": "Medical Info - Dengue Fever",
        "category": "diseases"
    },
    {
        "text": "There is no specific medicine for Dengue; treatment involves extreme rest, drinking lots of fluids, and paracetamol for fever (avoid aspirin/ibuprofen). Severe cases need hospital IV fluids or platelet transfusions. Visit the OPD for a high fever and body ache. Rush to the Emergency if you see bleeding, black stools, or severe stomach pain. Prevention tips: Use mosquito nets, repellents, and clear standing water.",
        "source": "Medical Info - Dengue Fever",
        "category": "diseases"
    },
    {
        "text": "Tuberculosis (TB) is a highly contagious bacterial infection that mainly affects the lungs (Pulmonary TB) but can affect other parts like bones or brain (Extrapulmonary TB). It is caused by Mycobacterium tuberculosis spreading through the air. Early symptoms include a cough lasting more than 3 weeks and mild chest pain. Advanced symptoms feature coughing up blood, extreme weight loss, and drenching night sweats.",
        "source": "Medical Info - Tuberculosis",
        "category": "diseases"
    },
    {
        "text": "TB is diagnosed using a Chest X-ray, Sputum test, and GeneXpert test. A normal Sputum/GeneXpert result is 'Negative' for TB bacteria. An X-ray of a healthy lung shows clear, black spaces without white patches. Please visit the Pulmonology Department. Approximate fees: Consultation ₹1200, Chest X-ray ₹400, Sputum GeneXpert ₹2000.",
        "source": "Medical Info - Tuberculosis",
        "category": "diseases"
    },
    {
        "text": "TB is completely curable but requires taking a strict combination of antibiotics for 6 to 9 months without missing a dose. Visit the OPD for a chronic cough or unexplained weight loss. Go to the Emergency if you are coughing up large amounts of blood or struggling to breathe. Prevention tips: Ensure babies get the BCG vaccine and wear masks around infected individuals.",
        "source": "Medical Info - Tuberculosis",
        "category": "diseases"
    },
    {
        "text": "A Stroke is a 'brain attack' that happens when blood flow to the brain is blocked by a clot (Ischemic Stroke) or a blood vessel bursts (Hemorrhagic Stroke). Causes include high blood pressure, diabetes, smoking, and high cholesterol. Symptoms appear suddenly. Remember FAST: Face drooping, Arm weakness, Speech difficulty. Time is critical. Advanced symptoms include paralysis of one side of the body and loss of consciousness.",
        "source": "Medical Info - Stroke",
        "category": "diseases"
    },
    {
        "text": "A Stroke is instantly diagnosed using a CT Scan or MRI of the Brain to see if there is bleeding or a blocked vessel. A normal scan shows healthy brain tissue with no bleeding or dark spots of dead tissue. Please visit the Neurology Department. Approximate fees: Emergency Consultation ₹1800, CT Scan Brain ₹3500, MRI Brain ₹7000.",
        "source": "Medical Info - Stroke",
        "category": "diseases"
    },
    {
        "text": "Treatment for an ischemic stroke involves clot-busting drugs (if given within 4.5 hours of symptoms starting). Bleeding strokes may require emergency brain surgery. Post-stroke care involves physical therapy. This is ALWAYS an Emergency—rush to the hospital immediately if you notice slurred speech or weakness. OPD is only for rehab and follow-ups. Prevention tips: Control your blood pressure and quit smoking.",
        "source": "Medical Info - Stroke",
        "category": "diseases"
    },
    {
        "text": "Osteoporosis is a bone disease where bones become weak, porous, and brittle, acting like a fragile sponge. Types include age-related osteoporosis and secondary osteoporosis (caused by medications like steroids). Causes include aging, menopause (drop in estrogen), and a lack of calcium/Vitamin D. Early on, there are zero symptoms. Advanced symptoms include a stooped posture, loss of height, and bones breaking very easily from a minor bump.",
        "source": "Medical Info - Osteoporosis",
        "category": "diseases"
    },
    {
        "text": "Osteoporosis is diagnosed using a DEXA Bone Density Scan. A normal bone density T-score is -1.0 or higher. A score of -2.5 or lower means you have osteoporosis. We also check Calcium and Vitamin D levels in the blood. Please visit the Orthopedics or Rheumatology Department. Approximate fees: Consultation ₹1200, DEXA Scan ₹2500, Vitamin D/Calcium Test ₹1200.",
        "source": "Medical Info - Osteoporosis",
        "category": "diseases"
    },
    {
        "text": "Treatment includes Calcium and Vitamin D supplements, alongside bone-building medications like Bisphosphonates. Lifestyle changes include weight-bearing exercises. Visit the OPD for general bone pain, screening after age 50, or posture issues. Go to the Emergency if you have a fall that results in sudden, severe pain, indicating a fracture. Prevention tips: Drink milk, get morning sunlight for Vitamin D, and walk daily.",
        "source": "Medical Info - Osteoporosis",
        "category": "diseases"
    }
]
def patient_programs_kb():
    return [
    {
            "text": "The Diabetes Management Program (Madhumeha Care) is designed to help patients achieve optimal blood sugar control and prevent complications like neuropathy or retinopathy. Eligible patients include anyone diagnosed with Type 1, Type 2, or Gestational Diabetes. The multidisciplinary team includes an Endocrinologist, a Certified Diabetes Educator (CDE), a Clinical Dietician, and a Podiatrist. The program includes quarterly HbA1c tests, continuous glucose monitoring (CGM) setup, personalized diet charts, and regular foot exams.",
            "source": "Program - Diabetes Management Program",
            "category": "patient_programs"
        },
    {
        "text": "The Diabetes Management Program runs as an annual subscription (12 months duration). Visit frequency is once a month for the educator/dietician and once a quarter for the Endocrinologist. The total annual cost is ₹18,000 (approx. ₹1,500/month). To enroll, ask your consulting doctor for a referral or register at the Endocrinology OPD desk on the 2nd Floor. Expected outcomes include lowering HbA1c below 7%, weight management, and prevention of diabetic foot ulcers or kidney damage.",
        "source": "Program - Diabetes Management Program",
        "category": "patient_programs"
    },
    {
        "text": "Our Cardiac Rehabilitation Program (Hridayam Rehab) aims to restore heart health and physical fitness after a major cardiac event. It is eligible for patients recovering from a heart attack, bypass surgery (CABG), angioplasty, or heart failure. The core team comprises a Preventive Cardiologist, Cardiac Physiotherapist, Clinical Psychologist, and Dietician. The program includes monitored exercise sessions (treadmill/ergometer with ECG telemetry), stress management counseling, and heart-healthy nutrition planning.",
        "source": "Program - Cardiac Rehabilitation",
        "category": "patient_programs"
    },
    {
        "text": "The Cardiac Rehabilitation Program is a 12-week intensive course. Patients are required to visit the rehab center 3 days a week for 1-hour sessions. The total cost for the 3-month program is ₹25,000. To enroll, bring your discharge summary to the Cardiac Rehab Center on the Ground Floor, Block A. Expected outcomes include a 30% increase in cardiovascular stamina, reduced chest pain, lower resting heart rate, and improved confidence in performing daily activities safely.",
        "source": "Program - Cardiac Rehabilitation",
        "category": "patient_programs"
    },
    {
        "text": "The Cancer Care Continuum Program provides holistic support for oncology patients, bridging the gap between active treatment and survivorship. Eligibility includes any patient currently undergoing or having recently completed chemotherapy, radiation, or cancer surgery. The multidisciplinary team features a Medical Oncologist, Palliative Care Physician, Onco-nutritionist, Psycho-oncologist, and specialized nursing staff. It includes pain management, nutritional support to prevent severe weight loss, and mental health counseling.",
        "source": "Program - Cancer Care Continuum",
        "category": "patient_programs"
    },
    {
        "text": "The Cancer Care Continuum Program duration varies but typically covers a 6-month active phase followed by annual surveillance. Visits are scheduled bi-weekly or aligned with chemotherapy cycles. The monthly cost is ₹5,000 (excluding chemo drugs/scans). To enroll, speak to your oncology coordinator at the Oncology Wing Helpdesk. Expected outcomes include better tolerance to chemotherapy side effects, improved nutritional status, reduced anxiety, and a structured roadmap for post-treatment life.",
        "source": "Program - Cancer Care Continuum",
        "category": "patient_programs"
    },
    {
        "text": "Our Comprehensive Dialysis Program ensures high-quality, infection-free renal replacement therapy for End-Stage Renal Disease (ESRD). It is eligible for patients with chronic kidney failure requiring regular hemodialysis. The team includes a Chief Nephrologist, Dialysis Technicians, Renal Dietician, and a Vascular Surgeon (for AV fistula care). The program includes state-of-the-art hemodiafiltration, monthly renal profile blood tests, iron/EPO injections (billed separately), and strict fluid-intake counseling.",
        "source": "Program - Dialysis Program",
        "category": "patient_programs"
    },
    {
        "text": "The Dialysis Program is an ongoing, lifelong program unless a kidney transplant occurs. Patients must visit the dialysis unit 2 to 3 times a week, with each session lasting 4 hours. The cost per dialysis session is ₹2,200 (approx. ₹26,400 monthly for 12 sessions). To enroll, consult the Nephrology OPD with your latest kidney function tests. Expected outcomes include stabilized blood pressure, removal of uremic toxins, prevention of fluid overload, and improved daily energy levels.",
        "source": "Program - Dialysis Program",
        "category": "patient_programs"
    },
    {
        "text": "The Post-Stroke Rehabilitation Program (Neuro-Restore) focuses on helping stroke survivors regain lost motor and cognitive functions. It is eligible for patients who have suffered an ischemic or hemorrhagic stroke within the last 6 months. The multidisciplinary team includes a Neurologist, Neuro-physiotherapist, Occupational Therapist, and Speech-Language Pathologist. It includes gait training, fine motor skill exercises, swallow therapy, and memory retraining.",
        "source": "Program - Post-Stroke Rehabilitation",
        "category": "patient_programs"
    },
    {
        "text": "The Post-Stroke Rehabilitation Program typically lasts for 6 months, as early intervention yields the best neuroplasticity results. Frequency is 4 to 5 sessions per week at our Neuro-Rehab Center. The monthly package cost is ₹15,000. To enroll, get a clearance certificate from your treating neurologist and register at Block B, 2nd Floor. Expected outcomes include regaining independent walking ability, improved speech clarity, ability to self-feed, and a significantly reduced risk of a second stroke.",
        "source": "Program - Post-Stroke Rehabilitation",
        "category": "patient_programs"
    },
    {
        "text": "The Obesity Management & Bariatric Support Program aims for sustainable weight loss to reverse metabolic syndromes. Eligible patients are those with a BMI over 30, or over 27 with co-morbidities like hypertension or sleep apnea. The team consists of a Bariatric Surgeon, Endocrinologist, Clinical Dietician, and Behavioral Therapist. The program includes comprehensive metabolic blood panels, customized calorie-deficit meal planning, pharmacological weight-loss support, and pre/post-bariatric surgery counseling.",
        "source": "Program - Obesity Management",
        "category": "patient_programs"
    },
    {
        "text": "The Obesity Management Program has a minimum duration of 6 months. Visits are scheduled every 15 days for weigh-ins and diet adjustments. The comprehensive 6-month package costs ₹20,000. To enroll, book an initial assessment at the Wellness Clinic on the Ground Floor. Expected outcomes include a 10-15% reduction in baseline body weight, reversal of pre-diabetes, improved joint mobility, and establishing a long-term healthy relationship with food.",
        "source": "Program - Obesity Management",
        "category": "patient_programs"
    },
    {
        "text": "The COPD Management Program (Swasa Care) is dedicated to improving the lung capacity and quality of life for patients with Chronic Obstructive Pulmonary Disease. Eligibility includes chronic smokers or individuals diagnosed with COPD, Emphysema, or chronic bronchitis. The care team involves a Pulmonologist, Respiratory Therapist, and Nutritionist. The program includes pulmonary function testing, inhaler technique workshops, oxygen therapy assessment, and chest physiotherapy to clear mucus.",
        "source": "Program - COPD Management",
        "category": "patient_programs"
    },
    {
        "text": "The COPD Management Program runs on a 6-month cycle. Patients visit the Pulmonary Rehab clinic twice a week for the first 8 weeks, then step down to once a month. The 6-month program cost is ₹12,000. Enrollment can be done directly at the Pulmonology OPD in Block C. Expected outcomes include reduced breathlessness during daily tasks, fewer hospital admissions for lung exacerbations, proper inhaler usage, and enhanced exercise tolerance.",
        "source": "Program - COPD Management",
        "category": "patient_programs"
    },
    {
        "text": "The Mental Health & Wellness Program offers structured support for chronic psychiatric conditions to ensure long-term stability. It is eligible for individuals diagnosed with clinical depression, severe anxiety disorders, bipolar disorder, or chronic stress. The multidisciplinary team comprises a Psychiatrist, Clinical Psychologist, Psychiatric Social Worker, and Yoga Therapist. The program encompasses psychiatric medication management, Cognitive Behavioral Therapy (CBT) sessions, and group therapy.",
        "source": "Program - Mental Health Program",
        "category": "patient_programs"
    },
    {
        "text": "The Mental Health Program duration is highly individualized but generally starts with a 3-month commitment. Therapy sessions happen weekly, with psychiatrist reviews once a month. The monthly cost is approximately ₹8,000 (covering 4 therapy sessions and 1 doctor consult). To enroll, call the psychiatry helpline or visit the Psychiatry Wing on the 4th Floor. Expected outcomes include better emotional regulation, reduction in panic attacks, improved sleep hygiene, and successful reintegration into work and social life.",
        "source": "Program - Mental Health Program",
        "category": "patient_programs"
    }
]
    
def health_packages_kb():
    return [
    {
        "text": "The Basic Health Checkup is ideal for generally healthy adults (18-35 years) looking for an annual preventive screening. Tests included: Complete Blood Count (CBC), Fasting Blood Sugar (FBS), Lipid Profile, Liver Function Test (SGPT, SGOT), Serum Creatinine (Kidney), and Urine Routine. Consultations included: 1 General Physician evaluation. Pricing: Individual test cost is roughly ₹3,000, but the package price is ₹1,500 (Savings: ₹1,500). Duration: 2 hours. Fasting required: Yes, 10-12 hours overnight fasting. Report delivery: Same day evening. How to book: Call our wellness desk or book via the hospital app. Free add-on: Complimentary BMI and Body Fat percentage assessment.",
        "source": "Health Package - Basic Health Checkup",
        "category": "packages"
    },
    {
        "text": "The Comprehensive Full Body Checkup is targeted at adults over 30 requiring an in-depth health overview. Tests included: CBC, Complete LFT, Complete KFT, Lipid Profile, Thyroid Profile (TSH, T3, T4), HbA1c, Vitamin D, Vitamin B12, resting ECG, Chest X-ray, and USG Abdomen & Pelvis. Consultations included: General Physician and Clinical Dietician. Pricing: Normal individual pricing is ₹8,500. Total package price: ₹4,500 (Savings: ₹4,000). Duration: 4-5 hours. Fasting required: Yes, 10-12 hours. Report delivery: Next day at 10:00 AM. How to book: Book via the app or walk in early morning. Free add-on: 10% discount voucher for any further radiological tests.",
        "source": "Health Package - Comprehensive Full Body Checkup",
        "category": "packages"
    },
    {
        "text": "The Cardiac Risk Assessment Package is essential for individuals 35+ with high stress, smoking habits, or a family history of heart disease. Tests included: Lipid Profile, Hs-CRP (Inflammation marker), Homocysteine, resting ECG, 2D Echocardiography, Treadmill Test (TMT), and Fasting Blood Sugar. Consultations included: 1 Expert Cardiologist consult. Pricing: Normal individual test cost is ₹6,500. Total package price: ₹3,500 (Savings: ₹3,000). Duration: 3 hours. Fasting required: Yes, 10 hours. Report delivery: Same day. How to book: Call the Cardiology OPD desk. Free add-on: Complimentary Blood Pressure tracking logbook.",
        "source": "Health Package - Cardiac Risk Assessment Package",
        "category": "packages"
    },
    {
        "text": "The Diabetes Monitoring Package is specifically for known diabetics or pre-diabetics to prevent organ damage. Tests included: Fasting & Post-Prandial (PP) Blood Sugar, HbA1c (3-month average), Serum Creatinine, Microalbuminuria (Kidney screening), Lipid Profile, Funduscopy (Eye check for retinopathy), and ECG. Consultations included: Endocrinologist/Diabetologist, Ophthalmologist, and a Diabetic Educator. Pricing: Normal individual cost is ₹5,000. Total package price: ₹2,500 (Savings: ₹2,500). Duration: 3-4 hours. Fasting required: Yes, strictly 10 hours. Report delivery: Same day evening. How to book: Register at the Endocrinology wing. Free add-on: Free home-glucometer calibration check.",
        "source": "Health Package - Diabetes Monitoring Package",
        "category": "packages"
    },
    {
        "text": "The Women's Health Package (Age 25-40) focuses on reproductive and general wellness for young women. Tests included: CBC, Thyroid Profile (TSH, T3, T4), Iron Studies (to check anemia), Fasting Blood Sugar, USG Pelvis, Pap Smear (Cervical screening), and Urine Routine. Consultations included: 1 Gynecologist consult. Pricing: Normal individual cost is ₹4,800. Total package price: ₹2,800 (Savings: ₹2,000). Duration: 3 hours. Fasting required: Yes, 10 hours. Report delivery: Blood tests same day; Pap Smear takes 3 days. How to book: Call the Gynecology helpdesk. Free add-on: Complimentary dental consultation.",
        "source": "Health Package - Women's Health Package (age 25-40)",
        "category": "packages"
    },
    {
        "text": "The Women's Health Package (Age 40+) is designed for peri and post-menopausal women to catch age-related conditions early. Tests included: CBC, Lipid Profile, Thyroid Profile, HbA1c, Bilateral Mammogram (Breast screening), Pap Smear, DEXA Scan (Bone Density), and USG Abdomen & Pelvis. Consultations included: Gynecologist and General Physician. Pricing: Normal individual cost is ₹9,000. Total package price: ₹5,500 (Savings: ₹3,500). Duration: 5 hours. Fasting required: Yes, 10 hours. Report delivery: 2-3 days. How to book: Book via the wellness department phone line. Free add-on: Free menopause nutrition guide and calcium planner.",
        "source": "Health Package - Women's Health Package (age 40+)",
        "category": "packages"
    },
    {
        "text": "The Senior Citizen Package (60+) provides gentle, comprehensive screening for the elderly. Tests included: CBC, Complete KFT & LFT, Lipid Profile, HbA1c, PSA (Prostate check for men) OR Thyroid Profile (for women), ECG, Chest X-ray, Stool Occult Blood, Calcium, Vitamin D, and Audiometry (Hearing). Consultations included: Geriatrician (or General Physician) and Eye Specialist. Pricing: Normal individual cost is ₹8,000. Total package price: ₹4,000 (Savings: ₹4,000). Duration: 4 hours. Fasting required: Yes, 10 hours. Report delivery: Next day. How to book: Call via the app. Free add-on: Priority wheelchair assistance throughout the visit and optional free home sample collection.",
        "source": "Health Package - Senior Citizen Package (60+)",
        "category": "packages"
    },
    {
        "text": "The Pre-Employment Health Checkup is for new job joiners fulfilling HR requirements. Tests included: CBC, Blood Group & Rh typing, Fasting Blood Sugar, Serum Creatinine, SGPT (Liver), Urine Routine, Chest X-ray, resting ECG, and Vision/Color Blindness Test. Consultations included: 1 General Physician evaluation. Pricing: Normal individual cost is ₹3,500. Total package price: ₹1,800 (Savings: ₹1,700). Duration: 2 hours. Fasting required: Yes, 10 hours. Report delivery: Same day evening. How to book: Corporate tie-up desk or walk-in. Free add-on: Officially stamped medical fitness certificate provided at no extra cost.",
        "source": "Health Package - Pre-Employment Health Checkup",
        "category": "packages"
    },
    {
        "text": "The Pre-Marital Health Screening is for couples planning to marry, focusing on genetics and transmissible diseases. Tests included: CBC, Blood Group & Rh, Thalassemia Profile (Hb Electrophoresis), VDRL (Syphilis), HIV I & II, HBsAg (Hepatitis B), HCV (Hepatitis C), Fasting Blood Sugar, Semen Analysis (for males) OR USG Pelvis (for females). Consultations included: General Physician and Gynecologist/Urologist. Pricing: Normal cost per person is ₹7,500. Total package price: ₹4,500 per person (Savings: ₹3,000). Duration: 3 hours. Fasting required: Yes, 10 hours. Report delivery: 2 days. How to book: Walk-in to the preventive health department. Free add-on: Flat 10% discount if booked as a couple.",
        "source": "Health Package - Pre-Marital Health Screening",
        "category": "packages"
    },
    {
        "text": "The Cancer Screening Package targets individuals over 40 or those with a family history of malignancy. Tests included: CBC, LFT, Tumor markers CA-125 (Women) OR PSA (Men), CEA (Colon marker), AFP (Liver marker), Low-Dose CT Chest (Smokers), Stool Occult Blood, Pap Smear (Women), and USG Abdomen. Consultations included: 1 Medical Oncologist consult. Pricing: Normal individual cost is ₹11,000. Total package price: ₹6,500 (Savings: ₹4,500). Duration: 5 hours. Fasting required: Yes, 10 hours. Report delivery: 3 days. How to book: Call the Oncology helpdesk. Free add-on: Complimentary family cancer risk and genetic counseling session.",
        "source": "Health Package - Cancer Screening Package",
        "category": "packages"
    },
    {
        "text": "The Executive Health Package is tailored for busy corporate professionals facing high stress and sedentary lifestyles. Tests included: CBC, Advanced Lipid Profile, Complete LFT & KFT, HbA1c, Thyroid Profile, Cardiac Biomarkers, TMT (Treadmill Test), 2D Echo, USG Abdomen, PFT (Pulmonary Function Test), and Audiometry. Consultations included: General Physician, Cardiologist, and Dietician. Pricing: Normal individual cost is ₹12,000. Total package price: ₹7,500 (Savings: ₹4,500). Duration: 6 hours. Fasting required: Yes, 10-12 hours. Report delivery: Next day. How to book: Executive Lounge booking desk. Free add-on: Complimentary executive breakfast in the VIP lounge after blood draw.",
        "source": "Health Package - Executive Health Package",
        "category": "packages"
    },
    {
        "text": "The Child Health & Growth Package is for monitoring the development and nutritional status of children aged 2-12 years. Tests included: CBC, Blood Group & Rh, Thyroid Profile, Iron Studies, Serum Calcium, Vitamin D3, Stool Routine (to check for worms), and Urine Routine. Consultations included: Pediatrician and Pediatric Dentist. Pricing: Normal individual cost is ₹4,500. Total package price: ₹2,500 (Savings: ₹2,000). Duration: 1.5 hours. Fasting required: Preferred (4 hours), but not strictly mandatory. Report delivery: Same day. How to book: Call the Pediatrics OPD. Free add-on: Free vaccination tracking chart and a dental sticker kit for the child.",
        "source": "Health Package - Child Health & Growth Package",
        "category": "packages"
    }
]
    
def fee_structure_kb():
    return [
    {
        "text": "OPD Consultation Fees: General Physician/Medical Officer: ₹500. Consultant: ₹1,000. Senior Consultant: ₹1,500. Head of Department (HOD) / Director: ₹2,000. Super-specialty consults (Oncology, Neurology, Interventional Cardiology) have a flat fee of ₹1,800. Included: One routine follow-up within 7 days is free. Extra: Any diagnostic tests or minor procedures done in the OPD room. Payment Modes: Cash, UPI, and all major Credit/Debit Cards. Insurance: OPD is generally out-of-pocket, but we provide stamped bills for reimbursement; cashless available only for specific corporate TPA plans. EMI: Not applicable for OPD. Senior Citizens: 10% flat discount on all OPD consultation fees.",
        "source": "Fees - OPD Consultation",
        "category": "fees"
    },
    {
        "text": "Inpatient Room Charges (Per Day): General Ward (6 beds): ₹2,000. Twin Sharing Room: ₹4,500. Single Private Room: ₹8,000. Deluxe Room: ₹12,000. VIP Suite: ₹18,000. Included in Room Rent: Hospital bed charges, nursing care, standard hospital meals (for patient only), and daily housekeeping. Charged Extra: Doctor visiting fees (billed per visit based on room category), pharmacy, consumables, diet modifications, and companion bed/meals. Payment Modes: Cash, UPI, Cards, and RTGS/NEFT for large amounts. Insurance: Fully cashless process available with 30+ major TPAs (Pre-authorization required 48 hrs before planned admission). EMI: Zero-cost EMI available via Bajaj Finserv. Senior Citizens: 10% discount on room rent for cash-paying patients.",
        "source": "Fees - Inpatient Rooms",
        "category": "fees"
    },
    {
        "text": "ICU and Critical Care Charges (Per Day): Medical/Surgical ICU (MICU/SICU): ₹12,000. Intensive Coronary Care Unit (ICCU): ₹14,000. Neonatal ICU (NICU): ₹8,000. Isolation ICU (Negative Pressure): ₹15,000. Included: 24/7 intensive nursing, continuous vital monitoring, standard bed charges, and resident duty doctor fees. Charged Extra: Mechanical Ventilator (₹4,000/day), BiPAP/CPAP (₹2,000/day), high-end lifesaving antibiotics, blood products, and specialist intensivist visits. Payment Modes: Cash, UPI, Credit/Debit cards. Insurance: Cashless facility available; emergency admissions require TPA intimation within 24 hours. EMI: Medical loan/EMI assistance available via hospital finance desk for bills exceeding ₹50,000. Senior Citizens: 10% discount on ICU bed charges.",
        "source": "Fees - ICU and Critical Care",
        "category": "fees"
    },
    {
        "text": "Operation Theatre (OT) Charges: Minor Surgery (e.g., lipoma removal): ₹15,000. Major Surgery (e.g., gallbladder removal): ₹45,000. Supra-Major Surgery (e.g., joint replacement, craniotomy): ₹85,000. Robotic Surgery Surcharge: Base OT + ₹75,000. Included: OT room rent for the stipulated time, basic surgical equipment, and standard sterilization. Charged Extra: Primary Surgeon fee, Anesthetist fee (usually 30% of surgeon fee), surgical implants/mesh/stents, specialized cautery tools, and anesthesia drugs. Payment Modes: Cash, UPI, Cards, Bank Transfer. Insurance: Cashless accepted for all planned surgeries pending TPA approval. EMI: 0% EMI for 6 months available on surgical packages via partner banks. Senior Citizens: 10% discount on OT rent.",
        "source": "Fees - Operation Theatre",
        "category": "fees"
    },
    {
        "text": "Diagnostic Imaging Fees: Digital X-Ray (per view): ₹500. Ultrasound (USG Abdomen/Pelvis): ₹1,500. Color Doppler: ₹2,500. CT Scan (Plain): ₹3,500. CT Angiography: ₹8,000. MRI Scan (1.5T Plain): ₹7,000. MRI Scan (3T Advanced): ₹10,000. PET-CT Scan (Whole Body): ₹22,000. Included: The scan, radiologist's physical report, and digital films/CD. Charged Extra: IV Contrast Dye (₹1,500 - ₹3,500 depending on scan) and anesthesia for claustrophobic/pediatric patients. Payment Modes: Cash, UPI, Credit/Debit cards. Insurance: Cashless covered only if part of an approved IPD admission; OPD scans are cash/reimbursement. EMI: Available for PET-CT and advanced 3T MRI via credit card. Senior Citizens: 15% discount on all imaging modalities.",
        "source": "Fees - Diagnostic Imaging",
        "category": "fees"
    },
    {
        "text": "Pathology Lab Fees (Common Panels representing 50+ tests): Complete Blood Count (CBC): ₹300. Blood Sugar (F/PP): ₹150. HbA1c: ₹500. Lipid Profile: ₹700. Liver Function Test (LFT): ₹700. Kidney Function Test (KFT): ₹700. Thyroid Profile (T3,T4,TSH): ₹600. Vitamin D3: ₹1,200. Vitamin B12: ₹1,000. Iron Studies: ₹800. Urine Routine: ₹200. Dengue NS1: ₹800. CRP: ₹450. Prothrombin Time (PT/INR): ₹400. Included: Venipuncture, vacutainers, and digital report delivery. Charged Extra: Home sample collection fee (₹200). Payment Modes: Cash, UPI, Cards. Insurance: OPD lab tests require upfront payment; GST invoices provided for reimbursement. EMI: Not applicable. Senior Citizens: Flat 15% discount on all pathology lab investigations.",
        "source": "Fees - Pathology Lab",
        "category": "fees"
    },
    {
        "text": "Physiotherapy and Rehabilitation Fees: Initial Assessment & Consultation: ₹800. Standard Daily Session (Ortho/Pain Management): ₹500/session. Advanced Neuro-Rehabilitation (Post-Stroke): ₹800/session. Cardiac/Pulmonary Rehab: ₹1,000/session. Home Visit Physiotherapy: ₹1,500/session. Included: Use of basic modalities (TENS, Ultrasound therapy, IFT) and guided exercises by a certified physiotherapist. Charged Extra: Advanced robotic gait training, Kinesio taping, and specialized dry needling. Payment Modes: Cash, UPI, Credit/Debit cards. Insurance: Covered under specific TPA policies for post-operative care; otherwise reimbursement basis. EMI: Not applicable. Offers/Discounts: 10% Senior Citizen discount, or book a package of 10 sessions upfront to get a 15% discount.",
        "source": "Fees - Physiotherapy",
        "category": "fees"
    },
    {
        "text": "Maternity Package Fees: Normal Delivery (2 Days stay): Twin Sharing ₹60,000 | Single Private ₹85,000. C-Section Delivery (3 Days stay): Twin Sharing ₹85,000 | Single Private ₹1,15,000. High-Risk Pregnancy Surcharge: ₹15,000. Included: Obstetrician fee, standard room rent, labor room/OT charges, standard ward medications, routine baby screening, and dietician consult. Charged Extra: NICU stays, phototherapy for baby jaundice, epidural (Painless Delivery ₹10,000 extra), baby vaccinations, and cross-specialty consultations. Payment Modes: Cash, UPI, Cards. Insurance: Cashless maternity claims processed subject to policy waiting periods (usually 9-24 months). EMI: 0% EMI options for 3-6 months via partnered NBFCs/Cards. Senior Citizens: N/A for maternity.",
        "source": "Fees - Maternity Packages",
        "category": "fees"
    }
]
    
def emergency_services_kb():
    return [
        {
            "text": "Our 24/7 Emergency Department is a state-of-the-art facility equipped to handle all medical, cardiac, and surgical emergencies. The department features a 15-bed triage area, dedicated isolation rooms, and a high-tech resuscitation bay equipped with biphasic defibrillators, transport ventilators, and central multi-parameter monitors. Our clinical team comprises Board-certified Emergency Medicine Physicians and ACLS/ATLS (Advanced Cardiovascular/Trauma Life Support) certified nursing staff. All major health insurance policies and TPAs are accepted for cashless emergency admissions as per IRDAI guidelines. Emergency Direct Line: 0831-240-8888.",
            "source": "Emergency - Department Overview",
            "category": "emergency"
        },
        {
        "text": "We operate a 24/7 fleet of GPS-enabled ambulances, including Basic Life Support (BLS), Advanced Life Support (ALS / ICU on wheels), and coordinated Air Ambulance services for inter-state transfers. ALS ambulances are fully equipped with transport ventilators, infusion pumps, oxygen cylinders, and defibrillators, staffed by certified emergency paramedics. We guarantee an ambulance dispatch time of under 3 minutes. Pricing: BLS Ambulance base charge is ₹1,000 plus ₹25 per km; ALS Ambulance base charge is ₹2,000 plus ₹50 per km. For immediate dispatch, call our Ambulance Hotline: 1066 or 99887-76655.",
        "source": "Emergency - Ambulance Services",
        "category": "emergency"
        },
    {
        "text": "Our Level 1 Trauma Center is specifically designed to maximize patient survival during the critical 'Golden Hour' following severe accidents. We utilize a pre-arrival activation protocol: trauma surgeons, neurosurgeons, and orthopedic specialists are assembled in the ER before the patient even arrives. The facility includes a dedicated emergency operation theatre (OT), crash carts, and instant access to the adjacent blood bank and 3T MRI/CT scan suite. Emergency trauma care, including medico-legal and motor accident claims, is covered under cashless insurance. Trauma Emergency Number: 1066.",
        "source": "Emergency - Trauma Center & Golden Hour",
        "category": "emergency"
    },
    {
        "text": "Save these crucial emergency contacts: Ambulance Dispatch: 1066; ER Direct: 0831-240-8888; Stroke/Heart Attack Rapid Response: 99887-76655. Upon arrival, patients undergo our rapid Triage Process using a color-coded Emergency Severity Index. 'Red' (immediate life threat like cardiac arrest) bypasses all queues for zero wait time. 'Yellow' (urgent but stable) patients are attended to within 15 minutes, and 'Green' (minor injuries) within 45 minutes. Our ATLS-certified triage nurses ensure critical resources are directed instantly to those who need them most.",
        "source": "Emergency - Contacts and Triage",
        "category": "emergency"
    },
    {
        "text": "While waiting for the ambulance (Call 1066), your immediate actions can save a life. For a suspected heart attack: make the patient sit calmly, loosen tight clothing, and if previously prescribed, place a Sorbitrate tablet under their tongue. For heavy bleeding: apply firm, direct pressure with a clean cloth. For seizures/fits: do not put anything in their mouth or restrain them; simply roll them onto their side and clear away hard objects. Our dispatchers are trained Emergency Medical Technicians (EMTs) who will stay on the phone to guide you through hands-only CPR until the ALS team arrives.",
        "source": "Emergency - First Aid Guidance",
        "category": "emergency"
    },
    {
        "text": "Pediatric and neonatal emergencies require highly specialized, delicate care. We have a dedicated Pediatric ER and a Neonatal Transport Incubator Ambulance for safely transferring critically ill newborns from other clinics. Our transport team includes a Senior Neonatologist and PALS (Pediatric Advanced Life Support) certified nurses. The Pediatric ER is equipped with child-sized defibrillator pads, specialized micro-ventilators, and vein illuminators. We guarantee a response time for NICU retrieval within city limits of under 20 minutes. Pediatric emergency care is fully covered under standard family floater health insurance policies. Pediatric ER Direct: 0831-240-8899.",
        "source": "Emergency - Pediatric and NICU",
        "category": "emergency"
    }
]
def diagnostic_services_kb():
        return [
    {
        "text": "Our Pathology Lab Services offer a comprehensive menu including Complete Blood Count (CBC) - ₹300, Lipid Profile - ₹700, Liver Function Test (LFT) - ₹700, Thyroid Profile (TSH, T3, T4) - ₹600, and HbA1c - ₹500. Turnaround time for routine blood tests is 6-8 hours. Fasting of 10-12 hours is strictly required for Lipid Profile and Fasting Blood Sugar. Timings: 24/7 at the Ground Floor, Block A Collection Center. Home sample collection is available for an extra ₹200. You can download your reports online using the hospital mobile app or portal with your UHID and registered mobile number.",
        "source": "Diagnostics - Pathology Lab",
        "category": "diagnostics"
    },
    {
        "text": "Our Radiology Services are equipped with the latest imaging tech. Available tests: Digital X-Ray (Chest/Bones) - ₹500, USG Abdomen & Pelvis (Ultrasound) - ₹1,500, CT Scan Plain Brain - ₹3,500, and 3T MRI Brain/Spine - ₹8,000. Turnaround time: X-rays and USG reports are provided immediately; CT/MRI reports within 12-24 hours. Fasting of 4-6 hours is required for USG Abdomen and any contrast-enhanced scans. Timings: 24/7 for emergencies, 8:00 AM - 8:00 PM for OPD at Basement, Block B. Home collection is not applicable, except for portable X-ray (₹2,000). Reports and digital films can be accessed via our online patient portal.",
        "source": "Diagnostics - Radiology",
        "category": "diagnostics"
    },
    {
        "text": "We provide advanced Cardiac Diagnostics to assess heart function. Tests include: Electrocardiogram (ECG) - ₹300, 2D Echocardiography (Echo) - ₹2,000, Treadmill Stress Test (TMT) - ₹2,500, 24-Hour Holter Monitor - ₹3,000, and CT Coronary Angiography - ₹12,000. Turnaround time: ECG, Echo, and TMT reports are given immediately; Holter requires 24 hours of wearing followed by next-day reporting. Fasting: 3 hours for TMT, 6 hours for Angiography. Timings: 9:00 AM - 5:00 PM at the 1st Floor Cardiology Wing. Home ECG is available for ₹1,000. Reports are uploaded directly to your online hospital app account.",
        "source": "Diagnostics - Cardiac",
        "category": "diagnostics"
    },
    {
        "text": "Our Neurological Diagnostics center evaluates brain and nerve health. Tests include: Electroencephalogram (EEG) - ₹2,000, Electromyography (EMG) - ₹2,500, Nerve Conduction Velocity (NCV) - ₹2,500, and Overnight Sleep Study (Polysomnography) - ₹10,000. Turnaround time is typically 24-48 hours for neurophysiological reporting. Fasting is not required, but patients coming for an EEG must have clean, washed, oil-free hair. Timings: Monday to Saturday, 9:00 AM - 4:00 PM at the 2nd Floor Neuro Lab. Home sleep study setup is available for ₹15,000. Approved PDF reports are accessible via the hospital website.",
        "source": "Diagnostics - Neurological",
        "category": "diagnostics"
    },
    {
        "text": "Our Women's Diagnostics wing ensures privacy and precision. Tests include: Bilateral Digital Mammography - ₹2,500, DEXA Scan (Bone Mineral Density) - ₹3,000, Pap Smear (Liquid-based cytology) - ₹1,200, and AMH (Anti-Müllerian Hormone) for fertility - ₹2,000. Turnaround time: AMH blood test is same day, Mammogram/DEXA next day, and Pap Smear takes 3-4 days. Fasting is not required for any of these tests. Timings: 9:00 AM - 6:00 PM at the 4th Floor Women's Wellness Clinic. Home collection is available only for blood tests (AMH/hormones) at ₹200 extra. Reports can be securely downloaded via the online portal.",
        "source": "Diagnostics - Women's Diagnostics",
        "category": "diagnostics"
    },
    {
        "text": "Our Genetic Testing department offers cutting-edge chromosomal and molecular analysis. Tests include: Karyotyping (Chromosomal Analysis) - ₹4,500, BRCA 1 & 2 Gene Mutation Analysis - ₹18,000, NIPT (Non-Invasive Prenatal Testing) - ₹15,000, and Clinical Exome Sequencing - ₹25,000. Turnaround time is longer: 10-14 days for Karyotyping/NIPT, and up to 3-4 weeks for Exome sequencing. Fasting is not required. Timings: 10:00 AM - 4:00 PM at the Genetics Dept, 3rd Floor. Specialized home phlebotomy is available for ₹500. Due to sensitivity, reports are shared via encrypted email or physical copy only.",
        "source": "Diagnostics - Genetic Testing",
        "category": "diagnostics"
    },
    {
        "text": "The Microbiology and Culture department identifies infectious agents. Tests include: Urine Routine & Culture - ₹800, Blood Culture - ₹1,200, Sputum Culture & Sensitivity - ₹1,000, Pus Swab Culture - ₹900, and RT-PCR for viral panels - ₹1,500. Turnaround time: Routine analysis takes 24 hours, but bacterial cultures strictly require 48-72 hours to allow organism growth. Fasting is not required, though the first-morning sample is highly recommended for urine and sputum. Timings: 24/7 Sample drop-off at Ground Floor. Home collection is available for ₹200. You will receive an SMS link to download the report once the culture is finalized.",
        "source": "Diagnostics - Microbiology",
        "category": "diagnostics"
    },
    {
        "text": "Our Home Sample Collection Service brings hospital-grade diagnostics to your doorstep anywhere within city limits. Available tests include all routine pathology blood and urine tests, genetic testing blood draws, and portable ECGs. Turnaround time begins once the sample reaches the lab (typically matching standard lab TATs). Fasting guidelines apply based on the test (e.g., morning slots for fasting sugar). Booking is 24/7, with collection slots from 6:30 AM - 8:00 PM. Extra charges: ₹200 flat convenience fee (waived for senior citizens and total bills over ₹2,000). Reports are sent directly to your WhatsApp and hospital app.",
        "source": "Diagnostics - Home Collection",
        "category": "diagnostics"
    }
]
def inpatient_services_kb():
            return[
    {
        "text": "We offer 5 tiers of room categories for inpatient stays. General Ward features 6 beds with privacy curtains and shared washrooms. Semi-Private rooms have 2 beds with an attached washroom and AC. Private rooms offer a single bed, attached washroom, AC, TV, and an attendant couch. Deluxe rooms are larger with premium furnishings and a mini-fridge. The VIP Suite includes a separate living area for visitors, premium amenities, and a dedicated attendant. Room upgrades are subject to availability at the time of admission.",
        "source": "Inpatient - Room Categories and Facilities",
        "category": "inpatient"
    },
    {
        "text": "The pre-admission process requires you to bring the admitting doctor's admission note, a valid government ID (Aadhar, PAN, or Voter ID), and your insurance TPA card if opting for cashless hospitalization. For planned surgeries, financial counseling and TPA pre-authorization are done 48 hours prior. A security deposit is required for cash admissions. Fasting instructions (usually 8-12 hours nil per oral) must be strictly followed for morning surgical admissions.",
        "source": "Inpatient - Pre-Admission Process",
        "category": "inpatient"
    },
    {
        "text": "Our surgical packages offer transparent pricing. Included: Surgeon/Anesthetist fees, OT charges, standard room rent (for stipulated days), routine ward medicines, and basic surgical consumables. Extra charges apply for: Implants (stents, mesh, joints, lenses), blood products, high-end antibiotics, and pre-op diagnostics. Approximate Total Costs: 1. Appendectomy (Lap): ₹45,000. 2. Total Knee Replacement (Single): ₹1,80,000. 3. Cataract (with standard IOL): ₹30,000. 4. Hernia Repair: ₹55,000. 5. Gallbladder Removal: ₹60,000. 6. Hysterectomy: ₹70,000. 7. TURP (Prostate): ₹65,000. 8. Tonsillectomy: ₹35,000. 9. Spinal Disc Surgery: ₹1,20,000. 10. CABG (Heart Bypass): ₹2,50,000.",
        "source": "Inpatient - Surgical Packages",
        "category": "inpatient"
    },
    {
        "text": "ICU admission is reserved for critically ill patients requiring continuous mechanical ventilation, advanced hemodynamic monitoring, or complex post-operative care. Criteria include unstable vitals, severe trauma, or acute organ failure. The ICU daily routine includes 24/7 one-on-one nursing, hourly vital checks, twice-daily intensivist rounds, and strict infection control protocols. To maintain a sterile environment, routine attendants are not permitted inside the ICU, though brief daily counseling sessions are held for the family.",
        "source": "Inpatient - ICU Admission and Routine",
        "category": "inpatient"
    },
    {
        "text": "The discharge process begins once the treating doctor signs the discharge clearance. Billing generation and pharmacy clearance typically take 2-3 hours. If you are using insurance, final TPA approval can take up to 4-6 hours after the bill is submitted. Once cleared, you will receive a detailed discharge summary, pending investigation reports, and a post-discharge care plan. A nursing supervisor will brief you on wound care, medication timings, and your follow-up appointment schedule before you leave.",
        "source": "Inpatient - Discharge Process",
        "category": "inpatient"
    },
    {
        "text": "Our visitor policy strictly permits visiting hours only between 4:00 PM and 6:00 PM daily to ensure patient rest and infection control. Only two visitors are allowed per patient at a time. Children under 12 are not permitted in the inpatient wards due to their vulnerability to hospital-acquired infections. One 24-hour attendant pass is issued per patient for a family member to stay overnight (applicable for Private rooms and above). Attendants must wear the pass at all times.",
        "source": "Inpatient - Visitor and Attendant Policy",
        "category": "inpatient"
    },
    {
        "text": "Patient meals and dietary services are entirely managed by our clinical nutrition department. Based on the doctor's orders, the in-house dietician prescribes a customized therapeutic diet (e.g., diabetic, low-sodium, renal, or clear liquid). Four freshly prepared meals are served daily directly to the patient's room: Breakfast, Lunch, Evening Soup/Snack, and Dinner. To prevent foodborne infections and ensure medical compliance, outside food and home-cooked meals are strictly prohibited for admitted patients.",
        "source": "Inpatient - Patient Meals and Dietary Services",
        "category": "inpatient"
    },
    {
        "text": "We maintain the highest nursing care standards, with all staff certified in Basic Life Support (BLS). Our nurse-to-patient ratio is 1:1 in the ICU and 1:4 in the general wards. Nursing duties prioritize precise medication administration, strict hygiene, fall prevention, and sterile wound dressing. We guarantee a call bell response time of under 2 minutes for any patient distress or requirement. A Nursing Superintendent is available 24/7 on every floor to address any immediate care concerns.",
        "source": "Inpatient - Nursing Care Standards",
        "category": "inpatient"
    }
]
def maternity_pediatrics_kb():
                return [
    {
        "text": "Our Comprehensive Antenatal Care (ANC) Program guides you safely from conception to delivery. The First Trimester (Weeks 1-12) includes a dating scan, NT scan, Double Marker test, and baseline blood profile (CBC, Blood Group, HIV, VDRL, HBsAg, Thyroid, Rubella). The Second Trimester (Weeks 13-26) covers the crucial Anomaly Scan (TIFFA) and Oral Glucose Tolerance Test (OGTT) for gestational diabetes. The Third Trimester (Weeks 27-40) includes growth scans, NST (Non-Stress Test) to monitor fetal heartbeat, and childbirth prep classes. Total Antenatal Package Price: ₹25,000 (includes all routine scans and 10 Obstetrician consultations).",
        "source": "Maternity - Antenatal Care Program",
        "category": "maternity"
    },
    {
        "text": "We offer transparent, all-inclusive Delivery Packages. Normal Delivery (2 days stay): ₹60,000. C-Section Delivery (3 days stay): ₹85,000. Water Birth (in specialized LDR Suite): ₹95,000. VBAC (Vaginal Birth After Cesarean) with continuous fetal monitoring: ₹75,000. Facilities include advanced LDR (Labor, Delivery, Recovery) suites allowing partners to stay, specialized birthing beds, and immediate access to emergency OTs. Painless delivery (Epidural) is available for an extra ₹10,000. A dedicated Neonatologist is available 24/7 and is mandatorily present at every birth to ensure immediate newborn resuscitation and care.",
        "source": "Maternity - Delivery Packages",
        "category": "maternity"
    },
    {
        "text": "Our Postnatal Care and Lactation Support program ensures a smooth transition to motherhood after delivery. It features our exclusive 'Latch & Bond' breastfeeding support program. Certified Lactation Consultants make daily ward visits to assist with proper latching techniques, resolving cracked nipples, managing engorgement, and teaching breast pump usage. We also offer pelvic floor physiotherapy. Post-discharge Home Care Package (includes 3 home visits by a lactation nurse and 2 online pediatrician consults): ₹5,500.",
        "source": "Maternity - Postnatal Care and Lactation Support",
        "category": "maternity"
    },
    {
        "text": "Our Level-3 Neonatal Intensive Care Unit (NICU) provides life-saving care for premature babies (born as early as 26 weeks) and critically ill newborns. The NICU is equipped with advanced Giraffe incubators, high-frequency transport ventilators, inhaled nitric oxide therapy, and LED phototherapy units. A Senior Neonatologist is physically present on the floor 24/7. NICU Charges: Level 1 (Basic care/Phototherapy for jaundice) - ₹5,000/day. Level 2 (CPAP/Continuous Monitoring) - ₹8,000/day. Level 3 (Advanced Ventilator support) - ₹15,000/day.",
        "source": "Maternity - NICU Services and Charges",
        "category": "maternity"
    },
    {
        "text": "The Newborn Care program begins immediately after birth with a comprehensive metabolic screening (Newborn Blood Spot test) and OAE Hearing Test (Package cost: ₹4,000). Our vaccination clinic strictly follows the Indian Academy of Pediatrics (IAP) schedule. Common vaccine prices per dose: BCG/Polio/Hep B (Birth) - ₹500; Hexavalent (6-in-1 painless at 6, 10, 14 weeks) - ₹3,500; Pneumococcal (PCV) - ₹3,800; Rotavirus Drops - ₹1,200; MMR (9 months) - ₹1,000; Typhoid - ₹2,000. The consultation fee for routine vaccination and newborn check-up visits is ₹800.",
        "source": "Maternity - Newborn Care and Vaccination",
        "category": "maternity"
    },
    {
        "text": "Our Pediatric OPD is designed to be child-friendly and stress-free, managing a wide spectrum of common childhood illnesses. Our pediatricians frequently treat conditions such as viral fevers, seasonal flu, pediatric asthma, gastrointestinal infections (diarrhea/vomiting), ear infections (Otitis Media), and skin conditions like eczema and diaper rash. The department features dedicated nebulization stations, a child play area, and specialized pediatric phlebotomists trained for painless blood draws. General Pediatric OPD Consultation fee: ₹800.",
        "source": "Maternity - Pediatric OPD",
        "category": "maternity"
    },
    {
        "text": "The Child Nutrition and Growth Monitoring Clinic focuses on identifying and managing developmental delays, picky eating behaviors, and childhood obesity. The clinic pairs a Senior Pediatrician with a Pediatric Clinical Dietician. Services include accurate BMI tracking on WHO growth charts, customized diet plans for anemic or underweight children, and height velocity tracking to detect growth hormone deficiencies early. Comprehensive Growth Clinic Package (includes Pediatric Consult, Dietician session, and Bone Age X-ray): ₹2,500.",
        "source": "Maternity - Child Nutrition Clinic",
        "category": "maternity"
    },
    {
        "text": "The Adolescent Health Clinic addresses the unique physical, hormonal, and emotional needs of teenagers aged 12-18 years. We offer confidential care for puberty-related concerns (such as early/delayed puberty), teenage acne, polycystic ovary syndrome (PCOS), and menstrual irregularities. We also provide crucial mental health counseling for academic stress, anxiety, and body image issues. The multidisciplinary team includes an Adolescent Pediatrician, a Gynecologist, and a Clinical Psychologist. Initial Comprehensive Consultation Fee: ₹1,200.",
        "source": "Maternity - Adolescent Health Clinic",
        "category": "maternity"
    }
]
def mental_health_kb():
        return [
    {
        "text": "Our Psychiatry Department offers expert OPD consultations and features a secure, 15-bed inpatient psychiatric ward for patients requiring acute stabilization or round-the-clock care in a safe environment. Initial psychiatric OPD assessments typically last 40 minutes, with 20-minute follow-ups. Consultation Fee: ₹1,500 (New), ₹1,000 (Follow-up). Under recent IRDAI mandates, inpatient psychiatric hospitalization is now covered by most standard health insurance policies. We adhere to a strict, legally binding confidentiality policy; no information is shared without your explicit consent.",
        "source": "Mental Health - Psychiatry Services",
        "category": "mental_health"
    },
    {
        "text": "Our Clinical Psychology and Counseling services focus on evidence-based talk therapies, including Cognitive Behavioral Therapy (CBT) and trauma-informed care. A standard individual therapy session lasts for 50 to 60 minutes. Depending on the care plan, frequency ranges from once a week to bi-weekly. Fee per session: ₹1,200. Absolute confidentiality is our cornerstone; therapy records are kept in highly encrypted, standalone servers distinct from general medical records, ensuring your privacy is protected.",
        "source": "Mental Health - Psychology and Counseling",
        "category": "mental_health"
    },
    {
        "text": "Our multidisciplinary team treats a comprehensive spectrum of mental illnesses, including Clinical Depression, Generalized Anxiety Disorder, Bipolar Disorder, Schizophrenia, Severe OCD (Obsessive-Compulsive Disorder), and PTSD (Post-Traumatic Stress Disorder). Treatment often involves a combined approach of pharmacotherapy and psychotherapy. If you or someone you know is experiencing a severe psychiatric emergency or suicidal thoughts, do not wait. Call our 24/7 Crisis Intervention Hotline immediately at 0831-240-9999.",
        "source": "Mental Health - Conditions Treated",
        "category": "mental_health"
    },
    {
        "text": "The 'Naya Savera' De-addiction Program helps individuals overcome substance use disorders, including alcohol, opioids, and prescription drugs. The program begins with medically supervised inpatient detoxification to manage withdrawal safely, followed by intensive rehab. It includes daily individual counseling and mandatory Group Therapy sessions held three times a week for peer support. A standard 21-day inpatient de-addiction package costs roughly ₹65,000. Outpatient follow-up sessions are billed at standard counseling rates.",
        "source": "Mental Health - De-addiction Program",
        "category": "mental_health"
    },
    {
        "text": "Our Child and Adolescent Mental Health clinic provides a safe space for youth struggling with ADHD, Autism Spectrum challenges, teenage depression, academic anxiety, and behavioral disorders. We utilize specialized modalities like play therapy for younger kids and targeted CBT for adolescents. Sessions run for 45-60 minutes (Fee: ₹1,500/session). While respecting the minor's need for a confidential space, we actively schedule separate family therapy sessions (usually bi-weekly) to equip parents with the right support tools.",
        "source": "Mental Health - Child and Adolescent",
        "category": "mental_health"
    },
    {
        "text": "For individuals navigating high-pressure careers or chronic daily stress, our Stress Management and Mindfulness Programs offer preventive mental health care. These programs teach practical coping mechanisms, deep breathing, and mindfulness meditation to prevent burnout and mild anxiety from escalating. Sessions are primarily conducted as interactive Group Therapy workshops over a 6-week module. Each 90-minute group session costs ₹600. Walk-in individual stress counseling is also available at ₹1,000 per 45-minute session.",
        "source": "Mental Health - Stress and Mindfulness",
        "category": "mental_health"
    }
]