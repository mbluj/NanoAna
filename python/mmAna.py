#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from NanoAna.MMAna.modules.MMAnalysis import MMAnalysis
#
from importlib import import_module
import os
import sys
import glob
#
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

### Input samples
dataDir = '/mnt/shared/slc7_sf/akalinow/CMS/Data/NanoAOD_MMSkim/'
samples = {
    # name " [files, x-sec-in-pb]
    'ggH125_tst': [dataDir+'/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_1.root',0.01057], #sigma*Br=0.01057pb
    'ggH125': [dataDir+'/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4*/*/0000/nanoAOD_Skim_*.root',0.01057], #sigma*Br=0.01057pb
    'vbfH125': [dataDir+'/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_*.root',0.0008228], #sigma*Br=0.0008228pb
    'DYToLL_tst': [dataDir+'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_10.root',6225.4], #sigma=6225.4pb
    'DYToLL': [dataDir+'/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_*.root',6225.4], #sigma=6225.4pb
    'ewk2l2j': [dataDir+'/EWK_LLJJ_MLL-50_MJJ-120_TuneCH3_PSweights_13TeV-madgraph-herwig7_corrected/nanoAOD_Skim_*.root',1.029], #sigma=1.029pb
    'tt2l2nu': [dataDir+'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_*.root',86.61], #sigma=86.61pb
    'tt2l2nu_tst': [dataDir+'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_MMSkim-v4/*/0000/nanoAOD_Skim_1.root',86.61], #sigma=86.61pb
    'ttsemil': [dataDir+'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/nanoAOD_Skim_*.root',358.57], #sigma=358.57pb, 100790000
    'atop_tch': [dataDir+'/ST_t-channel_antitop_5f_TuneCP5_13TeV-powheg-pythia8/nanoAOD_Skim_*.root',80.95], #sigma=80.95pb, 3955024
    'top_tch': [dataDir+'/ST_t-channel_top_5f_TuneCP5_13TeV-powheg-pythia8/nanoAOD_Skim_*.root',136.02], #sigma=136.02pb, 5903676
    'tWatop_ext1': [dataDir+'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_ext1/nanoAOD_Skim_*.root',39.5], #sigma=39.5pb, 7527000
    'tWtop_ext1': [dataDir+'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8_ext1/nanoAOD_Skim_*.root',39.5], #sigma=39.5pb, 9598000
    't_sch': [dataDir+'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/nanoAOD_Skim_*.root',3.40], #sigma=3.40pb, 19965000
    'ww2l2nu': [dataDir+'/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/nanoAOD_Skim_*.root',12.178], #7758900
    'wz3l1nu_ext1': [dataDir+'/WZTo3LNu_TuneCP5_13TeV-powheg-pythia8/nanoAOD_Skim_*.root',4.658], #1976600
    'wz2l2q': [dataDir+'/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/nanoAOD_Skim_*.root',6.321], #28193648 !negative w
    'zz2l2nu_ext1': [dataDir+'/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/nanoAOD_Skim_*.root',0.601], #8382600
    'zz2l2q': [dataDir+'/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/nanoAOD_Skim_*.root',3.696], #27900469 !negative w
    'zz4l_ext1': [dataDir+'/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/nanoAOD_Skim_*.root',1.325], #6689900
    'Run2018A': [dataDir+'/SingleMuon/Run2018A-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_*.root',-1], #315257-316996 14.03/fb
    'Run2018A_tst': [dataDir+'/SingleMuon/Run2018A-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_1.root',-1], #315257-316996 14.03/fb
    'Run2018B': [dataDir+'/SingleMuon/Run2018B-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_*.root',-1], #317080-319310 7.06/fb
    'Run2018C': [dataDir+'/SingleMuon/Run2018C-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_*.root',-1], #319337-320655 6.89/fb
    'Run2018D': [dataDir+'/SingleMuon/Run2018D-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_*.root',-1], #319337-320655 6.89/fb
    'Run2018All': [dataDir+'/SingleMuon/Run2018?-02Apr2020_NANOAOD_MMSkim-v3/*/0000/nanoAOD_Skim_*.root',-1], #59.83/fb
}

###
preselection ="" #MB: "HLT_IsoMu24" Trigger requirement moved into analyser for event counting and normalisation (anyway higly efficient on top of current preselection) Warning! preselection can affect automated normalisation!
#preselection ="HLT_IsoMu24 && nMuon>1 && Muon_pt[0]>26 && Muon_pt[1]>20"
#branchsel = None #no branch selection at input/output
branchsel = 'keep_and_drop_input_mm.txt' #file with branches selection to speedup processing
outDir="histoFiles"

### Process samples
for dataset in [
    ##'ggH125_tst',
    ##'tt2l2nu_tst',
    ##'DYToLL_tst',
    ##'Run2018A_tst',
    'ggH125',
    'vbfH125',
    'tt2l2nu',
    'ttsemil',
    'atop_tch',
    'top_tch',
    'tWatop_ext1',
    'tWtop_ext1',
    't_sch',
    'ww2l2nu',
    'wz3l1nu_ext1',
    'wz2l2q',
    'zz2l2nu_ext1',
    'zz2l2q',
    'zz4l_ext1',
    'ewk2l2j',
    'DYToLL',
    'Run2018All',
    ##'Run2018A',
    ##'Run2018B',
    ##'Run2018C',
    ##'Run2018D',
    ]:
    print 'Processing', dataset
    files = glob.glob(samples[dataset][0])
    histFileName = outDir+'/histOut_'+dataset+'.root'
    p = PostProcessor(
        outDir, files, cut=preselection, branchsel=branchsel, 
        modules=[
            MMAnalysis(xsec=samples[dataset][1]) #mm-analysis module
            ], 
        noOut=True, 
        histFileName=histFileName, histDirName="mmPlots")
    p.run()
