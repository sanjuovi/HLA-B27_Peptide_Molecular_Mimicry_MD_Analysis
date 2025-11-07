#!/bin/bash

# THIS SCRIPT WIL HELP TO PREPARE DOCKED FILE FOR MD IN GROMACS IT WILL START FROM CONVERTING THE DOCKED FORMATE FILE TO PDB (ADD PROTON, TIDYUP PBD FILE) THEN OPTIMIZED IT WITH AMBER PARAMETERS (TLEAP) AND CONVERT AMBER GENERATED .TOP AND .CRD FILES INTO .GRO AND .TOP FILE WHICH ARE DESIRED FORMATE FOR GROMACS. AFTER THIS ONE CAN GO FURTHER FOR EM, NVT,NPT AND MD ON GROMACS.

# Ask for the base name of the file (e.g., kp1)
echo "Enter the base name of your file (e.g., kp1):" # THIS LINE WILL ASK THE NAME OF BASE AND AS WE ENTER BASENAME, IT WILL START RUNNING THE SCRIP IN THAT PARTICULAR FILE (e.g., HERE IN kp1), IT WILL DO EVERYTHING BY ITSELF (MEANS ONE DONT NEED TO OPEN AND EDIT THIS SCRIPT WITH THEIR DESIRED FILE NAME)

read BASE_NAME 
# IT WILL DIRECTLY READ THE FILE WITH NAME (WATEVER WRITTEN IN BASENAME) FROM CURRENT FOLDER AND USE THAT FILE FOR WORK AND GIVE OUTPUTS WITH NAME INCLUDED BASENAME_DESIRED.FORMATE (e.g., IF MY BASE NAME IS KP1 IT WILL SELECT FILE KP1.cif FROM MY CURRENT FOLDER PROCESS AND GENERATE OUTPUT LIKEKP1_protonated.pdb KP1_amber.pdb etc., ONE JUST NEED TO TELL ONCE YOUR BASE NAME NO CHANGES IN FILE NAME REQUIRES FROM ANY OTHER PLACE)

# Step 1: Convert CIF to PDB
obabel ${BASE_NAME}.cif -O ${BASE_NAME}.pdb

# Step 1.1: Run propka for protonation
echo "Running propka3 on ${BASE_NAME}.pdb"
propka3 ${BASE_NAME}.pdb

# Step 2: Run pdb2pqr to add protons and create pka file
echo "Running pdb2pqr for ${BASE_NAME}.pdb"
pdb2pqr ${BASE_NAME}.pdb ${BASE_NAME}_protonated.pka --ff AMBER --with-ph 7 --pdb-output ${BASE_NAME}_protonated.pdb

# Step 3: Remove hydrogens safely using reduce
reduce -Trim ${BASE_NAME}_protonated.pdb > ${BASE_NAME}_noH.pdb

# Step 4: Run pdb4amber to prepare Amber PDB file
pdb4amber -i ${BASE_NAME}_noH.pdb -o ${BASE_NAME}_amber.pdb --reduce --dry

# Step 4.1: Assign chain A to residues 1–280, B to 281 onwards
awk 'BEGIN {chain="A"} 
     /^ATOM/ {
         resSeq = substr($0, 23, 4) + 0
         if (resSeq > 280) chain = "B"
         $0 = substr($0, 1, 21) chain substr($0, 23)
     } 
     {print}' ${BASE_NAME}_amber.pdb > ${BASE_NAME}_amber_chains.pdb

# Step 5: Create tleap input file
echo "Creating tleap input file"
cat <<EOT > tleap_${BASE_NAME}.in
source leaprc.protein.ff14SB
source leaprc.water.tip3p

loadAmberParams frcmod.ionsjc_tip3p

X = loadpdb ${BASE_NAME}_amber_chains.pdb
check X

solvatebox X TIP3PBOX 10

addions X Na+ 0
addions X Cl- 0

charge X

saveamberparm X ${BASE_NAME}_param.top ${BASE_NAME}_param.crd
savepdb X ${BASE_NAME}_param.pdb
quit
EOT

# Step 6: Run tleap
echo "Running tleap with input file tleap_${BASE_NAME}.in"
tleap -f tleap_${BASE_NAME}.in

# Step 7: Create ParmEd script for Amber → GROMACS conversion
echo "Generating ParmEd conversion script"
cat <<EOF > ParmEd_Amb2Gmx.py
import parmed as pmd
import os

BASE_NAME = "${BASE_NAME}"

# Remove old files if they exist
for ext in ['_topol.top', '_gro.gro']:
    fname = f"{BASE_NAME}{ext}"
    if os.path.exists(fname):
        os.remove(fname)

amber = pmd.load_file(f"{BASE_NAME}_param.top", f"{BASE_NAME}_param.crd")
amber.save(f"{BASE_NAME}_topol.top")
amber.save(f"{BASE_NAME}_gro.gro")
EOF

# Step 8: Run ParmEd
echo "Converting Amber to GROMACS format"
python ParmEd_Amb2Gmx.py