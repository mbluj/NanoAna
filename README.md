# NanoAna-MMAna
# Simple di-mu analysis based on NanoAOD (v7)
#
# Installation recipe (CMSSW-based)
# 1. CMSSW
cmsrel CMSSW_10_6_20
cd CMSSW_10_6_20/src
cmsenv
#git cms-init

# 2. NanoAOD-tools (https://github.com/cms-nanoAOD/nanoAOD-tools)
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

# 3. NanoAna-mmAna
git clone https://github.com/mbluj/NanoAna-MMAna.git NanoAna/MMAna
scram b
