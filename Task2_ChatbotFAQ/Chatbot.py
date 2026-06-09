
import re
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

# NLP libraries
import nltk
from nltk.corpus import stopwords
from nltk.stem   import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise        import cosine_similarity

# Download NLTK data silently (only once)
for pkg in ('punkt', 'stopwords', 'wordnet', 'punkt_tab'):
    nltk.download(pkg, quiet=True)


#  COMPREHENSIVE FAQ DATASET


FAQ_DATA = {

    # ── APPOINTMENTS ──────────────────────────────────────────
    "How do I book an appointment?":
        "📅 You can book an appointment through any of these ways:\n"
        "  • Call our helpline: 1800-XXX-XXXX (Mon–Sat, 8 AM–8 PM)\n"
        "  • Visit www.hospital.com/book-appointment\n"
        "  • Walk into the Reception Desk (Ground Floor)\n"
        "  • Use our Hospital Mobile App (available on iOS & Android)",

    "Can I book an appointment online?":
        "✅ Yes! Visit www.hospital.com/appointments, choose your department "
        "and preferred doctor, select a time slot, and confirm via OTP. "
        "You'll receive a confirmation SMS and email.",

    "How do I cancel or reschedule an appointment?":
        "📋 To cancel or reschedule:\n"
        "  • Online: Log into the patient portal and manage your appointments.\n"
        "  • Phone: Call 1800-XXX-XXXX at least 24 hours before your slot.\n"
        "  • Walk-in: Visit the Appointment Desk at the reception.\n"
        "Cancellations within 2 hours of the appointment may incur a ₹100 fee.",

    "What documents are needed for first visit?":
        "📄 For your first visit, please bring:\n"
        "  • Valid government-issued photo ID (Aadhaar, PAN, Passport)\n"
        "  • Health insurance card (if applicable)\n"
        "  • Previous medical records, X-rays, or test reports\n"
        "  • List of current medications and allergies\n"
        "  • Referral letter (if referred by another doctor)",

    "Can I get a same-day appointment?":
        "⚡ Same-day appointments are available for urgent cases. "
        "Visit the OPD walk-in counter early morning (opens at 8:30 AM) "
        "for same-day tokens. Availability depends on the doctor's schedule.",

    "How long will I have to wait for an appointment?":
        "⏳ Average waiting time is 15–30 minutes for scheduled appointments. "
        "Walk-in patients may wait 45–60 minutes. You will receive an SMS "
        "when your turn is approaching.",

    "Can I choose my doctor?":
        "👨‍⚕️ Yes! When booking online or by phone, you can browse available doctors "
        "by department and choose based on specialisation, availability, and patient ratings.",

    "Do you offer video or teleconsultation?":
        "💻 Yes! Our tele-consultation service is available Mon–Sat, 9 AM–6 PM. "
        "Book via the app or website. You'll receive a video link before your appointment. "
        "Charges: ₹300–₹600 depending on the specialist.",

    # ── EMERGENCY 
    "What should I do in a medical emergency?":
        "🚨 IN AN EMERGENCY:\n"
        "  1. Call 108 (National Ambulance Service) — FREE\n"
        "  2. Call our Emergency Helpline: 1800-XXX-9999 (24/7)\n"
        "  3. Come directly to our Emergency & Trauma Centre (ETC) — Gate 2\n"
        "DO NOT wait for an appointment. Our emergency team is available 24/7.",

    "Is the emergency ward open at night?":
        "🌙 Yes, our Emergency & Trauma Centre (ETC) operates 24 hours a day, "
        "365 days a year — including all public holidays.",

    "Do you have an ambulance service?":
        "🚑 Yes! We operate a fleet of fully equipped ambulances:\n"
        "  • Basic Life Support (BLS): ₹500–₹800\n"
        "  • Advanced Life Support (ALS) with ICU setup: ₹1,200–₹2,000\n"
        "  Call: 1800-XXX-9999 for immediate dispatch.",

    "What types of emergencies do you handle?":
        "🏥 Our Emergency Department handles:\n"
        "  Heart attacks, strokes, accidents & trauma, severe burns, "
        "fractures, poisoning, unconsciousness, severe breathing difficulty, "
        "high fever with convulsions, childbirth emergencies, and more.",

    "Is there a trauma centre?":
        "✅ Yes, our Level-II Trauma Centre is equipped with a dedicated trauma bay, "
        "emergency OT, ventilators, and 24/7 specialist cover for surgical emergencies.",

    # ── OPD & DEPARTMENT
    "What are the OPD timings?":
        "🕘 OPD Hours:\n"
        "  Monday – Friday : 9:00 AM – 5:00 PM\n"
        "  Saturday        : 9:00 AM – 2:00 PM\n"
        "  Sunday          : CLOSED (Emergency only)\n"
        "Some speciality OPDs run evening clinics till 7:00 PM.",

    "What departments does the hospital have?":
        "🏨 Our departments include:\n"
        "  Cardiology • Neurology • Orthopedics • Oncology • Gynecology & Obstetrics\n"
        "  Pediatrics • ENT • Ophthalmology • Dermatology • Psychiatry & Mental Health\n"
        "  Gastroenterology • Nephrology • Urology • Pulmonology • Endocrinology\n"
        "  Plastic Surgery • Dentistry • Physiotherapy • Dietetics • Radiology\n"
        "Visit our website for the complete list with doctor profiles.",

    "Is there a paediatrics department for children?":
        "👶 Yes! Our Paediatrics & Neonatology Department provides:\n"
        "  • Well-baby check-ups and immunisations\n"
        "  • Paediatric emergencies\n"
        "  • NICU (Neonatal Intensive Care Unit)\n"
        "  • Paediatric surgery\n"
        "OPD: Mon–Sat, 10 AM–4 PM. Emergency: 24/7.",

    "Do you have a cancer treatment centre?":
        "🎗️ Yes, our Comprehensive Cancer Care Centre offers:\n"
        "  • Medical Oncology (chemotherapy)\n"
        "  • Radiation Oncology (radiotherapy, LINAC)\n"
        "  • Surgical Oncology\n"
        "  • Palliative Care\n"
        "  • Cancer screening & early detection clinics",

    "Do you have a cardiology department?":
        "❤️ Yes, our Cardiology Department offers:\n"
        "  • ECG, Echo, Stress Test, Holter monitoring\n"
        "  • Angiography & Angioplasty\n"
        "  • Cardiac surgery & bypass\n"
        "  • 24/7 Heart Attack (STEMI) response team\n"
        "  • Cardiac rehabilitation programme",

    "Is there a maternity and delivery ward?":
        "🤰 Yes! Our Maternity & Women's Health Centre provides:\n"
        "  • Antenatal care and high-risk pregnancy management\n"
        "  • Normal & C-section deliveries\n"
        "  • Labour rooms with birthing partners allowed\n"
        "  • Postnatal care & lactation counselling\n"
        "  • NICU for premature babies",

    # ── VISITING HOURS ─
    "What are the visiting hours?":
        "🕐 Visiting Hours:\n"
        "  General Wards : 10:00 AM – 12:00 PM  &  5:00 PM – 7:00 PM\n"
        "  ICU / CCU     : 11:00 AM – 12:00 PM  &  5:00 PM – 6:00 PM (max 2 visitors)\n"
        "  NICU          : Parents only, 9 AM–9 PM with pass\n"
        "  Isolation Ward: Not permitted for visitors\n"
        "A maximum of 2 visitors per patient is allowed at a time.",

    "Can children visit patients in the hospital?":
        "👧 Children above 12 years may visit during general visiting hours. "
        "Children are not permitted in the ICU, NICU, or isolation wards "
        "to protect both the patients and the children.",

    "Are there any restrictions on visitors?":
        "⚠️ Visitor guidelines:\n"
        "  • Maximum 2 visitors at a time\n"
        "  • Visitor passes are mandatory (collect at Reception)\n"
        "  • Masks recommended in clinical areas\n"
        "  • No food from outside in ICU or surgical wards\n"
        "  • Mobile phones on silent mode in wards",

    # ── BILLING & INSURANCE ───────────────────────────────────
    "Does the hospital accept health insurance?":
        "💳 Yes, we are empanelled with 50+ insurance providers including:\n"
        "  Star Health • HDFC Ergo • ICICI Lombard • New India Assurance\n"
        "  United India • Oriental Insurance • Bajaj Allianz • Niva Bupa\n"
        "  Government schemes: Ayushman Bharat (PMJAY), CGHS, ECHS, ESI\n"
        "Visit the Insurance Desk (Ground Floor) with your policy documents.",

    "How do I get a cost estimate before treatment?":
        "📊 Pre-treatment cost estimates are available at:\n"
        "  • Billing Counter — Ground Floor (Mon–Sat, 8 AM–8 PM)\n"
        "  • Call: 1800-XXX-2222\n"
        "  • Email: billing@hospital.com\n"
        "Estimates are provided in writing within 1 working day for planned procedures.",

    "What payment methods are accepted?":
        "💰 Accepted payment methods:\n"
        "  Cash • Credit/Debit Cards (Visa, Mastercard, RuPay)\n"
        "  UPI: GPay, PhonePe, Paytm, BHIM • Net banking\n"
        "  EMI available for bills above ₹10,000 (select banks)\n"
        "  Demand Draft / Cheque for insurance settlements",

    "Can I pay in instalments?":
        "📆 Yes, EMI / instalment options are available for bills above ₹10,000 "
        "through select bank credit cards (6 / 12 / 18 months). "
        "Speak to the Billing Counter for details.",

    "Is there any financial assistance available?":
        "🤝 Yes, we offer:\n"
        "  • Ayushman Bharat (PMJAY) for eligible families\n"
        "  • Hospital Charitable Fund for BPL patients (apply at Social Welfare Desk)\n"
        "  • Concession for senior citizens (10% on OPD consultation)\n"
        "  • Tie-ups with NGOs for cancer and dialysis patients",

    "How do I get a receipt or invoice?":
        "🧾 Receipts are issued at the Billing Counter after every payment. "
        "Detailed GST invoices can be downloaded from the Patient Portal "
        "(www.hospital.com/portal) or requested at the billing desk.",

    # ── LABORATORY & DIAGNOSTICS ──────────────────────────────
    "How do I collect my lab test reports?":
        "🧪 Lab reports are available via:\n"
        "  • Patient Portal: www.hospital.com/portal (within 24–48 hours)\n"
        "  • SMS/Email notification when ready\n"
        "  • Printed copy at Pathology Counter (Lab, Ground Floor)\n"
        "Routine reports: 24–48 hours. Urgent/STAT reports: 4–6 hours.",

    "Can I get my reports online?":
        "💻 Yes! Register at www.hospital.com/portal with your patient ID "
        "to access all reports, prescriptions, and discharge summaries anytime.",

    "What tests are available in the lab?":
        "🔬 Our NABL-accredited laboratory offers:\n"
        "  Complete Blood Count (CBC) • Blood Sugar (FBS/PPBS/HbA1c)\n"
        "  Lipid Profile • Liver & Kidney Function Tests • Thyroid Profile\n"
        "  Urine Routine • Culture & Sensitivity • Hormone tests\n"
        "  Biopsy & Histopathology • Genetic testing • COVID RT-PCR",

    "Are home sample collection services available?":
        "🏠 Yes! We offer home sample collection:\n"
        "  • Book via app / website or call 1800-XXX-3333\n"
        "  • Available 7 AM – 11 AM, Mon–Sat\n"
        "  • Service charge: ₹100 (waived for seniors above 70)\n"
        "  • Reports delivered digitally within 24 hours",

    "Do you have MRI and CT scan facilities?":
        "🖥️ Yes, our Radiology Department has:\n"
        "  • 3 Tesla MRI (latest high-definition imaging)\n"
        "  • 128-slice CT Scanner\n"
        "  • Digital X-Ray & Fluoroscopy\n"
        "  • 4D Ultrasound & Colour Doppler\n"
        "  • Bone Density (DEXA) Scan\n"
        "Reports are provided by experienced radiologists within 2–4 hours.",

    # ── ADMISSIONS & DISCHARGE ────────────────────────────────
    "How do I get admitted to the hospital?":
        "🛏️ Admission process:\n"
        "  1. Doctor issues an admission advice slip\n"
        "  2. Visit the Admission Desk (Ground Floor) with the slip & ID\n"
        "  3. Choose ward category (General / Semi-Private / Private / Suite)\n"
        "  4. Pay admission deposit (amount varies by ward type)\n"
        "  5. Get escorted to your room by our ward staff",

    "What types of rooms / wards are available?":
        "🏨 Room options:\n"
        "  General Ward   : Shared (6–8 beds) — most affordable\n"
        "  Semi-Private   : 2-bed room with attached bathroom\n"
        "  Private Room   : Single occupancy with TV, AC, attendant sofa\n"
        "  Deluxe Suite   : Premium amenities, separate lounge for family\n"
        "  ICU / ICCU     : Intensive care with 24/7 monitoring",

    "What is the discharge process?":
        "📤 Discharge steps:\n"
        "  1. Treating doctor issues a Discharge Summary\n"
        "  2. Nursing team gives final medication instructions\n"
        "  3. Visit Billing Counter to clear dues & settle insurance\n"
        "  4. Collect medicines from pharmacy\n"
        "  5. Collect all documents (reports, discharge card, follow-up slip)\n"
        "Typical discharge time: 10 AM – 2 PM. Process takes 2–4 hours.",

    "Can someone else collect discharge documents on my behalf?":
        "✅ Yes. An authorised representative may collect documents with:\n"
        "  • Their own valid photo ID\n"
        "  • A signed authorisation letter from the patient\n"
        "  • Copy of patient's ID proof",

    "Can I get a duplicate discharge summary?":
        "📋 Yes, duplicate discharge summaries can be issued.\n"
        "  • Visit Medical Records Department (1st Floor) with your patient ID.\n"
        "  • Processing time: 2–3 working days.\n"
        "  • Charges: ₹200 for duplicate copy.",

    # ── MEDICATIONS & PHARMACY ────────────────────────────────
    "Is there a pharmacy in the hospital?":
        "💊 Yes! Our 24/7 In-house Pharmacy is located near the main entrance (Ground Floor).\n"
        "  • Stocks branded and generic medicines\n"
        "  • Surgical consumables and medical equipment\n"
        "  • Compounding services available\n"
        "  • 10% discount for inpatients on hospital prescriptions",

    "Can I bring my own medicines from outside?":
        "💊 Yes, you may bring your regular medicines from home. However, all medications "
        "must be declared to the nursing team on admission. The doctor will review them "
        "and advise whether to continue or switch.",

    "Do you have a blood bank?":
        "🩸 Yes, our licensed Blood Bank operates 24/7:\n"
        "  • All blood groups available\n"
        "  • Platelet concentrate, FFP, packed RBCs\n"
        "  • Voluntary blood donation camps held monthly\n"
        "  Contact: 1800-XXX-4444 or visit Ground Floor, Wing B",

    # ── FACILITIES & SERVICES ─────────────────────────────────
    "Is parking available at the hospital?":
        "🚗 Yes, multi-level parking is available:\n"
        "  • 400 car spaces + 200 two-wheeler spaces\n"
        "  • First 2 hours: FREE\n"
        "  • ₹30 per hour thereafter; ₹200 per day cap\n"
        "  • Valet parking available at Main Entrance: ₹100",

    "Is there a cafeteria or food service?":
        "🍽️ Food options on campus:\n"
        "  • Main Cafeteria (1st Floor): 7 AM – 9 PM — healthy meals & snacks\n"
        "  • Coffee Kiosk (Ground Floor): 6 AM – 10 PM\n"
        "  • Inpatient meal service: 3 meals/day included in room charge\n"
        "  • Diet meals prepared per dietician advice for patients",

    "Is there a chemist or medical store nearby?":
        "🏪 Our 24/7 in-house pharmacy stocks everything you need. "
        "Additionally, two external pharmacies are located within 200 metres of the hospital.",

    "Do you have free Wi-Fi for patients?":
        "📶 Free Wi-Fi (HospitalGuest) is available throughout the campus. "
        "Ask Reception for the current password. Speed is 10 Mbps shared.",

    "Are wheelchairs and stretchers available?":
        "♿ Complimentary wheelchairs and stretchers are available at:\n"
        "  • Main Entrance\n"
        "  • Emergency Gate\n"
        "  • Each floor lift lobby\n"
        "Request one at Reception or from any ward staff.",

    "Is there an ATM on campus?":
        "🏧 Yes, an SBI ATM is located at the Main Entrance (Ground Floor, left side). "
        "A second ATM (HDFC) is near the cafeteria on the 1st Floor.",

    "Are attendant facilities available for inpatients?":
        "🛋️ One attendant is permitted per inpatient. Attendant cots/recliner chairs "
        "are provided in private and semi-private rooms. Bathroom facilities are shared "
        "in general wards. Attendant meals can be ordered from the cafeteria.",

    # ── COVID & INFECTION CONTROL ─────────────────────────────
    "What COVID-19 precautions are in place?":
        "😷 Current safety measures:\n"
        "  • Hand sanitiser stations at all entry points\n"
        "  • Masks recommended in OPD, wards, and elevators\n"
        "  • Fever screening at the main entrance\n"
        "  • Dedicated isolation rooms for respiratory cases\n"
        "  • Regular deep-cleaning of all patient areas",

    "Do you offer COVID-19 testing?":
        "🧬 Yes, we offer:\n"
        "  • RT-PCR test: Results in 12–24 hours (₹500)\n"
        "  • Rapid Antigen Test: Results in 30 minutes (₹300)\n"
        "  • Home sample collection available (call 1800-XXX-3333)\n"
        "  • Certificate issued for travel purposes",

    # ── MENTAL HEALTH ─────────────────────────────────────────
    "Do you have a psychiatry or mental health department?":
        "🧠 Yes, our Psychiatry & Mental Health Department offers:\n"
        "  • Consultations for depression, anxiety, OCD, schizophrenia\n"
        "  • Addiction & De-addiction counselling\n"
        "  • Child & Adolescent Mental Health\n"
        "  • Inpatient psychiatric ward (closed ward with supervision)\n"
        "  • Tele-psychiatry sessions available\n"
        "OPD: Mon, Wed, Fri — 10 AM to 1 PM",

    "Is counselling available at the hospital?":
        "💬 Yes! Our team of clinical psychologists and counsellors offer:\n"
        "  • Individual therapy sessions\n"
        "  • Grief and bereavement support\n"
        "  • Pre & post-surgery anxiety management\n"
        "  • Family counselling for caregivers\n"
        "Book through reception or ask your treating doctor for a referral.",

    # ── PHYSIOTHERAPY & REHABILITATION ───────────────────────
    "Is physiotherapy available?":
        "🏃 Yes! Our Physiotherapy & Rehabilitation Centre offers:\n"
        "  • Post-surgery and post-fracture rehabilitation\n"
        "  • Stroke and neuro-rehabilitation\n"
        "  • Sports injury management\n"
        "  • Back and neck pain therapy\n"
        "  • Paediatric physiotherapy\n"
        "Timings: Mon–Sat, 8 AM – 6 PM. Home visits available on request.",

    # ── SECOND OPINION & RECORDS ──────────────────────────────
    "How can I get a second opinion?":
        "🩺 You can request a second opinion in two ways:\n"
        "  1. Ask your doctor to arrange a MDT (Multi-Disciplinary Team) meeting.\n"
        "  2. Book separately with a specialist in the same department.\n"
        "All your records are available on the Patient Portal to share easily.",

    "How do I get copies of my medical records?":
        "📁 Visit the Medical Records Department (1st Floor):\n"
        "  • Bring your patient ID and photo ID proof\n"
        "  • Fill a record request form\n"
        "  • Records dispatched within 3–5 working days\n"
        "  • Charges: ₹5 per page (physical) | Free digital download via portal",

    # ── GENERAL & CONTACT ─────────────────────────────────────
    "What are the hospital contact details?":
        "📞 Contact us:\n"
        "  Main Helpline : 1800-XXX-XXXX (Mon–Sat, 8 AM–8 PM)\n"
        "  Emergency     : 1800-XXX-9999 (24/7)\n"
        "  Ambulance     : 108 (National) or 1800-XXX-9999\n"
        "  Email         : info@hospital.com\n"
        "  Website       : www.hospital.com\n"
        "  Address       : 123 Health Avenue, City — 440001",

    "Where is the hospital located?":
        "📍 We are located at:\n"
        "  123 Health Avenue, Near City Mall, Nagpur – 440001\n"
        "  Landmarks: Opposite Central Park, next to City Bank\n"
        "  Google Maps: maps.hospital.com\n"
        "  Bus routes: 12, 34, 56 stop at Hospital Gate\n"
        "  Nearest Metro: Central Metro Station (5 min walk)",

    "Do you have a patient feedback or complaint process?":
        "📝 We value your feedback!\n"
        "  • Fill a feedback form at Reception or online at www.hospital.com/feedback\n"
        "  • For complaints: contact Patient Relations Officer — 1800-XXX-5555\n"
        "  • Email: grievance@hospital.com\n"
        "  • Complaint resolution within 48 working hours",

    "Is the hospital accredited?":
        "🏅 Yes, our hospital is:\n"
        "  • NABH Accredited (National Accreditation Board for Hospitals)\n"
        "  • NABL Accredited Laboratory\n"
        "  • ISO 9001:2015 Certified\n"
        "  • Empanelled with Ayushman Bharat and all major insurers",

    "Do you offer health check-up packages?":
        "🩺 Yes! We offer preventive health check-up packages:\n"
        "  • Basic Package (₹999): CBC, Blood Sugar, Urine, ECG\n"
        "  • Comprehensive (₹2,499): 50+ tests + doctor consultation\n"
        "  • Senior Citizen Package (₹1,799): Age-specific screenings\n"
        "  • Executive Health Check (₹4,999): Full body with imaging\n"
        "Book online or call 1800-XXX-XXXX.",

    "Is there a special diet or dietician service?":
        "🥗 Yes! Our Clinical Dietetics Department offers:\n"
        "  • Customised diet plans for diabetes, kidney disease, heart conditions\n"
        "  • Weight management programmes\n"
        "  • Pre and post-surgery nutrition counselling\n"
        "  • Inpatient therapeutic meal planning\n"
        "Consultation: OPD, Mon–Sat, 10 AM – 4 PM",

    "Do you have an eye / ophthalmology department?":
        "👁️ Yes! Our Ophthalmology Department offers:\n"
        "  • Cataract surgery (phacoemulsification)\n"
        "  • LASIK and refractive surgery\n"
        "  • Glaucoma and retina clinics\n"
        "  • Paediatric eye care\n"
        "  • Diabetic retinopathy screening\n"
        "OPD: Mon–Sat, 9 AM – 1 PM & 3 PM – 5 PM",

    "Do you have a dental department?":
        "🦷 Yes! Our Dental & Maxillofacial Surgery unit offers:\n"
        "  • General dentistry (fillings, extractions, cleaning)\n"
        "  • Root canal treatment\n"
        "  • Dental implants and crowns\n"
        "  • Orthodontics (braces & aligners)\n"
        "  • Oral surgery & jaw procedures\n"
        "OPD: Mon–Sat, 9 AM – 5 PM",

    "What are the ICU facilities like?":
        "🏥 Our Intensive Care Units:\n"
        "  • Medical ICU (MICU): 20 beds with ventilators\n"
        "  • Surgical ICU (SICU): 16 beds, post-op monitoring\n"
        "  • Cardiac ICU (CICU): specialised cardiac monitoring\n"
        "  • Neonatal ICU (NICU): 10 incubators & warmers\n"
        "  • Paediatric ICU (PICU): 8 beds\n"
        "  All ICUs have 24/7 intensivist cover.",

    "Is a social worker or support available for patients?":
        "🤲 Yes! Our Medical Social Work team helps with:\n"
        "  • Financial assistance applications\n"
        "  • Government scheme enrolment (Ayushman Bharat etc.)\n"
        "  • Discharge planning and home care arrangements\n"
        "  • Emotional support and family counselling\n"
        "  • Legal documentation (medico-legal cases)\n"
        "Contact: Social Work Dept, 1st Floor, Mon–Sat 9 AM – 5 PM",
}



lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text: str) -> str:
    """Lowercase → strip punctuation → tokenise → remove stopwords → lemmatise."""
    text   = text.lower()
    text   = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return ' '.join(tokens)

# Build TF-IDF matrix from all FAQ questions
faq_questions = list(FAQ_DATA.keys())
faq_answers   = list(FAQ_DATA.values())
processed_qs  = [preprocess(q) for q in faq_questions]

vectorizer   = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_qs)

THRESHOLD = 0.12   # minimum similarity to return a real answer

def get_answer(user_input: str) -> str:
    """Return the best-matching FAQ answer or a fallback message."""
    processed = preprocess(user_input)
    user_vec   = vectorizer.transform([processed])
    sims       = cosine_similarity(user_vec, tfidf_matrix)[0]
    best_idx   = sims.argmax()
    best_score = sims[best_idx]

    if best_score < THRESHOLD:
        return (
            "❓ I'm sorry, I couldn't find a matching answer for that question.\n\n"
            "Please try rephrasing, or contact us directly:\n"
            "  📞 Helpline : 1800-XXX-XXXX\n"
            "  📧 Email    : info@hospital.com\n"
            "  🌐 Website  : www.hospital.com"
        )
    return faq_answers[best_idx]




QUICK_REPLIES = [
    "Book an appointment",
    "OPD timings",
    "Emergency services",
    "Insurance accepted",
    "Lab reports",
    "Visiting hours",
    "Discharge process",
    "Pharmacy",
    "Parking",
    "Contact details",
]

