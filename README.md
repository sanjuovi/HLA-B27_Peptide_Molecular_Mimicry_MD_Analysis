# Project Overview
This repository documents a complete computational workflow to identify **Klebsiella pneumoniae–derived peptides** that mimic **human Annexin peptides** in binding to **HLA-B27:05** (PDB ID: 5txs).  
The goal is to investigate how microbial peptides might structurally and energetically resemble human peptides, potentially triggering **autoimmune T-cell activation** via molecular mimicry to identify pathogen-derived microbe peptides that potentially contributing to molecular mimicry-driven immune activation.

# HLA-B27_Peptide_Molecular_Mimicry_MD_Analysis
Molecular Dynamics simulations analysis of  human protein HLA-B27:05 to some peptide sequences associated with host protein Annexine and Gut Microbiota (Klebsiella pneumoniae) to identify microbe derived peptides that mimic host peptides in binding behavior to providing insights into molecular mimicry in autoimmune disease such as Ankylosing spondylitis.

##  Overview of the Pipeline

1. **Peptide Generation (Biopython):**  
   - Sliced peptides (9–12 mers) from *Annexin* (human) and *Klebsiella pneumoniae* proteome.  
   - Applied anchor residue rules for HLA-B27 (A/G/S/T–R/K–L/F/Y/M/V/W/I).  
   - Scripts used: `generate_peptides2.py`, `generate_all_peptides.py`, `kp_slice_pep.py`, `kp_9mer_pep.py`.

2. **Peptide Filtering and Splitting:**  
   - Filtered peptides by HLA-binding rules.  
   - Split large peptide files into smaller chunks for batch processing in NetMHCpan.  
   - Script used: `split_peptides.py`.

3. **MHC Binding Prediction (NetMHCpan):**  
   - Each peptide chunk was screened for HLA-B27 binding affinity using NetMHCpan (online server).  
   - Outputs contained predicted binding strength: **Strong Binder (SB)** or **Weak Binder (WB)**.

4. **Binder Extraction and Labeling:**  
   - Extracted SB/WB binders and separated them into labeled files.  
   - Scripts used:  
     - `separate_binding_pep.py`  
     - `separate_sbwb_all_pep.py`  
     - `extract_pep_lines.py`  
   - Generated:  
     - `strong_binders.txt`  
     - `weak_binders.txt`  
     - `annexin_peptides.txt`  
     - `kleb_peptides.txt`

5. **Sequence Similarity and Mimicry Search (Biopython / BLAST):**  
   - Performed **pairwise alignment** between Annexin and Klebsiella peptides to identify mimicry candidates.  
   - Scripts used:  
     - `check_mimicry_kp_anxn.py` (BLOSUM62 matrix for scoring)  
     - `top5_mimicry_kp_anxn.py` (selects top 5 mimics per Annexin peptide)  
   - Generated: `top_5_mimics_per_annexin.txt`

6. **Docking and Structural Preparation (HADDOCK / AlphaFold / AmberTools):**  
   - Selected the most similar Annexin and Klebsiella peptides for 3D modeling with **HLA-B27**.  
   - Refined complexes using **AmberTools23 tleap**.  
   - Converted AMBER parameters to GROMACS format using `parmed`:
     python script- "ParmEd_Amb2Gmx.py"

7. **Molecular Dynamics Simulations (GROMACS):**
   Each peptide–HLA complex molecular dynamics simulations were conducted on the **DelftBlue Supercomputer** at **TU Delft**, using **GROMACS 2023** compiled with MPI parallelization. The complexes was optimized using **AmberTools 23 (tleap)** and converted to GROMACS format via **ParmEd** (mentioned in section 6).  
The production MD runs were performed for **1 µs (1000000 ps)** in an **explicit TIP3P water box** with **periodic boundary conditions**.  
Simulation parameters included a **2 fs time step**, **V-rescale thermostat (300 K)**, and **Parrinello-Rahman barostat (1 bar)**.

Job submission and resource allocation on DelftBlue were managed through the batch script [`md.sh`](md_simulations/production_runs/md.sh):

This script executed the following simulation workflow:

Energy minimization

NVT equilibration

NPT equilibration

1 µs production run

### 🧩 Trajectory Correction and Processing

After completion of the 1 µs molecular dynamics simulations, **periodic boundary condition (PBC) corrections** and trajectory reductions were performed using the automated batch script [`md_correction.sh`](md_simulations/scripts/md_correction.sh).

This script standardizes all post-simulation trajectory corrections across peptide systems to remove periodic boundary artifacts (molecules crossing box edge), centerlise the protein–peptide complex in the simulation box and to generate reduced-size trajectories by skipping frames.it ensures proper visualization and fit trajectories for faster analysis such as RMSD/RMSF/SASA/PCA post-analysis in gromacs

