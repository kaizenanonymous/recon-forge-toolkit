import os

def banner():
    print("""
=====================================================
                RECONFORGE TOOLKIT
        Advanced Recon & Security Scanner 
             Dev. By Anonymous Kaizen
=====================================================
""")
def menu():

    print("""
[1] Admin Panel Finder
[2] Subdomain Finder
[3] Directory Finder
[4] Technology Detector
[5] JavaScript File Finder
[0] Exit
""")

while True:

    banner()
    menu()

    choice = input("Select option: ")

    if choice == "1":
        os.system("py tools/admin-finder/admin_finder.py")

    elif choice == "2":
        os.system("py tools/subdomains_finder/sub_finder.py")

    elif choice == "3":
        os.system("py tools/directory_finder/dir_finder.py")

    elif choice == "4":
        os.system("py tools/tech_detector/tech_detector.py")

    elif choice == "5":
        os.system("py tools/js_finder/js_finder.py")

    elif choice == "0":
        print("Exiting toolkit...")
        break

    else:
        print("Invalid option")

    input("\nPress Enter to return to menu...")