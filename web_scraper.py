from bs4 import BeautifulSoup as bs
from termcolor import colored
import argparse
import requests
import socket
import sys
import threading

LOCALHOST = "127.0.0.1"
PORT = 9001
ENCODING_TYPE = "ascii"
MAX_BYTES = 1024

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @staticmethod
    def count_img(html):
        return len(html.find_all("img"))

    @staticmethod
    def count_paragraph(html):
        count = 0
        for p in html.find_all("p"):
            if not p.find_all("p"):
                count += 1
        return count

    def thread(self, conn, addr):
        try:
            url = conn.recv(MAX_BYTES).decode(ENCODING_TYPE)

            page = requests.get(url, allow_redirects=True)
            soup = bs(page.text, "html.parser")

            print(colored(f"Scraping the webpage {url}...", "yellow"))
            img = self.count_img(soup)
            p = self.count_paragraph(soup)
            msg = f"{img} {p}".encode(ENCODING_TYPE)
            conn.send(msg)
            print(colored("Operation done.", "green"))
            
        except requests.exceptions.ConnectionError:
            print(f"Provided website cannot be reached. Connection with {addr} is closed.")
        except:
            print(f"There was an error with {addr}. Connection closed.")
        finally:
            conn.close()
            print()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen()
        print(colored(f"Server started on {sock.getsockname()}", "magenta"))

        while True:
            try:
                conn, addr = sock.accept()
                print(colored(f"Connection from {addr}", "cyan"))
                thread = threading.Thread(target=self.thread, args=(conn,addr,))
                thread.start()

            except KeyboardInterrupt:
                print('Server is being closed.')
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                break
            except:
                print(f"There was an error with {addr}. Connection closed.")
                continue

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self, url):
        try:
            requests.get(url, allow_redirects=True)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((LOCALHOST, PORT))

            sock.send(url.encode(ENCODING_TYPE))
            answer = sock.recv(MAX_BYTES).decode(ENCODING_TYPE)
            img, p = answer.split()
            print(f"There are {colored(img, 'cyan')} images and {colored(p, 'cyan')} paragraphs in the page `{url}`")
            
        except requests.exceptions.ConnectionError:
            print(f"Provided website cannot be reached. Connection wasn't created.")
        except socket.timeout:
            print("Connection couldn't be created.")
        except ConnectionRefusedError:
            print("Server cannot be reached.")
        except:
            print("Connection closed due to an error.")
        finally:
            if "sock" in locals():
                sock.close()


def main():
    choices = {"client", "server"}
    parser = argparse.ArgumentParser()
    parser.add_argument("choice", choices=choices, help="Type of connection")
    parser.add_argument("-p", "--page", metavar="PAGE", type=str, help="Webpage URL")
    args = parser.parse_args()

    if args.choice == "server":
        Server(LOCALHOST, PORT).start()
    elif args.choice == "client":
        if not args.page:
            print(colored("Provide a URL.", "red"))
            sys.exit(1)
        Client(LOCALHOST, PORT).connect(args.page if "http://" in args.page or "https://" in args.page else f"https://{args.page}")
        

if __name__ == "__main__":
    main()