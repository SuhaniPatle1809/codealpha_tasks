# 🏥 Hospital FAQ Chatbot

A simple and intelligent **Hospital FAQ Chatbot** built using **Python**, **NLTK**, and **Scikit-learn**. The chatbot uses **Natural Language Processing (NLP)** techniques and **TF-IDF similarity matching** to understand user questions and provide relevant answers from a predefined hospital knowledge base.

## 🌟 Features

* 🤖 Interactive terminal-based chatbot
* 🧠 NLP-powered question matching
* 🔍 TF-IDF vectorization with cosine similarity
* 📝 Text preprocessing using NLTK

  * Tokenization
  * Stopword removal
  * Lemmatization
* 🎯 Confidence-based answer selection
* 🏥 Covers common hospital-related queries
* 🎨 Colored terminal interface using Colorama
* 📋 Built-in help menu with sample questions

## 📚 Supported Topics

The chatbot can answer questions related to:

* Appointment Booking
* Appointment Rescheduling
* Emergency Services
* Visiting Hours
* Billing & Insurance
* Hospital Departments
* Pharmacy Information
* Lab Reports & Medical Records
* COVID-19 Precautions
* Parking Facilities
* Cafeteria Services
* Discharge Procedures
* Hospital Timings
* Contact Information

## 🛠️ Technologies Used

* Python 3
* NLTK (Natural Language Toolkit)
* Scikit-learn
* TF-IDF Vectorizer
* Cosine Similarity
* Colorama

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-faq-chatbot.git
cd hospital-faq-chatbot
```

### 2. Install Required Libraries

```bash
pip install nltk scikit-learn colorama
```

### 3. Run the Application

```bash
python hospital_chatbot.py
```

## 🚀 How It Works

### Step 1: Text Preprocessing

User input is cleaned and normalized by:

* Converting text to lowercase
* Removing punctuation and special characters
* Tokenizing words
* Removing stopwords
* Applying lemmatization

### Step 2: TF-IDF Vectorization

All FAQ questions are converted into TF-IDF vectors to represent their importance within the dataset.

### Step 3: Similarity Matching

The chatbot:

1. Converts the user's question into a TF-IDF vector.
2. Calculates cosine similarity against all FAQ questions.
3. Finds the most relevant question.
4. Returns the corresponding answer.

### Step 4: Confidence Check

If the similarity score is below the threshold (0.15), the chatbot provides a fallback response and suggests contacting the hospital helpline.

## 💬 Example Conversation

```text
You: How can I book an appointment?

Bot: You can book an appointment by calling our helpline at
1800-XXX-XXXX, visiting our website, or walking into the reception desk.
```

```text
You: What are your visiting hours?

Bot: General visiting hours are 10:00 AM – 12:00 PM and
5:00 PM – 7:00 PM. ICU visits are restricted to 15 minutes
twice a day with prior permission.
```

## 📂 Project Structure

```text
hospital-faq-chatbot/
│
├── hospital_chatbot.py
├── README.md
└── requirements.txt
```

## ⚙️ Key Components

### FAQ Dataset

Stores predefined hospital question-answer pairs.

### Preprocessing Module

Uses NLTK for text cleaning and normalization.

### Vectorization Engine

Uses TF-IDF to convert text into numerical vectors.

### Similarity Matcher

Uses cosine similarity to identify the most relevant FAQ.

### Interactive Chat Interface

Provides a user-friendly terminal chat experience with colorized output.

## 🔮 Future Enhancements

* GUI using Tkinter
* Web-based chatbot using Flask or Django
* Voice-based interaction
* Integration with hospital databases
* Multi-language support
* Machine Learning intent classification
* Appointment booking integration
* Live hospital support handoff

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository, improve the chatbot, and submit pull requests.

## 📜 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed as an NLP-based Hospital FAQ Assistant to demonstrate the use of Natural Language Processing, TF-IDF Vectorization, and Information Retrieval techniques in healthcare support systems.

---

⭐ If you found this project useful, consider giving it a star on GitHub!
