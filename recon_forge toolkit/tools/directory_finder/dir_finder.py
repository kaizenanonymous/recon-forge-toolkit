import requests
import os
from urllib.parse import urljoin
import sys

BANNER = """
=======================================================
                DIRECTORY FINDER PRO
           Smart Directory Discovery Tool
              Dev by Anonymous Kaizen
=======================================================
"""

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def get_wordlist():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(base_dir, "../../"))
    wordlist = os.path.join(root, "wordlists", "directories.txt")

    if not os.path.exists(wordlist):
        print(f"{RED}[ERROR] Wordlist not found: {wordlist}{RESET}")
        return None

    return wordlist


def load_words(path):

    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_results(results):

    if not results:
        return

    os.makedirs("results", exist_ok=True)

    path = os.path.join("results", "directories_found.txt")

    with open(path, "w") as f:
        for r in results:
            f.write(r + "\n")

    print(f"\n{GREEN}[+] Results saved → {path}{RESET}")


def progress_bar(current, total):

    percent = int((current / total) * 100)
    bar = "#" * (percent // 5) + "-" * (20 - percent // 5)

    sys.stdout.write(f"\r[{bar}] {percent}% ({current}/{total})")
    sys.stdout.flush()


def scan(target, words):

    print(f"\n{YELLOW}[+] Scanning directories...\n{RESET}")

    session = requests.Session()
    found = set()
    results = []

    try:
        home = session.get(target, timeout=5)
        homepage_content = home.text
    except:
        print(f"{RED}[-] Cannot reach target site{RESET}")
        return []

    total = len(words)

    for i, word in enumerate(words, start=1):

        url = urljoin(target + "/", word)

        try:
            r = session.get(url, timeout=5, allow_redirects=True)

            # ignore redirect to homepage
            if r.url.rstrip("/") == target.rstrip("/"):
                continue

            # ignore homepage duplicate
            if r.text == homepage_content:
                continue

            # valid directory responses
            if r.status_code in [200,301,302,403]:

                if url not in found:
                    print(f"\n{GREEN}[FOUND]{RESET} {url} (Status {r.status_code})")
                    results.append(url)
                    found.add(url)

        except requests.RequestException:
            pass

        progress_bar(i, total)

    print()
    return results


def main():

    print(BANNER)

    target = input("Enter target website (https://example.com): ").strip()

    if not target.startswith("http"):
        target = "https://" + target

    wordlist = get_wordlist()

    if not wordlist:
        return

    words = load_words(wordlist)

    results = scan(target, words)

    if not results:
        print(f"\n{RED}[-] No directories discovered{RESET}")

    save_results(results)

    input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()