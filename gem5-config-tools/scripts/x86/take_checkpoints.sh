#!/bin/bash
#SBATCH --partition=ce_200
#SBATCH --job-name=gem5_checkpoints
#SBATCH --output=ckpts-x86-logs/slurm-%j.out
#SBATCH --error=ckpts-x86-logs/slurm-%j.err
#SBATCH --cpus-per-task=16
#SBATCH --mem=40GB

echo "=========================================================="
echo "Iniciando trabajo de SLURM: Toma de checkpoints en paralelo"
echo "Nodo asignado: $SLURM_JOB_NODELIST"
echo "=========================================================="

# Ejecutar tu script de automatización usando el Python del sistema (que es el 3.13)
python3 /nfs/home/ce/simciucd/gem5/gem5-config-tools/configs/x86/v25/full_system/generate-all-specs-checkpoints.py

echo "=========================================================="
echo "Trabajo finalizado."
echo "=========================================================="
