# Email Classification for Lead Management

This document outlines the approach and technologies for building an email classification system that can automatically categorize incoming emails as business leads, information requests, or other categories.

## Table of Contents

1. [Overview](#overview)
2. [Technology Options](#technology-options)
3. [Implementation Steps](#implementation-steps)
4. [Code Examples](#code-examples)
5. [Evaluation and Improvement](#evaluation-and-improvement)
6. [Deployment Considerations](#deployment-considerations)
7. [Resources](#resources)

## Overview

Email classification is a text classification problem that uses Natural Language Processing (NLP) and Machine Learning (ML) to automatically categorize emails based on their content. For lead management, we want to classify emails into categories like:

- Business leads (potential customers showing interest in products/services)
- Information requests (general inquiries that may not indicate purchase intent)
- Other (newsletters, spam, operational emails, etc.)

This classification enables efficient email routing, prioritization, and automated responses, saving time and improving customer service.

## Technology Options

### 1. Machine Learning Approaches

#### Traditional ML Algorithms

- **Naive Bayes**: Fast, simple, works well for text classification with limited data
- **Support Vector Machines (SVM)**: Effective for text with clear boundaries between categories
- **Random Forest**: Good for handling diverse features and robust against overfitting
- **Logistic Regression**: Simple and interpretable for baseline models

#### Deep Learning Options

- **BERT/RoBERTa**: Pre-trained language models that understand context and semantics
- **Transformer-based models**: State-of-the-art for text understanding
- **LSTM/GRU networks**: Good for sequence data, though being replaced by transformers

### 2. NLP Libraries and Frameworks

- **scikit-learn**: Easy to use for traditional ML algorithms and text processing
- **spaCy**: Industrial-strength NLP with pre-built pipelines
- **NLTK**: Comprehensive toolkit for text processing
- **Hugging Face Transformers**: Easy access to state-of-the-art models
- **TensorFlow/PyTorch**: For custom deep learning solutions

### 3. Email Processing Tools

- **Python's built-in email modules**: For extracting email content from various formats
- **imaplib/poplib**: For fetching emails from servers
- **email-parser**: For structured extraction of email components

## Implementation Steps

### 1. Data Collection and Preparation

1. **Collect training data**: Gather a diverse set of emails for each category
2. **Extract text**: Extract body, subject, sender information from emails
3. **Clean data**: Remove signatures, footers, HTML tags, and irrelevant content
4. **Label data**: Manually classify emails into your target categories

### 2. Text Preprocessing

1. **Tokenization**: Breaking text into words or subwords
2. **Normalization**: Converting to lowercase, removing special characters
3. **Stop word removal**: Eliminating common words that don't add meaning
4. **Stemming/Lemmatization**: Reducing words to their root forms
5. **Feature extraction**: Converting text to numerical features (TF-IDF, embeddings)

### 3. Model Training

1. **Split data**: Divide into training, validation, and test sets
2. **Select algorithm**: Choose appropriate model based on data size and complexity
3. **Train model**: Fit the model to your training data
4. **Optimize parameters**: Tune hyperparameters for best performance

### 4. Evaluation

1. **Measure performance**: Calculate accuracy, precision, recall, F1-score
2. **Analyze errors**: Review misclassified examples
3. **Iterate and improve**: Refine model based on error analysis

## Code Examples

### Example 1: Basic Email Classification with scikit-learn

```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Assume we have a DataFrame with 'email_text' and 'category' columns
# df = pd.read_csv('email_dataset.csv')

# Example data
data = {
    'email_text': [
        "I'm interested in your product pricing and would like a demo",
        "Can you send me information about your services?",
        "Please update my subscription details",
        "Looking to purchase your enterprise plan for my team of 10",
        "What are your office hours?",
        "Newsletter: 10 tips for better productivity"
    ],
    'category': [
        'business_lead', 'information_request', 'other',
        'business_lead', 'information_request', 'other'
    ]
}
df = pd.DataFrame(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    df['email_text'], df['category'], test_size=0.3, random_state=42
)

# Create TF-IDF features
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = clf.predict(X_test_tfidf)

# Evaluate
print(classification_report(y_test, y_pred))

# Function to classify new emails
def classify_email(email_text):
    # Preprocess and transform
    email_tfidf = vectorizer.transform([email_text])
    # Predict
    category = clf.predict(email_tfidf)[0]
    # Return prediction
    return category

# Example usage
new_email = "I would like to discuss implementing your solution in our company"
print(f"Classified as: {classify_email(new_email)}")
```

### Example 2: Using BERT with Hugging Face Transformers

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset

# Same example data as before
data = {
    'email_text': [
        "I'm interested in your product pricing and would like a demo",
        "Can you send me information about your services?",
        "Please update my subscription details",
        "Looking to purchase your enterprise plan for my team of 10",
        "What are your office hours?",
        "Newsletter: 10 tips for better productivity"
    ],
    'category': [
        'business_lead', 'information_request', 'other',
        'business_lead', 'information_request', 'other'
    ]
}
df = pd.DataFrame(data)

# Map categories to integers
label_dict = {'business_lead': 0, 'information_request': 1, 'other': 2}
df['label'] = df['category'].map(label_dict)

# Split data
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# Create a custom dataset
class EmailDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Prepare datasets
train_dataset = EmailDataset(train_df['email_text'].tolist(), train_df['label'].tolist(), tokenizer)
test_dataset = EmailDataset(test_df['email_text'].tolist(), test_df['label'].tolist(), tokenizer)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Train the model
# Note: In a real scenario, you would need more data
# trainer.train()

# Function to classify with BERT
def classify_with_bert(email_text):
    inputs = tokenizer(email_text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(predictions, dim=1).item()
    
    # Map back to category
    categories = {0: 'business_lead', 1: 'information_request', 2: 'other'}
    return categories[predicted_class]
```

### Example 3: Email Processing and Pipeline Integration

```python
import imaplib
import email
from email.header import decode_header
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def connect_to_email(username, password, imap_server="imap.gmail.com"):
    """Connect to the email server and return the connection."""
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    return mail

def get_email_content(msg):
    """Extract content from an email message."""
    subject = ""
    body = ""
    
    # Get subject
    if msg["subject"]:
        subject = decode_header(msg["subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
    
    # Get body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except:
            pass
    
    # Clean HTML and extra whitespace
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    
    return subject, body

def preprocess_email(subject, body):
    """Combine and preprocess email content."""
    # Combine subject and body with subject given more weight
    combined_text = subject + " " + subject + " " + body
    
    # Basic preprocessing
    combined_text = combined_text.lower()
    
    return combined_text

def fetch_and_classify_emails(mail, classifier, vectorizer, limit=10):
    """Fetch emails and classify them."""
    mail.select("INBOX")
    
    # Search for all emails in inbox
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    
    # Process the most recent emails
    results = []
    for email_id in email_ids[-limit:]:
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Get sender
        sender = msg["from"] if msg["from"] else "Unknown"
        if "<" in sender:
            sender = sender.split("<")[1].split(">")[0]
        
        # Get content
        subject, body = get_email_content(msg)
        processed_text = preprocess_email(subject, body)
        
        # Classify
        features = vectorizer.transform([processed_text])
        category = classifier.predict(features)[0]
        confidence = max(classifier.predict_proba(features)[0])
        
        # Store results
        results.append({
            "sender": sender,
            "subject": subject,
            "category": category,
            "confidence": confidence,
            "date": msg["date"]
        })
    
    return pd.DataFrame(results)

# Example usage
def main():
    # Load trained model and vectorizer
    # These would be saved after training
    classifier = joblib.load('email_classifier.pkl')
    vectorizer = joblib.load('email_vectorizer.pkl')
    
    # Connect to email
    mail = connect_to_email("your_email@gmail.com", "your_password")
    
    # Fetch and classify emails
    results = fetch_and_classify_emails(mail, classifier, vectorizer)
    
    # Process results
    leads = results[results["category"] == "business_lead"]
    
    print(f"Found {len(leads)} potential business leads:")
    for _, lead in leads.iterrows():
        print(f"From: {lead['sender']}, Subject: {lead['subject']}")
    
    # Close connection
    mail.logout()

# When deploying, you'd run this with a scheduler or as a service
# if __name__ == "__main__":
#     main()
```

## Evaluation and Improvement

### Metrics to Track

- **Accuracy**: Overall correctness
- **Precision**: How many of the identified leads are actual leads
- **Recall**: How many actual leads were identified
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Visual representation of classification performance

### Improvement Strategies

1. **Collect more training data**: More examples improve model accuracy
2. **Feature engineering**: Create specialized features for email classification
3. **Model ensembling**: Combine multiple models for better performance
4. **Regular retraining**: Update models as email patterns change
5. **Active learning**: Identify uncertain classifications for human review

## Deployment Considerations

### Infrastructure Options

1. **Scheduled batch processing**:
   - Run classification on new emails at regular intervals
   - Simple to implement with cron jobs or task schedulers

2. **Real-time processing**:
   - Classify emails as they arrive
   - Requires webhook or polling mechanism

3. **API service**:
   - Deploy model behind a REST API with Flask/FastAPI
   - Email systems call the API when needed

### Security and Privacy

- **Data encryption**: Protect email content during processing
- **Authentication**: Secure API endpoints
- **Data retention**: Establish policies for storing email data
- **Compliance**: Ensure GDPR, CCPA, or other relevant compliance

### Scalability

- **Containerization**: Use Docker for consistent deployment
- **Load balancing**: Distribute processing across multiple instances
- **Database storage**: Efficiently store classification results
- **Monitoring**: Track system performance and model drift

## Resources

### Libraries and Tools

- [scikit-learn](https://scikit-learn.org/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [spaCy](https://spacy.io/)
- [NLTK](https://www.nltk.org/)
- [TensorFlow](https://www.tensorflow.org/)
- [PyTorch](https://pytorch.org/)

### Learning Resources

- [Practical Natural Language Processing](https://www.oreilly.com/library/view/practical-natural-language/9781492054047/)
- [Hugging Face NLP Course](https://huggingface.co/course/chapter1/1)
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Example Datasets

- [Enron Email Dataset](https://www.cs.cmu.edu/~enron/)
- [SpamAssassin Public Corpus](https://spamassassin.apache.org/old/publiccorpus/)
- [Kaggle Email Datasets](https://www.kaggle.com/datasets?search=email) 