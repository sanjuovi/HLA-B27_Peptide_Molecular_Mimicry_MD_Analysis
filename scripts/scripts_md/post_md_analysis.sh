#!/bin/bash
#SBATCH --job-name=anx_postmd
#SBATCH --time=12:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute-p1,compute-p2
#SBATCH --mem-per-cpu=3800MB
#SBATCH --account=Research-AS-BN
#SBATCH --output=/scratch/sanjusingh/Output/anx_post_analysis.out
#SBATCH --error=/scratch/sanjusingh/md/anx_re_md/anx_log_err/anx_post_analysis.err

# ========== CONFIGURATION ==========
set -e  # Stop script if any command fails
pep_id="anx"   # <== Set your peptide ID here only

tpr="md.tpr"
xtc="${pep_id}_center.xtc"   # Final corrected and fitted trajectory
ndx="${pep_id}_index.ndx"
# ===================================

# === Load GROMACS (choose the correct method for your system) ===
module load 2024r1 openmpi gromacs
# source ~/gromacs_env.sh

# === RMSD ===
echo "\n🔹 RMSD Calculation: To check structural deviation from initial conformation"
printf "19\n19\n" | gmx_mpi rms -s "$tpr" -f "$xtc" -o "${pep_id}_comp_rmsd.xvg" -n "$ndx"

echo "\n🔹 RMSD Calculation: To check structural deviation from initial conformation"
printf "17\n17\n" | gmx_mpi rms -s "$tpr" -f "$xtc" -o "${pep_id}_prot_rmsd.xvg" -n "$ndx"

echo "\n🔹 RMSD Calculation: To check structural deviation from initial conformation"
printf "18\n18\n" | gmx_mpi rms -s "$tpr" -f "$xtc" -o "${pep_id}_pep_rmsd.xvg" -n "$ndx"

printf "4\n4\n" | gmx_mpi rms -s "$tpr" -f "$xtc" -o "${pep_id}_backbone_rmsd.xvg" -n "$ndx"

# === RMSF ===
echo "\n🔹 RMSF Calculation: To observe flexibility of each residue"
gmx_mpi rmsf -s "$tpr" -f "$xtc" -o "${pep_id}_comp_rmsf.xvg" -res -n "$ndx" <<< "19"

echo "\n🔹 RMSF Calculation: To observe flexibility of each residue"
gmx_mpi rmsf -s "$tpr" -f "$xtc" -o "${pep_id}_pep_rmsf.xvg" -res -n "$ndx" <<< "18"

echo "\n🔹 RMSF Calculation: To observe flexibility of each residue"
gmx_mpi rmsf -s "$tpr" -f "$xtc" -o "${pep_id}_prot_rmsf.xvg" -res -n "$ndx" <<< "17"

gmx_mpi rmsf -s "$tpr" -f "$xtc" -o "${pep_id}_backbone_rmsf.xvg" -res -n "$ndx" <<< "4"

# === Radius of Gyration ===
echo "\n🔹 Radius of Gyration: To evaluate compactness"
gmx_mpi gyrate -s "$tpr" -f "$xtc" -o "${pep_id}_prot_rgyr.xvg" -n "$ndx" <<< "17"

echo "\n🔹 Radius of Gyration: To evaluate compactness"
gmx_mpi gyrate -s "$tpr" -f "$xtc" -o "${pep_id}_pep_rgyr.xvg" -n "$ndx" <<< "18"

echo "\n🔹 Radius of Gyration: To evaluate compactness"
gmx_mpi gyrate -s "$tpr" -f "$xtc" -o "${pep_id}_comp_rgyr.xvg" -n "$ndx" <<< "19"

gmx_mpi gyrate -s "$tpr" -f "$xtc" -o "${pep_id}_backbone_rgyr.xvg" -n "$ndx" <<< "4"
# === SASA (Solvent Accessible Surface Area) ===
echo "\n🔹 SASA Calculation: To study surface exposure"
gmx_mpi sasa -s "$tpr" -f "$xtc" -o "${pep_id}_prot_sasa.xvg" -n "$ndx" <<< "17"

gmx_mpi sasa -s "$tpr" -f "$xtc" -o "${pep_id}_pep_sasa.xvg" -n "$ndx" <<< "18"

gmx_mpi sasa -s "$tpr" -f "$xtc" -o "${pep_id}_backbone_sasa.xvg" -n "$ndx" <<< "4"

gmx_mpi sasa -s "$tpr" -f "$xtc" -o "${pep_id}_comp_sasa.xvg" -n "$ndx" <<< "19"
# === Hydrogen Bonds ===
echo "\n🔹 Hydrogen Bond Analysis: Peptide-protein interactions"
printf "17\n18\n" | gmx_mpi hbond -s "$tpr" -f "$xtc" -n "$ndx" -num "${pep_id}_hbnum.xvg" -dist "${pep_id}_hbdist.xvg"

# === Salt Bridges ===
echo "\n🔹 Salt Bridge Detection: Electrostatic interaction check"
printf "17\n18\n" | gmx_mpi mindist -s "$tpr" -f "$xtc" -n "$ndx" -od "${pep_id}_saltbridge.xvg" -group

echo "\n✅ All post-MD analyses completed for: $pep_id"









