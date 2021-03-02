#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
import math
from copy import deepcopy
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#
# Module to preform a simple di-mu analysis
# M. Bluj, NCBJ, Poland
# January 2021
# 
class MMAnalysis(Module):
    def __init__(self, xsec=-1.):
        self.writeHistFile = True
        self.xsec = xsec #in pb

    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)

        self.genEventSumw = 0

        ## Book histograms
        # event counter
        self.h_count = ROOT.TH1F('hcount', 'efficiency', 10, 0, 10)
        cut_names = ['init', 'mu-trig', 'met-flags', 'good-PV', 'di-mu']
        ibin = 1
        for label in cut_names:
            self.h_count.GetXaxis().SetBinLabel(ibin,label)
            ibin += 1
        self.addObject(self.h_count)
        
        # variables of interest
        self.h_npv = ROOT.TH1F('npv', ';no. of vertices; Events', 80, 0, 80)
        self.addObject(self.h_npv)
        self.h_npv_raw = ROOT.TH1F('npv_raw', ';no. of vertices; Events', 80, 0, 80)
        self.addObject(self.h_npv_raw)

        self.h_pt1 = ROOT.TH1F('pt1', ';leading p_{T}^{#mu} (GeV); Events', 150, 0, 150)
        self.addObject(self.h_pt1)
        self.h_pt2 = ROOT.TH1F('pt2', ';trailing p_{T}^{#mu} (GeV); Events', 100, 0, 100)
        self.addObject(self.h_pt2)

        self.h_pt_mm = ROOT.TH1F('pt_mm', ';p_{T}^{#mu#mu} (GeV); Events', 200, 0, 200)
        self.addObject(self.h_pt_mm)
        self.h_m_mm = ROOT.TH1F('m_mm', ';m_{#mu#mu} (GeV); Events', 120, 40, 160)
        self.addObject(self.h_m_mm)

        self.h_ptm_mm = ROOT.TH2F('ptm_mm', ';p_{T}^{#mu#mu} (GeV); m_{#mu#mu} (GeV); Events', 50, 0, 200, 60, 40, 160)
        self.addObject(self.h_ptm_mm)

        

    def endJob(self):
        #Normalise histograms at the end to xsec/sumw

        # event count -> efficiency
        nbins = self.h_count.GetNbinsX()
        n_init = self.h_count.GetBinContent(1)
        for ibin in range(1,nbins+2):
            self.h_count.SetBinContent(ibin,self.h_count.GetBinContent(ibin)/n_init)
        Module.endJob(self)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.hasMuCorr = bool(inputTree.GetBranch("Muon_corrected_pt"))
        if not self.hasMuCorr:
            print "[MMAnalysis]: Input tree does not contain muon-pt corrections"
        self.hasPUWeight = bool(inputTree.GetBranch("puWeight"))

        runTree = inputFile.Get("Runs")
        self.doNorm = False
        self.doNorm = bool(runTree.GetBranch("genEventSumw")) and bool(inputTree.GetBranch("genWeight"))
        if self.doNorm:
            for entry in range(runTree.GetEntries()):
                runTree.GetEntry(entry)
                self.genEventSumw += runTree.genEventSumw

    def analyze(self, event):
        # some consts

        # collections of objects
        muons = Collection(event, "Muon") #sorted descending in pt
        
        # gen-weight
        genWeight = 1.
        if self.doNorm:
            genWeight = event.genWeight

        icut = 1
        self.h_count.AddBinContent(icut,genWeight)

        # check trigger bit(s)
        if not event.HLT_IsoMu24: return False
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)
        
        # MET flags to remove rare events with spurious MET caused by detector issues
        if not (event.Flag_goodVertices and
                event.Flag_globalSuperTightHalo2016Filter and
                event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and
                event.Flag_EcalDeadCellTriggerPrimitiveFilter and
                event.Flag_BadPFMuonFilter and
                event.Flag_ecalBadCalibFilterV2): return False #MB comment as for trigger
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        # require at least one good vertex
        if not (event.PV_npvsGood > 0): return False
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        # select events with at least 2 muons
        if not len(muons) >= 2: return False
        # proxy: do not loop over muons, simply check if 1st and 2nd fullfil amalysis requirements
        # 1st muon:
        mu1 = muons[0]
        if not (mu1.pt>26 #assume that this one triggers
                and abs(mu1.eta)<2.4
                and mu1.mediumId
                and mu1.pfRelIso04_all<0.25): return False
        # 2nd muon:
        mu2 = muons[1]
        if not (mu2.pt>20 #assume that this one triggers
                and abs(mu2.eta)<2.4
                and mu2.mediumId
                and mu2.pfRelIso04_all<0.25): return False
        # require opposite electroc charge
        if (mu2.charge*mu1.charge)>0: return False
        diMu = mu1.p4() + mu2.p4()

        # consider to apply a minimal pt(mm) cut

        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        # PU-weight
        puWeight = 1.
        if self.hasPUWeight:
            puWeight = event.puWeight
        self.h_npv_raw.Fill(event.PV_npvsGood,genWeight)
        self.h_npv.Fill(event.PV_npvsGood,puWeight*genWeight)

        # Fill histograms 
        self.h_pt1.Fill(mu1.pt,puWeight*genWeight)
        self.h_pt2.Fill(mu2.pt,puWeight*genWeight)
        self.h_pt_mm.Fill(diMu.Pt(),puWeight*genWeight)
        self.h_m_mm.Fill(diMu.M(),puWeight*genWeight)
        self.h_ptm_mm.Fill(diMu.Pt(),diMu.M(),puWeight*genWeight)

        # the End
        return True
