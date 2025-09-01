import hashlib
import os
import requests
import json
import tkinter as tk
from tkinter import filedialog, messagebox

API_KEY = '6c25e36ac655774edf26d1b2832f1a2ceb6d41064d9029214399b34a1ba92dfd'
BASE_URL = 'https://www.virustotal.com/api/v3/files/'

def calculate_hash(file_path, hash_type='sha256'):
    hash_obj = None
    if hash_type == 'md5':
        hash_obj = hashlib.md5()
    elif hash_type == 'sha1':
        hash_obj = hashlib.sha1()
    elif hash_type == 'sha256':
        hash_obj = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def check_file_in_virustotal(file_hash):
    headers = {
        'x-apikey': API_KEY
    }
    url = f"{BASE_URL}{file_hash}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']['attributes']['last_analysis_stats']
        else:
            return {"error": "Fișierul nu a fost găsit pe VirusTotal sau încă nu a fost procesat."}
    elif response.status_code == 404:
        return {"error": "Fișierul nu a fost găsit pe VirusTotal."}
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

def extract_metadata(file_path):
    file_info = {}
    stats = os.stat(file_path)
    file_info['size'] = stats.st_size
    file_info['creation_time'] = stats.st_ctime
    file_info['modification_time'] = stats.st_mtime
    return file_info

def analyze_file(file_path):
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Fișierul nu există.")
        return
    
    file_hash = calculate_hash(file_path, 'sha256')
    vt_report = check_file_in_virustotal(file_hash)
    file_metadata = extract_metadata(file_path)
    
    report = f"Fișier: {file_path}\nSHA-256 Hash: {file_hash}\nVirusTotal Analysis: {json.dumps(vt_report, indent=4)}\n\nMetadate: {json.dumps(file_metadata, indent=4)}"
    
    report_window = tk.Toplevel(root)
    report_window.title("Raportul analizei fișierului")
    report_text = tk.Text(report_window, wrap=tk.WORD, width=80, height=20)
    report_text.insert(tk.END, report)
    report_text.config(state=tk.DISABLED)
    report_text.pack(padx=10, pady=10)

def open_file():
    file_path = filedialog.askopenfilename(title="Selectați un fișier", filetypes=[("Toate fișierele", "*.*")])
    
    if file_path:
        analyze_file(file_path)

root = tk.Tk()
root.title("Tool de analiză fișiere")
root.geometry("400x200")

label = tk.Label(root, text="Bine ați venit la tool-ul de analiză fișiere", font=("Arial", 14))
label.pack(pady=20)

import_button = tk.Button(root, text="Importă fișier", command=open_file, font=("Arial", 12), width=20)
import_button.pack(pady=20)

root.mainloop()
