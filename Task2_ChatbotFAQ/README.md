# 🏥 Hospital FAQ Chatbot

A smart and interactive **Hospital FAQ Chatbot** built using **Python, Tkinter, NLTK, and Scikit-Learn**. The chatbot uses **Natural Language Processing (NLP)** techniques and **TF-IDF similarity matching** to understand user queries and provide accurate responses from a comprehensive hospital knowledge base.

The application features a modern healthcare-themed graphical user interface, quick-reply buttons, real-time chat interactions, and support for a wide range of hospital-related questions.

---

## 🌟 Features

### 🤖 Intelligent FAQ Assistant

* Understands natural language questions.
* Uses TF-IDF Vectorization and Cosine Similarity for question matching.
* Provides relevant answers from an extensive hospital FAQ database.
* Handles appointment, emergency, billing, laboratory, pharmacy, and facility-related queries.

### 🧠 NLP-Powered Processing

* Text preprocessing using NLTK:

  * Tokenization
  * Stopword Removal
  * Lemmatization
  * Text Normalization

### 💬 Modern Chat Interface

* Healthcare-themed GUI built with Tkinter.
* User and bot chat bubbles.
* Automatic scrolling chat window.
* Message timestamps.
* Responsive and user-friendly design.

### ⚡ Quick Reply Buttons

Users can instantly ask common questions such as:

* Book an Appointment
* OPD Timings
* Emergency Services
* Insurance Information
* Lab Reports
* Visiting Hours
* Discharge Process
* Pharmacy Services
* Parking Information
* Contact Details

### 🔄 Multi-Threaded Response System

* Prevents UI freezing during query processing.
* Smooth and responsive user experience.

### 📚 Comprehensive Hospital Knowledge Base

Includes FAQs related to:

* Appointments
* Emergency Services
* OPD Timings
* Departments & Specialties
* Insurance & Billing
* Diagnostics & Laboratory
* Admissions & Discharge
* Pharmacy & Blood Bank
* Facilities & Amenities
* COVID-19 Services
* Mental Health Services
* Physiotherapy & Rehabilitation
* Medical Records
* Contact Information

---

## 🛠️ Technologies Used

| Technology               | Purpose                      |
| ------------------------ | ---------------------------- |
| Python                   | Core Programming Language    |
| Tkinter                  | GUI Development              |
| NLTK                     | Natural Language Processing  |
| Scikit-Learn             | TF-IDF & Similarity Matching |
| Threading                | Background Query Processing  |
| Regular Expressions (re) | Text Cleaning                |

---

## 📦 Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-faq-chatbot.git
cd hospital-faq-chatbot
```

### Install Required Dependencies

```bash
pip install nltk scikit-learn
```

### Run the Application

```bash
python hospital_chatbot.py
```

---

## 🚀 How It Works

### Step 1: User Query Input

The user enters a question through the chat interface.

### Step 2: Text Preprocessing

The chatbot:

* Converts text to lowercase.
* Removes punctuation and special characters.
* Tokenizes words.
* Removes stopwords.
* Applies lemmatization.

### Step 3: TF-IDF Vectorization

FAQ questions are transformed into TF-IDF vectors.

### Step 4: Similarity Matching

Cosine similarity compares the user's question with stored FAQ questions.

### Step 5: Response Generation

The chatbot returns the most relevant answer if the similarity score exceeds the confidence threshold.

---

## 💬 Example Queries

```text
How do I book an appointment?
```

```text
What are the OPD timings?
```

```text
Does the hospital accept health insurance?
```

```text
How do I collect my lab reports?
```

```text
What is the discharge process?
```

```text
Is parking available at the hospital?
```

```text
Do you have a cardiology department?
```

---

## 🏗️ System Architecture

```text
User Input
     │
     ▼
Text Preprocessing
     │
     ▼
TF-IDF Vectorization
     │
     ▼
Cosine Similarity Matching
     │
     ▼
Best FAQ Selection
     │
     ▼
Chatbot Response
```

---

## 🎨 GUI Highlights

* Professional hospital-themed color palette.
* Online status indicator.
* Scrollable chat area.
* User and assistant message bubbles.
* Quick-access FAQ buttons.
* Responsive window layout.
* Timestamped conversations.

---

## 🔮 Future Enhancements

* Voice-enabled chatbot
* Speech-to-text support
* Text-to-speech responses
* Multi-language support
* AI-powered intent detection
* Hospital database integration
* Online appointment booking
* Patient login system
* Chat history storage
* Web and mobile versions

---

## 🎯 Learning Outcomes

This project demonstrates:

* Natural Language Processing (NLP)
* Information Retrieval Systems
* TF-IDF Vectorization
* Cosine Similarity
* GUI Development with Tkinter
* Multithreading in Python
* Healthcare Chatbot Design

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed as an NLP-based Healthcare Assistant project to demonstrate intelligent FAQ retrieval, chatbot development, and desktop GUI design using Python.

⭐ If you found this project useful, consider starring the repository on GitHub!
