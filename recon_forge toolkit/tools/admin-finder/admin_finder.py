import requests
import os
from urllib.parse import urljoin

def banner():
    print("="*55)
    print("                ADMIN FINDER")
    print("        Detect Admin / Login Panels")
    print("              Dev by Anonymous Kaizen")
    print("="*55)


def detect_type(html):

    html = html.lower()

    if "username" in html and "password" in html:
        return "LOGIN PANEL"

    if "admin" in html and "password" in html:
        return "ADMIN LOGIN PANEL"

    if "dashboard" in html:
        return "DASHBOARD"

    if "admin" in html:
        return "POSSIBLE ADMIN PAGE"

    return None


def find_admin(target):

    print("\n[+] Scanning...\n")

    # script location
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # go to toolkit root
    toolkit_root = os.path.abspath(os.path.join(base_dir, "../../"))

    # wordlist path
    wordlist_path = os.path.join(toolkit_root, "wordlists", "admin_paths.txt")

    if not os.path.exists(wordlist_path):
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        return

    with open(wordlist_path, "r") as f:
        paths = f.read().splitlines()

    for path in paths:

        url = urljoin(target, path)

        try:
            r = requests.get(url, timeout=5)

            if r.status_code == 200:

                page_type = detect_type(r.text)

                if page_type:
                    print(f"[{page_type}] -> {url}")

        except:
            pass


def main():

    banner()

    target = input("\nEnter target website (https://example.com): ")

    if not target.startswith("http"):
        target = "https://" + target

    find_admin(target)

    input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()