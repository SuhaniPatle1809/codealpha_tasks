

import nltk
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Download required NLTK data (runs once)
nltk.download('punkt',      quiet=True)
nltk.download('stopwords',  quiet=True)
nltk.download('wordnet',    quiet=True)

from nltk.corpus   import stopwords
from nltk.stem     import WordNetLemmatizer

# ─────────────────────────────────────────────────
# Step 2: Hospital FAQ Dataset
#         (question → answer pairs)
# ─────────────────────────────────────────────────
FAQ_DATA = {
    # ── Appointments ──────────────────────────────
    "How do I book an appointment?":
        "You can book an appointment by calling our helpline at 1800-XXX-XXXX, "
        "visiting our website, or walking into the reception desk.",

    "Can I reschedule my appointment?":
        "Yes! Call us at least 24 hours before your appointment to reschedule "
        "without any charges.",

    "What documents do I need for my first visit?":
        "Please bring a valid government ID, your insurance card, any previous "
        "medical records, and a list of current medications.",

    # ── Emergency ─────────────────────────────────
    "What should I do in a medical emergency?":
        "Call 108 (ambulance) immediately or visit our 24/7 Emergency Department "
        "at the hospital entrance. Do NOT wait for an appointment in emergencies.",

    "Is there an emergency ward available at night?":
        "Yes, our Emergency & Trauma Centre is open 24 hours a day, 7 days a week, "
        "including all holidays.",

    # ── Visiting Hours ────────────────────────────
    "What are the visiting hours?":
        "General visiting hours are 10:00 AM – 12:00 PM and 5:00 PM – 7:00 PM. "
        "ICU visits are restricted to 15 minutes twice a day with prior permission.",

    "Can children visit patients?":
        "Children above 12 years are allowed during general visiting hours. "
        "For ICU or isolation wards, children are not permitted.",

    # ── Billing & Insurance ───────────────────────
    "Does the hospital accept insurance?":
        "Yes, we are empanelled with most major insurance providers including "
        "Star Health, HDFC Ergo, and government schemes like Ayushman Bharat.",

    "How do I get a billing estimate before treatment?":
        "You can request a pre-treatment cost estimate at the Billing Counter (Ground Floor) "
        "or call our billing helpline. Estimates are provided in writing.",

    "What payment methods are accepted?":
        "We accept cash, all major credit/debit cards, UPI (GPay, PhonePe, Paytm), "
        "and net banking. EMI options are available for bills above ₹10,000.",

    # ── Departments ───────────────────────────────
    "What departments does the hospital have?":
        "We have Cardiology, Neurology, Orthopedics, Pediatrics, Oncology, "
        "Gynecology, ENT, Dermatology, Psychiatry, and many more. "
        "Visit our website for the full list.",

    "Do you have a pharmacy inside the hospital?":
        "Yes, our in-house pharmacy is open 24/7 on the Ground Floor near the main entrance.",

    # ── Tests & Reports ───────────────────────────
    "How do I collect my lab reports?":
        "Reports are available online via our patient portal within 24–48 hours, "
        "or you can collect printed copies from the Pathology counter.",

    "Can I get an online medical report?":
        "Yes! Register on our patient portal at www.hospital.com/portal "
        "to download reports, prescriptions, and discharge summaries anytime.",

    # ── COVID / Infection Control ─────────────────
    "What COVID-19 precautions are in place?":
        "All visitors must sanitize hands at entry. Masks are recommended in OPD areas. "
        "Patients with fever are screened before entry as a precaution.",

    # ── Parking & Facilities ──────────────────────
    "Is parking available at the hospital?":
        "Yes, we have a multi-level car park with 300 spaces. "
        "Parking is free for the first 2 hours; ₹30/hour thereafter.",

    "Is there a cafeteria in the hospital?":
        "Yes, our cafeteria on the 1st Floor is open from 7:00 AM to 9:00 PM, "
        "serving healthy meals, snacks, and beverages.",

    # ── Discharge ─────────────────────────────────
    "What is the discharge process?":
        "The treating doctor issues a discharge summary. After that, visit the "
        "Billing Counter to clear dues, collect medicines, and get final documents. "
        "The process usually takes 2–4 hours.",

    "Can someone else collect my discharge documents?":
        "Yes, an authorised representative with your ID proof and a signed consent "
        "letter can collect discharge documents on your behalf.",

    # ── General ───────────────────────────────────
    "What are the hospital timings?":
        "OPD hours are Monday–Saturday, 9:00 AM – 5:00 PM. "
        "Emergency services run 24/7. The hospital is closed for OPD on Sundays.",

    "How do I contact the hospital?":
        "Call us at 1800-XXX-XXXX (toll-free) or email info@hospital.com. "
        "You can also use the 'Contact Us' form on our website.",
}


