import hashlib
import json
import time
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Blockchain:
    def __init__(self):
        self.chain = []
        self.votes = []
        self.create_block(previous_hash='0')
        self.voted_users = set()
        self.candidates = ["Ion", "Maria", "Vasile"]

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'votes': self.votes,
            'previous_hash': previous_hash
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        self.votes = []
        return block

    def add_vote(self, voter_id, candidate):
        if voter_id in self.voted_users:
            return "Utilizatorul a votat deja!"
        if candidate not in self.candidates:
            return "Candidat invalid!"
        self.votes.append({'voter_id': voter_id, 'candidate': candidate})
        self.voted_users.add(voter_id)
        self.create_block(self.chain[-1]['hash'])
        return "Vot adăugat!"

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def get_chain(self):
        return self.chain

    def has_voted(self, voter_id):
        return voter_id in self.voted_users
    
    def count_votes(self):
        vote_count = {candidate: 0 for candidate in self.candidates}
        for block in self.chain:
            for vote in block['votes']:
                vote_count[vote['candidate']] += 1
        return vote_count

def vote():
    voter_id = voter_id_entry.get()
    candidate = candidate_var.get()
    result = blockchain.add_vote(voter_id, candidate)
    if result == "Vot adăugat!":
        messagebox.showinfo("Confirmare Vot", f"Ați votat cu succes pentru {candidate}")
        show_results()
    else:
        messagebox.showerror("Eroare Vot", result)

def show_chain():
    chain_data = json.dumps(blockchain.get_chain(), indent=4)
    chain_window = tk.Toplevel()
    chain_window.title("Blockchain")
    chain_text = tk.Text(chain_window, wrap=tk.WORD)
    chain_text.insert(tk.END, chain_data)
    chain_text.pack()

def check_vote():
    voter_id = voter_id_entry.get()
    if blockchain.has_voted(voter_id):
        messagebox.showinfo("Verificare Vot", "Acest utilizator a votat deja.")
    else:
        messagebox.showinfo("Verificare Vot", "Acest utilizator NU a votat încă.")

def show_results():
    results = blockchain.count_votes()
    candidates = list(results.keys())
    votes = list(results.values())
    
    result_text = "Rezultate vot:\n" + "\n".join([f"{candidate}: {votes} voturi" for candidate, votes in results.items()])
    result_window = tk.Toplevel()
    result_window.title("Rezultate Vot")
    result_label = tk.Label(result_window, text=result_text, font=('Arial', 12))
    result_label.pack()

    plt.bar(candidates, votes, color=['blue', 'green', 'red'])
    plt.title('Rezultate Vot')
    plt.xlabel('Candidati')
    plt.ylabel('Număr de Voturi')
    plt.show()

blockchain = Blockchain()

root = tk.Tk()
root.title("Sistem Electronic de Vot")
root.geometry("600x400")

tk.Label(root, text="ID Votant:").pack()
voter_id_entry = tk.Entry(root)
voter_id_entry.pack()

candidate_var = tk.StringVar(value=blockchain.candidates[0])
tk.Label(root, text="Selectează Candidat:").pack()
for candidate in blockchain.candidates:
    tk.Radiobutton(root, text=candidate, variable=candidate_var, value=candidate).pack()

tk.Button(root, text="Votează", command=vote, font=('Arial', 12), bg='lightblue').pack(pady=5)
tk.Button(root, text="Verifică Vot", command=check_vote, font=('Arial', 12), bg='lightgreen').pack(pady=5)
tk.Button(root, text="Afișează Blockchain", command=show_chain, font=('Arial', 12), bg='lightyellow').pack(pady=5)
tk.Button(root, text="Afișează Rezultate", command=show_results, font=('Arial', 12), bg='lightcoral').pack(pady=5)

root.mainloop()
