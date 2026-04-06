import os
from flask import Flask, render_template, request, url_for, redirect, session
from utils.generate_email import scrape_website, generate_email
from utils.send_email import send_email
from utils.search_email import crawl_site_for_emails
from functools import wraps
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") 
USERNAME = os.getenv("USERNAME_LOGIN") 
PASSWORD = os.getenv("PASSWORD_LOGIN") 

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == USERNAME and request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
@login_required
def search():
    results = []
    for i in range(1, 6):
        business_name = request.form.get(f'name{i}')
        business_url = request.form.get(f'url{i}')
        business_email = request.form.get(f'email{i}')
        if not business_name or not business_url:
            continue

        print(f"Scraping {business_url}...")
        website_content = scrape_website(business_url)
        print("Generating personalized email...")
        email_body = generate_email(business_name, website_content)

        found_emails = []
        if business_email:
            found_emails.append(business_email)
        print("Finding emails...")
        emails = list(crawl_site_for_emails(business_url))
        for email in emails:
            if email not in found_emails:
                found_emails.append(email)
                print(found_emails)

        results.append({
            "name": business_name,
            "url": business_url,
            "email_body": email_body,
            "found_emails": found_emails,
        })

    session['results'] = results
    return redirect(url_for('verify'))


@app.route("/verify")
@login_required
def verify():
    results = session.get('results', [])
    return render_template("verify.html", results=results)


@app.route("/send-confirmed", methods=['POST'])
@login_required
def send_confirmed():
    results = session.get('results', [])
    for i, result in enumerate(results):
        chosen_email = request.form.get(f'chosen_email_{i}')
        email_body = request.form.get(f'email_body_{i}')
        if chosen_email and email_body: 
            print(f"Sending to {chosen_email}...")
            send_email(chosen_email, email_body)
        else:
            print(f"Skipping {result['name']}")
    session.pop('results', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)