# ─────────────────────────────────────────────────
# Step 3: Text Preprocessing with NLTK
# ─────────────────────────────────────────────────

lemmatizer   = WordNetLemmatizer()
stop_words   = set(stopwords.words('english'))

def preprocess(text: str) -> str:
    """
    Clean and normalise a text string:
    1. Lowercase
    2. Remove punctuation & special characters
    3. Tokenise
    4. Remove stopwords
    5. Lemmatize
    """
    text   = text.lower()
    text   = re.sub(r'[^a-z0-9\s]', '', text)           # remove punctuation
    tokens = nltk.word_tokenize(text)                    # tokenise
    tokens = [t for t in tokens if t not in stop_words] # remove stopwords
    tokens = [lemmatizer.lemmatize(t) for t in tokens]  # lemmatize
    return ' '.join(tokens)


# ─────────────────────────────────────────────────
# Step 4: Build TF-IDF Vectors for All FAQ Questions
# ─────────────────────────────────────────────────

faq_questions = list(FAQ_DATA.keys())
faq_answers   = list(FAQ_DATA.values())

# Preprocess every FAQ question once
processed_questions = [preprocess(q) for q in faq_questions]

# Fit TF-IDF on the processed questions
vectorizer  = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_questions)  # shape: (n_faqs, vocab)


# ─────────────────────────────────────────────────
# Step 5: Match User Question to Best FAQ
# ─────────────────────────────────────────────────

CONFIDENCE_THRESHOLD = 0.15   # minimum cosine similarity to return an answer

def get_best_answer(user_input: str) -> tuple[str, float]:
    """
    Vectorise the user query, compute cosine similarity against
    all FAQ questions, and return the best matching answer + score.
    """
    processed_input  = preprocess(user_input)
    user_vec         = vectorizer.transform([processed_input])       # (1, vocab)
    similarities     = cosine_similarity(user_vec, tfidf_matrix)[0] # (n_faqs,)

    best_idx   = similarities.argmax()
    best_score = similarities[best_idx]

    if best_score < CONFIDENCE_THRESHOLD:
        return (
            "I'm sorry, I couldn't find a matching answer. "
            "Please call our helpline at 1800-XXX-XXXX for assistance.",
            best_score
        )

    return faq_answers[best_idx], best_score


# ─────────────────────────────────────────────────
# Step 6: Interactive Chat UI (Terminal)
# ─────────────────────────────────────────────────

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║        🏥  HOSPITAL FAQ CHATBOT  🏥               ║
║  Ask me anything about appointments, billing,     ║
║  departments, timings, or emergency services.     ║
║  Type  'help'  to see sample questions.           ║
║  Type  'quit'  or  'exit'  to leave.              ║
╚══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

SAMPLE_QUESTIONS = [
    "How do I book an appointment?",
    "Is there an emergency ward at night?",
    "What are visiting hours?",
    "Does the hospital accept insurance?",
    "How do I get my lab reports?",
    "What is the discharge process?",
]

def show_help():
    print(f"\n{Fore.YELLOW}📋 Sample questions you can ask:{Style.RESET_ALL}")
    for i, q in enumerate(SAMPLE_QUESTIONS, 1):
        print(f"  {Fore.WHITE}{i}. {q}{Style.RESET_ALL}")
    print()

def chat():
    print(BANNER)

    while True:
        # ── Get user input ──────────────────────
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.CYAN}Bot: Thank you for visiting. Stay healthy! 👋{Style.RESET_ALL}\n")
            break

        if not user_input:
            continue

        # ── Special commands ────────────────────
        if user_input.lower() in ('quit', 'exit', 'bye'):
            print(f"{Fore.CYAN}Bot: Thank you for visiting. Stay healthy! 👋{Style.RESET_ALL}\n")
            break

        if user_input.lower() == 'help':
            show_help()
            continue

        # ── Find best answer ────────────────────
        answer, score = get_best_answer(user_input)

        # Show confidence only when debugging (comment out for clean UI)
        confidence_tag = (
            f" {Fore.YELLOW}[confidence: {score:.0%}]{Style.RESET_ALL}"
            if score >= CONFIDENCE_THRESHOLD else ""
        )

        print(f"\n{Fore.CYAN}Bot: {answer}{confidence_tag}\n{Style.RESET_ALL}")


# ─────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────

if __name__ == "__main__":
    chat()
