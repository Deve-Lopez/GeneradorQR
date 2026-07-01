"""
GeneradorQR - Aplicación de escritorio para generar códigos QR masivos
Autor: Daniel López
Descripción: Genera códigos QR a partir de un archivo CSV con nombres y URLs.
"""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import qrcode


def seleccionar_carpeta():
    """Abre un diálogo para seleccionar la carpeta de salida."""
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de salida")
    if carpeta:
        carpeta_salida.set(carpeta)


def generar_qr():
    """Función principal: genera QR y nuevo CSV a partir del archivo seleccionado."""
    carpeta = carpeta_salida.get()

    if not carpeta:
        messagebox.showerror("Error", "Por favor, selecciona una carpeta de salida.")
        return

    # Seleccionar archivo CSV
    archivo_csv = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )

    if not archivo_csv:
        messagebox.showerror("Error", "Por favor, selecciona un archivo CSV.")
        return

    # Leer datos del CSV
    pdfs = []
    try:
        with open(archivo_csv, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Saltar la cabecera

            for row in reader:
                if len(row) >= 2:  # Asegurar que tenga al menos nombre y URL
                    nombre = row[0].strip()
                    url = row[1].strip()
                    if nombre and url:
                        pdfs.append({"nombre": nombre, "url": url})
                else:
                    print(f"Fila ignorada (formato incorrecto): {row}")

        if not pdfs:
            messagebox.showerror("Error", "El archivo CSV no contiene datos válidos.")
            return

    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el CSV: {str(e)}")
        return

    # Generar QR y nuevo CSV
    csv_path = os.path.join(carpeta, "productos_y_qrs.csv")
    try:
        with open(csv_path, "w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nombre del Producto", "Enlace"])  # Cabecera

            for pdf in pdfs:
                # Escribir en el nuevo CSV
                writer.writerow([pdf["nombre"], pdf["url"]])

                # Generar código QR
                qr = qrcode.make(pdf["url"])
                qr_path = os.path.join(carpeta, f'{pdf["nombre"].replace(" ", "_")}.png')
                qr.save(qr_path)
                print(f'QR generado: {qr_path}')

        messagebox.showinfo("Éxito", 
            f"Se generaron {len(pdfs)} códigos QR y el archivo productos_y_qrs.csv correctamente.")
        print("Proceso completado exitosamente.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al generar los archivos: {str(e)}")


# ====================== INTERFAZ GRÁFICA ======================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador de Códigos QR")
    root.geometry("500x300")
    root.resizable(False, False)

    # Variable para la carpeta
    carpeta_salida = tk.StringVar()

    # Título
    tk.Label(root, text="Generador de Códigos QR", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Label(root, text="Selecciona el archivo CSV con los enlaces de descarga directa:").pack(pady=5)

    # Botón para seleccionar carpeta
    tk.Button(root, text="Seleccionar carpeta de salida", 
              command=seleccionar_carpeta, width=30).pack(pady=10)

    # Botón principal
    tk.Button(root, text="Generar QR y CSV", 
              command=generar_qr, width=30, bg="#4CAF50", fg="white").pack(pady=20)

    root.mainloop()