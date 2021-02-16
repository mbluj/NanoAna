#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *

# this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

#from PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *


selectionStr = "nMuon>1 && Muon_pt[0]>20 && Muon_pt[1]>10"
branchSel = "my_keep_and_drop.txt"
p = PostProcessor(".",
                  inputFiles(),
                  branchsel=branchSel,
                  outputbranchsel=branchSel,
                  cut=selectionStr,
                  #modules=[exampleModuleConstr()],
                  #modules=[],
                  modules=[
                      puWeight_2018(), #MB: PU weight with up and down variations, added to v4
                      muonScaleRes2018() #MB: muon scale corrections (Rochester), added to v2
                  ],
                  prefetch=True, #MB: copy input files locally, added to v2
                  provenance=True,
                  fwkJobReport=True,
                  jsonInput=runsAndLumis(),
                  haddFileName="nanoAOD_Skim.root"
              )
p.run()

print("DONE")
