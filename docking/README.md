# Peptide-HLA-B27 Docking

This folder contains **docking results and model selection steps** used to identify the most promising human-microbial peptide pairs for molecular mimicry analysis:

- **docking_anx_pep/** - Docked model for Annexin peptides.
- **dockinh_kp_pep/** - Docked models for Klebsiella peptides (KP1, KP2, KP3).
- Each docking folder contains:
- pepid_model.cif` : Predicted 3D model of corresponding peptide-HLA complex.
- pepid_confidences.json` : Confidence information reported by AlphaFold server.


##  Purpose of Docking

Initially, multiple **Annexin (human self-peptides)** and **Klebsiella pneumoniae (kp microbial mimic peptides)** were identified from sequence similarity searches (via BLAST and BioAlign).  
Docking was then performed to **evaluate structural complementarity** between each peptide and **HLA**, helping to shortlist the most stable and biologically relevant peptide-HLA complexes.


## ⚙️ Tools and Methods

| **AlphaFold Multimer** - Docking was performed using **AlphaFold-Multimer** on the online server [🌐 https://alphafoldserver.com/].
| **HADDOCK 2.4** | (results not retrievable due to account expiration) 
| **PyMOL** | Docked structure inspection and figure preparation.


## Workflow Summary

1. **Input Preparation**
   - 1 Human Annexin peptides (anx) and corresponding 5 Klebsiella peptides (kp1, kp2, kp3, kp4, kp5) were used as inputs.
2. **Docking Execution**
   - Each peptide-HLA complex was modeled using AlphaFold and HADDOCK docking softwares.
3. **Model Selection**
   -for each peptide-HLA complex, ColabFold/AlphaFold-Multimer generated multiple models ranked by its internal scoring. The highest-ranked model with stable peptide placement in the groove was selected confidence color scale and ranking score. Visual inspection in PyMOL confirmed correct binding orientation, hydrogen bonding, and burial within the MHC pocket. These final models were used as input for AMBER optimization and MD.
 
4. **Final Selection**
   - From all models, **Annexin peptide (ANX)** and three Klebsiella peptides (**KP1, KP2, KP3**) were selected for complete molecular dynamics analysis.
   - These peptide-HLA complexes showed **highest confidence and most stable binding interfaces**.

##  HADDOCK Results Note

HADDOCK jobs were completed during the TU Delft project period, but the results could not be downloaded before project end and account deactivation.  
To reproduce:
- Run HADDOCK 2.4 (https://wenmr.science.uu.nl/haddock2.4)
- Use same peptide-HLA sequences as those used in AlphaFold runs.


##  Next Step

Selected docked complexes (ANX, KP1, KP2, KP3) were **converted to PDB**, solvated, and subjected to **1 μs Molecular Dynamics simulations** (see `/md_simulations/`).