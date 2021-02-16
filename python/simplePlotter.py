# The following needs to come before any other ROOT import and before argparse
from copy import deepcopy
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import gROOT, gStyle
from ROOT import TH1F, TFile, TCanvas, TPad, TLegend, \
    TGraphAsymmErrors, Double, TLatex, TMath

from officialStyle import officialStyle
import CMS_lumi

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def configureLegend(leg, ncolumn):
    leg.SetNColumns(ncolumn)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
    #leg.SetTextSize(0.02)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

histoDir = 'histoFiles_v2/'
lumi=14.03+7.06+6.89+31.83
print 'lumi(2018A+B+C+D) =',lumi,'fb-1'
hscaling=100.
samples = {
    'DYToLL': ['Z/#gamma*#rightarrow#mu#mu',6225.4*1000,100194597],
    'tt2l2nu': ['t#bar{t}',86.61*1000,64310000],
    #'ewk2l2j': ['Zjj-EW',1.029*1000,2959970],
    'ggH125': ['gg#rightarrowH#rightarrow#mu#mu',0.01057*1000,1920000],
    'vbfH125': ['q#bar{q}#rightarrowq#bar{q}H#rightarrow#mu#mu',0.0008228*1000,1000000],
    'Run2018All': ['Data',-1,-1]
}

h_names = {
    'm_mm_wb': [],
    'm_mm': [],
    'm_mm_fsr': [],
    'm_mm_corr': [],
    #'m_mm_bst': [],
    #'m_mm_vbf': [],
    'pt_mm_fsr': [],
    'pt_mm': [],
    #'hcount': [],
    'npv': [],
    'npv_raw': [],
    'pt1_corr': [],
    'pt1_corr': [],
    ##'nlep': [],
    'ptj1': [],
    'ptj2': [],
    'm_jj': [],
    'deta_jj': [],
    'njet': [],
    'nbjet': [],
}

for sample in ['tt2l2nu','DYToLL','ggH125','vbfH125','Run2018All']:
    #print sample, samples[sample][0], samples[sample][1], samples[sample][2]
    f_in=ROOT.TFile.Open(histoDir+'histOut_'+sample+'.root')
    #f_in.cd('mmPlots')
    #f_in.ls()
    scale = 1
    if samples[sample][1] > -1:
        scale = lumi*samples[sample][1]/samples[sample][2]
    print sample, scale
    for h_name in h_names:
        h = f_in.Get('mmPlots/'+h_name).Clone(h_name+'_'+sample)
        h.Scale(scale)
        h_names[h_name].append(deepcopy(h))

    #f_in.Close()

canvas = TCanvas()
#leg = TLegend(0.2, 0.7, 0.5, 0.9)
leg = TLegend(0.58, 0.6, 0.9, 0.9)
configureLegend(leg, 1)

hscaling_str = ''
for h_name in h_names:
    hSum = ROOT.THStack()
    leg.Clear()
    #DY
    h_names[h_name][1].SetFillColor(ROOT.kOrange-3)
    h_names[h_name][1].SetLineColor(ROOT.kBlack)
    hSum.Add(h_names[h_name][1])
    #tt
    h_names[h_name][0].SetFillColor(ROOT.kGreen+1)
    h_names[h_name][0].SetLineColor(ROOT.kBlack)
    hSum.Add(h_names[h_name][0])
    #H125
    h_H125 = h_names[h_name][2].Clone(h_name+'_H125')
    h_H125.Reset()
    #ggH
    h_names[h_name][2].SetLineColor(ROOT.kRed+1)
    if hscaling>1 and h_name.find('m_mm')>-1:
        h_names[h_name][2].Scale(hscaling)
    h_H125.Add(h_names[h_name][2])
    #vbfH
    h_names[h_name][3].SetLineColor(ROOT.kBlue+4)
    if hscaling>1 and h_name.find('m_mm')>-1:
        h_names[h_name][3].Scale(hscaling)
    h_H125.Add(h_names[h_name][3])
    h_H125.SetFillColor(ROOT.kBlue)
    h_H125.SetLineColor(ROOT.kBlack)
    hSum.Add(h_H125)
    
    hSum.Draw("hist")
    hSum.GetXaxis().SetTitle(h_names[h_name][1].GetXaxis().GetTitle())
    hSum.GetYaxis().SetTitle(h_names[h_name][1].GetYaxis().GetTitle())
    #hSum.Print()
    #data
    h_names[h_name][len(h_names[h_name])-1].SetLineColor(ROOT.kBlack)
    h_names[h_name][len(h_names[h_name])-1].SetMarkerStyle(20)
    h_names[h_name][len(h_names[h_name])-1].SetMarkerSize(0.5)
    h_names[h_name][len(h_names[h_name])-1].Draw("same e")
    #ggH & VBF H no stacked
    if h_name.find('m_mm')>-1:
        h_names[h_name][2].Draw("same hist")
        h_names[h_name][3].Draw("same hist")

    leg.AddEntry(h_names[h_name][len(h_names[h_name])-1],"Data","LPE") #add marker to data?
    leg.AddEntry(h_names[h_name][1],'Z/#gamma*#rightarrow#mu#mu',"F1")
    leg.AddEntry(h_names[h_name][0],'t#bar{t}',"F1")
    if hscaling>1 and h_name.find('m_mm')>-1:
        #hscaling_str = ' #times'+str(hscaling)
        hscaling_str = ' #times'+str(int(round(hscaling)))
    leg.AddEntry(h_H125,'H#rightarrow#mu#mu'+hscaling_str,"F1")
    if hscaling>1 and h_name.find('m_mm')>-1:
        leg.AddEntry(h_names[h_name][2],'gg#rightarrowH#rightarrow#mu#mu'+hscaling_str,"L")
        leg.AddEntry(h_names[h_name][3],'qq#rightarrowqqH#rightarrow#mu#mu'+hscaling_str,"L")
        
    leg.Draw()
    canvas.SetLogy()
    #change the CMS_lumi variables (see CMS_lumi.py)
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = "Private work"
    CMS_lumi.lumi_sqrtS = str(round(lumi,1))+' fb^{-1} (13 TeV)' #used with iPeriod = 0 (default is an empty string)
    iPeriod = 0
    iPos = 0
    if( iPos==0 ): CMS_lumi.relPosX = 0.16
    CMS_lumi.CMS_lumi(canvas,iPeriod,iPos)
    
    canvas.SaveAs(h_name+'.png')
