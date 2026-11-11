#!/usr/bin/env python3
import os
import glob
import math
import statistics

# Valor de la t de Student para 95% de confianza y 4 grados de libertad (n-1, donde n=5)
T_STUDENT = 2.776 
NUM_RUNS = 5

def leer_fichero(filepath):
    """Lee un fichero de PAPI y devuelve un diccionario con los valores de los eventos"""
    eventos = {}
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        for linea in f:
            if not linea.strip():
                continue
            partes = linea.strip().split(';')
            if len(partes) >= 5:
                valor = float(partes[2])
                nombre_evento = partes[4]
                eventos[nombre_evento] = valor
    return eventos

def calcular_media_geometrica(datos):
    """Calcula la media geométrica de una lista de valores"""
    if not datos or any(x <= 0 for x in datos):
        return 0.0 # Si hay ceros, la media geométrica se anula
    # Fórmula: e^( sum(ln(x)) / n )
    return math.exp(sum(math.log(x) for x in datos) / len(datos))

# Buscar todos los benchmarks a partir de los archivos run1
archivos_run1 = glob.glob('papi_results_*_run1.csv')
benchmarks = [f.replace('papi_results_', '').replace('_run1.csv', '') for f in archivos_run1]

csv_salida = "metricas_finales_estadistica.csv"

with open(csv_salida, 'w') as f_out:
    # Cabecera del CSV
    cabecera = [
        "Aplicacion", 
        "IPC_GeoMean", "IPC_StdDev", "IPC_Error_95%(t)",
        "Branch_MR_GeoMean", "Branch_MR_StdDev", "Branch_MR_Error_95%",
        "L1_MR_GeoMean", "L1_MR_StdDev", "L1_MR_Error_95%",
        "LLC_MR_GeoMean", "LLC_MR_StdDev", "LLC_MR_Error_95%"
    ]
    f_out.write(";".join(cabecera) + "\n")

    for bench in benchmarks:
        ipc_list = []
        bmr_list = []
        l1mr_list = []
        llcmr_list = []

        for i in range(1, NUM_RUNS + 1):
            filepath = f"papi_results_{bench}_run{i}.csv"
            datos = leer_fichero(filepath)
            
            if datos:
                # 1. Calcular IPC = Instrucciones / Ciclos
                if "perf::INSTRUCTIONS" in datos and "perf::CYCLES" in datos and datos["perf::CYCLES"] > 0:
                    ipc = datos["perf::INSTRUCTIONS"] / datos["perf::CYCLES"]
                    ipc_list.append(ipc)
                
                # 2. Calcular Branch Miss Rate = Branch Misses / Branches
                if "perf::BRANCH-MISSES" in datos and "perf::BRANCHES" in datos and datos["perf::BRANCHES"] > 0:
                    bmr = datos["perf::BRANCH-MISSES"] / datos["perf::BRANCHES"]
                    bmr_list.append(bmr)

                # 3. Calcular L1 Miss Rate = L1 Misses / L1 Loads
                if "perf::L1-DCACHE-LOAD-MISSES" in datos and "perf::L1-DCACHE-LOADS" in datos and datos["perf::L1-DCACHE-LOADS"] > 0:
                    l1_mr = datos["perf::L1-DCACHE-LOAD-MISSES"] / datos["perf::L1-DCACHE-LOADS"]
                    l1mr_list.append(l1_mr)

                # 4. Calcular LLC Miss Rate = LLC Misses / LLC Loads
                if "perf::LLC-LOAD-MISSES" in datos and "perf::LLC-LOADS" in datos and datos["perf::LLC-LOADS"] > 0:
                    llc_mr = datos["perf::LLC-LOAD-MISSES"] / datos["perf::LLC-LOADS"]
                    llcmr_list.append(llc_mr)

        # Si tenemos las 5 pasadas calculamos estadística
        if len(ipc_list) > 1:
            def procesar_metrica(lista):
                geo_mean = calcular_media_geometrica(lista)
                std_dev = statistics.stdev(lista)
                # Fórmula t de Student: (t * s) / sqrt(n)
                margen_error = (T_STUDENT * std_dev) / math.sqrt(len(lista))
                return geo_mean, std_dev, margen_error

            ipc_geo, ipc_std, ipc_err = procesar_metrica(ipc_list)
            bmr_geo, bmr_std, bmr_err = procesar_metrica(bmr_list)
            l1_geo, l1_std, l1_err = procesar_metrica(l1mr_list)
            llc_geo, llc_std, llc_err = procesar_metrica(llcmr_list)

            # Escribir la línea formateada en el CSV
            linea = f"{bench};{ipc_geo:.6f};{ipc_std:.6f};{ipc_err:.6f};" \
                    f"{bmr_geo:.6f};{bmr_std:.6f};{bmr_err:.6f};" \
                    f"{l1_geo:.6f};{l1_std:.6f};{l1_err:.6f};" \
                    f"{llc_geo:.6f};{llc_std:.6f};{llc_err:.6f}\n"
            f_out.write(linea.replace('.', ',')) # Cambiamos puntos por comas por si tu Excel está en español

print(f"✅ Proceso completado. Resultados en: {csv_salida}")
