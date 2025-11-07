import parmed as pmd
import os
import glob

amber = pmd.load_file('pepid_param.top', 'pepid_param.crd')
amber.save('pepid_topol.top')
amber.save('pepid_gro.gro')



