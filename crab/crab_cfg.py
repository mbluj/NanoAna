from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
config = config()

config.General.requestName = 'Dummy' #MB: job depended
config.General.workArea = 'crab3_NanoAODSkim'
config.General.transferOutputs = True
#config.General.transferLogs = True #MB: needed?, default False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
# hadd nano will not be needed once nano tools are in cmssw
# MB: ln -s $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py .
# MB: my_keep_and_drop.txt defines slimming of in/out collections
config.JobType.inputFiles = ['crab_script.py', 'haddnano.py', 'my_keep_and_drop.txt']
config.JobType.sendPythonFolder = True

config.Data.inputDataset = 'Dummy' #MB: job depended: FIXME
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2 #MB: 1 for signal, 3 for DY, 10 for data?
config.Data.totalUnits = -1

#config.Data.outLFNDirBase = '/store/user/%s/NanoPost' % (
#    getUsernameFromSiteDB())
config.Data.outLFNDirBase = '/store/user/bluj/NanoAOD_MMSkim'
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoAOD_MMSkim'

#config.JobType.numCores = 4
#config.JobType.maxMemoryMB = 2500 # 2000 -> 2500 which is granted at T2s
#config.JobType.maxJobRuntimeMin = 2630 # 2630 min = ~44hrs (2xdefault)

config.Site.storageSite = "T2_PL_Swierk"

#config.Site.storageSite = "T2_CH_CERN"
# config.section_("User")
#config.User.voGroup = 'dcms'
