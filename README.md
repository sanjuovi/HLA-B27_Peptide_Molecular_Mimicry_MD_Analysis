# HLA-B27 Molecular Mimicry Study — MD Simulation & Analysis

 	##  **Project Overview** 
This repository documents a complete computational workflow to identify **Klebsiella pneumoniae–derived peptides** that mimic a **human Annexin peptide (ANX)** in binding to **HLA-B27:05**, a Class-I MHC associated with autoimmune diseases such as **Ankylosing Spondylitis**.
The objective is to investigate whether microbial peptides can:
•	Bind HLA-B27 in a similar way as human peptides.
•	Form stable structural interactions.
•	Exhibit comparable post-MD behavior  

→ Supporting a potential **molecular mimicry mechanism**.

I focused on learning:
- Peptide generation and filtering
- HLA-B27 binding predictions
- Sequence similarity and mimicry search
- Peptide docking and molecular dynamics (MD)
- Trajectory analysis (RMSD, RMSF, SASA, PCA, MMGBSA
  
---

 	## Overview of the Pipeline
   
1. Generate peptides from human Annexin (anx) and full *K. pneumoniae* (kp)proteome  
2. HLA-B27 binding prediction using NetMHCpan  
3. Sequence similarity & mimic scoring  
4. Docking using AlphaFold-Multimer  
5. Structure optimization with AmberTools23 (tleap)  
6. Molecular Dynamics (MD) simulation in GROMACS 2024.
7. Post-process trajectories (centering, frame skipping, fitting)  
8. Post-MD analysis: RMSD, RMSF, Rg, SASA, H-bonds, MM-GBSA  
9. Identification of strongest microbial mimic

    ⚠️ **Note: ** The workflow was developed through trial and error, is **not fully automated**, and may **not be fully reproducible**. Scripts are shared to illustrate my learning process.
This workflow includes:

---
 	##  Repository Structure

hlab27-mimicry-study/
│── README.md
│── .gitignore
│
├── data/
│ ├── Human_pep_fasta/
│ ├── kleb_proteome/
│ └── processed/
│
├── docking/
│ ├── docking_anx_pep/
│ └── docking_kleb_pep/
│
├── md_simulations/
│ ├── tleap_input/
│ ├── amber_to_gromacs/
│ ├── gromacs_inputs/
│ └── scripts/
│
├── results/
│ ├── plots/
│ └── summary_table/
│
└── scripts/
├── pep_slicing/
└── pep_mimicking/

---

 	##  Materials and Methods

 	### Protein and Peptides:

o	**Target protein:** 
   
   HLA-B27:05 (Reference PDB structure with similar binding groove, used as model template)  
   
o	**Peptides studied:**

•	Human: ANX
•	Microbial: KP1, KP2, KP3

 	### Software / Tools:
   
•	Python 3.10+ / Biopython – peptide generation and sequence alignment
•	NetMHCpan – HLA-B27 binding predictions
•	BLAST / Bio.Align – sequence similarity search
•	AlphaFold / HADDOCK – peptide docking
•	AmberTools23 – preparation of peptide–HLA complexes
•	GROMACS 2024 – MD simulations and trajectory analysis
•	gmx_MMPBSA – binding free energy calculations

 	###  Peptide Generation
   
- Peptides (9–12-mers) were generated from Annexin and the full *K. pneumoniae* proteome.
- HLA-B27 anchor rules applied: **A/G/S/T – X – R/K – X – L/F/V/I/M/W**
- Tools: Biopython  
- Scripts: `generate_anx_peps_with_rule.py`, `generate_kleb_peps_with_rule.py`

 	###  Binding Prediction — NetMHCpan
  
- All peptides screened for HLA-B27 binding
- Strong binder (SB) and weak binder (WB) extracted

 	###  Mimicry Scoring
  
- Sequence similarity using Biopython (BLOSUM62)
- Scripts: `check_mimicry_kp_anxn.py`, `top5_mimicry_kp_anxn.py`
- Top Klebsiella mimics selected for modeling

 	###  Docking — AlphaFold-Multimer
  
- ANX + KP1/KP2/KP3 docked with HLA-B27
- Output: `.cif` model + confidence `.json`  
- Visual inspection done in PyMOL (binding orientation and position in HLA groove)

 	### Structure Optimization & MD Setup
  
- Minimization + solvation via AmberTools23 (tleap)
- Converted to GROMACS using ParmEd

 	### MD Simulation
  
- Software: **GROMACS 2023/2024**
- Water: TIP3P
- Ensemble: NVT → NPT → 1 µs production
- Conditions: 300 K, 1 bar, PME electrostatics, 2 fs timestep
- Hardware: **DelftBlue Supercomputer (TU Delft)**

Batch script: `md.sh`  
Trajectory correction: `md_correction.sh`

 	### Post-MD Analysis
   
Performed using GROMACS:
- RMSD
- RMSF
- Radius of gyration
- SASA
- Hydrogen bonds
- MM-GBSA free energy (gmx_MMPBSA)

Plots & summary tables stored in `/results/`.

---

 	##  Key Findings

- **ANX (human peptide)** formed the most stable and compact complex with HLA-B27.
- **KP1** showed the closest behavior to ANX in:
  ✅ RMSD  
  ✅ Rg  
  ✅ SASA  
  ✅ Hydrogen bonds  
  ✅ Binding energy
  
  → **Strongest mimic candidate**
- **KP2** showed high flexibility and weak binding
- **KP3** behaved intermediately

---

 	## Reproducibility Note
   
project was created for learning purposes. The scripts were developed through trial and error and are not fully automated, so the workflow may not be fully reproducible.The scripts are shared mainly to illustrate the approach and my learning process, not as a polished, production-ready workflow. 

---

 📌 ## Citation
 
If you use this repository, analysis pipeline, or scripts, please cite:
Singh S. (2025). GitHub Repository for HLA-B27 molecular mimicry MD analysis.
Link: https://github.com/singh-sanju/HLA-B27_Peptide_Molecular_Mimicry_MD_Analysis

---

🙏 ## Acknowledgments

This work was completed under the mentorship of
Dr Nikolina Šoštarić, Bionanoscience department, Delft University of Technology (TU Delft), Netherlands. I sincerely thank my PI for guidance, supervision, and the opportunity to pursue this research project.
Computational work, including molecular dynamics production runs and post-processing, was performed on the
DelftBlue Supercomputer at TU Delft, using GROMACS 2024 (module load GROMACS/2024r1-openmpi).
I would also like to thank colleagues and lab members at TU Delft for technical help, feedback, and support during this study.


