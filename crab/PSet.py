# this fake PSET is needed for local test and for crab to figure the output
# filename you do not need to edit it unless you want to do a local test using
# a different input file than the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANOSkim')
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(),
    # lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
    #'../../NanoAOD/test/lzma.root'  # you can change only this line
    '../../../samples/Nano/SingleMuon_Run2018A-02Apr2020-v1/7C2DFA75-CBFC-9341-9704-7F5E3A8EAE60.root'
    #'../../../samples/Nano/VBFHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8_RunIIAutumn18NanoAOD-102X_upgrade2018_realistic_v15-v1/161EC9D3-D848-5649-8E57-49E50BBD1D96.root'
]
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('nanoAOD_Skim.root'))
process.out = cms.EndPath(process.output)
