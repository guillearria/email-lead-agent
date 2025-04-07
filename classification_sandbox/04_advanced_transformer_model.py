#!/usr/bin/env python3
"""
Advanced Email Classification with Transformers

This script demonstrates how to use a BERT-based transformer model
for more accurate email classification.
"""

import pandas as pd
import numpy as np
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time
import warnings
warnings.filterwarnings('ignore')

# Sample data (expanded from previous examples)
data = {
    'email_text': [
        "I'm interested in your product pricing and would like to schedule a demo",
        "Can you tell me more about your enterprise solution? Looking to implement it for my team",
        "Looking to purchase your software for my team of 15 people",
        "Please schedule a call to discuss implementation options for your solution",
        "What's the pricing for the premium plan? I need 10 licenses",
        "We're considering switching to your product from a competitor",
        "I'd like to explore partnership opportunities with your company",
        "Our company needs your solution. Can we discuss pricing?",
        "I saw your recent presentation and would like to learn more about becoming a customer",
        "We're planning to upgrade our systems and interested in your offerings",
        
        "Can you send me information about your services?",
        "Do you offer support for international customers?",
        "What are your office hours?",
        "When do you open on weekends?",
        "Is there a user manual available for your product?",
        "How long does shipping usually take?",
        "Do you have a catalog I can browse?",
        "I'd like to know more about your refund policy",
        "What payment methods do you accept?",
        "Can I get technical specifications for your products?",
        
        "Please update my subscription details",
        "I'd like to cancel my account",
        "Newsletter: 10 tips for better productivity",
        "Your invoice #1234 is attached",
        "Meeting minutes from yesterday's call",
        "The latest security patch is available",
        "Your account password has been reset",
        "Reminder: Team meeting tomorrow at 2pm",
        "System maintenance scheduled for this weekend",
        "Weekly statistics report attached"
    ],
    'category': [
        'business_lead', 'business_lead', 'business_lead', 'business_lead', 'business_lead',
        'business_lead', 'business_lead', 'business_lead', 'business_lead', 'business_lead',
        
        'information_request', 'information_request', 'information_request', 'information_request', 'information_request',
        'information_request', 'information_request', 'information_request', 'information_request', 'information_request',
        
        'other', 'other', 'other', 'other', 'other',
        'other', 'other', 'other', 'other', 'other'
    ]
}

class EmailDataset(Dataset):
    """Dataset class for email classification with transformers."""
    
    def __init__(self, texts, labels, tokenizer, max_length=128):
        """Initialize the dataset with texts and labels."""
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length)
        self.labels = labels

    def __getitem__(self, idx):
        """Get item at a specific index."""
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        """Get dataset length."""
        return len(self.labels)

def map_labels_to_ids(categories):
    """Map text categories to numeric IDs."""
    unique_categories = sorted(set(categories))
    label_map = {cat: i for i, cat in enumerate(unique_categories)}
    id_to_label = {i: cat for cat, i in label_map.items()}
    
    return [label_map[cat] for cat in categories], label_map, id_to_label

def prepare_datasets(model_name="distilbert-base-uncased"):
    """Prepare datasets for training and evaluation."""
    print("Creating training and test datasets...")
    
    # Create DataFrame
    df = pd.DataFrame(data)
    print(f"Dataset size: {len(df)} emails")
    print(f"Category distribution:\n{df['category'].value_counts()}")
    
    # Map labels to IDs
    labels, label_map, id_to_label = map_labels_to_ids(df['category'])
    df['label_id'] = labels
    
    # Split data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['category'])
    
    # Load tokenizer
    print(f"\nLoading tokenizer for {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Create datasets
    train_dataset = EmailDataset(
        train_df['email_text'].tolist(),
        train_df['label_id'].tolist(),
        tokenizer
    )
    
    test_dataset = EmailDataset(
        test_df['email_text'].tolist(),
        test_df['label_id'].tolist(),
        tokenizer
    )
    
    return train_dataset, test_dataset, test_df, tokenizer, label_map, id_to_label

def train_transformer_model(train_dataset, test_dataset, id_to_label, model_name="distilbert-base-uncased"):
    """Train a transformer model for email classification."""
    num_labels = len(id_to_label)
    
    print(f"Loading model: {model_name}")
    # Load pre-trained model
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, 
        num_labels=num_labels
    )
    
    # Configure training parameters
    training_args = TrainingArguments(
        output_dir='./transformer_results',
        evaluation_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=50,
        weight_decay=0.01,
        logging_dir='./transformer_logs',
        logging_steps=10,
        load_best_model_at_end=True,
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )
    
    # Train the model
    print("\nTraining the transformer model...")
    trainer.train()
    
    return model, trainer

