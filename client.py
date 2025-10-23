import tkinter as tk
from tkinter import messagebox
import socket
import os

def send_to_server(file_path, host='localhost', port=12345):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(file_path.encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            return response
    except Exception as e:
        return f"Error: {e}"

class SecureDeleteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Deletion Tool")
        self.root.geometry("400x200")
        
        self.label = tk.Label(root, text="Enter file path to delete securely:")
        self.label.pack(pady=10)
        
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)
        
        self.button = tk.Button(root, text="Delete File", command=self.delete_file)
        self.button.pack(pady=20)
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=10)
    
    def delete_file(self):
        file_path = self.entry.get().strip()
        if not file_path:
            messagebox.showerror("Error", "Please enter a file path")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File does not exist")
            return
        
        response = send_to_server(file_path)
        self.status_label.config(text=response)
        if "successfully" in response.lower() or "deleted" in response.lower():
            messagebox.showinfo("Success", response)
        else:
            messagebox.showerror("Error", response)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureDeleteApp(root)
    root.mainloop()