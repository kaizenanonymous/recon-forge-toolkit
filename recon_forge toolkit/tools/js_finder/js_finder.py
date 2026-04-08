import requests
import re
import os
from urllib.parse import urljoin, urlparse

BANNER = """
=======================================================
                 JS FILE FINDER find js files

                 Dev by ANONYMOUS KAIZEN
=======================================================
"""

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


KEYWORDS = [
    "api", "token", "key", "secret", "password",
    "auth", "access", "client", "firebase", "aws"
]


def get_html(url):

    try:
        r = requests.get(url, timeout=10)
        return r.text
    except:
        print(f"{RED}[-] Could not fetch website{RESET}")
        return None


def extract_js(html, base_url):

    pattern = r'<script[^>]+src=["\'](.*?)["\']'
    matches = re.findall(pattern, html, re.I)

    js_files = set()

    for m in matches:
        full_url = urljoin(base_url, m)
        js_files.add(full_url)

    return list(js_files)


def scan_js(js_url):

    findings = []

    try:
        r = requests.get(js_url, timeout=10)
        data = r.text.lower()

        for k in KEYWORDS:
            if k in data:
                findings.append(k)

    except:
        pass

    return findings


def save_results(js_files):

    os.makedirs("results", exist_ok=True)

    path = "results/js_files.txt"

    with open(path, "w") as f:
        for js in js_files:
            f.write(js + "\n")

    print(f"\n{GREEN}[+] Results saved → {path}{RESET}")


def main():

    print(BANNER)

    url = input("Enter target (https://example.com): ").strip()

    if not url.startswith("http"):
        url = "https://" + url

    html = get_html(url)

    if not html:
        return

    print(f"\n{YELLOW}[*] Extracting JS files...{RESET}\n")

    js_files = extract_js(html, url)

    if not js_files:
        print("[-] No JS files found")
        return

    for js in js_files:

        print(f"{GREEN}[JS]{RESET} {js}")

        findings = scan_js(js)

        if findings:
            print(f"   {YELLOW}Keywords found:{RESET} {', '.join(findings)}")

    save_results(js_files)


if __name__ == "__main__":
    main()