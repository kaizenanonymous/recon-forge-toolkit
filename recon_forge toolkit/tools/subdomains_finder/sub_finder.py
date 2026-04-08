import requests
import os

def banner():
    print("="*55)
    print("                SUBDOMAIN FINDER")
    print("           Find hidden subdomains")
    print("              Dev by Anonymous Kaizen")
    print("="*55)


def find_subdomains(domain):

    print("\n[+] Scanning for subdomains...\n")

    # script location
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # toolkit root
    toolkit_root = os.path.abspath(os.path.join(base_dir, "../../"))

    # wordlist path
    wordlist_path = os.path.join(toolkit_root, "wordlists", "subdomains.txt")

    if not os.path.exists(wordlist_path):
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        return

    with open(wordlist_path, "r") as f:
        subs = f.read().splitlines()

    found = []

    for sub in subs:

        url = f"https://{sub}.{domain}"

        try:
            r = requests.get(url, timeout=3)

            if r.status_code < 400:
                print(f"[FOUND] {url}")
                found.append(url)

        except:
            pass

    if not found:
        print("[-] No subdomains found")


def main():

    banner()

    domain = input("\nEnter target domain (example.com): ")

    domain = domain.replace("https://","").replace("http://","").strip("/")

    find_subdomains(domain)

    input("\nPress Enter to return to menu...")


if __name__ == "__main__":
    main()