import smtplib
import os
import requests
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def scrape_website(url):
    """Scrape text content from a website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove junk tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        # Get clean text
        text = soup.get_text(separator=" ", strip=True)

        # Trim it down so we don't overload the AI
        return text[:3000]

    except Exception as e:
        return f"Could not scrape website: {e}"

def generate_email(business_name, website_content):
    """Use AI to write a personalized email based on website content."""
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="""
        You are an expert copywriter writing personalized cold emails. 
        Your tone is friendly, natural, and persuasive (not salesy or robotic). 
        Always reference specific details from the business's website to show personalization. 
        Keep emails concise and under 150 words. 
        Never include a subject line. 
        Always include the sender's name (Joseph Marques) and phone number (416-833-7383) at the end. 
        Do not use placeholders or filler text. 
        Write in complete, polished sentences.
        Don't use mdashes.
        Humanize the content.
        """,
        input=f"""
        Business name: {business_name}

        Website content:
        {website_content}

        Write a short, personalized cold email offering mural painting services.
        Make it feel tailored to this specific business.
        """
    )
    return response.output_text

