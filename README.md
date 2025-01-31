# Montessori Schools Scraper

This project scrapes Montessori school information from the Opera Nazionale Montessori website.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python scraper.py
```

The script will create a `schools.csv` file containing the following information for each school:
- Name
- Address
- Province
- Website
- Phone number
- Email address
- Additional notes

## Requirements
- Python 3.8+
- Chrome browser installed (for Selenium WebDriver)
