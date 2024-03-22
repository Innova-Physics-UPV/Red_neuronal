import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import pickle  # Utilizamos pickle para guardar y cargar datos en archivos binarios

class SeleccionadorCarpeta:
    def __init__(self, root):
        self.root = root
        self.ruta_carpeta = None
        self.imagenes_seleccionadas = []

        # Configurar la ventana principal
        self.root.title("Seleccionar Carpeta")
        
        # Botón para seleccionar carpeta
        self.boton_seleccionar = tk.Button(root, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar.pack(pady=10)

    def seleccionar_carpeta(self):
        # Diálogo para seleccionar carpeta
        self.ruta_carpeta = filedialog.askdirectory()
        
        if self.ruta_carpeta:
            print("Carpeta seleccionada:", self.ruta_carpeta)

            # Obtener las rutas de las imágenes y almacenarlas en la lista
            self.imagenes_seleccionadas = self.obtener_rutas_imagenes()

            # Mostrar las imágenes en la carpeta
            self.mostrar_imagenes()

    def obtener_rutas_imagenes(self):
        return [os.path.join(self.ruta_carpeta, archivo) for archivo in os.listdir(self.ruta_carpeta)
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg'))]

    def mostrar_imagenes(self):
        rutas_imagenes = self.imagenes_seleccionadas

        # Mostrar cada imagen en una nueva ventana
        for ruta_imagen in rutas_imagenes:
            imagen = Image.open(ruta_imagen)
            
            # Mostrar la imagen en una nueva ventana
            ventana_imagen = tk.Toplevel(self.root)
            imagen_tk = ImageTk.PhotoImage(imagen)
            etiqueta_imagen = tk.Label(ventana_imagen, image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
            etiqueta_imagen.pack()

    def guardar_rutas_en_archivo(self, nombre_archivo="rutasimagenesconruido.dat"):
        # Guardar las rutas en un archivo usando pickle
        with open(nombre_archivo, 'wb') as archivo:
            pickle.dump(self.imagenes_seleccionadas, archivo)

if __name__ == "__main__":
    root = tk.Tk()
    app = SeleccionadorCarpeta(root)
    root.mainloop()

    # Después de cerrar la ventana principal, guardar las rutas en un archivo
    app.guardar_rutas_en_archivo()
