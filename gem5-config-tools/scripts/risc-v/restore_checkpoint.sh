#!/bin/bash

# Rutas principales
CHECKPOINT_DIR="/nfs/shared/ce/gem5/de_felix_para_dragos/ckpts_fs_SPEC17/"
BASE_OUTDIR="/nfs/home/ce/simciucd/prueba_ckpt/resultados_spec_riscv_4seg_v2"

# Iterar sobre todas las carpetas que empiecen por "ckpt-"
for ckpt_path in ${CHECKPOINT_DIR}/ckpt-*; do

    # Extraer el nombre de la app (ej: de "ckpt-505.mcf_r" nos quedamos con "505.mcf_r")
    app=$(basename ${ckpt_path} | sed 's/ckpt-//')
    
    # Crear el directorio de salida específico para este benchmark
    output_dir="${BASE_OUTDIR}/${app}"
    mkdir -p ${output_dir}
    
    echo "Encolando: ${app}..."

    # Enviar el trabajo a Slurm usando un Here-Document
    sbatch <<EOF
#!/bin/bash
#SBATCH --partition=ce_200
#SBATCH --mem=8GB
#SBATCH --job-name=restore_spec_${app}
#SBATCH --output=${output_dir}/slurm-%j.out
#SBATCH --error=${output_dir}/slurm-%j.err


echo "Iniciando simulacion SPEC: ${app}"
echo "Directorio de checkpoint: ${ckpt_path}"
echo "Directorio de salida: ${output_dir}"

# Comando gem5 (sin --num_ticks para que corra hasta el final)
/nfs/home/ce/simciucd/gem5/build/RISCV/gem5.fast -re \\
  --outdir=${output_dir} \\
  /nfs/home/ce/simciucd/gem5/gem5-config-tools/configs/risc-v/v25_1/fs-restore-checkpoint.py \\
  --config BeagleV-Ahead \\
  --disk_image /nfs/shared/ce/gem5/de_felix_para_dragos/riscv-ubuntu-spec.img \\
  --ckpt_path ${ckpt_path} \\
  --mem_size 4 \\
  --num_cores 1 \\
  --num_ticks 4000000000000 \\
  --works 3

echo "Simulacion de ${app} finalizada."
EOF

done

echo "¡Todos los trabajos han sido enviados a Slurm!"
