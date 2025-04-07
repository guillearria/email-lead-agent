#!/usr/bin/env python3
"""
Email Processing and Classification Script

This script connects to an email server via IMAP, retrieves emails,
and classifies them using a pre-trained model.
"""

import imaplib
import email
from email.header import decode_header
import re
import pandas as pd
import joblib
import os
import configparser
import datetime
import json
from tqdm import tqdm

def load_config(config_file='email_config.ini'):
    """Load configuration from file."""
    if not os.path.exists(config_file):
        # Create a sample config file if it doesn't exist
        config = configparser.ConfigParser()
        config['EMAIL'] = {
            'username': 'your_email@gmail.com',
            'password': 'your_app_password',  # Use app password for Gmail
            'imap_server': 'imap.gmail.com',
            'imap_port': '993',
            'inbox_folder': 'INBOX'
        }
        with open(config_file, 'w') as f:
            config.write(f)
        print(f"Created sample config file: {config_file}")
        print("Please edit this file with your email credentials before running again.")
        exit(1)
    
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def connect_to_email(config):
    """Connect to the email server using configuration."""
    try:
        mail = imaplib.IMAP4_SSL(
            config['EMAIL']['imap_server'], 
            int(config['EMAIL'].get('imap_port', 993))
        )
        mail.login(config['EMAIL']['username'], config['EMAIL']['password'])
        return mail
    except Exception as e:
        print(f"Failed to connect to email: {e}")
        return None

def get_email_content(msg):
    """Extract content from an email message."""
    subject = ""
    body = ""
    date = None
    sender = ""
    
    # Get date
    if msg["date"]:
        try:
            date_str = msg["date"]
            # Convert to datetime object (this is approximate as email date formats vary)
            date = datetime.datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
        except:
            pass
    
    # Get sender
    if msg["from"]:
        sender = msg["from"]
        # Extract email from format "Name <email@example.com>"
        if "<" in sender:
            sender = sender.split("<")[1].split(">")[0]
    
    # Get subject
    if msg["subject"]:
        subject = decode_header(msg["subject"])[0][0]
        if isinstance(subject, bytes):
            try:
                subject = subject.decode()
            except:
                subject = subject.decode('utf-8', errors='replace')
    
    # Get body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            # Skip attachments
            if "attachment" in content_disposition:
                continue
                
            if content_type == "text/plain":
                try:
                    body_part = part.get_payload(decode=True)
                    if body_part:
                        body_part = body_part.decode('utf-8', errors='replace')
                        body += body_part + "\n"
                except Exception as e:
                    print(f"Error decoding email part: {e}")
    else:
        # Not multipart - get payload directly
        try:
            body = msg.get_payload(decode=True)
            if body:
                body = body.decode('utf-8', errors='replace')
        except:
            pass
    
    # Clean HTML and extra whitespace
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body).strip()
    
    return {
        "subject": subject,
        "body": body,
        "date": date,
        "sender": sender
    }

def preprocess_email(email_content):
    """Combine and preprocess email content."""
    subject = email_content["subject"]
    body = email_content["body"]
    
    # Combine subject and body with subject given more weight (repeated)
    combined_text = subject + " " + subject + " " + body
    
    # Basic preprocessing
    combined_text = combined_text.lower()
    
    return combined_text

def fetch_and_classify_emails(mail, classifier, vectorizer, max_emails=20):
    """Fetch emails and classify them."""
    results = []
    
    # Select inbox
    mail.select(config['EMAIL']['inbox_folder'])
    
    # Search for all emails in inbox
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    
    # Only process the most recent emails up to max_emails
    email_count = min(len(email_ids), max_emails)
    if email_count == 0:
        print("No emails found.")
        return results
    
    print(f"Processing {email_count} emails...")
    
    # Process from newest to oldest
    for email_id in tqdm(reversed(email_ids[-email_count:])):
        try:
            result, data = mail.fetch(email_id, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract content
            email_content = get_email_content(msg)
            processed_text = preprocess_email(email_content)
            
            # Classify
            features = vectorizer.transform([processed_text])
            category = classifier.predict(features)[0]
            probabilities = classifier.predict_proba(features)[0]
            confidence = max(probabilities)
            
            # Add to results
            email_content["category"] = category
            email_content["confidence"] = float(confidence)
            email_content["email_id"] = email_id.decode()
            
            results.append(email_content)
        except Exception as e:
            print(f"Error processing email: {e}")
    
    return results

def save_results(results, output_file="classified_emails.json"):
    """Save classification results to a JSON file."""
    # Convert dates to string format for JSON serialization
    for email in results:
        if email.get("date"):
            email["date"] = email["date"].strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_file}")

def summarize_results(results):
    """Print a summary of classification results."""
    if not results:
        print("No results to summarize.")
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(results)
    
    print("\n=== Classification Summary ===")
    print(f"Total emails processed: {len(df)}")
    print("\nCategory distribution:")
    print(df['category'].value_counts())
    
    print("\nHigh confidence business leads:")
    leads = df[(df['category'] == 'business_lead') & (df['confidence'] > 0.8)]
    if len(leads) > 0:
        for _, lead in leads.iterrows():
            print(f"From: {lead['sender']}, Subject: {lead['subject']}, Confidence: {lead['confidence']:.2f}")
    else:
        print("No high confidence business leads found.")

if __name__ == "__main__":
    print("=== Email Classification Processor ===")
    
    # Check for model and vectorizer
    if not os.path.exists('models/email_classifier.pkl') or not os.path.exists('models/email_vectorizer.pkl'):
        print("Model or vectorizer not found. Please run 01_train_basic_classifier.py first.")
        exit(1)
    
    # Load model and vectorizer
    classifier = joblib.load('models/email_classifier.pkl')
    vectorizer = joblib.load('models/email_vectorizer.pkl')
    
    # Load configuration
    config = load_config()
    
    # Connect to email
    mail = connect_to_email(config)
    if not mail:
        print("Failed to connect to email server. Please check your configuration.")
        exit(1)
    
    # Fetch and classify emails
    results = fetch_and_classify_emails(mail, classifier, vectorizer)
    
    # Save and summarize results
    if results:
        save_results(results)
        summarize_results(results)
    
    # Close connection
    mail.logout()
    
    print("\nEmail processing complete!") 