#### Description of Steps:
1. **PBC Removal:**  
   Removes jumps caused by periodic boundaries using `-pbc whole` and `-pbc nojump`.
   ⚙️ Step 1: Remove Periodic Boundary Conditions (PBC) and Center the Protein
Command 1: Remove PBC (Whole Molecule Reconstruction)
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "$xtc" -o "${pep_id}_whole.xtc" -pbc whole -n "$ndx"


Purpose:

Reconstructs molecules that may have been broken across the simulation box due to periodic boundary conditions.

Ensures the entire complex (protein + peptide) is continuous.

Output file:
<pep_id>_whole.xtc — trajectory with complete molecules.

Command 2: Remove Jumps
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_whole.xtc" -o "${pep_id}_nojump.xtc" -pbc nojump -n "$ndx"


Purpose:

Removes large translational jumps caused when the molecule crosses the simulation box boundary.

Keeps the motion continuous and smooth for visualization and RMSD analysis.

Output file:
<pep_id>_nojump.xtc — trajectory without jumps.

Command 3: Center Protein
printf "0\n0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_nojump.xtc" -o "${pep_id}_center.xtc" -center -n "$ndx"


Purpose:

Moves the protein (or the entire complex) to the center of the simulation box.

Prevents drifting during visualization and RMSD/Rg calculations.

Output file:
<pep_id>_center.xtc — centered trajectory.

Command 4: Clean Temporary Files
rm "${pep_id}_whole.xtc"


Purpose:

Removes intermediate file to save storage space.

The _nojump.xtc and _center.xtc versions are sufficient for further steps.

⚙️ Step 2: Skip Frames and Fit Trajectory
Command 5: Skip Every 100th Frame
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_center.xtc" -o "${pep_id}_traj_100.xtc" -n "$ndx" -skip 100


Purpose:

Extracts every 100th frame to reduce the size of the trajectory (e.g., from 50,000 frames → 500).

Useful for quick RMSD or SASA analysis and smoother plotting.

Output file:
<pep_id>_traj_100.xtc — reduced trajectory (1 frame every 100 steps).

Command 6: Fit Reduced Trajectory
printf "19\n0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_traj_100.xtc" -o "${pep_id}_100_ref.xtc" -n "$ndx" -fit rot+trans


Purpose:

Aligns all frames to a reference structure by removing rotational and translational movement.

Keeps only internal fluctuations, ideal for RMSD/RMSF analysis.

Output file:
<pep_id>_100_ref.xtc — aligned reduced trajectory.

⚙️ Step 3: Create an Even Smaller (Every 1000th) Trajectory
Command 7: Skip Every 1000th Frame
printf "0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_100_ref.xtc" -o "${pep_id}_1000.xtc" -n "$ndx" -skip 10


Purpose:

Further compresses the already reduced trajectory (for extremely large runs like 1 µs).

Helpful for PCA or quick inspection in visualization tools.

Output file:
<pep_id>_1000.xtc — highly compressed trajectory.

Command 8: Fit Final Compressed Trajectory
printf "19\n0\n" | gmx_mpi trjconv -s "$tpr" -f "${pep_id}_1000.xtc" -o "${pep_id}_1000_ref.xtc" -n "$ndx" -fit rot+trans


Purpose:

Final alignment step to remove any remaining rotational/translational drift.

Produces the smallest possible, analysis-ready trajectory.

Output file:
<pep_id>_1000_ref.xtc — final, fully aligned, lightweight trajectory file.

✅ Final Result:

After running this script, you’ll have the following clean and usable trajectory files:

File Name	Description
<pep_id>_nojump.xtc	Trajectory without jumps
<pep_id>_center.xtc	Centered system
<pep_id>_traj_100.xtc	Every 100th frame
<pep_id>_100_ref.xtc	Fitted trajectory (for RMSD, SASA, etc.)
<pep_id>_1000_ref.xtc	Heavily reduced & fitted trajectory (for PCA)
🧾 Why this is important

Without these corrections:

Proteins appear broken or moving outside the box.

RMSD/RMSF values become noisy and unreliable.

Visualization in VMD/PyMOL is distorted.

PCA or MMGBSA analyses may fail due to discontinuities.

With this pipeline:

All trajectories are continuous, centered, fitted, and optimized for analysis.

3. **Centering:**  
   Centers the complex inside the simulation box.

4. **Frame Skipping:**  
   - Creates a new trajectory every **100th frame** (`-skip 100`)  
   - Further compresses every **1000th frame** for fast plotting.

5. **Fitting:**  
   Aligns trajectories using rotational and translational fitting (`-fit rot+trans`).

