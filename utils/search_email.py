import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {"User-Agent": "Mozilla/5.0"}

def find_emails_on_page(url):
    """Fetch a webpage and extract all email addresses from it."""
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

    # Search for emails in raw HTML (catches emails in JS, comments, etc.)
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    emails = set(re.findall(email_pattern, response.text))
    
    return emails

def crawl_site_for_emails(start_url, max_pages=5):
    """Crawl a site (up to max_pages) and collect all emails found."""
    visited = set()
    to_visit = [start_url]
    all_emails = set()
    base_domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        print(f"Scanning: {url}")
        visited.add(url)
        emails = find_emails_on_page(url)
        all_emails.update(emails)

        # Find internal links to follow
        try:
            soup = BeautifulSoup(requests.get(url, headers=headers, timeout=10,  verify=False).text, "html.parser")
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                if urlparse(link).netloc == base_domain and link not in visited:
                    to_visit.append(link)
        except Exception:
            pass

    return all_emails

# --- Usage ---
"""
target = "https://trexity.com/"
emails = crawl_site_for_emails(target, max_pages=5)

print("\nEmails found:")
for email in sorted(emails):
    print(f"  {email}")
"""