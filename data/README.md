# Data Folder
This directory contains all input and processed data used in the HLA-B27 peptide mimicry study.

- **Human_pep_fasta/** - FASTA sequences of selected human proteins (Annexin, Collagen, COMP).
- **kp_proteome/** -Complete Klebsiella pneumoniae proteome from UniProt.
- **processed/** - Generated and filtered peptide lists, NetMHCpan outputs, and similarity results (from BLAST and Bioalignment).

data/
│── human_pep_fasta
│── kp_proteome
└── processed/             
    ├── anx/
    ├── kp/
        └──kp_netMHCpan_results
    ├── similarity_results/