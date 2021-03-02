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
        self.isDY = 0
        if histFile!=None and histFile.GetName().find('DY')>-1:
            self.isDY = 1
            if histFile.GetName().find('NLO')>-1:
                self.isDY = 2

        self.h_count = ROOT.TH1F('hcount', 'efficiency', 10, 0, 10)
        cut_names = ['init', 'mu-trig', 'met-flags', 'good-PV', 'di-mu', 'trig-match', 'lept-veto', 'b-veto']
        ibin = 1
        for label in cut_names:
            self.h_count.GetXaxis().SetBinLabel(ibin,label)
            ibin += 1
        self.addObject(self.h_count)        
        
        self.h_npv = ROOT.TH1F('npv', ';no. of vertices; Events', 80, 0, 80)
        self.addObject(self.h_npv)
        self.h_npv_raw = ROOT.TH1F('npv_raw', ';no. of vertices w/o pileup weight; Events', 80, 0, 80)
        self.addObject(self.h_npv_raw)
        self.h_pt1 = ROOT.TH1F('pt1', ';leading p_{T}^{#mu} (GeV); Events', 150, 0, 150)
        self.addObject(self.h_pt1)
        self.h_pt2 = ROOT.TH1F('pt2', ';trailing p_{T}^{#mu} (GeV); Events', 100, 0, 100)
        self.addObject(self.h_pt2)
        self.h_ptn = ROOT.TH1F('ptn', ';negative p_{T}^{#mu} (GeV); Events', 150, 0, 150)
        self.addObject(self.h_ptn)
        self.h_ptp = ROOT.TH1F('ptp', ';positive p_{T}^{#mu} (GeV); Events', 150, 0, 150)
        self.addObject(self.h_ptp)
        self.h_pt1_corr = ROOT.TH1F('pt1_corr', ';leading p_{T}^{#mu} w/ corrections (GeV); Events', 150, 0, 150)
        self.addObject(self.h_pt1_corr)
        self.h_pt2_corr = ROOT.TH1F('pt2_corr', ';trailing p_{T}^{#mu} w/ corrections (GeV); Events', 100, 0, 100)
        self.addObject(self.h_pt2_corr)
        self.h_pt_mm = ROOT.TH1F('pt_mm', ';p_{T}^{#mu#mu} (GeV); Events', 200, 0, 200)
        self.addObject(self.h_pt_mm)
        self.h_m_mm = ROOT.TH1F('m_mm', ';m_{#mu#mu} (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm)
        self.h_pt_mm_wb = ROOT.TH1F('pt_mm_wb', ';p_{T}^{#mu#mu} w/o b-veto (GeV); Events', 200, 0, 200)
        self.addObject(self.h_pt_mm_wb)
        self.h_m_mm_wb = ROOT.TH1F('m_mm_wb', ';m_{#mu#mu} w/o b-veto (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm_wb)
        self.h_pt_mm_corr = ROOT.TH1F('pt_mm_corr', ';p_{T}^{#mu#mu} w/ corrections (GeV); Events', 200, 0, 200)
        self.addObject(self.h_pt_mm_corr)
        self.h_m_mm_corr = ROOT.TH1F('m_mm_corr', ';m_{#mu#mu} w/ corrections (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm_corr)
        self.h_pt_mm_fsr = ROOT.TH1F('pt_mm_fsr', ';p_{T}^{#mu#mu} w/ FSR (GeV); Events', 200, 0, 200)
        self.addObject(self.h_pt_mm_fsr)
        self.h_m_mm_fsr = ROOT.TH1F('m_mm_fsr', ';m_{#mu#mu} w/ FSR (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm_fsr)
        self.h_m_mm_bst = ROOT.TH1F('m_mm_bst', 'Boosted: p_{T}^{#mu#mu}> 130 GeV;m_{#mu#mu} w/ FSR (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm_bst)
        self.h_m_mm_vbf = ROOT.TH1F('m_mm_vbf', 'VBF: m_{jj}> 400 GeV, |#eta_{jj}| > 2.5;m_{#mu#mu} w/ FSR (GeV); Events', 100, 60, 160)
        self.addObject(self.h_m_mm_vbf)
        # pt(mm) for reweight
        self.h_pt_mm_z = ROOT.TH1F('pt_mm_z', '70 < m_{#mu#mu}<110 GeV;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_z)
        self.h_pt_mm_zw = ROOT.TH1F('pt_mm_zw', '70 < m_{#mu#mu}<110 GeV;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_zw)
        self.h_pt_mm_0j = ROOT.TH1F('pt_mm_0j', '70 < m_{#mu#mu}<110 GeV, 0-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_0j)
        self.h_pt_mm_0jw = ROOT.TH1F('pt_mm_0jw', '70 < m_{#mu#mu}<110 GeV, 0-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_0jw)
        self.h_pt_mm_1j = ROOT.TH1F('pt_mm_1j', '70 < m_{#mu#mu}<110 GeV, 1-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_1j)
        self.h_pt_mm_1jw = ROOT.TH1F('pt_mm_1jw', '70 < m_{#mu#mu}<110 GeV, 1-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_1jw)
        self.h_pt_mm_2j = ROOT.TH1F('pt_mm_2j', '70 < m_{#mu#mu}<110 GeV, #geq2-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_2j)
        self.h_pt_mm_2jw = ROOT.TH1F('pt_mm_2jw', '70 < m_{#mu#mu}<110 GeV, #geq2-jet;p_{T}^{#mu#mu} w/ FSR (GeV); Events', 50, 0, 200)
        self.addObject(self.h_pt_mm_2jw)
        #additional leptons
        self.h_nlep = ROOT.TH1F('nlep', ';no. of additional lepton; Events', 3, 0, 3)
        self.addObject(self.h_nlep)
        #jet variables
        self.h_ptj1 = ROOT.TH1F('ptj1', ';leading p_{T}^{j} (GeV); Events', 60, 0, 300)
        self.addObject(self.h_ptj1)
        self.h_ptj2 = ROOT.TH1F('ptj2', ';trailing p_{T}^{j} (GeV); Events', 60, 0, 300)
        self.addObject(self.h_ptj2)
        self.h_m_jj = ROOT.TH1F('m_jj', ';m_{jj} (GeV); Events', 150, 0, 750)
        self.addObject(self.h_m_jj)
        self.h_deta_jj = ROOT.TH1F('deta_jj', ';#Delta#eta_{jj}; Events', 80, --10,10)
        self.addObject(self.h_deta_jj)
        self.h_njet = ROOT.TH1F('njet', ';no. of jets; Events', 10, 0, 10)
        self.addObject(self.h_njet)
        self.h_njet_z = ROOT.TH1F('njet_z', '70 < m_{#mu#mu}<110 GeV;no. of jets; Events', 10, 0, 10)
        self.addObject(self.h_njet_z)
        self.h_njet_zw = ROOT.TH1F('njet_zw', '70 < m_{#mu#mu}<110 GeV;no. of jets; Events', 10, 0, 10)
        self.addObject(self.h_njet_zw)
        self.h_nbjet = ROOT.TH1F('nbjet', ';no. of loosely b-tagged jets (Loose WP) ; Events', 5, 0, 5)
        self.addObject(self.h_nbjet)
        self.h_nbjet2 = ROOT.TH1F('nbjet2', ';no. of b-tagged jets (Medium WP); Events', 5, 0, 5)
        self.addObject(self.h_nbjet2)

    def endJob(self):
        #Normalise histograms at the end to xsec/sumw
        if self.doNorm:
            for obj in self.objs:
                if isinstance(obj, ROOT.TH1):
                    scale = 1./self.genEventSumw
                    if self.xsec > 0:
                        scale *= self.xsec
                    obj.Scale(scale)
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
        self.doNorm = bool(runTree.GetBranch("genEventSumw")) and bool(inputTree.GetBranch("genWeight"))
        if self.doNorm:
            for entry in range(runTree.GetEntries()):
                runTree.GetEntry(entry)
                self.genEventSumw += runTree.genEventSumw

    def analyze(self, event):
        # some consts
        trigMatch_maxdR2 = 0.3*0.3
        jetMatch_maxdR2 = 0.4*0.4

        # collections of objects
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        fsrPhotons = Collection(event, "FsrPhoton")
        jets = Collection(event, "Jet")
        trigObjs = Collection(event, "TrigObj")
        
        # gen-weight
        genWeight = 1.
        if self.doNorm:
            genWeight = event.genWeight

        icut = 1
        self.h_count.AddBinContent(icut,genWeight)

        # check trigger bit(s)
        if not event.HLT_IsoMu24: return False #MB: can be used as preselection for some speedup
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)
        
        # MET flags, needed???
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
        mu1_idx=mu2_idx=-1
        i_mu1=-1
        for mu1 in muons:  # 1st loop on muons
            i_mu1+=1
            if mu1_idx>-1 and mu2_idx>-1: break
            if not mu1.pt>20: continue #then check trg matching and pT>26
            if not abs(mu1.eta)<2.4: continue
            if not mu1.mediumId : continue
            if not mu1.pfRelIso04_all<0.25: continue #then subtract fsrPhoton (not trivial => neglected)
            mu1_idx=i_mu1
            i_mu2=-1
            for mu2 in muons: # 2nd loop on muons
                i_mu2+=1
                if mu2_idx>-1: break
                if i_mu2==mu1_idx: continue
                if not mu2.pt>20: continue #then check trg matching and pT>26
                if not abs(mu2.eta)<2.4: continue
                if not mu2.mediumId: continue
                if not mu2.pfRelIso04_all<0.25: continue #then subtract fsrPhoton (not trivial => neglected)
                if (mu2.charge*mu1.charge)>0: continue
                mu2_idx=i_mu2
        if mu1_idx<0 or mu2_idx<0: return False

        # Corrected muons p4
        mu1CorrP4 = ROOT.TLorentzVector()
        mu2CorrP4 = ROOT.TLorentzVector()
        #check if corrections are stored
        if self.hasMuCorr:
            mu1CorrP4.SetPtEtaPhiM(muons[mu1_idx].corrected_pt,muons[mu1_idx].eta,muons[mu1_idx].phi,muons[mu1_idx].mass)
            mu2CorrP4.SetPtEtaPhiM(muons[mu2_idx].corrected_pt,muons[mu2_idx].eta,muons[mu2_idx].phi,muons[mu2_idx].mass)
        else: #use uncorrected pt
            mu1CorrP4.SetPtEtaPhiM(muons[mu1_idx].pt,muons[mu1_idx].eta,muons[mu1_idx].phi,muons[mu1_idx].mass)
            mu2CorrP4.SetPtEtaPhiM(muons[mu2_idx].pt,muons[mu2_idx].eta,muons[mu2_idx].phi,muons[mu2_idx].mass)

        # FSR recovery
        mu1WFsrP4 = deepcopy(mu1CorrP4)
        mu2WFsrP4 = deepcopy(mu2CorrP4)
        if muons[mu1_idx].fsrPhotonIdx>-1:
            fsrIdx=muons[mu1_idx].fsrPhotonIdx
            if (fsrPhotons[fsrIdx].dROverEt2<0.012 and
                fsrPhotons[fsrIdx].relIso03<1.8 and
                fsrPhotons[fsrIdx].pt/mu1CorrP4.Pt()<0.4):
                fsrPhotonP4 = ROOT.TLorentzVector()
                fsrPhotonP4.SetPtEtaPhiM(fsrPhotons[fsrIdx].pt,fsrPhotons[fsrIdx].eta,fsrPhotons[fsrIdx].phi,0)
                mu1WFsrP4 += fsrPhotonP4
        if muons[mu2_idx].fsrPhotonIdx>-1:
            fsrIdx=muons[mu2_idx].fsrPhotonIdx
            if (fsrPhotons[fsrIdx].dROverEt2<0.012 and
                fsrPhotons[fsrIdx].relIso03<1.8 and
                fsrPhotons[fsrIdx].pt/mu2CorrP4.Pt()<0.4):
                fsrPhotonP4 = ROOT.TLorentzVector()
                fsrPhotonP4.SetPtEtaPhiM(fsrPhotons[fsrIdx].pt,fsrPhotons[fsrIdx].eta,fsrPhotons[fsrIdx].phi,0)
                mu2WFsrP4 += fsrPhotonP4

        diMu = muons[mu1_idx].p4() + muons[mu2_idx].p4()
        diMuCorr = mu1CorrP4 + mu2CorrP4
        diMuWFsr = mu1WFsrP4 + mu2WFsrP4


        if diMuWFsr.M()<=50: return False #needed as DY MC has this cut (use scale and fsr corrected muons)
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        #check trigger matching
        isTrigMatchedDiMu = False
        for trigObj in trigObjs:
            # first find triger objects corresponting with IsoMu24
            if trigObj.id!=13: continue #mu trigger
            if not trigObj.pt>24: continue
            if not ( trigObj.filterBits & (1<<1) ): continue #2nd bit means that muon-iso filter is fired
            dEta_mu = trigObj.eta - muons[mu1_idx].eta
            dPhi_mu = ROOT.TVector2.Phi_mpi_pi(trigObj.phi - muons[mu1_idx].phi)
            dR2_mu = dEta_mu*dEta_mu + dPhi_mu*dPhi_mu
            if dR2_mu<trigMatch_maxdR2 and muons[mu1_idx].pt>26:
                isTrigMatchedDiMu = True
                break
            dEta_mu = trigObj.eta - muons[mu2_idx].eta
            dPhi_mu = ROOT.TVector2.Phi_mpi_pi(trigObj.phi - muons[mu2_idx].phi)
            dR2_mu = dEta_mu*dEta_mu + dPhi_mu*dPhi_mu
            if dR2_mu<trigMatch_maxdR2 and muons[mu2_idx].pt>26:
                isTrigMatchedDiMu = True
                break
        if not isTrigMatchedDiMu: return False
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        # PU-weight
        puWeight = 1.
        if self.hasPUWeight:
            puWeight = event.puWeight
        self.h_npv_raw.Fill(event.PV_npvsGood,genWeight)
        self.h_npv.Fill(event.PV_npvsGood,puWeight*genWeight)

        #Additional lepton veto
        nLeptons=0
        #1. Muon veto: same selection as for signal muons
        #MB: in principle muons could be counted in previous loops
        i_mu=-1
        for mu in muons:
            i_mu+=1
            if i_mu==mu1_idx or i_mu==mu2_idx: continue
            if not mu.pt>20: continue
            if not abs(mu.eta)<2.4: continue
            if not mu.mediumId: continue
            if not mu1.pfRelIso04_all<0.25: continue
            nLeptons+=1 #MB: can break loop here and exit, but want to count additional leptons (they should be rare in general)
        #2. Electron veto: similar selection as for signal muons
        for ele in electrons:
            if not ele.pt>20: continue
            if not abs(ele.eta)<2.5: continue
            if not ele.mvaFall17V2Iso_WP90: continue #Id with iso variables, WP90
            nLeptons+=1 #MB: can break loop here and exit, but want to count additional leptons (they should be rare in general)
        self.h_nlep.Fill(nLeptons,puWeight*genWeight)
        #3. actual lepton veto
        if nLeptons>=1: return False
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        # jets
        nJets=nBJetsL=nBJetsM=0
        jet1_idx=jet2_idx=-1
        i_jet=-1
        for jet in jets:
            i_jet+=1
            if not jet.pt>25: continue
            if not abs(jet.eta)<4.7: continue
            if not ( jet.jetId & (1<<1) ): continue #2nd bit stands for tight WP
            #FIXME: jet.puIdDisc #define loose WP
            #cleaning wrt muons
            dEta_mu = jet.eta - muons[mu1_idx].eta
            dPhi_mu = ROOT.TVector2.Phi_mpi_pi(jet.phi - muons[mu1_idx].phi)
            dR2_mu = dEta_mu*dEta_mu + dPhi_mu*dPhi_mu
            if not dR2_mu>jetMatch_maxdR2: continue
            dEta_mu = jet.eta - muons[mu2_idx].eta
            dPhi_mu = ROOT.TVector2.Phi_mpi_pi(jet.phi - muons[mu2_idx].phi)
            dR2_mu = dEta_mu*dEta_mu + dPhi_mu*dPhi_mu
            if not dR2_mu>jetMatch_maxdR2: continue
            nJets+=1
            if jet1_idx<0: jet1_idx=i_jet
            if (jet2_idx<0 and i_jet!=jet1_idx): jet2_idx=i_jet
            #b-jets
            if not abs(jet.eta)<2.5: continue
            if jet.btagDeepB>0.1241: nBJetsL+=1
            if jet.btagDeepB>0.4184: nBJetsM+=1                    

        # di-jet (VBF) variables
        deta_jj = 0
        diJ = ROOT.TLorentzVector()
        if jet1_idx>-1 and jet2_idx>-1:
            deta_jj = jets[jet1_idx].eta - jets[jet2_idx].eta
            diJ = jets[jet1_idx].p4() + jets[jet2_idx].p4()
        #VBF abs(deta_jj)>2.5 and diJ.M()>400

        #DY pt(mm) weight to account for missing higher order calc and resummation
        #Delivered by comparing DY MC and data around Z-peak in n-jet bins and
        # ad-hoc parameterised with polynomials of 7/8-th order
        nJetWeight = 1.
        ptWeight = 1.
        if self.isDY > 0:
            diMu_pt = min(diMuWFsr.Pt(),194.5)
            if self.isDY == 1: #LO
                if jet1_idx == -1: #0-jet
                    nJetWeight = 0.8284
                    ptWeight = (0.671731
                                +0.062859 * diMu_pt
                                -0.0035237 * pow(diMu_pt,2)
                                +0.000106116 * pow(diMu_pt,3)
                                -1.51184e-06 * pow(diMu_pt,4)
                                +1.07451e-08 * pow(diMu_pt,5)
                                -3.7115e-11 * pow(diMu_pt,6)
                                +4.96315e-14 * pow(diMu_pt,7))
                elif jet2_idx == -1: #1-jet
                    nJetWeight = 1.0151
                    ptWeight = (0.60034
                                +0.0719654 * diMu_pt
                                -0.00359921 * pow(diMu_pt,2)
                                +8.13379e-05 * pow(diMu_pt,3)
                                -9.57577e-07 * pow(diMu_pt,4)
                                +6.09171e-09 * pow(diMu_pt,5)
                                -1.98696e-11 * pow(diMu_pt,6)
                                +2.60659e-14 * pow(diMu_pt,7))
                else: #>=2-jet
                    nJetWeight = 1.1443
                    ptWeight = (0.555797
                                +0.0712998 * diMu_pt
                                -0.00360608 * pow(diMu_pt,2)
                                +9.1347e-05 * pow(diMu_pt,3)
                                -1.31615e-06 * pow(diMu_pt,4)
                                +1.12552e-08 * pow(diMu_pt,5)
                                -5.6584e-11 * pow(diMu_pt,6)
                                +1.54439e-13 * pow(diMu_pt,7)
                                -1.76493e-16 * pow(diMu_pt,8))
            else: #NLO
                if jet1_idx == -1: #0-jet
                    nJetWeight = 0.9040
                    diMu_pt = min(diMu_pt,110)
                    ptWeight = (0.660414
                                +0.0701017 * diMu_pt
                                -0.00375595 * pow(diMu_pt,2)
                                +9.02523e-05 * pow(diMu_pt,3)
                                -9.67396e-07 * pow(diMu_pt,4)
                                +4.65835e-09 * pow(diMu_pt,5)
                                -8.26500e-12 * pow(diMu_pt,6))
                elif jet2_idx == -1: #1-jet
                    nJetWeight = 0.9618
                    ptWeight = (0.631134
                                +0.120251 * diMu_pt
                                -0.00843519 * pow(diMu_pt,2)
                                +0.000253573 * pow(diMu_pt,3)
                                -4.063e-06 * pow(diMu_pt,4)
                                +3.73354e-08 * pow(diMu_pt,5)
                                -1.97356e-10 * pow(diMu_pt,6)
                                +5.57979e-13 * pow(diMu_pt,7)
                                -6.53513e-16 * pow(diMu_pt,8))
                else: #>=2-jet
                    nJetWeight = 1.0247
                    ptWeight = (0.646843
                                +0.106985 * diMu_pt
                                -0.00773057 * pow(diMu_pt,2)
                                +0.000255507 * pow(diMu_pt,3)
                                -4.71148e-06 * pow(diMu_pt,4)
                                +5.23243e-08 * pow(diMu_pt,5)
                                -3.57873e-10 * pow(diMu_pt,6)
                                +1.47479e-12 * pow(diMu_pt,7)
                                -3.35721e-15 * pow(diMu_pt,8)
                                +3.24135e-18 * pow(diMu_pt,9))

        # fill histograms
        self.h_njet.Fill(nJets,puWeight*genWeight*ptWeight*nJetWeight)
        self.h_nbjet.Fill(nBJetsL,puWeight*genWeight*ptWeight*nJetWeight)
        self.h_nbjet2.Fill(nBJetsM,puWeight*genWeight*ptWeight*nJetWeight)

        self.h_pt_mm_wb.Fill(diMu.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_m_mm_wb.Fill(diMu.M(),puWeight*genWeight*ptWeight*nJetWeight)
        #b-jet veto
        if (nBJetsL>=2 or nBJetsM>=1): return False
        icut += 1
        self.h_count.AddBinContent(icut,genWeight)

        self.h_pt1.Fill(muons[mu1_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
        self.h_pt2.Fill(muons[mu2_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
        self.h_pt1_corr.Fill(mu1CorrP4.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_pt2_corr.Fill(mu2CorrP4.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        if muons[mu1_idx].charge<0:
            self.h_ptn.Fill(muons[mu1_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
            self.h_ptp.Fill(muons[mu2_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
        else:
            self.h_ptp.Fill(muons[mu1_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
            self.h_ptn.Fill(muons[mu2_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
            
        #di-mu variables
        self.h_pt_mm.Fill(diMu.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_m_mm.Fill(diMu.M(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_pt_mm_corr.Fill(diMuCorr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_m_mm_corr.Fill(diMuCorr.M(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_pt_mm_fsr.Fill(diMuWFsr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        self.h_m_mm_fsr.Fill(diMuWFsr.M(),puWeight*genWeight*ptWeight*nJetWeight)
        #pT(mm) for reweight
        if diMuWFsr.M() > 70 and diMuWFsr.M() < 110:
            self.h_njet_z.Fill(nJets,puWeight*genWeight)
            self.h_njet_zw.Fill(nJets,puWeight*genWeight*ptWeight*nJetWeight)
            self.h_pt_mm_z.Fill(diMuWFsr.Pt(),puWeight*genWeight)
            self.h_pt_mm_zw.Fill(diMuWFsr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
            if jet1_idx == -1:
                self.h_pt_mm_0j.Fill(diMuWFsr.Pt(),puWeight*genWeight)
                self.h_pt_mm_0jw.Fill(diMuWFsr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
            elif jet2_idx == -1:
                self.h_pt_mm_1j.Fill(diMuWFsr.Pt(),puWeight*genWeight)
                self.h_pt_mm_1jw.Fill(diMuWFsr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
            else:
                self.h_pt_mm_2j.Fill(diMuWFsr.Pt(),puWeight*genWeight)
                self.h_pt_mm_2jw.Fill(diMuWFsr.Pt(),puWeight*genWeight*ptWeight*nJetWeight)
        #jet variables
        if jet1_idx>-1:
            self.h_ptj1.Fill(jets[jet1_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
            if jet2_idx>-1:
                self.h_ptj2.Fill(jets[jet2_idx].pt,puWeight*genWeight*ptWeight*nJetWeight)
                self.h_deta_jj.Fill(deta_jj,puWeight*genWeight*ptWeight*nJetWeight)
                self.h_m_jj.Fill(diJ.M(),puWeight*genWeight*ptWeight*nJetWeight)
        #VBF
        if (jet1_idx>-1 and jet2_idx>-1 and jets[jet1_idx].pt>35 and
            diJ.M()>400 and abs(deta_jj)>2.5):
            self.m_mm_vbf.Fill(diMuWFsr.M(),puWeight*genWeight*ptWeight*nJetWeight)
        elif diMuWFsr.Pt()>130:
            self.m_mm_bst.Fill(diMuWFsr.M(),puWeight*genWeight*ptWeight*nJetWeight)

        #the End
        return True
