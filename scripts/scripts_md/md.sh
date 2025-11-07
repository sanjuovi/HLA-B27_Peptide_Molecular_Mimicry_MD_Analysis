#!/bin/bash

#SBATCH --job-name=pepid_md
#SBATCH --time=48:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-task=1
#SBATCH --partition=gpu-v100
#SBATCH --mem-per-cpu=1GB
#SBATCH --account=Research-AS-BN
#SBATCH --output=/scratch/sanjusingh/Output/pepid_md.out
#SBATCH --mail-type=ALL

module load 2024r1 openmpi gromacs

# energy minimization
gmx grompp -f minim.mdp -c pepid_gro.gro -p pepid_topol.top -o em.tpr
gmx mdrun -v -deffnm em

# equilibration nvt
gmx grompp -f nvt.mdp -c em.gro -r em.gro -p pepid_topol.top -o nvt.tpr
gmx mdrun -v  -deffnm nvt

# equilibration npt
gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p pepid_topol.top -o npt.tpr
gmx mdrun -v  -deffnm npt

# production phase
gmx grompp -f md.mdp -c npt.tpr -t npt.cpt -p pepid_topol.top -o md.tpr
gmx mdrun -v  -deffnm md




