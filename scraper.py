import tkinter as tk
from tkinter import messagebox
import requests
import random
from PIL import Image, ImageTk

class SubdomainScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sidhaant's Web Scraper")
        self.root.attributes("-fullscreen", True)  # Enable full-screen mode
        self.root.bind("<Escape>", self.exit_fullscreen)  # Bind Escape key to exit full-screen

        # Load and set the wallpaper
        self.bg_image = Image.open("C:/Users/sid/Downloads/Bugbounty-Project/matrix-style-binary-code-digital-falling-numbers-blue-background_1017-37387.jpg")
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)  # Resize to fit the screen
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Make the label fill the window

        self.title_label = tk.Label(root, text="Sidhaant's Web Scraper", font=("Helvetica", 20), bg="#282c34", fg="white")
        self.title_label.pack(pady=10)

        self.url_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
        self.url_entry.insert(0, "www.")
        self.url_entry.pack(pady=20)

        self.scrape_button = tk.Button(root, text="Scrape the Web", command=self.scrape_subdomains, font=("Helvetica", 14), bg="#61afef", fg="white")
        self.scrape_button.pack(pady=20)

        # Create two list boxes for vulnerable and safe subdomains
        self.vulnerable_label = tk.Label(root, text="Vulnerable Sites:", font=("Helvetica", 14), bg="#282c34", fg="white")
        self.vulnerable_label.pack(pady=(10, 0))
        
        self.vulnerable_list = tk.Listbox(root, width=70, height=10, font=("Helvetica", 12), bg="#ffcccc")
        self.vulnerable_list.pack(pady=5)

        self.safe_label = tk.Label(root, text="Safe Sites:", font=("Helvetica", 14), bg="#282c34", fg="white")
        self.safe_label.pack(pady=(10, 0))

        self.safe_list = tk.Listbox(root, width=70, height=10, font=("Helvetica", 12), bg="#ccffcc")
        self.safe_list.pack(pady=5)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)  # Exit full-screen mode
        self.root.geometry("600x500")  # Set a default window size

    def scrape_subdomains(self):
        url = self.url_entry.get()
        if not url.startswith("www."):
            messagebox.showerror("Error", "Please enter a valid website starting with 'www.'")
            return

        domain = url[4:]  # Remove "www."
        subdomains = self.find_subdomains(domain)

        # Clear previous results
        self.vulnerable_list.delete(0, tk.END)
        self.safe_list.delete(0, tk.END)

        if subdomains:
            vulnerable_subdomains = []
            safe_subdomains = []

            # Simulate checking for bugs in subdomains
            for subdomain in sorted(subdomains):
                has_bug = random.choice([True, False])  # Randomly assign bug status for demo
                if has_bug:
                    vulnerable_subdomains.append(subdomain)
                else:
                    safe_subdomains.append(subdomain)

            # Display results
            for subdomain in vulnerable_subdomains:
                self.vulnerable_list.insert(tk.END, f"- {subdomain} (Vulnerable)")

            for subdomain in safe_subdomains:
                self.safe_list.insert(tk.END, f"- {subdomain} (Safe)")

            messagebox.showinfo("Info", f"Found {len(subdomains)} subdomains.")
        else:
            messagebox.showinfo("Info", "No subdomains found.")

    def find_subdomains(self, domain):
        subdomains = set()
        try:
            # Use the Hackertarget subdomain API
            response = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}")
            if response.status_code == 200:
                for line in response.text.splitlines():
                    subdomain_info = line.split(",")
                    if len(subdomain_info) > 1:
                        subdomains.add(subdomain_info[0])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        return subdomains

if __name__ == "__main__":
    root = tk.Tk()
    app = SubdomainScraperApp(root)
    root.mainloop()
