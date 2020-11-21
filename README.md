# Web scraper
 
This is a client-server application over TCP sockets that offers web scraping service. 

![Screenshot of running test.py](https://github.com/vuusale/web_scraper/blob/master/screenshot.png)

## Prerequisites
It is required to have Python3 installed in order to run the application. Just go to the [official Python website](https://python.org/) and download the release suitable to your machine. For example, if you have 64-bit Windows operating system, download *Windows x86-64 executable installer*. 

After ensuring that Python3 is set up, follow the below steps:

- Clone the repository into a desired location:
  
      $ git clone https://github.com/vuusale/text_service.git
      
- Install the requirements:
  
      $ pip install -r requirements.txt
  
Now you are ready to run the program. 

## Usage
Open 2 terminals: one for server and one for client. Then, run the following command in the first tab for server setup:
  
    $ python3 web_scraping.py server
  
To use the web scraping service, issue below command in the second terminal:
    
    $ python3 web_scraping.py -p WEBPAGE_URL
    
-p, --page: Specify the URL of the webpage you want to scrap

## Task
The goal is to create a client-server console app “web_scraper” with the next abilities:
- ###### Calculate the number of pictures in the webpage
- ###### Calculate the number of leaf paragraphs in the webpage

Server must be started and wait for the request from the client. It must scrape the webpage to extract two parameters: the number of pictures and the number of leaf paragraphs. Leaf paragraphs in HTML document are only the last paragraphs in nested paragraph structures. All the calculation must be done on the server side.

## Threading
This application implements threading in order to serve to clients concurrently. Since web requests are involved, threading speeds up the process by seperating subthreads from the main thread to prevent time-intensive operations from stopping the execution. It does not mean that tasks are carried out at the same time. While one thread is sitting idle waiting for something to happen, execution switches to another thread, once the previous operation is finished, execution is shifted back. Threading is different from multiprocessing in that multiprocessing uses different CPU cores for parallel computation. Threading is more advantegous for I/O operations such as web scraping, however, it provides no benefit when program is CPU bound.
