#!/bin/bash

# Rutas principales para x86
CHECKPOINT_DIR="/nfs/home/ce/simciucd/checkpoints_x86"
BASE_OUTDIR="/nfs/home/ce/simciucd/prueba_ckpt/resultados_spec_x86_5seg_v3"

# Iterar sobre todas las carpetas que empiecen por "ckpt-"
for ckpt_path in ${CHECKPOINT_DIR}/ckpt-*; do

    # Extraer el nombre de la app (ej: de "ckpt-namd" nos quedamos con "namd")
    app=$(basename ${ckpt_path} | sed 's/ckpt-//')
    
    # Crear el directorio de salida específico para este benchmark
    output_dir="${BASE_OUTDIR}/${app}"
    mkdir -p ${output_dir}
    
    echo "Encolando: ${app}..."

    # Enviar el trabajo a Slurm usando un Here-Document
    sbatch <<EOF
#!/bin/bash
#SBATCH --partition=ce_200
#SBATCH --mem=6GB
#SBATCH --job-name=restore_x86_${app}
#SBATCH --output=${output_dir}/slurm-%j.out
#SBATCH --error=${output_dir}/slurm-%j.err

echo "Iniciando simulacion SPEC x86: ${app}"
echo "Directorio de checkpoint: ${ckpt_path}"
echo "Directorio de salida: ${output_dir}"

# Comando gem5 para x86
/nfs/home/ce/simciucd/gem5/build/X86/gem5.opt -re \\
  --outdir=${output_dir} \\
  /nfs/home/ce/simciucd/gem5/gem5-config-tools/configs/x86/v25/full_system/fs-restore-checkpoint-2.py \\
  --config Xeon4514Y \\
  --disk_image /nfs/home/ce/simciucd/full_system/x86-ubuntu-24.04-20250515 \\
  --ckpt_path ${ckpt_path} \\
  --mem_size 3 \\
  --num_cores 1 \\
  --works 3 \\
  --num_ticks 5000000000000

echo "Simulacion de ${app} finalizada."
EOF

done

echo "¡Todos los trabajos x86 han sido enviados a Slurm!"
