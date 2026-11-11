#!/bin/bash
#SBATCH --partition=ce
#SBATCH --nodelist=ce209
#SBATCH --job-name=gem5_ckpt_riscv
#SBATCH --output=logs_riscv_mcf/slurm-riscv-%j.out
#SBATCH --error=logs_riscv_mcf/slurm-riscv-%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=10GB

echo "=========================================================="
echo "Iniciando trabajo de SLURM: Toma de checkpoints RISC-V"
echo "Nodo asignado: $SLURM_JOB_NODELIST"
echo "=========================================================="

# Ejecutar el script lanzador masivo de Python para RISC-V
# ¡OJO! Pon aquí la ruta exacta donde hayas guardado tu script lanzador modificado
python3 /nfs/home/ce/simciucd/gem5/gem5-config-tools/configs/risc-v/v25_1/riscv-generate-all-spec-checkpoints.py

echo "=========================================================="
echo "Trabajo finalizado."
echo "=========================================================="