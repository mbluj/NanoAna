# The following needs to come before any other ROOT import and before argparse
import os
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

histoDir = 'histoFiles/'
outDir = 'plots/'
lumi=14.03+7.06+6.89+31.83
print 'lumi(2018A+B+C+D) =',lumi,'fb-1'
hscaling=100.
samples = {
    'DYToLL': ['Z/#gamma*#rightarrow#mu#mu'],
    'tt2l2nu': ['t#bar{t}'],
    'ewk2l2j': ['Zjj-EW'],
    'atop_tch': ['#bar{t}, t-channel'],
    'top_tch': ['t, t-channel'],
    't_sch': ['t, s-channel'],
    'ttsemil': ['t#bar{t}'],
    'tWatop_ext1': ['#bar{t}W'],
    'tWtop_ext1': ['tW'],
    'ww2l2nu': ['WW'],
    'wz3l1nu_ext1': ['WZ'],
    'wz2l2q': ['WZ'],
    'zz2l2nu_ext1': ['ZZ'],
    'zz2l2q': ['ZZ'],
    'zz4l_ext1': ['ZZ'],
    'ggH125': ['gg#rightarrowH#rightarrow#mu#mu'],
    'vbfH125': ['q#bar{q}#rightarrowq#bar{q}H#rightarrow#mu#mu'],
    'Run2018All': ['Data']
}

h_names = {
    'm_mm': [],
    'pt_mm': [],
    #'hcount': [],
    'npv': [],
    'npv_raw': [],
    'pt1_corr': [],
    'pt2_corr': [],
    'ptj1': [],
    'ptj2': [],
}

if not os.path.isdir(outDir):
    os.mkdir(outDir)

for sample in ['tt2l2nu','DYToLL','ggH125','vbfH125','ewk2l2j',
               'ttsemil','atop_tch','top_tch','tWatop_ext1','tWtop_ext1','t_sch',
               'ww2l2nu','wz3l1nu_ext1','wz2l2q','zz2l2nu_ext1','zz2l2q','zz4l_ext1',
               'Run2018All']:
    #print sample, samples[sample][0], samples[sample][1], samples[sample][2]
    f_in=ROOT.TFile.Open(histoDir+'histOut_'+sample+'.root')
    scale = 1.
    if samples[sample][0].find('Data')==-1 and sample.find('Run')==-1:
        scale = lumi*1000.
    #print sample, scale
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
    #Zjj-EW
    h_names[h_name][4].SetFillColor(ROOT.kMagenta+1)
    h_names[h_name][4].SetLineColor(ROOT.kBlack)
    hSum.Add(h_names[h_name][4])
    #di-boson
    h_VV = deepcopy(h_names[h_name][11].Clone(h_name+'_VV'))
    h_VV.Reset()
    h_VV.Add(h_names[h_name][11]) #WW->2l2nu
    h_VV.Add(h_names[h_name][12]) #WZ->3l1nu
    h_VV.Add(h_names[h_name][13]) #WZ->2l2q
    h_VV.Add(h_names[h_name][14]) #ZZ->2l2nu
    h_VV.Add(h_names[h_name][15]) #ZZ->2l2q
    h_VV.Add(h_names[h_name][16]) #ZZ->4l
    h_VV.SetFillColor(ROOT.kCyan-3)
    h_VV.SetLineColor(ROOT.kBlack)
    hSum.Add(h_VV)
    #top
    h_top = deepcopy(h_names[h_name][0].Clone(h_name+'_top'))
    h_top.Reset()
    #tt fully-leptonic
    h_top.Add(h_names[h_name][0])
    #tt semi-leptonic
    h_top.Add(h_names[h_name][5])
    #single-t t-channel
    h_top.Add(h_names[h_name][6])
    h_top.Add(h_names[h_name][7])
    #tW
    h_top.Add(h_names[h_name][8])
    h_top.Add(h_names[h_name][9])
    #single-t s-channel
    h_top.Add(h_names[h_name][10])
    h_top.SetFillColor(ROOT.kGreen+1)
    h_top.SetLineColor(ROOT.kBlack)
    hSum.Add(h_top)
    #H125
    h_H125 = deepcopy(h_names[h_name][2].Clone(h_name+'_H125'))
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
    leg.AddEntry(h_names[h_name][4],'#mu#mujj-EW',"F1") #FIXME: always?
    leg.AddEntry(h_top,'Top quark',"F1")
    leg.AddEntry(h_VV,'Di-boson',"F1")
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
    
    canvas.SaveAs(outDir+'/'+h_name+'.png')
    canvas.SetLogy(0)
    canvas.SaveAs(outDir+'/'+h_name+'_lin.png')
