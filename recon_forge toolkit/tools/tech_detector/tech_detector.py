import requests
import re
import os

BANNER = """
=======================================================
                     TECH DETECTOR 
                Dev By ANONYMOUS KAIZEN
=======================================================
"""

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def fetch_site(url):

    try:
        r = requests.get(url, timeout=10)
        return r
    except requests.RequestException:
        print(f"{RED}[-] Could not connect to target{RESET}")
        return None


def detect_headers(headers):

    results = []

    server = headers.get("Server")
    powered = headers.get("X-Powered-By")

    if server:
        results.append(f"Server: {server}")

    if powered:
        results.append(f"Powered By: {powered}")

    return results


def detect_cms(html):

    html = html.lower()
    results = []

    patterns = {
        "WordPress": ["wp-content", "wordpress"],
        "Joomla": ["joomla"],
        "Drupal": ["drupal"],
        "Shopify": ["shopify"],
        "Magento": ["magento"],
        "Blogger": ["blogger"]
    }

    for cms, signs in patterns.items():
        for s in signs:
            if s in html:
                results.append(f"CMS: {cms}")
                break

    return results


def detect_js_frameworks(html):

    html = html.lower()

    patterns = {
        "React": "react",
        "Vue": "vue",
        "Angular": "angular",
        "jQuery": "jquery",
        "Bootstrap": "bootstrap"
    }

    results = []

    for tech, keyword in patterns.items():
        if keyword in html:
            results.append(f"Frontend: {tech}")

    return results


def detect_backend(headers, html):

    results = []

    headers_str = str(headers).lower()
    html = html.lower()

    if "php" in headers_str or "php" in html:
        results.append("Backend: PHP")

    if "asp.net" in headers_str or "asp.net" in html:
        results.append("Backend: ASP.NET")

    if "node" in headers_str:
        results.append("Backend: Node.js")

    if "django" in html:
        results.append("Backend: Django")

    if "flask" in html:
        results.append("Backend: Flask")

    if "laravel" in html:
        results.append("Backend: Laravel")

    return results


def detect_meta_generator(html):

    results = []

    match = re.search(r'<meta name="generator" content="([^"]+)"', html, re.I)

    if match:
        results.append(f"Generator: {match.group(1)}")

    return results


def check_security_headers(headers):

    security_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    missing = []

    for h in security_headers:
        if h not in headers:
            missing.append(h)

    return missing


def save_results(results):

    os.makedirs("results", exist_ok=True)

    file = "results/tech_results.txt"

    with open(file, "w") as f:
        for r in results:
            f.write(r + "\n")

    print(f"\n{GREEN}[+] Results saved → {file}{RESET}")


def main():

    print(BANNER)

    url = input("Enter target (https://example.com): ").strip()

    if not url.startswith("http"):
        url = "https://" + url

    response = fetch_site(url)

    if not response:
        return

    html = response.text
    headers = response.headers

    results = []

    print(f"\n{YELLOW}[*] Detecting technologies...\n{RESET}")

    results += detect_headers(headers)
    results += detect_cms(html)
    results += detect_js_frameworks(html)
    results += detect_backend(headers, html)
    results += detect_meta_generator(html)

    if results:

        print(f"{GREEN}[+] Detected Technologies{RESET}\n")

        for r in results:
            print(f"  {r}")

    else:
        print("[-] No technologies detected")

    missing_headers = check_security_headers(headers)

    print(f"\n{YELLOW}[*] Security Headers Check{RESET}")

    if missing_headers:
        for h in missing_headers:
            print(f"{RED}Missing: {h}{RESET}")
    else:
        print(f"{GREEN}All major security headers present{RESET}")

    save_results(results)


if __name__ == "__main__":
    main()