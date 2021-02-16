#!/usr/bin/env python

import os, re
import commands
import math
import urllib

from crab_cfg import *

dataset_name = {
    'ggH125': ['/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',1,-1], #sigma*Br=0.01057pb
    'ggH125_ext1': ['/GluGluHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',1,-1], #sigma*Br=0.01057pb
    'vbfH125': ['/VBFHToMuMu_M-125_TuneCP5_PSweights_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',1,-1], #sigma*Br=0.0008228pb
    'DYToLL': ['/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',3,-1], #sigma=6225.4pb (Warning! 5954pb for 2016 sample, i.e. ~4% less, due to different pdf??)
    'tt2l2nu': ['/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',3,-1], #sigma=86.61pb
    'ewk2l2j': ['/EWK_LLJJ_MLL-50_MJJ-120_TuneCH3_PSweights_13TeV-madgraph-herwig7_corrected/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',3,-1], #sigma=1.029pb, 2959970evts
    'Run2018A': ['/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD',5,-1], #315257-316996 14.03/fb
    'Run2018B': ['/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD',5,-1], #317080-319310 7.06/fb
    'Run2018C': ['/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD',5,-1], #319337-320655 6.89/fb
    'Run2018D': ['/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD',5,-1], #320500-325175 31.83/fb
}

def prepareCrabCfg(dataset,
                   filesPerJob=1,
                   storage_element='T2_PL_Swierk',
                   publish_data_suffix='test'):

    workdir = 'crab3_NanoAODSkim'
    config.Data.outputDatasetTag = 'RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21'
    if dataset.find('Run')!=-1:
        config.Data.outputDatasetTag = dataset+'-02Apr2020_NANOAOD'
        #FIXME: use different JSons for different years
        config.Data.lumiMask = 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
    elif dataset.find('ext')!=-1:
        config.Data.outputDatasetTag += '_'+dataset[dataset.find("ext"):]
    config.Data.outputDatasetTag += '_MMSkim'
    config.General.requestName = 'NanoAODv7_MMSkim_'+dataset
    if publish_data_suffix != '':
        workdir += '_'+publish_data_suffix
        config.Data.outputDatasetTag += '-'+publish_data_suffix
        config.General.requestName += '_'+publish_data_suffix
    config.General.workArea = workdir
    config.Data.inputDataset = dataset_name[dataset][0]

    ##Modify CRAB3 configuration
    config.JobType.psetName = 'PSet.py'
    config.Data.unitsPerJob  = filesPerJob
    config.Data.totalUnits = dataset_name[dataset][2]
    config.JobType.maxMemoryMB = 2500 # default 2000, 2500 is granted at T2
    config.JobType.maxJobRuntimeMin = 2750 # 2630 min = ~44hrs (2xdefault), 2750 - max allowed

    #config.Site.whitelist = ["T2_PL_Swierk"]
    #Set the following to run as cloase to PU samples as possible
    config.Data.ignoreLocality = False
    if config.Data.ignoreLocality:
        config.Site.whitelist = ['T2_PL_*','T2_DE_*']
        #config.Site.whitelist = ['T2_CH_CERN','T2_US_*','T1_US_*']
        #config.Site.whitelist = ['T2_BE_IIHE','T2_US_Caltech','T1_US_*']
        print "Ignore locality and run on these sites:", config.Site.whitelist
    config.Site.blacklist = ['T2_KR_*','T2_CN_*','T2_BR_*','T2_US_Florida','T2_US_UCSD','T2_US_Nebraska','T3_KR_*']

    out = open('crabNanoAODSkimTmp.py','w')
    out.write(config.pythonise_())
    out.close()
    os.system("crab submit -c crabNanoAODSkimTmp.py")
    os.system("rm crabNanoAODSkimTmp.py crabNanoAODSkimTmp.pyc")

#################

#for dataset in ['ggH125', 'ggH125_ext1', 'vbfH125', 'DYToLL']:
for dataset in [
        #'ggH125',
        #'ggH125_ext1',
        #'vbfH125',
        #'tt2l2nu',
        'ewk2l2j',
        #'DYToLL',
        #'Run2018A',
        #'Run2018B',
        #'Run2018C',
        #'Run2018D',
]:
    prepareCrabCfg(
        dataset=dataset,
        filesPerJob=dataset_name[dataset][1],
        storage_element='T2_PL_Swierk',
        publish_data_suffix='v4'
        )
