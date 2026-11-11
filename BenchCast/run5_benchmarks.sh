#!/bin/bash

# Definimos la lista de todos los benchmarks en un array
BENCHMARKS=(
    "gcc.5"
    #"bwaves.1"
    "mcf.1"
    "cactuBSSN.1"
    "namd.1"
    "parest.1"
    "povray.1"
    "lbm.1"
    #"omnetpp.1"
    #"wrf.1"
    "xalanbmk.1"
    "x264.1"
    "blender.1"
    #"cam4.1"
    "deepsjeng.1"
    "leela.1"
    "nab.1"
    #"exchange2.1"
    #"fotonik3d.1"
    #"roms.1"
    "xz.3"
)

# Definimos la carpeta de destino y el número de ejecuciones
OUTPUT_DIR="papi_results/5-5"
NUM_RUNS=5

# Creamos la carpeta y sus subcarpetas si no existen
mkdir -p "$OUTPUT_DIR"

echo "Iniciando la ejecución de ${#BENCHMARKS[@]} benchmarks ($NUM_RUNS repeticiones cada uno)..."
echo "--------------------------------------------------------"

# Iteramos sobre cada benchmark de la lista
for benchmark in "${BENCHMARKS[@]}"; do
    
    echo "[$(date +'%H:%M:%S')] Empezando: $benchmark"
    
    # Bucle interno para ejecutar el benchmark 5 veces
    for i in $(seq 1 $NUM_RUNS); do
        echo "  -> Ejecución $i de $NUM_RUNS..."
        
        # Archivo de salida específico para esta iteración
        OUT_FILE="$OUTPUT_DIR/papi_results_${benchmark}_run${i}.csv"
        
        # Ejecutamos el comando
        ./bench_cast -c spec-cast -p 1 -l 1 -s 5 -v "$OUT_FILE" --SPEC "$benchmark"
        
        # Comprobamos si el comando terminó correctamente
        if [ $? -eq 0 ]; then
            echo "    ✅ Pasada $i finalizada con éxito."
        else
            echo "    ⚠️ Error o interrupción en la pasada $i. Continuando..."
        fi
    done
    
    
    echo "--------------------------------------------------------"

done

echo "[$(date +'%H:%M:%S')] ¡Todos los benchmarks han terminado!"