6. **Output:**  
   Generates processed trajectories:
   - `<pep_id>_center.xtc`  
   - `<pep_id>_traj_100.xtc`  
   - `<pep_id>_100_ref.xtc`  
   - `<pep_id>_1000_ref.xtc`During post-processing, PBC corrections were applied to trajectories using:









8. **Post-MD Analysis:**
Trajectory analyses were then performed for:
RMSD (gmx rms), RMSF (gmx rmsf), Radius of gyration (gmx gyrate). Solvent-accessible surface area (gmx sasa), Hydrogen bonds (gmx hbond), Saltbridge, PCA (gmx covar, gmx anaeig), MM-GBSA free-energy estimation (gmx_MMPBSA)
These analyses were carried out under explicit solvent, periodic boundary conditions, and standard physiological parameters, ensuring realistic peptide–HLA interactions.RMSD, RMSF, Rg, SASA, hydrogen bonds, salt bridges, PCA, MM-GBSA free energy.  
   - Scripts & commands used:
     - `gmx rms`, `gmx rmsf`, `gmx gyrate`, `gmx sasa`, `gmx hbond`, `gmx covar`, `gmx anaeig`
     - `gmx_MMPBSA` for binding energy.

9. **Comparative Analysis & Visualization:**  
   - Combined plots comparing all peptides (Annexin vs. Klebsiella).  
   - Identified **one Klebsiella peptide** with similar behavior to Annexin in RMSD, SASA, H-bonds, and binding energy — potential mimicry candidate.
## Repository Structure

hlab27-mimicry-study/
│
├── scripts/
│   ├── generate_peptides2.py
│   ├── generate_all_peptides.py
│   ├── kp_slice_pep.py
│   ├── kp_9mer_pep.py
│   ├── split_peptides.py
│   ├── separate_binding_pep.py
│   ├── separate_sbwb_all_pep.py
│   ├── extract_pep_lines.py
│   ├── check_mimicry_kp_anxn.py
│   ├── top5_mimicry_kp_anxn.py
│
├── md_simulations/
│   ├── tleap_input/
│   ├── amber_to_gromacs/
│   ├── gromacs_inputs/
│   ├── production_runs/
│   └── analysis_scripts/
│
├── results/
│   ├── RMSD/
│   ├── RMSF/
│   ├── SASA/
│   ├── Hbond/
│   ├── PCA/
│   └── MMGBSA/
│
└── docs/
    ├── pipeline_overview.pdf
    └── combined_plots_report.pdf

# ⚙️Tools and Dependencies
Tool	Purpose
Biopython	for Peptide slicing & sequence alignment
NetMHCpan	for HLA-B27 binding affinity prediction
BLAST / Bio.Align	for Sequence similarity search
AmberTools23	for tleap optimization of peptide–HLA complexes
GROMACS 2023	for MD simulation and post-analysis
gmx_MMPBSA	for Binding free energy estimation
Python 3.10+	for Script execution and automation

# How to Reproduce the Pipeline
1️⃣ Clone this repository
bash
Copy code
git clone https://github.com/<yourusername>/hlab27-mimicry-study.git
cd hlab27-mimicry-study
2️⃣ Create the environment
bash
Copy code
conda env create -f environment.yml
conda activate hlab27
3️⃣ Generate peptides
bash
python scripts/generate_peptides2.py
python scripts/kp_slice_pep.py
python scripts/kp_9mer_pep.py
4️⃣ Run mimicry comparison
bash
python scripts/check_mimicry_kp_anxn.py
python scripts/top5_mimicry_kp_anxn.py
5️⃣ Perform MD simulation and analysis
Use md_simulations/ folder for input/output of Amber & GROMACS runs.
Analysis commands include:

bash
gmx rms
gmx rmsf
gmx sasa
gmx gyrate
gmx covar
gmx anaeig

# Citation
If you use or adapt this workflow, please cite:

Singh S. et al. (2025)
Computational identification of Klebsiella pneumoniae peptides mimicking human Annexin peptides in HLA-B27 binding.
GitHub Repository: hlab27-mimicry-study

## Methods Summary

Protein Target: HLA-B27:05 (PDB: 5txs)
  - Peptides Studied:
     Host peptide  - Annexine (Anx 1:
     Gut Microbe - Klebsiella pneumoniae: KLEB12, KLEB5, KLEB6, KLEB4, KLEB7
  - Simulation Software: GROMACS 2024
  - Force Field: ff14SB
  - Solvent Model: TIP3P
  - Simulation Length: 1 μs per peptide complex
  - Parameters: 300 K, 1 bar, PME electrostatics, LINCS constraints


