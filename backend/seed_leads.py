import requests

SAMPLE_LEADS = [
    {"name": "Aarav Mehta", "email": "aarav.mehta@gmail.com", "phone": "+919812345678", "source": "website_form", "message": "Hi! Saw your post on LinkedIn — we need help automating our customer onboarding workflow. Can we hop on a call this week? Budget is around 50k/month for the right partner."},
    {"name": "Priya Sharma", "email": "priya.sh@startupinc.co", "phone": "+918765432109", "source": "whatsapp", "message": "is your service free or paid? just exploring options for now"},
    {"name": "Rohan Kapoor", "email": "rkapoor@coldmail.in", "phone": "+917654321098", "source": "email", "message": "To Whom It May Concern, I came across your business and would like to know more. Please send me a brochure."},
    {"name": "Neha Patel", "email": "neha@growth.io", "phone": "+916543210987", "source": "website_form", "message": "Hey team — I'm building a Shopify store and need an automation that posts orders to Slack and tags products using AI. Need it live by end of month."},
    {"name": "Vikram Singh", "email": "vsingh@gmail.com", "phone": "+915432109876", "source": "whatsapp", "message": "hello"},
    {"name": "Ananya Iyer", "email": "ananya.iyer@bigcorp.com", "phone": "+914321098765", "source": "email", "message": "Hi, I'm the Ops Manager at a 200-person company. We're evaluating vendors for a 6-month engagement to streamline our internal ticketing and AI-assisted triage. Targeting RFP closure by mid-June."},
    {"name": "Karan Joshi", "email": "karan@notasked.in", "phone": "+913210987654", "source": "website_form", "message": "win iphone 15 click here www.shadydeal.in"},
    {"name": "Riya Desai", "email": "riya.desai@gmail.com", "phone": "+912109876543", "source": "whatsapp", "message": "hi, I run a small content studio. need help setting up a workflow that takes a YouTube transcript and turns it into LinkedIn posts automatically. willing to pay one-time fee. when can we talk?"},
    {"name": "Saurabh Reddy", "email": "sreddy@quietcompany.co", "phone": "+911098765432", "source": "email", "message": "unsubscribe"},
    {"name": "Meera Nair", "email": "meera@founderfriendly.com", "phone": "+919876543210", "source": "website_form", "message": "Hey! Big fan of your content on automation. Just wanted to say hi and connect — no immediate project but happy to refer folks your way."},
]

print("Sending 10 leads to backend...\n")

for i, lead in enumerate(SAMPLE_LEADS, start=1):
    try:
        response = requests.post("http://localhost:8000/lead", json=lead)
        result = response.json()
        print(f"[{i}] {lead['name']} → {result.get('classification', 'ERROR')}")
    except Exception as e:
        print(f"[{i}] {lead['name']} → FAILED: {e}")

print("\nAll done!")