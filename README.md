# Mural Outreach

A Flask web app that automates personalized cold email outreach for mural painting services. It scrapes business websites, generates tailored emails using AI, finds contact emails, and lets you review everything before sending.

## Features

- Scrapes up to 5 business websites per run
- Generates personalized cold emails using GPT-4o-mini
- Crawls sites to find contact emails automatically
- Review page to edit emails, choose a recipient, or skip sending
- Simple login to keep it private

## Setup

1. **Install dependencies**
   ```bash
   pip install flask openai beautifulsoup4 requests python-dotenv
   ```

2. **Create a `.env` file** in the project root:
   ```
   API_KEY=your_openai_api_key
   PASSWORD=your_gmail_app_password
   ```
   > For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

3. **Set your login credentials** in `app.py`:
   ```python
   USERNAME = "your_username"
   PASSWORD = "your_password"
   ```

4. **Run the app**
   ```bash
   python app.py
   ```
   Then open [http://localhost:5001](http://localhost:5001)

## Project Structure

```
├── app.py
├── templates/
│   ├── index.html        # Main input form
│   ├── verify.html       # Review & send page
│   └── login.html        # Login page
├── static/styles/
│   └── index.css
└── utils/
    ├── generate_email.py  # Scraping + AI email generation
    ├── search_email.py    # Email crawler
    └── send_email.py      # SMTP sender
```

## Usage

1. Enter up to 5 business names and their website URLs
2. Optionally provide a known email — otherwise the app will try to find one
3. Hit **Submit** and wait while it scrapes and generates
4. On the review page: edit the email body, pick a recipient, or select **Don't send**
5. Hit **Send All** to send to all selected businesses
