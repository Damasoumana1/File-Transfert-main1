import sys
import tkinter as tk
# from tkinter import *
from tkinter import ttk
import os
import socket
import subprocess
from tkinter import PhotoImage


hostname = socket.gethostname()
server_ip  = socket.gethostbyname(hostname)
class FileTransferApp:
    server_running=True
    def __init__(self, root):
        self.root = root
        root=tk
        self.root.title("File Transfert")
        self.root.geometry("600x400")
        self.root.pack_propagate(False)
        self.root.config(bg="#BFBFBF")
        self.sl = False
        self.server_ip = server_ip 
        self.server_port = 3000
        # self.server_folder = tk.StringVar()
        # self.server_folder.set(self.server_folder)
        self.create_widgets()
   
    def create_widgets(self):
        # Titre
        title_label = tk.Label(self.root, text="File Transfert", font=("Arial", 20, "bold underline"), bg="#BFBFBF", fg="#2457FE")
        title_label.pack(pady=20)

        # Entrée IP du serveur
        Label=tk.Label(self.root, text="IP SERVER:", font=("Arial",12), bg="#BFBFBF", fg="#2457FE")
        Label.pack()
        self.ip_input = tk.Entry(self.root, font=("Arial", 12))
        #self.ip_input = tk.Entry(self.root, font=("Arial", 12), state="readonly")
        self.ip_input.insert(0, self.server_ip)
        self.ip_input.pack()

        # Entrée Port du serveur
        Label=tk.Label(self.root, text="Port:", font=("Arial", 12), bg="#BFBFBF", fg="#2457FE")
        Label.pack()
        self.port_input = tk.Entry(self.root, font=("Arial", 12))
        self.port_input.insert(0, self.server_port)
        self.port_input.pack()
        #File transfert
        space2 =tk.Label(self.root,text="^",font="Arial 3",bg="#BFBFBF",fg="#BFBFBF")
        space2.pack(pady=5,padx=0)
        self.dossier =tk.PhotoImage(file="C:/Users/Soumana DAMA/Desktop/File-Transfert-main1/icons/floder.png")
        # Ajoutez une icône de dossier pour ouvrir la page B
        self.Button= tk.Button(root,text='folder', font=("Arial",12) ,command=files_list, width=6, height=2)
        self.Button.pack()
        # Bouton START/STOP
        self.start_stop_button = tk.Button(self.root, text="START", activebackground='blue', font=("Arial", 16, "bold"), command=self.toggle_start_stop)
        self.start_stop_button.pack(pady=20)
        # Console de messages
        self.console = tk.Text(self.root, font=("Arial", 12), bg="#FFFFFF", fg="#000000", width=50, height=6)
        self.console.pack()
        #function defined
    def toggle_start_stop(self ,isStart=False):
        print(str(self.ip_input.get())+ " "+str(self.port_input.get()))
        if self.sl==False:
            self.start_stop_button.config(text="STOP")
            subprocess.Popen('python "C:/Users/Soumana DAMA/Desktop/File-Transfert-main1/ser1.py" '+str(self.ip_input.get())+ " "+str(self.port_input.get()))
            # subprocess.run(['python C:/Users/Soumana DAMA/Desktop/File-Transfert-main1/ser1.py', self.ip_input.get()])
            self.console.insert(tk.END, "STARTING: Send the File\n")
            print("run serveur")
            self.sl = True
            # os.system('python "C:/Users/Soumana DAMA/Desktop/File-Transfert-main1/ser1.py" '+str(self.ip_input.get())+ " "+str(self.port_input.get()) )
            # Ajoutez ici la logique pour démarrer le serveur
        else:
            self.start_stop_button.config(text="START")
            self.console.insert(tk.END, "STOPPING: Server stopped\n")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.ip_input.get(), int(self.port_input.get())))
            client_socket.send(b"STOP")
            client_socket.close()
            self.sl = False
        

server_folder = "folder"
def list_files():
    files = os.listdir(server_folder)
    return files
def send_file(client_socket, filename):
    file_path = os.path.join(server_folder, filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file.read(1024)
    else:
        client_socket.send(b'File not found')

# Create a socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def files_list():
        files_list = tk.Toplevel(root)
        files_list.title("File_folder")
        files_list.geometry("600x400")
        dama=list_files()
        file_combobox = ttk.Combobox(files_list, font=("Arial", 15), width=15, height=10, )
        file_combobox["values"] = dama
        file_combobox.pack()

        # def action(event):
        #         # Obtenir l'élément sélectionné
        #         select =file_combobox.get()
        #         print("Vous avez sélectionné : '", select,"'")
        #         labelChoix = tk.Label(root, text = "Liste des fichiers du serfer !")
        #         labelChoix.pack()
        #         file_combobox.current(0)
        #         file_combobox.bind("<<ComboboxSelected>>", action)
                
        # server_running=True
        # while server_running:
        # # Accept incoming connections
        #         client_socket, client_address = server_socket.accept()
        #         print(f"Accepted connection from {client_address}")
        #     # Receive client request
        #         request = client_socket.recv(1024).decode("utf-8")
        #         print(request)
        #         if request == 'LIST':
        #         # List files in the server folder
        #             files = list_files()
        #             file_list = "\n".join(files)
        #             client_socket.send(file_list.encode())
        #         elif request.startswith('GET'):
        #             # Extract filename from the request
        #             filename = request.split(' ')[1]
            
        #             # Send the requested file to the client
        #             send_file(client_socket, filename)
        
        #         # Close the client socket
        # client_socket.close()

# Fonction pour quitter la page A
def quitter_page_a():
    root.destroy()     

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()
