#!/bin/bash 
#SBATCH --job-name=pepid_correction
#SBATCH --time=4:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute-p1,compute-p2
#SBATCH --mem-per-cpu=3800MB
#SBATCH --account=Research-AS-BN
#SBATCH --output=/scratch/sanjusingh/Output/pepid_correction.outi
#SBATCH --error=/scratch/sanjusingh/md/pepid_md/pepid_correction.err  

# ========== CONFIGURATION ==========
set -e  # Stop script if any command fails
pep_id="kp1"   # <== Set your peptide ID here only

# Input file names (assumed fixed)
tpr="md.tpr"
xtc="md.xtc"
ndx="${pep_id}_index.ndx"  # Auto-adjusts to pep_id
# ===================================

# Activate GROMACS (conda or module, as needed)
# Uncomment one of these as per available system:

# source ~/gromacs_env.sh                # For manual source direct run on supercomputer
# conda activate gmx_env_name            # For conda users when running on laptop
module load 2024r1 openmpi gromacs             # If using environment modules in supercompute (here I am using this)

# === Step 1: Remove Periodic Boundary Conditions (PBC) and centering Protein ===
echo "Step 1.1: Removing PBC..."
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "$xtc" -o "${pep_id}_whole.xtc" -pbc whole -n "$ndx"
echo "Step 1.2: Removing jumps"
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_whole.xtc" -o "${pep_id}_nojump.xtc" -pbc nojump -n "$ndx"
echo "Step 1.3: Centering Protein"
printf '0\n0\n' | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_nojump.xtc" -o "${pep_id}_center.xtc" -center -n "$ndx"

rm "${pep_id}_whole.xtc"

# === Step 2: Skip 100 frames, then fit ===
echo "Step 2.1: Skipping every 100th frame..."
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_center.xtc" -o "${pep_id}_traj_100.xtc" -n "$ndx" -skip 100

echo "Step 2.2: Fitting (rot+trans) 100-skipped trajectory..."
printf "19\n0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_traj_100.xtc" -o "${pep_id}_100_ref.xtc" -n "$ndx" -fit rot+trans

# === Step 3: Further skip every 10th frame from the 100-skipped trajectory ===
echo "Step 3.1: Skipping every 10th from 100-skipped trajectory..."
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_100_ref.xtc" -o "${pep_id}_1000.xtc" -n "$ndx" -skip 10

echo "Step 3.2: Fitting (rot+trans) 1000-skipped trajectory..."
printf "19\n0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_1000.xtc" -o "${pep_id}_1000_ref.xtc" -n "$ndx" -fit rot+trans

# === DONE ===
echo "✅ All trajectory files processed for peptide ID: $pep_id"






