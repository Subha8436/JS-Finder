import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
import clipboard

def find_js_files(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        js_files = []

        for script in soup.find_all('script', src=True):
            src = script['src']
            if src.endswith('.js'):
                js_files.append(src)

        return js_files
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def get_js_files():
    url = url_entry.get()
    js_files_listbox.delete(0, tk.END)
    progress_bar.config(mode="indeterminate")
    progress_bar.start()
    js_files = find_js_files(url)
    for file in js_files:
        js_files_listbox.insert(tk.END, file)
    progress_bar.stop()
    progress_bar.config(mode="determinate")

def copy_link():
    selected_index = js_files_listbox.curselection()
    if selected_index:
        link = js_files_listbox.get(selected_index)
        clipboard.copy(link)

def open_link():
    selected_index = js_files_listbox.curselection()
    if selected_index:
        link = js_files_listbox.get(selected_index)
        import webbrowser
        webbrowser.open(link)

root = tk.Tk()
root.title("JS File Finder")

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

find_button = tk.Button(root, text="Find JS Files", command=get_js_files)
find_button.pack()

js_files_listbox = tk.Listbox(root, width=50)
js_files_listbox.pack()

copy_button = tk.Button(root, text="Copy Link", command=copy_link)
copy_button.pack(side=tk.LEFT)

open_button = tk.Button(root, text="Open Link", command=open_link)
open_button.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

root.mainloop()