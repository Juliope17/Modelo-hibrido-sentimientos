import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
from docx import Document  # Para manejar archivos .docx
import PyPDF2  # Para manejar archivos PDF
import os

# Función para cargar un archivo
def cargar_documento():
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("Todos los archivos", "*.*"), 
                   ("Archivos de texto", "*.txt"), 
                   ("Documentos Word", "*.docx"), 
                   ("Archivos PDF", "*.pdf"))
    )

    if ruta_archivo:
        extension = os.path.splitext(ruta_archivo)[1].lower()

        try:
            if extension == ".txt":
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    texto = archivo.read()
            elif extension == ".docx":
                doc = Document(ruta_archivo)
                texto = '\n'.join([para.text for para in doc.paragraphs])
            elif extension == ".pdf":
                with open(ruta_archivo, 'rb') as archivo_pdf:
                    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
                    texto = ''
                    for pagina in lector_pdf.pages:
                        texto += pagina.extract_text()
            else:
                messagebox.showerror("Error", "Formato de archivo no compatible.")
                return

            # Mostrar el contenido del archivo en el cuadro de texto
            entrada_texto.delete(1.0, tk.END)  # Limpiar el campo de texto
            entrada_texto.insert(tk.END, texto)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

# Función de análisis simulado
def analizar_texto():
    texto = entrada_texto.get(1.0, tk.END).strip()
    if not texto:
        messagebox.showerror("Error", "Debe ingresar o cargar un texto para analizar.")
        return
    
    # Cambiar a la ventana de análisis
    cambiar_ventana(ventana_analizando)
    
    # Simular análisis con una barra de progreso (espera)
    ventana_analizando.update()
    time.sleep(2)  # Simular análisis (2 segundos)
    
    # Cambiar a la ventana de resultados
    cambiar_ventana(ventana_resultado)
    texto_resultado.config(state=tk.NORMAL)
    texto_resultado.delete(1.0, tk.END)  # Limpiar el resultado previo
    texto_resultado.insert(tk.END, f"Resultado del análisis: {texto}\n")
    texto_resultado.config(state=tk.DISABLED)

# Función para cambiar entre ventanas
def cambiar_ventana(ventana):
    ventana_presentacion.pack_forget()
    ventana_inicio.pack_forget()
    ventana_analizando.pack_forget()
    ventana_resultado.pack_forget()
    ventana.pack(fill="both", expand=True)

# Función para eliminar el texto de marcador de posición
def eliminar_placeholder(event=None):
    if entrada_texto.get(1.0, tk.END).strip() == "Ingresa o pega el texto aquí...":
        entrada_texto.delete(1.0, tk.END)

# Función para restablecer el cuadro de texto con el placeholder
def restablecer_texto_inicio():
    entrada_texto.delete(1.0, tk.END)  # Limpiar el campo de texto
    entrada_texto.insert(tk.END, "Ingresa o pega el texto aquí...")  # Insertar el placeholder

# Función para redimensionar la imagen de fondo según el tamaño de la ventana
def ajustar_imagen(event, label_fondo):
    nuevo_ancho = event.width
    nuevo_alto = event.height
    imagen_redimensionada = imagen_comun.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    fondo_comun_resized = ImageTk.PhotoImage(imagen_redimensionada)
    label_fondo.config(image=fondo_comun_resized)
    label_fondo.image = fondo_comun_resized  # Evitar que la imagen sea recolectada por el garbage collector

# Inicialización de la ventana principal
root = tk.Tk()
root.title("Analizador de Textos")
root.geometry("600x500")

# Deshabilitar redimensionamiento
root.resizable(True, True)

# Cambiar el color de fondo a #2E6EC2
root.configure(bg="#2E6EC2")

# Estilo de los botones
boton_style = {
    "font": ("Arial", 14),
    "bg": "#0056b3",
    "fg": "white",
    "activebackground": "#004090",
    "activeforeground": "white",
    "bd": 0,
    "relief": tk.FLAT
}

# Imagen común para las ventanas (excepto la de inicio)
imagen_comun = Image.open("fondo.png")  # Imagen sobre el fondo azul

# Ventana de presentación
ventana_presentacion = tk.Frame(root, bg="#2E6EC2")
ventana_presentacion.pack(fill="both", expand=True)

