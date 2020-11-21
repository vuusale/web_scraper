import os
import threading

def run_command(url):
    os.system(f"python3 web_scraper.py client {url}")

urls = ["-p www.pcworld.com", "-p https://stackoverflow.com", "", "-p www.pcworld.comm"]
for i in range(len(urls)):
    thread = threading.Thread(target=run_command, args=(urls[i],))
    thread.start()