def evaluate_model(model, trainer, test_df, tokenizer, label_map, id_to_label):
    """Evaluate the trained model."""
    print("\nEvaluating model...")
    
    # Prepare test data
    texts = test_df['email_text'].tolist()
    true_labels = test_df['category'].tolist()
    
    # Tokenize inputs
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    
    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_labels = torch.argmax(predictions, dim=1).cpu().numpy()
    
    # Convert IDs back to labels
    predicted_categories = [id_to_label[label_id] for label_id in predicted_labels]
    
    # Evaluate
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_categories))
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    cm = pd.crosstab(pd.Series(true_labels, name='Actual'), 
                    pd.Series(predicted_categories, name='Predicted'))
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
    plt.title('Confusion Matrix')
    plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    plt.savefig('models/transformer_confusion_matrix.png')
    
    return predicted_categories, predictions.cpu().numpy()

def save_model_and_tokenizer(model, tokenizer, label_map, id_to_label):
    """Save the model, tokenizer, and label mappings."""
    os.makedirs('models/transformer', exist_ok=True)
    
    # Save model and tokenizer
    model.save_pretrained('models/transformer/model')
    tokenizer.save_pretrained('models/transformer/tokenizer')
    
    # Save label mappings
    joblib.dump(
        {'label_map': label_map, 'id_to_label': id_to_label},
        'models/transformer/label_mappings.pkl'
    )
    
    print("\nModel, tokenizer, and label mappings saved to models/transformer/")

def classify_new_emails(texts, model, tokenizer, id_to_label):
    """Classify new emails using the trained model."""
    # Tokenize inputs
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    
    # Move to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_labels = torch.argmax(predictions, dim=1).cpu().numpy()
    
    # Convert IDs back to labels
    predicted_categories = [id_to_label[label_id] for label_id in predicted_labels]
    confidence_scores = [float(predictions[i, predicted_labels[i]]) for i in range(len(predicted_labels))]
    
    return predicted_categories, confidence_scores

def main():
    """Main function to train and evaluate the transformer model."""
    print("=== Advanced Email Classification with Transformers ===")
    
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Start timer
    start_time = time.time()
    
    # Use a smaller, faster model for demonstration
    model_name = "distilbert-base-uncased"
    
    # Prepare datasets
    train_dataset, test_dataset, test_df, tokenizer, label_map, id_to_label = prepare_datasets(model_name)
    
    # Train model
    model, trainer = train_transformer_model(train_dataset, test_dataset, id_to_label, model_name)
    
    # Evaluate model
    predicted_categories, predictions = evaluate_model(
        model, trainer, test_df, tokenizer, label_map, id_to_label
    )
    
    # Save model
    save_model_and_tokenizer(model, tokenizer, label_map, id_to_label)
    
    # Test with new examples
    print("\nTesting with new examples:")
    test_examples = [
        "I would like to purchase your premium plan for my business. Please contact me.",
        "Can you tell me if you ship to international locations?",
        "Thank you for attending yesterday's webinar. The slides are attached.",
        "I'm the CEO of a Fortune 500 company and we need your solution immediately.",
        "What time does your customer service department open on Saturdays?"
    ]
    
    predicted_categories, confidence_scores = classify_new_emails(
        test_examples, model, tokenizer, id_to_label
    )
    
    for i, (text, category, confidence) in enumerate(zip(test_examples, predicted_categories, confidence_scores)):
        print(f"\nText: '{text}'")
        print(f"Classified as: {category} (confidence: {confidence:.2f})")
    
    # Print total time
    elapsed_time = time.time() - start_time
    print(f"\nTotal execution time: {elapsed_time:.2f} seconds")
    print("\nTraining and evaluation complete!")

if __name__ == "__main__":
    main() 