from lib.datos_de_calibracion import temperaturas # type: ignore
import tkinter as tk
from tkinter import ttk
import csv
import matplotlib.pyplot as plt


# Entrada Analógica
V2 = 2.5
R3 = 127000
R4 = 30900
R5 = 39200

def voltaje_a_resistencia(VA,V1,R1,j):
    VB = ((VA/R3) + (V2/R4))*(1/((1/R5)+(1/R4)+(1/R3)))
    I1_ = (V1-VA) / R1[j]
    I2_ = (V2-VB) / R4
    RT_ = (VA*(R3+R5))/((I1_*(R3+R5))+(I2_*R5)-(VA))
    return RT_

def resistencia_a_temperatura(resistencia,temp_offset,j):
    i = 1
    for temperatura in temperaturas:
        if (resistencia >= temperatura[1]):
            x1 = temperatura[0]
            x2 = temperaturas[i][0]
            y1 = temperatura[1]
            y2 = temperaturas[i][1]
            return ((x1 + ((resistencia - y1) / (y2 - y1)) * (x2 - x1))*1.0)+ temp_offset[j]
        i += 1

def filtro_alpha(temp,tempf, alpha):
    # Aplicar el filtro alfa
    return alpha * temp + (1 - alpha) * tempf

def obtener_datos():
    # Esta función se ejecuta cuando el usuario presiona "Submit"
    def submit():
        nonlocal dispositivo, tiempo_muestreo, tiempo_entre_muestreos, nombre_archivo
        # Captura los valores de las entradas
        dispositivo = dispositivo_var.get()
        tiempo_muestreo = float(tiempo_muestreo_entry.get())
        tiempo_entre_muestreos = float(tiempo_entre_muestreos_entry.get())
        nombre_archivo = nombre_archivo_entry.get()
        # Cierra la ventana
        root.destroy()

    # Variables para almacenar los resultados
    dispositivo = "Dev2"
    tiempo_muestreo = 10.0
    tiempo_entre_muestreos = 5.0
    nombre_archivo = "temperaturas"

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Configuración de muestreo")

    # Variables para los widgets
    dispositivo_var = tk.StringVar(value=dispositivo)
    tiempo_muestreo_var = tk.StringVar(value=tiempo_muestreo)  # Valor predeterminado de 10 minutos
    tiempo_entre_muestreos_var = tk.StringVar(value=tiempo_entre_muestreos)  # Valor predeterminado de 5 segundos
    nombre_archivo_var = tk.StringVar(value=nombre_archivo)  # Valor predeterminado del nombre del archivo

    # Toggle para seleccionar el dispositivo
    dispositivo_label = ttk.Label(root, text="Dispositivo:")
    dispositivo_label.grid(row=0, column=0, padx=10, pady=10)

    dispositivo_toggle = ttk.Radiobutton(root, text="Dispositivo 1", variable=dispositivo_var, value="Dev1")
    dispositivo_toggle.grid(row=0, column=1, padx=10, pady=10)

    dispositivo_toggle2 = ttk.Radiobutton(root, text="Dispositivo 2", variable=dispositivo_var, value="Dev2")
    dispositivo_toggle2.grid(row=0, column=2, padx=10, pady=10)

    # Entrada para el tiempo de muestreo
    tiempo_muestreo_label = ttk.Label(root, text="Tiempo de muestreo (min):")
    tiempo_muestreo_label.grid(row=1, column=0, padx=10, pady=10)

    tiempo_muestreo_entry = ttk.Entry(root, textvariable=tiempo_muestreo_var)
    tiempo_muestreo_entry.grid(row=1, column=1, padx=10, pady=10)

    # Entrada para el tiempo entre muestreos
    tiempo_entre_muestreos_label = ttk.Label(root, text="Tiempo entre muestreos (seg):")
    tiempo_entre_muestreos_label.grid(row=2, column=0, padx=10, pady=10)

    tiempo_entre_muestreos_entry = ttk.Entry(root, textvariable=tiempo_entre_muestreos_var)
    tiempo_entre_muestreos_entry.grid(row=2, column=1, padx=10, pady=10)

    # Entrada para el nombre del archivo
    nombre_archivo_label = ttk.Label(root, text="Nombre del archivo:")
    nombre_archivo_label.grid(row=3, column=0, padx=10, pady=10)

    nombre_archivo_entry = ttk.Entry(root, textvariable=nombre_archivo_var)
    nombre_archivo_entry.grid(row=3, column=1, padx=10, pady=10)

    # Botón de submit
    submit_button = ttk.Button(root, text="Enter", command=submit)
    submit_button.grid(row=4, column=0, columnspan=3, pady=20)

    # Vincular la tecla "Enter" al botón de submit
    root.bind('<Return>', lambda event: submit())

    # Iniciar el loop de la ventana
    root.mainloop()

    # Retorna los valores ingresados después de cerrar la ventana
    return dispositivo, tiempo_muestreo, tiempo_entre_muestreos, "data/"+nombre_archivo+".csv"

def graficar_csv(nombre_archivo):
    plt.close('all')
    # Inicializar listas para almacenar los datos
    tiempo = []
    temperatura1 = []
    temperatura2 = []
    temperatura3 = []
    temperatura4 = []

    # Leer el archivo CSV
    with open(nombre_archivo, mode='r') as archivo:
        lector_csv = csv.reader(archivo)
        next(lector_csv)  # Omitir el encabezado
        for fila in lector_csv:
            tiempo.append(float(fila[0]))
            temperatura1.append(float(fila[1]))
            temperatura2.append(float(fila[2]))
            temperatura3.append(float(fila[3]))
            temperatura4.append(float(fila[4]))

    # Crear la gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo, temperatura1, label="Temperatura 1", color="r")
    plt.plot(tiempo, temperatura2, label="Temperatura 2", color="g")
    plt.plot(tiempo, temperatura3, label="Temperatura 3", color="b")
    plt.plot(tiempo, temperatura4, label="Temperatura 4", color="y")

    # Configurar etiquetas y título
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Temperaturas vs Tiempo")
    plt.legend()

    # Guardar la gráfica como imagen
    nombre_imagen = nombre_archivo.replace('.csv', '.png')
    plt.savefig(nombre_imagen)


    # Mostrar la gráfica
    plt.show(block=True)


def leer_datos_csv(nombre_archivo):
    tiempos_csv = []
    T1_csv = []
    T2_csv = []
    T3_csv = []
    T4_csv = []

    with open(nombre_archivo, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Saltar encabezado
        for row in csv_reader:
            tiempos_csv.append(float(row[0]))
            T1_csv.append(float(row[1]))
            T2_csv.append(float(row[2]))
            T3_csv.append(float(row[3]))
            T4_csv.append(float(row[4]))

    return tiempos_csv, T1_csv, T2_csv, T3_csv, T4_csv



