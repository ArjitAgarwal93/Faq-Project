# FAQ Translation System

A Django-based FAQ system that automatically translates content into Hindi and Bengali with caching support.

## Setup

1. Clone and install dependencies:
```bash
git clone https://github.com/ArjitAgarwal93/Faq-Project.git
cd faq_project
pip install -r requirements.txt
```

2. Initialize database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Features

- Automatic translation to Hindi and Bengali
- Translation caching for better performance
- RESTful API endpoints
- Django admin interface

## API Usage

Get FAQs (default English):
```bash
GET /api/faqs/
```

Get translated FAQs:
```bash
GET /api/faqs/?lang=hi  # Hindi
GET /api/faqs/?lang=bn  # Bengali
```

Create FAQ:
```bash
POST /api/faqs/
{
    "question": "Who is the Prime Minister of India?",
    "answer": "Its Narendra Modi."
}
```

## Admin Access

Access admin panel at `/admin/` to manage FAQs.

## Running Tests

```bash
python manage.py test
```

## Requirements

- Python 3.8+
- Django 4.2+
- Redis Server Running 
For help or issues, contact a.agarwal0903@gmail.com