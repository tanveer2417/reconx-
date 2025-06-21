import requests
import whois
from googlesearch import search
import re
from bs4 import BeautifulSoup
import urllib.request
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

output_lines = []

def log(msg):
    output_lines.append(str(msg))

# -------------------------
# 1. GOOGLE DORKS
# -------------------------
def google_dorks(domain):
    dorks = [
        f"site:{domain} intitle:index.of",
        f"site:{domain} inurl:admin",
        f"site:{domain} filetype:sql",
        f"site:{domain} ext:php",
        f"site:{domain} inurl:login",
        f"site:{domain} ext:env",
        f"site:{domain} ext:log",
        f"site:{domain} ext:json"
    ]
    log(f"\n[+] Google Dorks for {domain}")
    for dork in dorks:
        log(f"\n[>] Searching: {dork}")
        try:
            results = search(dork, num_results=5)
            for result in results:
                log(f"  - {result}")
        except Exception as e:
            log(f"[!] Error during search: {e}")

# -------------------------
# 2. GITHUB DORKS
# -------------------------
def github_dorks(domain):
    dork = f"site:github.com {domain} password"
    log(f"\n[+] GitHub Dorks for {domain}")
    try:
        results = search(dork, num_results=5)
        for result in results:
            log(f"  - {result}")
    except Exception as e:
        log(f"[!] Error: {e}")

def github_repos(domain):
    dork = f"site:github.com {domain}"
    log(f"\n[+] GitHub Repositories for {domain}")
    try:
        results = search(dork, num_results=5)
        for result in results:
            log(f"  - {result}")
    except Exception as e:
        log(f"[!] Error: {e}")

# -------------------------
# 3. FIND EMAILS
# -------------------------
def get_email_accounts(domain):
    log(f"\n[+] Finding email accounts for {domain}")
    dork = f"{domain} email contact"
    try:
        results = search(dork, num_results=3)
        found_emails = set()
        for url in results:
            try:
                html = urllib.request.urlopen(url).read().decode("utf-8", errors="ignore")
                emails = re.findall(r"[\w\.-]+@[\w\.-]+", html)
                found_emails.update(emails)
            except:
                continue
        if found_emails:
            log("\nEmails found:")
            for e in found_emails:
                log(f" - {e}")
        else:
            log("No emails found.")
    except Exception as e:
        log(f"[!] Error: {e}")

# -------------------------
# 4. DOMAIN INFO
# -------------------------
def domain_info(domain):
    log(f"\n[+] Domain Info for {domain}")
    try:
        info = whois.whois(domain)
        for key in ["domain_name", "registrar", "creation_date", "expiration_date", "emails"]:
            log(f"{key}: {info.get(key)}")
    except Exception as e:
        log(f"[!] Error fetching WHOIS data: {e}")

# -------------------------
# 5. API LEAKS DORKS
# -------------------------
def check_api_leaks(domain):
    log(f"\n[+] Checking API leaks for {domain}")
    dorks = [
        f"site:pastebin.com {domain} api_key",
        f"site:trello.com {domain} password",
        f"site:gitlab.com {domain} token"
    ]
    for dork in dorks:
        log(f"\n[>] Searching: {dork}")
        try:
            results = search(dork, num_results=5)
            for result in results:
                log(f"  - {result}")
        except Exception as e:
            log(f"[!] Error during API dork search: {e}")

# -------------------------
# 6. IP INFO
# -------------------------
def ip_info(ip):
    log(f"\n[+] IP Info for {ip}")
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()
        for k in ["query", "country", "regionName", "city", "isp", "org", "timezone"]:
            log(f"{k}: {data.get(k)}")
    except Exception as e:
        log(f"[!] Error fetching IP info: {e}")

# -------------------------
# 7. SCREENSHOT SAVING
# -------------------------
def save_screenshot(domain):
    log(f"\n[+] Saving screenshot of {domain}")
    try:
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        url = f"http://{domain}"
        driver.set_window_size(1920, 1080)
        driver.get(url)
        os.makedirs("screenshots", exist_ok=True)
        filepath = f"screenshots/{domain}.png"
        driver.save_screenshot(filepath)
        log(f"[+] Screenshot saved to {filepath}")
        driver.quit()
    except Exception as e:
        log(f"[!] Error saving screenshot: {e}")

# -------------------------
# 8. SHODAN API
# -------------------------
def shodan_lookup(ip, shodan_key):
    log(f"\n[+] Shodan Lookup for {ip}")
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={shodan_key}"
        res = requests.get(url)
        data = res.json()
        for k in ["ip_str", "org", "os", "isp", "country_name", "city", "last_update"]:
            log(f"{k}: {data.get(k)}")
    except Exception as e:
        log(f"[!] Error fetching Shodan data: {e}")

# -------------------------
# 9. METADATA (Placeholder)
# -------------------------
def extract_metadata(file_path):
    log(f"\n[+] Extracting metadata from {file_path} (placeholder)")

# -------------------------
# MAIN ENTRY POINT (optional)
# -------------------------
def run_osint_all(domain):
    google_dorks(domain)
    github_dorks(domain)
    github_repos(domain)
    get_email_accounts(domain)
    domain_info(domain)
    check_api_leaks(domain)
    return '\n'.join(output_lines)
