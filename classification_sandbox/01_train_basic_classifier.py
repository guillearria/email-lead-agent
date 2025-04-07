#!/usr/bin/env python3
"""
Basic Email Classifier Training Script

This script demonstrates how to train a simple email classifier using scikit-learn.
It uses a small sample dataset but can be extended to use real email data.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Create a sample dataset (replace with your real data)
data = {
    'email_text': [
        "I'm interested in your product pricing and would like a demo",
        "Can you tell me more about your enterprise solution?",
        "Looking to purchase your software for my team of 15 people",
        "Please schedule a call to discuss implementation options",
        "What's the pricing for the premium plan?",
        "Can you send me information about your services?",
        "Do you offer support for international customers?",
        "What are your office hours?",
        "When do you open on weekends?",
        "Please update my subscription details",
        "I'd like to cancel my account",
        "Newsletter: 10 tips for better productivity",
        "Your invoice #1234 is attached",
        "Meeting minutes from yesterday's call",
        "The latest security patch is available",
    ],
    'category': [
        'business_lead', 'business_lead', 'business_lead', 'business_lead', 'business_lead',
        'information_request', 'information_request', 'information_request', 'information_request', 
        'other', 'other', 'other', 'other', 'other', 'other'
    ]
}

def train_and_save_model():
    """Train a basic email classifier and save the model."""
    # Create DataFrame from sample data
    df = pd.DataFrame(data)
    print(f"Dataset size: {len(df)} emails")
    print(f"Category distribution:\n{df['category'].value_counts()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['email_text'], df['category'], test_size=0.3, random_state=42
    )
    
    # Create TF-IDF features
    print("\nConverting text to TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=1000, 
        stop_words='english',
        ngram_range=(1, 2)  # Use both unigrams and bigrams
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Train a Naive Bayes classifier
    print("Training Naive Bayes classifier...")
    clf = MultinomialNB()
    clf.fit(X_train_tfidf, y_train)
    
    # Make predictions
    y_pred = clf.predict(X_test_tfidf)
    
    # Evaluate
    print("\nModel Evaluation:")
    print(classification_report(y_test, y_pred))
    
    # Create output directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save the model and vectorizer
    print("\nSaving model and vectorizer...")
    joblib.dump(clf, 'models/email_classifier.pkl')
    joblib.dump(vectorizer, 'models/email_vectorizer.pkl')
    
    # Create and save confusion matrix visualization
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=clf.classes_, yticklabels=clf.classes_)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig('models/confusion_matrix.png')
    
    # Display important features for each category
    print("\nMost important features for each category:")
    feature_names = vectorizer.get_feature_names_out()
    for i, category in enumerate(clf.classes_):
        top_features_idx = np.argsort(clf.feature_log_prob_[i])[-10:]
        top_features = [feature_names[idx] for idx in top_features_idx]
        print(f"{category}: {', '.join(top_features)}")
    
    return clf, vectorizer

def test_classifier(clf, vectorizer):
    """Test the classifier with a few examples."""
    print("\nTesting classifier on new examples:")
    test_examples = [
        "I would like to purchase your product for my business",
        "Can you please provide more details about your service?",
        "Please find attached the minutes from yesterday's meeting",
        "What time do you close on Fridays?",
        "I'm looking for pricing information for a team of 20 people"
    ]
    
    for text in test_examples:
        features = vectorizer.transform([text])
        category = clf.predict(features)[0]
        probs = clf.predict_proba(features)[0]
        confidence = max(probs)
        print(f"Text: '{text}'")
        print(f"Classified as: {category} (confidence: {confidence:.2f})")
        print("-" * 50)

if __name__ == "__main__":
    print("=== Email Classifier Training ===")
    clf, vectorizer = train_and_save_model()
    test_classifier(clf, vectorizer)
    print("\nTraining and evaluation complete! Model saved to 'models/' directory.") 