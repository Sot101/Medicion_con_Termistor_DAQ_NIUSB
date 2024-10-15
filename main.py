import nidaqmx # type: ignore
from nidaqmx.constants import TerminalConfiguration # type: ignore
from lib.funciones import *
from lib.datos_de_calibracion import dispositivo_1, dispositivo_2 # type: ignore
import matplotlib.pyplot as plt # type: ignore
import csv
import time

# Configuración canales DAQ
samples_per_channel = 10
sampling_rate = 1000

# Configuración filtro (0 < alpha <= 1)
alpha = 0.1

# Definir el número máximo de muestras que se mostrarán en la gráfica
max_samples = 50
decimales = 1 

# Inicializar listas para almacenar los datos de las 4 entradas
temp_filtrada = [None] * 4
y_data = [[] for _ in range(4)]
yf_data = [[] for _ in range(4)]

# Configura el modo interactivo de Matplotlib
plt.ion()

# Inicializar listas para almacenar los datos
x_data = []  # muestras

# Pedir datos al usuario
device, tiempo_muestreo, tiempo_entre_muestreos, nombre_archivo = obtener_datos()
# Variables para el dispositivo seleccionado
V1 = None
R1 = None
temp_offset = None
if device == "Dev1":
    V1 = dispositivo_1["V1"]
    R1 = dispositivo_1["R1"]
    temp_offset = dispositivo_1["temp_offset"]
    v_offset = dispositivo_1["v_offset"]
    k = dispositivo_1["k"]
elif device == "Dev2":
    V1 = dispositivo_2["V1"]
    R1 = dispositivo_2["R1"]
    temp_offset = dispositivo_2["temp_offset"]
    v_offset = dispositivo_2["v_offset"]
    k = dispositivo_2["k"]

# Primero, borrar el contenido del archivo (o crear uno nuevo si no existe)
with open(nombre_archivo, mode='w', newline='') as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["tiempo", "T1", "T2", "T3", "T4"])  # Encabezados

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan(device + "/ai0", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan(device + "/ai1", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan(device + "/ai2", terminal_config=TerminalConfiguration.RSE)
    task.ai_channels.add_ai_voltage_chan(device + "/ai3", terminal_config=TerminalConfiguration.RSE)
    task.timing.cfg_samp_clk_timing(rate=sampling_rate, samps_per_chan=samples_per_channel)

    # Crear la figura y los subplots fuera del bucle
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))  # Ajusta el tamaño de la figura si es necesario

    # Empezar tiempo de referencia
    t0 = time.time()

    i = 0
    while True:
        # Tiempo actual
        t = round(time.time() - t0, 1)
        x_data.append(t)
        voltages = task.read(number_of_samples_per_channel=1)

        min_temp = 25.0
        max_temp = 25.0

        for j in range(4):
            voltage = voltages[j][0] + v_offset[j]
            rterm = voltaje_a_resistencia(voltage, V1, R1, j) * k[j]
            temp = resistencia_a_temperatura(rterm, temp_offset, j)

            if temp_filtrada[j] is None:
                temp_filtrada[j] = temp
            else:
                temp_filtrada[j] = filtro_alpha(temp, temp_filtrada[j], alpha)

            y_data[j].append(temp)
            yf_data[j].append(temp_filtrada[j])

            # Actualizar el mínimo y máximo
            if temp_filtrada[j] < min_temp:
                min_temp = temp_filtrada[j]
            if temp_filtrada[j] > max_temp:
                max_temp = temp_filtrada[j]

        diff = max(yf_data[0][-1], yf_data[1][-1], yf_data[2][-1], yf_data[3][-1]) - min(
            yf_data[0][-1], yf_data[1][-1], yf_data[2][-1], yf_data[3][-1]
        )
        prom = (yf_data[0][-1] + yf_data[1][-1] + yf_data[2][-1] + yf_data[3][-1]) / 4

        print(f"Tiempo: {t}    -  T1[°C]: {yf_data[0][-1]:.2f}  - T2[°C]: {yf_data[1][-1]:.2f}  -  T3[°C]: {yf_data[2][-1]:.2f}  -  T4[°C]: {yf_data[3][-1]:.2f}  - Diff: {diff:.2f} °C   - Prom: {prom:.2f}")

        if len(x_data) > max_samples:
            x_data = x_data[-max_samples:]
            for j in range(4):
                y_data[j] = y_data[j][-max_samples:]
                yf_data[j] = yf_data[j][-max_samples:]

        # Actualizar la gráfica en tiempo real
        ax1.clear()
        ax1.plot(x_data, yf_data[0], c="r", label="T1")
        ax1.plot(x_data, yf_data[1], c="g", label="T2")
        ax1.plot(x_data, yf_data[2], c="b", label="T3")
        ax1.plot(x_data, yf_data[3], c="y", label="T4")

        # Añadir etiquetas para los últimos valores
        for j, color in enumerate(["r", "g", "b", "y"]):
            ax1.annotate(f'{yf_data[j][-1]:.2f}°C', 
                        xy=(x_data[-1], yf_data[j][-1]), 
                        xytext=(x_data[-1] + 0.5, yf_data[j][-1]),
                        textcoords='data', color=color, fontsize=9)


        ax1.set_xlabel("Tiempo [s]")
        ax1.set_ylabel("Temperatura (°C)")
        ax1.set_xlim(min(x_data), max(x_data))
        ax1.set_ylim(min_temp - 3, max_temp + 3)  # Añade un pequeño margen
        ax1.legend()
        ax1.set_title("Datos en tiempo real")

        # Leer los datos del CSV y actualizar la segunda gráfica
        tiempos_csv, T1_csv, T2_csv, T3_csv, T4_csv = leer_datos_csv(nombre_archivo)  # Función para leer datos del CSV
        ax2.clear()
        ax2.plot(tiempos_csv, T1_csv, c="r", label="T1 CSV")
        ax2.plot(tiempos_csv, T2_csv, c="g", label="T2 CSV")
        ax2.plot(tiempos_csv, T3_csv, c="b", label="T3 CSV")
        ax2.plot(tiempos_csv, T4_csv, c="y", label="T4 CSV")
        ax2.set_xlabel("Tiempo [s]")
        ax2.set_ylabel("Temperatura (°C)")
        ax2.legend()
        ax2.set_title("Datos guardados en CSV")

        plt.tight_layout()  # Ajusta los espacios entre subplots
        plt.pause(0.01)

        # Guardar en CSV
        if (t <= (tiempo_muestreo * 60) + 0.2):
            if t >= (tiempo_entre_muestreos * i):
                with open(nombre_archivo, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([t, round(yf_data[0][-1], decimales), round(yf_data[1][-1], decimales),
                                         round(yf_data[2][-1], decimales), round(yf_data[3][-1], decimales)])
                i += 1
        else:
            break

        time.sleep(0.1)

graficar_csv(nombre_archivo=nombre_archivo)
