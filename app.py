from flask import Flask, render_template, request, url_for, redirect
from utils.generate_email import scrape_website, generate_email
from utils.send_email import send_email
from utils.search_email import crawl_site_for_emails

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def hello_world():
    if request.method == 'POST':
        for i in range(1,6):
            print(i)
            business_name = request.form.get(f'name{i}')
            business_url = request.form.get(f'url{i}')
            business_email = request.form.get(f'email{i}')
            if not business_name or not business_url:
                continue
            print(f"Scraping {business_url}...")
            website_content = scrape_website(business_url)
            print("Generating personalized email...")
            email_body = generate_email(business_name, website_content)
            if business_email:
                print("Sending Email...")
                send_email(business_email, email_body)
            else:
                print("Finding Email...")
                emails = crawl_site_for_emails(business_url)
                print(emails)
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)