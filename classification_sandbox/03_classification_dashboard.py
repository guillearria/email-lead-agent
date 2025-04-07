#!/usr/bin/env python3
"""
Email Classification Dashboard

A simple Flask web application to visualize the results of email classification.
This dashboard provides an overview of classified emails and allows filtering by category.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)

# Ensure the templates directory exists
os.makedirs('templates', exist_ok=True)

# Create HTML templates
def create_templates():
    # Create base template
    with open('templates/base.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Email Classification Dashboard{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .email-card {
            margin-bottom: 15px;
            border-left: 5px solid #ccc;
        }
        .business-lead {
            border-left-color: #28a745;
        }
        .information-request {
            border-left-color: #17a2b8;
        }
        .other {
            border-left-color: #6c757d;
        }
        .high-confidence {
            background-color: rgba(40, 167, 69, 0.1);
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Email Classification Dashboard</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>""")

    # Create index template
    with open('templates/index.html', 'w') as f:
        f.write("""{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-4">
        <div class="card mb-4">
            <div class="card-header">
                <h5>Statistics</h5>
            </div>
            <div class="card-body">
                <p><strong>Total Emails:</strong> {{ stats.total }}</p>
                <p><strong>Business Leads:</strong> {{ stats.business_leads }} ({{ stats.business_leads_pct }}%)</p>
                <p><strong>Information Requests:</strong> {{ stats.information_requests }} ({{ stats.information_requests_pct }}%)</p>
                <p><strong>Other:</strong> {{ stats.other }} ({{ stats.other_pct }}%)</p>
                <hr>
                <p><strong>High Confidence Leads:</strong> {{ stats.high_confidence_leads }}</p>
            </div>
        </div>
        <div class="card">
            <div class="card-header">
                <h5>Category Distribution</h5>
            </div>
            <div class="card-body text-center">
                <img src="data:image/png;base64,{{ plots.category_dist }}" class="img-fluid">
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <div class="card mb-4">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5>Email Classification Results</h5>
                <div class="btn-group">
                    <button class="btn btn-sm btn-outline-secondary filter-btn active" data-filter="all">All</button>
                    <button class="btn btn-sm btn-outline-success filter-btn" data-filter="business_lead">Business Leads</button>
                    <button class="btn btn-sm btn-outline-info filter-btn" data-filter="information_request">Information Requests</button>
                    <button class="btn btn-sm btn-outline-secondary filter-btn" data-filter="other">Other</button>
                </div>
            </div>
            <div class="card-body">
                <div class="input-group mb-3">
                    <span class="input-group-text">Search</span>
                    <input type="text" id="searchInput" class="form-control" placeholder="Search in emails...">
                </div>
                <div id="emailList">
                    {% for email in emails %}
                    <div class="card email-card {{ email.category }} {% if email.confidence > 0.8 %}high-confidence{% endif %}" data-category="{{ email.category }}">
                        <div class="card-body">
                            <h5 class="card-title">{{ email.subject }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">From: {{ email.sender }}</h6>
                            <p class="card-text">{{ email.body[:150] }}{% if email.body|length > 150 %}...{% endif %}</p>
                            <div class="d-flex justify-content-between">
                                <span class="badge {% if email.category == 'business_lead' %}bg-success{% elif email.category == 'information_request' %}bg-info{% else %}bg-secondary{% endif %}">
                                    {{ email.category }} ({{ (email.confidence * 100)|int }}% confidence)
                                </span>
                                <small class="text-muted">{{ email.date }}</small>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    $(document).ready(function() {
        // Filter functionality
        $('.filter-btn').click(function() {
            $('.filter-btn').removeClass('active');
            $(this).addClass('active');
            
            var filter = $(this).data('filter');
            if (filter === 'all') {
                $('.email-card').show();
            } else {
                $('.email-card').hide();
                $('.email-card[data-category="' + filter + '"]').show();
            }
        });
        
        // Search functionality
        $('#searchInput').on('keyup', function() {
            var value = $(this).val().toLowerCase();
            $('#emailList .email-card').filter(function() {
                var text = $(this).text().toLowerCase();
                var isVisible = text.indexOf(value) > -1;
                $(this).toggle(isVisible);
            });
        });
    });
</script>
{% endblock %}""")

def load_classification_data(file_path="classified_emails.json"):
    """Load classification results from JSON file."""
    if not os.path.exists(file_path):
        # Return sample data if file doesn't exist
        return [
            {
                "subject": "Sample Business Lead Email",
                "body": "I'm interested in your product for my company.",
                "date": "2023-06-15 10:30:00",
                "sender": "potential_client@example.com",
                "category": "business_lead",
                "confidence": 0.92
            },
            {
                "subject": "Question about your service",
                "body": "Could you tell me more about your pricing?",
                "date": "2023-06-14 14:45:00",
                "sender": "inquirer@example.com",
                "category": "information_request",
                "confidence": 0.85
            },
            {
                "subject": "Weekly Newsletter",
                "body": "Here are this week's top stories and updates.",
                "date": "2023-06-13 09:15:00",
                "sender": "newsletter@example.com",
                "category": "other",
                "confidence": 0.78
            }
        ]
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return data

def generate_statistics(emails):
    """Generate statistics from email classification results."""
    total = len(emails)
    if total == 0:
        return {
            "total": 0,
            "business_leads": 0,
            "information_requests": 0,
            "other": 0,
            "business_leads_pct": 0,
            "information_requests_pct": 0,
            "other_pct": 0,
            "high_confidence_leads": 0
        }
    
    # Count categories
    business_leads = sum(1 for e in emails if e["category"] == "business_lead")
    information_requests = sum(1 for e in emails if e["category"] == "information_request")
    other = sum(1 for e in emails if e["category"] == "other")
    
    # Calculate percentages
    business_leads_pct = round((business_leads / total) * 100, 1)
    information_requests_pct = round((information_requests / total) * 100, 1)
    other_pct = round((other / total) * 100, 1)
    
    # Count high confidence leads
    high_confidence_leads = sum(1 for e in emails 
                               if e["category"] == "business_lead" and e["confidence"] > 0.8)
    
    return {
        "total": total,
        "business_leads": business_leads,
        "information_requests": information_requests,
        "other": other,
        "business_leads_pct": business_leads_pct,
        "information_requests_pct": information_requests_pct,
        "other_pct": other_pct,
        "high_confidence_leads": high_confidence_leads
    }

def generate_plots(emails):
    """Generate plots for the dashboard."""
    plots = {}
    
    # Create DataFrame
    df = pd.DataFrame(emails)
    
    # Category distribution plot
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(data=df, x='category', order=['business_lead', 'information_request', 'other'])
    ax.set_title('Email Category Distribution')
    ax.set_xlabel('Category')
    ax.set_ylabel('Count')
    
    # Add value labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'bottom', 
                   xytext = (0, 5), textcoords = 'offset points')
    
    # Convert plot to base64 for embedding in HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plots['category_dist'] = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return plots

@app.route('/')
def index():
    """Dashboard homepage."""
    # Load classification results
    emails = load_classification_data()
    
    # Generate statistics and plots
    stats = generate_statistics(emails)
    plots = generate_plots(emails)
    
    return render_template('index.html', emails=emails, stats=stats, plots=plots)

def main():
    """Run the Flask application."""
    # Create templates if they don't exist
    create_templates()
    
    print("=== Email Classification Dashboard ===")
    print("Starting Flask server...")
    print("Visit http://127.0.0.1:5000/ to view the dashboard")
    app.run(debug=True)

if __name__ == "__main__":
    main() 