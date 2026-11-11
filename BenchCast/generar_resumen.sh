#!/bin/bash

OUTPUT_CSV="resumen_total_benchmarks.csv"

# 1. Creamos la cabecera del CSV (usamos punto y coma para que Excel lo separe automáticamente en columnas)
echo "Aplicacion;CYCLES;INSTRUCTIONS;BRANCHES;BRANCH-MISSES;L1-DCACHE-LOADS;L1-DCACHE-LOAD-MISSES;LLC-LOADS;LLC-LOAD-MISSES" > "$OUTPUT_CSV"

echo "Agrupando los ficheros _MEDIA en $OUTPUT_CSV..."

# 2. Recorremos todos los archivos que terminen en _MEDIA.csv
for file in papi_results_*_MEDIA.csv; do
    
    # Nos aseguramos de que el archivo existe para evitar errores si no hay coincidencias
    if [ ! -f "$file" ]; then
        continue
    fi
    
    # Obtenemos el nombre del benchmark (ej: gcc.5)
    benchmark=$(echo "$file" | sed 's/papi_results_\(.*\)_MEDIA.csv/\1/')
    
    # 3. Usamos awk para leer las filas de ese benchmark y transformarlas en columnas
    awk -F';' -v app="$benchmark" '
    {
        # Guardamos el valor (columna 3) usando el nombre del evento (columna 5) como clave
        stats[$5] = $3
    }
    END {
        # Imprimimos la fila completa con todos los datos ordenados
        printf "%s;%s;%s;%s;%s;%s;%s;%s;%s\n", app, 
            stats["perf::CYCLES"], 
            stats["perf::INSTRUCTIONS"], 
            stats["perf::BRANCHES"], 
            stats["perf::BRANCH-MISSES"], 
            stats["perf::L1-DCACHE-LOADS"], 
            stats["perf::L1-DCACHE-LOAD-MISSES"], 
            stats["perf::LLC-LOADS"], 
            stats["perf::LLC-LOAD-MISSES"]
    }' "$file" >> "$OUTPUT_CSV"
    
done

echo "✅ Proceso completado. Todos los datos están en: $OUTPUT_CSV"