#   TKINTER GUI
# ── Colour palette 
C_BG          = "#F0F4F8"   # page background — soft blue-grey
C_HEADER_BG   = "#1A5276"   # header — deep navy (trust / medicine)
C_HEADER_FG   = "#FFFFFF"
C_CHAT_BG     = "#FFFFFF"   # chat area
C_USER_BUBBLE = "#1A5276"   # user message — navy
C_USER_FG     = "#FFFFFF"
C_BOT_BUBBLE  = "#EAF2FB"   # bot message — light blue
C_BOT_FG      = "#1A252F"
C_INPUT_BG    = "#FFFFFF"
C_SEND_BG     = "#1A5276"
C_SEND_FG     = "#FFFFFF"
C_SEND_HOVER  = "#154360"
C_CHIP_BG     = "#D6EAF8"
C_CHIP_FG     = "#1A5276"
C_CHIP_HOVER  = "#AED6F1"
C_ACCENT      = "#2E86C1"

FONT_HEADER  = ("Segoe UI", 15, "bold")
FONT_SUB     = ("Segoe UI", 9)
FONT_CHAT    = ("Segoe UI", 10)
FONT_INPUT   = ("Segoe UI", 11)
FONT_SEND    = ("Segoe UI", 10, "bold")
FONT_CHIP    = ("Segoe UI", 9)
FONT_TIME    = ("Segoe UI", 8)


class HospitalChatbotApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self._build_window()
        self._build_header()
        self._build_chat_area()
        self._build_quick_replies()
        self._build_input_bar()
        self._welcome_message()

    # ── Window setup ──
    def _build_window(self):
        self.root.title("🏥 Hospital FAQ Chatbot")
        self.root.geometry("780x680")
        self.root.minsize(600, 500)
        self.root.configure(bg=C_BG)
        self.root.resizable(True, True)
        # Centre window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 780) // 2
        y = (self.root.winfo_screenheight() - 680) // 2
        self.root.geometry(f"780x680+{x}+{y}")

    # ── Header banner ───
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C_HEADER_BG, pady=12)
        hdr.pack(fill=tk.X)

        tk.Label(
            hdr, text="🏥  City General Hospital",
            font=FONT_HEADER, bg=C_HEADER_BG, fg=C_HEADER_FG
        ).pack()

        tk.Label(
            hdr, text="Patient FAQ Assistant  •  Available 24 / 7",
            font=FONT_SUB, bg=C_HEADER_BG, fg="#AED6F1"
        ).pack()

        # Status dot
        status_frame = tk.Frame(hdr, bg=C_HEADER_BG)
        status_frame.pack(pady=(4, 0))
        tk.Label(status_frame, text="●", fg="#58D68D",
                 bg=C_HEADER_BG, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        tk.Label(status_frame, text=" Online", fg="#AED6F1",
                 bg=C_HEADER_BG, font=FONT_SUB).pack(side=tk.LEFT)

    # ── Scrollable chat area ───────────────────────────────────
    def _build_chat_area(self):
        outer = tk.Frame(self.root, bg=C_BG)
        outer.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

        # Canvas + scrollbar for custom bubble layout
        self.canvas = tk.Canvas(outer, bg=C_CHAT_BG, highlightthickness=0)
        scrollbar   = ttk.Scrollbar(outer, orient="vertical",
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inner frame that holds all message bubbles
        self.chat_frame = tk.Frame(self.canvas, bg=C_CHAT_BG)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.chat_frame, anchor="nw"
        )

        # Keep canvas width in sync with window width
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.chat_frame.bind("<Configure>",
                             lambda e: self.canvas.configure(
                                 scrollregion=self.canvas.bbox("all")))

        # Mouse-wheel scroll
        self.canvas.bind_all("<MouseWheel>",    self._on_mousewheel)
        self.canvas.bind_all("<Button-4>",      self._on_mousewheel)
        self.canvas.bind_all("<Button-5>",      self._on_mousewheel)

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ── Quick-reply chips ─────────────────────────────────────
    def _build_quick_replies(self):
        chips_outer = tk.Frame(self.root, bg=C_BG)
        chips_outer.pack(fill=tk.X, padx=10, pady=(6, 0))

        tk.Label(chips_outer, text="Quick questions:",
                 bg=C_BG, fg="#5D6D7E", font=FONT_TIME).pack(anchor="w")

        # Two rows of chips using a canvas for horizontal scroll if needed
        chips_inner = tk.Frame(chips_outer, bg=C_BG)
        chips_inner.pack(fill=tk.X)

        row1 = tk.Frame(chips_inner, bg=C_BG)
        row1.pack(anchor="w")
        row2 = tk.Frame(chips_inner, bg=C_BG)
        row2.pack(anchor="w", pady=(2, 0))

        for i, label in enumerate(QUICK_REPLIES):
            parent = row1 if i < 5 else row2
            btn = tk.Button(
                parent, text=label, font=FONT_CHIP,
                bg=C_CHIP_BG, fg=C_CHIP_FG,
                relief=tk.FLAT, bd=0, cursor="hand2",
                padx=10, pady=4, borderwidth=0,
                activebackground=C_CHIP_HOVER,
                command=lambda q=label: self._chip_click(q)
            )
            btn.pack(side=tk.LEFT, padx=(0, 6))
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=C_CHIP_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=C_CHIP_BG))

    def _chip_click(self, text):
        self.input_var.set(text)
        self._send_message()

    # ── Input bar ─────────────────────────────────────────────
    def _build_input_bar(self):
        bar = tk.Frame(self.root, bg=C_BG, pady=8)
        bar.pack(fill=tk.X, padx=10, pady=(6, 10))

        # Text entry
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(
            bar, textvariable=self.input_var,
            font=FONT_INPUT, bg=C_INPUT_BG, fg="#1A252F",
            relief=tk.FLAT, bd=0,
            insertbackground=C_ACCENT,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,
                        ipady=10, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._send_message())
        self.entry.insert(0, "Type your question here…")
        self.entry.configure(fg="#95A5A6")
        self.entry.bind("<FocusIn>",  self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._restore_placeholder)

        # Send button
        send_btn = tk.Button(
            bar, text="Send  ➤", font=FONT_SEND,
            bg=C_SEND_BG, fg=C_SEND_FG,
            relief=tk.FLAT, bd=0, cursor="hand2",
            padx=18, pady=10,
            activebackground=C_SEND_HOVER,
            command=self._send_message
        )
        send_btn.pack(side=tk.RIGHT)
        send_btn.bind("<Enter>", lambda e: send_btn.configure(bg=C_SEND_HOVER))
        send_btn.bind("<Leave>", lambda e: send_btn.configure(bg=C_SEND_BG))

        # Separator line above input
        sep = tk.Frame(self.root, height=1, bg="#D5D8DC")
        sep.place(relx=0, rely=1.0, anchor="sw",
                  width=780)   # just visual, positioned via pack order

        self.entry.focus_set()

    def _clear_placeholder(self, _event):
        if self.entry.get() == "Type your question here…":
            self.entry.delete(0, tk.END)
            self.entry.configure(fg="#1A252F")

    def _restore_placeholder(self, _event):
        if not self.entry.get().strip():
            self.entry.insert(0, "Type your question here…")
            self.entry.configure(fg="#95A5A6")

    # ── Welcome message ───────────────────────────────────────
    def _welcome_message(self):
        self._add_bot_bubble(
            "👋 Welcome to City General Hospital!\n\n"
            "I'm your virtual FAQ assistant. I can help you with:\n"
            "  • Appointments & OPD timings\n"
            "  • Emergency services\n"
            "  • Billing & insurance\n"
            "  • Lab reports & diagnostics\n"
            "  • Admissions, discharge & more\n\n"
            "Type your question below or tap a quick-reply chip to get started."
        )

    # ── Message sending flow ──────────────────────────────────
    def _send_message(self):
        text = self.input_var.get().strip()
        if not text or text == "Type your question here…":
            return
        self.input_var.set("")
        self.entry.configure(fg="#1A252F")
        self._add_user_bubble(text)
        # Run NLP in background thread to keep UI responsive
        threading.Thread(target=self._fetch_answer, args=(text,),
                         daemon=True).start()

    def _fetch_answer(self, text: str):
        answer = get_answer(text)
        self.root.after(0, lambda: self._add_bot_bubble(answer))

    # ── Bubble rendering ──────────────────────────────────────
    def _add_user_bubble(self, text: str):
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")

        row = tk.Frame(self.chat_frame, bg=C_CHAT_BG)
        row.pack(fill=tk.X, padx=12, pady=(6, 2))

        # Timestamp
        tk.Label(row, text=f"You  {now}", bg=C_CHAT_BG,
                 fg="#95A5A6", font=FONT_TIME).pack(anchor="e")

        bubble = tk.Label(
            row, text=text, font=FONT_CHAT,
            bg=C_USER_BUBBLE, fg=C_USER_FG,
            wraplength=480, justify=tk.LEFT,
            padx=14, pady=10,
        )
        bubble.pack(anchor="e", pady=(0, 2))
        self._scroll_to_bottom()

    def _add_bot_bubble(self, text: str):
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")

        row = tk.Frame(self.chat_frame, bg=C_CHAT_BG)
        row.pack(fill=tk.X, padx=12, pady=(6, 2))

        # Timestamp
        tk.Label(row, text=f"🏥 Assistant  {now}", bg=C_CHAT_BG,
                 fg="#95A5A6", font=FONT_TIME).pack(anchor="w")

        bubble = tk.Label(
            row, text=text, font=FONT_CHAT,
            bg=C_BOT_BUBBLE, fg=C_BOT_FG,
            wraplength=520, justify=tk.LEFT,
            padx=14, pady=10,
        )
        bubble.pack(anchor="w", pady=(0, 2))
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        self.root.after(50, lambda: self.canvas.yview_moveto(1.0))



#  ENTRY POINT

if __name__ == "__main__":
    root = tk.Tk()
    app  = HospitalChatbotApp(root)
    root.mainloop()
