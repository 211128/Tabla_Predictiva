from tkinter import scrolledtext
import tkinter as tk
from tkinter import ttk
from Tabla_predictiva import analizar_entrada

def analizar():
    entrada = txt_entrada.get("1.0", tk.END).strip()
    resultado = analizar_entrada(entrada)
    txt_resultado.delete("1.0", tk.END)
    
    if "completado con éxito" in resultado.lower():
        # Aplicar etiqueta de color verde
        txt_resultado.tag_configure("success", foreground="green")
        txt_resultado.insert(tk.INSERT, resultado, "success")
    else:
        txt_resultado.insert(tk.INSERT, resultado)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador Sintáctico")

# Crear el estilo y aplicarlo a la ventana
estilo = ttk.Style()
estilo.theme_use("clam")  # Puedes cambiar "clam" por otros temas disponibles

# Ajustar algunos parámetros visuales
estilo.configure("TLabel", font=("Arial", 12))  # Cambiar la fuente de las etiquetas
estilo.configure("TButton", font=("Arial", 12), padding=5)  # Cambiar la fuente y el padding de los botones

# Crear el widget de entrada
lbl_entrada = ttk.Label(ventana, text="Texto a analizar:")
lbl_entrada.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

txt_entrada = scrolledtext.ScrolledText(ventana, width=40, height=10, font=("Arial", 12))
txt_entrada.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
txt_entrada.insert(tk.INSERT, '{displayData ("texto")}')

# Crear el botón para analizar
btn_analizar = ttk.Button(ventana, text="Analizar", command=analizar)
btn_analizar.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)

# Crear el contenedor para la salida
frame_salida = ttk.Frame(ventana)
frame_salida.grid(row=0, column=1, rowspan=3, pady=5, padx=5, sticky=tk.NSEW)

# Crear el widget de salida para resultados
lbl_resultado = ttk.Label(frame_salida, text="Resultado del análisis:")
lbl_resultado.pack()

txt_resultado = scrolledtext.ScrolledText(frame_salida, width=40, height=15, font=("Arial", 12))
txt_resultado.pack()

# Configurar el contenedor para expandirse con la ventana
ventana.grid_rowconfigure(0, weight=1)
ventana.grid_columnconfigure(1, weight=1)

# Iniciar el loop principal
ventana.mainloop()
