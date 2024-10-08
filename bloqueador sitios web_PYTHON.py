import tkinter as tk
from tkinter import PhotoImage
import mysql.connector

class Application():
    hostsFile = "C:/Windows/System32/drivers/etc/hosts"

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x400")
        self.window.title("Bloqueador de Páginas")
        self.window.resizable(width=False, height=False)

        # Configuración de color de fondo
        self.window.configure(bg='lightblue')

        # Cargar y colocar imagen
        self.image = PhotoImage(file="bloqueo.png")  # Cambia a la ruta de tu imagen
        self.image_label = tk.Label(self.window, image=self.image, bg='lightblue')
        self.image_label.pack()

        self.createLabel()
        self.createEntry()
        self.boton_crear()
        self.boton_eliminar()
        self.boton_listar()
        self.connect_database()
        self.window.mainloop()

    def createLabel(self):
        self.label = tk.Label(self.window, text="Ingresa URL:", bg='lightblue', fg='black')
        self.label.pack(pady=5)

    def createEntry(self):
        self.entry = tk.Entry(self.window, width=30)
        self.entry.pack()

    def boton_crear(self):     
        self.addButton = tk.Button(self.window, text="Añadir", command=self.agregar_url, bg='white', fg='black')
        self.addButton.pack(pady=5)

    def boton_eliminar(self):     
        self.removeButton = tk.Button(self.window, text="Eliminar", command=self.eliminar_url, bg='white', fg='black')
        self.removeButton.pack(pady=5)
        
    def boton_listar(self):
        self.addButton = tk.Button(self.window, text="Listar", command=self.listar_url, bg='white', fg='black')
        self.addButton.pack(pady=5)

    def connect_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Cambia a tu usuario de MySQL
                password="1234",  # Cambia a tu contraseña de MySQL
                database="paginas"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def agregar_url(self):
     url = self.entry.get()
     if url:
        # Agregar la URL al archivo hosts
        with open(self.hostsFile, 'a') as file:
            file.write(f"\n127.0.0.1\t{url}")

        # Guardar la URL en la base de datos
        self.guardar_url_db(url)
        
        self.entry.delete(0, tk.END)
       

    def guardar_url_db(self, url):
        try:
            self.cursor.execute("INSERT INTO registros (url) VALUES (%s)", (url,))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al guardar en la base de datos: {err}")

    def eliminar_url(self):
        url = self.entry.get()
        if url:
            with open(self.hostsFile, 'r') as file:
                lines = file.readlines()
            with open(self.hostsFile, 'w') as file:
                for line in lines:
                    if not line.strip().endswith(url):
                        file.write(line)
            self.entry.delete(0, tk.END)
            self.eliminar_url_db(url)

    def eliminar_url_db(self, url):
        try:
            self.cursor.execute("DELETE FROM registros WHERE url = %s", (url,))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al eliminar de la base de datos: {err}")

    def listar_url(self):
        new_window = tk.Tk()
        new_window.geometry("400x400")
        new_window.title("Páginas Bloqueadas")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg='lightblue')

        with open(self.hostsFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip().startswith("127.0.0.1\t"):
                    label = tk.Label(new_window, text=line.strip(), bg='lightblue', fg='black')
                    label.pack(pady=5)
        new_window.mainloop()

app = Application()
