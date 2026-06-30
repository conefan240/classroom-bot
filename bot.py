import time
from playwright.sync_api import sync_playwright
import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_classroom():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        context = browser.new_context()
        page = context.new_page()

        # Google login page
        page.goto("https://classroom.google.com")

        # ⚠️ First run will require login manually (we handle session later)
        page.wait_for_timeout(10000)

        # Try to load assignments page
        page.goto("https://classroom.google.com/a/not-turned-in/all")

        page.wait_for_timeout(5000)

        content = page.inner_text("body")

        browser.close()

        return content

if __name__ == "__main__":
    data = check_classroom()
    send("📚 Classroom check complete:\n\n" + data[:1500])
