
import os
import re
import statistics
import csv
from scipy import stats

# Configuración de la carpeta base
BASE_DIR = "."
CSV_OUTPUT = "resultados_estadisticas_perf.csv"


def extraer_valor_perf(texto, metrica):
    patron = rf"([\d,]+)\s+{re.escape(metrica)}"
    match = re.search(patron, texto)

    if match:
        valor_str = match.group(1).replace(",", "")
        return float(valor_str)

    return None


def analizar_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        contenido = f.read()

    # Contadores originales de perf
    instrucciones = extraer_valor_perf(contenido, "instructions")
    ciclos = extraer_valor_perf(contenido, "cycles")

    l1_loads = extraer_valor_perf(contenido, "L1-dcache-loads")
    l1_misses = extraer_valor_perf(contenido, "L1-dcache-load-misses")

    llc_loads = extraer_valor_perf(contenido, "LLC-loads")
    llc_misses = extraer_valor_perf(contenido, "LLC-load-misses")

    branches = extraer_valor_perf(contenido, "branches")
    branch_misses = extraer_valor_perf(contenido, "branch-misses")

    resultados = {
        'instructions': instrucciones,
        'cycles': ciclos,
        'l1_loads': l1_loads,
        'l1_misses': l1_misses,
        'llc_loads': llc_loads,
        'llc_misses': llc_misses,
        'branches': branches,
        'branch_misses': branch_misses
    }

    # IPC
    if instrucciones is not None and ciclos is not None and ciclos > 0:
        resultados['ipc'] = instrucciones / ciclos

    # Tasa de fallos L1
    if l1_loads is not None and l1_misses is not None and l1_loads > 0:
        resultados['l1_miss_rate'] = l1_misses / l1_loads

    # Tasa de fallos LLC/L3
    if llc_loads is not None and llc_misses is not None and llc_loads > 0:
        resultados['llc_miss_rate'] = llc_misses / llc_loads

    # Tasa de fallos de predicción de saltos
    if branches is not None and branch_misses is not None and branches > 0:
        resultados['branch_miss_rate'] = branch_misses / branches

    return resultados


def procesar_directorios():
    datos = {}

    for benchmark in os.listdir(BASE_DIR):
        ruta_bench = os.path.join(BASE_DIR, benchmark)

        if not os.path.isdir(ruta_bench) or not re.match(r"\d+\.\w+", benchmark):
            continue

        datos[benchmark] = {}

        for archivo in os.listdir(ruta_bench):
            if not archivo.endswith(".txt"):
                continue

            match_nombre = re.match(r"(\d+)_", archivo)

            if not match_nombre:
                continue

            duracion = match_nombre.group(1)
            ruta_archivo = os.path.join(ruta_bench, archivo)

            metricas = analizar_archivo(ruta_archivo)

            if duracion not in datos[benchmark]:
                datos[benchmark][duracion] = {
                    'instructions': [],
                    'cycles': [],
                    'ipc': [],
                    'l1_loads': [],
                    'l1_misses': [],
                    'l1_miss_rate': [],
                    'llc_loads': [],
                    'llc_misses': [],
                    'llc_miss_rate': [],
                    'branches': [],
                    'branch_misses': [],
                    'branch_miss_rate': []
                }

            for metrica, valor in metricas.items():
                if valor is not None:
                    datos[benchmark][duracion][metrica].append(valor)

    return datos


def formatear_excel_es(valor):
    """Convierte valores numéricos a coma decimal para Excel en español."""

    if isinstance(valor, (float, int)):
        return f"{valor:.6f}".replace(".", ",")

    return valor


def calcular_estadisticas(lista_valores):
    if not lista_valores:
        return "", ""

    try:
        geo_mean = statistics.geometric_mean(lista_valores)

        std_dev = (
            statistics.stdev(lista_valores)
            if len(lista_valores) > 1
            else 0.0
        )

        return geo_mean, std_dev

    except statistics.StatisticsError:
        return "Error", "Error"


def reporte_estadistico_y_csv(datos):

    lista_metricas = [
        'instructions',
        'cycles',
        'ipc',
        'l1_loads',
        'l1_misses',
        'l1_miss_rate',
        'llc_loads',
        'llc_misses',
        'llc_miss_rate',
        'branches',
        'branch_misses',
        'branch_miss_rate'
    ]

    cabeceras = ['Benchmark', 'Tiempo (s)', 'N']

    for metrica in lista_metricas:
        cabeceras.extend([
            f'{metrica}_Media_Geo',
            f'{metrica}_Desv_Est',
            f'{metrica}_p-value',
            f'{metrica}_Diferente?'
        ])

    filas_csv = []

    for bench, duraciones in sorted(datos.items()):

        t_tests = {}

        # Comparación entre ejecuciones de 5 y 40 segundos
        if '5' in duraciones and '40' in duraciones:

            for metrica in lista_metricas:

                val_5s = duraciones['5'].get(metrica, [])
                val_40s = duraciones['40'].get(metrica, [])

                if len(val_5s) > 1 and len(val_40s) > 1:

                    _, p_value = stats.ttest_ind(
                        val_5s,
                        val_40s,
                        equal_var=False
                    )

                    sig = (
                        "SI"
                        if p_value < 0.05
                        else "NO"
                    )

                    t_tests[metrica] = (p_value, sig)

                else:
                    t_tests[metrica] = ("", "")

        else:
            for metrica in lista_metricas:
                t_tests[metrica] = ("", "")

        # Generación de filas CSV
        for duracion in ['5', '40']:

            if duracion not in duraciones:
                continue

            valores_dict = duraciones[duracion]

            n = max(
                (len(v) for v in valores_dict.values()),
                default=0
            )

            fila = [bench, duracion, n]

            for metrica in lista_metricas:

                lista_valores = valores_dict.get(metrica, [])

                geo_mean, std_dev = calcular_estadisticas(
                    lista_valores
                )

                p_val, sig = t_tests.get(
                    metrica,
                    ("", "")
                )

                fila.extend([
                    formatear_excel_es(geo_mean),
                    formatear_excel_es(std_dev),
                    formatear_excel_es(p_val),
                    sig
                ])

            filas_csv.append(fila)

    # Exportación CSV para Excel en español
    with open(
        CSV_OUTPUT,
        mode='w',
        newline='',
        encoding='utf-8'
    ) as archivo_csv:

        writer = csv.writer(
            archivo_csv,
            delimiter=';'
        )

        writer.writerow(cabeceras)
        writer.writerows(filas_csv)

    print(
        f"¡Completado! Datos guardados en: "
        f"{os.path.abspath(CSV_OUTPUT)}"
    )


if __name__ == "__main__":

    datos_extraidos = procesar_directorios()

    reporte_estadistico_y_csv(datos_extraidos)