label_titulo_presentacion = tk.Label(ventana_presentacion, text="Bienvenido al Analizador de Sentimientos", bg="#2E6EC2", fg="white", font=("Arial", 18))
label_titulo_presentacion.pack(pady=20)

# Cargar y mostrar imagen de presentación
imagen_presentacion = Image.open("Escudo.png")  # Ruta de la imagen de presentación
imagen_presentacion = imagen_presentacion.resize((200, 200), Image.Resampling.LANCZOS)
img_presentacion = ImageTk.PhotoImage(imagen_presentacion)
label_imagen_presentacion = tk.Label(ventana_presentacion, image=img_presentacion, bg="#2E6EC2")
label_imagen_presentacion.pack(pady=10)

label_autores = tk.Label(ventana_presentacion, text=" José Jimenez \n Edinson Palacio \n Julio Peñaloza", bg="#2E6EC2", fg="white", font=("Arial", 14))
label_autores.pack(pady=10)

# Botón para comenzar
boton_comenzar = tk.Button(ventana_presentacion, text="Comenzar", command=lambda: cambiar_ventana(ventana_inicio))
boton_comenzar.pack(pady=20)

# Ventana de inicio
ventana_inicio = tk.Frame(root, bg="#2E6EC2")

# Imagen de fondo sobre el fondo azul
label_fondo_inicio = tk.Label(ventana_inicio, bg="#2E6EC2")
label_fondo_inicio.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_inicio.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_inicio))

label_bienvenida = tk.Label(ventana_inicio, text="Analizar Sentimientos", bg="#2E6EC2", fg="white", font=("Arial", 16))
label_bienvenida.pack(pady=20)

# Cuadro de texto con placeholder
entrada_texto = tk.Text(ventana_inicio, height=10, width=50, wrap=tk.WORD)
entrada_texto.pack(pady=10)
entrada_texto.insert(tk.END, "Ingresa o pega el texto aquí...")
entrada_texto.bind("<FocusIn>", eliminar_placeholder)

# Crear un frame para alinear los botones horizontalmente
frame_botones = tk.Frame(ventana_inicio, bg="#2E6EC2")
frame_botones.pack(pady=10)

# Redimensionar el icono de carga
imagen_icono = Image.open("cargar.png")  # Cargar la imagen del icono
imagen_icono = imagen_icono.resize((30, 30), Image.Resampling.LANCZOS)
icono_cargar = ImageTk.PhotoImage(imagen_icono)

# Botón para analizar
boton_analizar = tk.Button(frame_botones, text="Analizar", command=analizar_texto, **boton_style)
boton_analizar.grid(row=0, column=0, padx=5)

# Icono de carga (en lugar del botón de texto)
boton_cargar = tk.Button(frame_botones, image=icono_cargar, command=cargar_documento, bg="white", bd=0)
boton_cargar.grid(row=0, column=1, padx=5)

# Ventana de análisis
ventana_analizando = tk.Frame(root, bg="#2E6EC2")

label_fondo_analizando = tk.Label(ventana_analizando, bg="#2E6EC2")
label_fondo_analizando.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_analizando.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_analizando))

label_analizando = tk.Label(ventana_analizando, text="Analizando...", bg="#2E6EC2", fg="white", font=("Arial", 16))
label_analizando.pack(pady=20)

# Spinner simulado
label_spinner = tk.Label(ventana_analizando, text="⏳", font=("Arial", 50), bg="#2E6EC2", fg="white")
label_spinner.pack(pady=20)

# Ventana de resultado
ventana_resultado = tk.Frame(root, bg="#2E6EC2")

label_fondo_resultado = tk.Label(ventana_resultado, bg="#2E6EC2")
label_fondo_resultado.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_resultado.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_resultado))

texto_resultado = tk.Text(ventana_resultado, height=10, width=50, state=tk.DISABLED, wrap=tk.WORD)
texto_resultado.pack(pady=10)

# Botón para volver a la ventana de inicio y restablecer el texto
boton_volver = tk.Button(ventana_resultado, text="Volver", command=lambda: [restablecer_texto_inicio(), cambiar_ventana(ventana_inicio)], **boton_style)
boton_volver.pack(pady=10)

# Mostrar ventana de presentación al iniciar
cambiar_ventana(ventana_presentacion)

# Iniciar el loop principal
root.mainloop()
