#!/bin/bash

# Extraemos los nombres de los benchmarks automáticamente a partir de los archivos _run1
BENCHMARKS=$(ls papi_results_*_run1.csv | sed 's/papi_results_\(.*\)_run1.csv/\1/')

echo "Iniciando el cálculo de medias..."
echo "---------------------------------"

for benchmark in $BENCHMARKS; do
    echo "Calculando media para: $benchmark"
    
    awk -F';' -v OFS=';' '
    {
        # Guardamos el orden original de los eventos para no desordenar el CSV
        if (!visto[$5]++) {
            orden[++n] = $5
        }
        
        sum[$5] += $3        # Sumamos el valor (columna 3)
        count[$5]++          # Contamos las pasadas
        
        # Guardamos los metadatos de las otras columnas
        col1[$5] = $1 
        col2[$5] = $2
        col6[$5] = $6
    }
    END {
        # Imprimimos siguiendo el orden en que entraron
        for (i = 1; i <= n; i++) {
            evento = orden[i]
            # %.0f redondea a número entero sin notación científica
            printf "%s;%s;%.0f;;%s;%s\n", col1[evento], col2[evento], sum[evento]/count[evento], evento, col6[evento]
        }
    }' papi_results_${benchmark}_run*.csv > papi_results_${benchmark}_MEDIA.csv
    
done

echo "---------------------------------"
echo "✅ ¡Todas las medias han sido calculadas y guardadas!"
