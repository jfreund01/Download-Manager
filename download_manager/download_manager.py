from tkinter import *
import sv_ttk
import customtkinter as ctk
from sys import exit

from libgen_api import LibgenSearch
from concurrent.futures import as_completed, ThreadPoolExecutor
import requests
from urllib.parse import urlparse
from os.path import splitext
from sys import exit



class App(Tk):
    def __init__(self,size):
        super().__init__()
        # Initialize Window
        self.title("Class Based App")
        self.minsize(size[0],size[1])
        self.geometry(f'{size[0]}x{size[1]}')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.Menu = Menu(self)
        sv_ttk.set_theme('dark')

        self.mainloop()
        return(self)


class Menu(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Frame(self)
        self.grid(row=0, column=0, rowspan=4, sticky='nswe', padx=10, pady=10)
        self.rowconfigure((0,1,2,3), weight=1)
        self.columnconfigure((0,1), weight=1)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        book1=StringVar()
        book2=StringVar()
        book3=StringVar()
        author1=StringVar()
        author2=StringVar()
        author3=StringVar()
        url1 = StringVar()
        url2 = StringVar()
        url3 = StringVar()
        self.bookEntry1 = ctk.CTkEntry(self, placeholder_text='Enter Book Title...',textvariable=book1)
        self.bookEntry2 = ctk.CTkEntry(self, placeholder_text='Enter Book Title...',textvariable=book2)
        self.bookEntry3 = ctk.CTkEntry(self, placeholder_text='Enter Book Title...',textvariable=book3)
        self.authorEntry1 = ctk.CTkEntry(self, placeholder_text='Enter Author Title...',textvariable=author1)
        self.authorEntry2 = ctk.CTkEntry(self, placeholder_text='Enter Author Title...',textvariable=author2)
        self.authorEntry3 = ctk.CTkEntry(self, placeholder_text='Enter Author Title...',textvariable=author3)
        self.urlEntry1 = ctk.CTkEntry(self, placeholder_text='Enter Urls',textvariable=url1)
        self.urlEntry2 = ctk.CTkEntry(self, placeholder_text='Enter Urls',textvariable=url2)
        self.urlEntry3 = ctk.CTkEntry(self, placeholder_text='Enter Urls',textvariable=url3)
        self.authors = [author1, author2, author3]
        
        self.books = [book1, book2, book3]
        
        self.urls = [url1, url2, url3]
        
        self.button1 = ctk.CTkButton(self, text='DOWNLOAD',command= lambda: self.start_download(self.books, \
                                                                                                self.authors, self.urls))

    def create_layout(self):
        
        self.button1.grid(row=0,column=0,sticky='news',padx=10,pady=10,columnspan=2)
        self.urlEntry1.grid()
        self.bookEntry1.grid(row=1,column=0,sticky='we',padx=10,pady=10)
        self.bookEntry2.grid(row=2,column=0,sticky='we',padx=10,pady=10)
        self.bookEntry3.grid(row=3,column=0,sticky='we',padx=10,pady=10)
        self.authorEntry1.grid(row=1,column=1,sticky='we',padx=20,pady=10)
        self.authorEntry2.grid(row=2,column=1,sticky='we',padx=20,pady=10)
        self.authorEntry3.grid(row=3,column=1,sticky='we',padx=20,pady=10)
        self.urlEntry1.grid(row=4,column=0,sticky='we',columnspan=2,padx=10,pady=5)
        self.urlEntry2.grid(row=5,column=0,sticky='we',columnspan=2,padx=10,pady=5)
        self.urlEntry3.grid(row=6,column=0,sticky='we',columnspan=2,padx=10,pady=5)
    
    def start_download(self, books, authors, urls):
        self.authors = [authors[0].get(),\
                        authors[1].get(),\
                        authors[2].get()]
        
        self.books = [books[0].get(),\
                      books[1].get(),\
                      books[2].get()]
        
        self.urls = [urls[0].get(),\
                     urls[1].get(),\
                     urls[2].get()]
        
        download(self.books, self.authors, self.urls)
        exit()




def download(books, authors, urls_list):
    s = LibgenSearch()
    data_list = []

    # Parse book entry data to get data blocks
    for i in range(len(books)):
        if books[i] != '':
            data_list.append(book_data_parse(s,books[i],authors[i]))

    # Parse url entry data to get data blocks
    for i in range(len(urls_list)):
        if urls_list[i] != '':
            data = [urls_list[i], 0, \
                    f"{i + 1}{get_ext(urls_list[i])}"]
            data_list.append(data)

    ## Creates executor to feed data blocks into download function
    with ThreadPoolExecutor(6) as executor:
        futures = []
        for file in data_list:
            print(file)
            if len(file) != 0:
                futures.append(executor.submit(download_url, data = file))
        for future in as_completed(futures):
            print(future.result())

def download_url(data):
    filename = data[0]
    size = data[1]
    url = data[2]

    response = requests.get(url, stream=True)
    with open(f"/Users/jacobfreund/Downloads/{filename}", mode="wb") as file:
        written=0
        for chunk in response.iter_content(chunk_size=1024*1024):
            file.write(chunk)
            written += 1
            print (written/size)
    print(f"Downloaded File {filename}") 
    return 1

def book_data_parse(crawler, book, author):
    result = crawler.search_title_filtered(book, {"Author":author}, exact_match=False)
    if len(result) != 0:
        return [result[0]['Title'], result[0]['Size'], crawler.resolve_download_links(result[0])['GET']]
    else:
        return []

def get_ext(url):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext  # or ext[1:] if you don't want the leading '.'



size = (600,600)
App(size)

