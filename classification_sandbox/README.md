# Email Classification Sandbox

This directory contains a collection of Python scripts for classifying emails as business leads, information requests, or other categories.

## Overview

Email classification is a powerful tool for lead management, allowing businesses to automatically identify and prioritize potential customers from their email inboxes. This sandbox provides practical implementations ranging from simple ML models to advanced transformer-based approaches.

## Scripts Included

1. **01_train_basic_classifier.py**: Trains a basic email classifier using scikit-learn and TF-IDF features with a Naive Bayes model.

2. **02_process_emails.py**: Connects to an email server via IMAP, fetches emails, and classifies them using the trained model.

3. **03_classification_dashboard.py**: A Flask web application that visualizes classification results with statistics and filtering options.

4. **04_advanced_transformer_model.py**: Implements a more advanced BERT-based transformer model for improved classification accuracy.

## Setup Instructions

### 1. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Classification Workflow

```bash
# 1. Train a basic model
python 01_train_basic_classifier.py

# 2. Process emails with the trained model
python 02_process_emails.py

# 3. View results in the dashboard
python 03_classification_dashboard.py
```

### Advanced Classification with Transformers

```bash
# Train and evaluate a transformer model
python 04_advanced_transformer_model.py
```

## Configuration

### Email Configuration

Before running `02_process_emails.py`, you'll need to configure your email settings:

1. The script will generate a sample `email_config.ini` file on first run
2. Edit this file with your email credentials:

```ini
[EMAIL]
username = your_email@gmail.com
password = your_app_password
imap_server = imap.gmail.com
imap_port = 993
inbox_folder = INBOX
```

**Note**: For Gmail, you'll need to use an App Password rather than your regular password. See [Google Account Help](https://support.google.com/accounts/answer/185833) for instructions.

## Output Files

The scripts will generate several output files:

- `models/email_classifier.pkl`: The trained scikit-learn classifier
- `models/email_vectorizer.pkl`: The TF-IDF vectorizer
- `models/confusion_matrix.png`: Confusion matrix visualization
- `classified_emails.json`: Classification results from processed emails
- `models/transformer/`: Directory containing the saved transformer model

## Extending the Project

Here are some ways to extend this project:

1. **Add more categories**: Extend beyond the three basic categories
2. **Improve preprocessing**: Add more sophisticated text cleaning
3. **Implement active learning**: Allow users to correct misclassifications
4. **Add auto-responses**: Automatically respond to different email types
5. **Build an API**: Create a REST API for classification services

## Documentation

For more information on email classification, see the comprehensive `CLASSIFICATION_BASICS.md` document.

## License

This project is provided as-is for educational purposes. 