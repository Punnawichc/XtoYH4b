#include "HistoMaker_XtoYH4b.h"
#include <TH1.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include<iostream>
#include<vector>
#include<fstream>
#include<string>
#include <bits/stdc++.h>

string input_path = "/data/dust/user/chatterj/XToYHTo4b/SmallNtuples/Analysis_NTuples/";
string output_path = "/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/XtoYH4b/HistoMaker/output/";

void initializeJetHistograms(vector<TH1F*>& histograms, const string& prefix, vector<tuple<string, string, tuple<int, double, double>>> histinfo, int njetmax) {
    
    for (int ijet = 0; ijet < njetmax; ++ijet) {
        for (const auto& [suffix, titlesuffix, params] : histinfo) {
            auto [bins, min, max] = params;
            string hname = prefix + "_" + suffix + "_" + to_string(ijet + 1);
            string htitle = prefix + " " + to_string(ijet + 1) + " " + titlesuffix;
            histograms.push_back(getHisto1F(hname, htitle, bins, min, max));
        }
    }
}

void initializeCombinationHistograms(vector<TH1F*>& histograms, const string& prefix, vector<tuple<string, string, tuple<int, double, double>>> histinfo,
								     int ncomb, int jpair, const string& titleSuffix) {
   
    for (int icomb = 0; icomb < ncomb; ++icomb) {
		for (const auto& [suffix, titlesuffix, params] : histinfo) {
			auto [bins, min, max] = params;
			string pairinfo="";
			if(jpair == 0) { pairinfo = "LeadingPair_"; }
			if(jpair == 1) { pairinfo = "SubleadingPair_"; }
			string hname = prefix+"_Comb" + to_string(icomb + 1) + "_" + pairinfo + suffix;
			string htitle = prefix+" Combination: " + to_string(icomb + 1) + " "+ titleSuffix + " "+titlesuffix;
			histograms.push_back(getHisto1F(hname, htitle,bins, min, max));
		}
	}
   
}

int main(int argc, char *argv[])
{
  if((argc-1)!=4){
	cout<<"Need exactly 4 arguments. Exiting!"<<endl;
	return 0;
  }
   
 std::istringstream(argv[1]) >> isDATA; 
 std::istringstream(argv[2]) >> isSignal; 
 year = string(argv[4]);
 cout<<"Running with options: isDATA? "<<isDATA<<" Signal? "<<isSignal<<endl;
 cout<<"Running on file : " << argv[3] << std::endl;
 
//  input_path += year+"/v1/"; //2022
 input_path += year+"/"; //2023
 output_path += year+"/";
 
 if(isSignal){ input_path += "SIGNAL/" ; }
 
 TString inputFile= input_path+argv[3];	
 inputFile= input_path+argv[3];
 
 isMC = (!isDATA);
	
 std::cout <<"Input file "<< inputFile << std::endl;
 
 std::string fileName = "MC_Summary_"+year+".txt";
 if(isSignal) {  fileName = "MC_Summary_"+year+"_SIGNAL.txt"; }
 if(isMC){
	auto sampleMap = CalculateXsecWeights(fileName,isSignal);
	auto it = sampleMap.find(string(argv[3]).substr(0, string(argv[3]).find('.')));
	xsec_weight = (it->second).XsecWeight;
	cout<<"xsec_weight "<<xsec_weight<<endl;
	cout<<"Entries "<<(it->second).Entries<<" SumLHEWeights "<<(it->second).SumofLHEWeights<<" SumGENWeights "<<(it->second).SumofGENWeights<<" Xsec "<<(it->second).XSec<<endl;
 }
   
 char file_name[1000]; 
 sprintf(file_name,"%s/Histogram_%s",output_path.c_str(),argv[3]);
 TFile* final_file = TFile::Open(file_name, "RECREATE");  
 TTree *JetTree = new TTree("JetTree", "Tree storing JetAK4_btag_PNetB_WP");

 TFile *file = TFile::Open(inputFile,"read");
 TTree *tree = (TTree*)file->Get("Tout");
         
 // read branches //
 readTree(tree, isMC);
  
 bool use_sys = false;
   
 // Declaration of histograms //
  
 final_file->cd();
   
 TH1D* h_nom;
 
 // common histograms //
 
 TH1F *h_NPV			 = getHisto1F("h_PV_npvsGood","# of primary vertices",100,0,100);  
 
 vector<TH1F*> h_AK4jets;
 vector<tuple<string, string, tuple<int, double, double>>> jetInfo = {
        {"pt", "p_{T} (GeV)", {40, 20, 1020}},
        {"eta", "#eta", {40, -2.5, 2.5}},
        {"phi", "#phi", {65, -M_PI, M_PI}},
        {"mass", "mass (GeV)", {40, 20, 220}},
        {"DeepFlavB", "DeepFlavB score", {40, 0, 1}},
        {"DeepFlavB_WP", "DeepFlavB score (WP-binned)", {6, -0.5, 5.5}},
        {"DeepFlavQG", "DeepFlavQG score", {40, 0, 1}},
        {"PNetB", "PNetB score", {40, 0, 1}},
        {"PNetB_WP", "PNetB score (WP-binned)", {6, -0.5, 5.5}},
        {"PNetQG", "PNetQG score", {40, 0, 1}},
        {"RobustParTAK4B","RobustParTAK4B score", {40, 0, 1}},
        {"RobustParTAK4B_WP","RobustParTAK4B score (WP-binned)", {6, -0.5, 5.5}},
        {"RobustParTAK4QG", "RobustParTAK4QG score", {40, 0, 1}}
 };
 int njetvars = jetInfo.size(); 

 initializeJetHistograms(h_AK4jets, "Jet", jetInfo, njetmax);
 
 file->cd();

   std::vector<float> Weight_nom(njetmax);
   std::vector<float> jet_btag_PNetB_WP(njetmax);
   std::vector<float> jet_btag_RobustParTAK4B_WP(njetmax);

   bool b_tag_PNetB_pass_L[njetmax];
   bool b_tag_PNetB_pass_M[njetmax];
   bool b_tag_PNetB_pass_T[njetmax];
   bool b_tag_PNetB_pass_XT[njetmax];
   bool b_tag_PNetB_pass_XXT[njetmax]; 

   bool b_tag_RobustParTAK4B_pass_L[njetmax];
   bool b_tag_RobustParTAK4B_pass_M[njetmax];
   bool b_tag_RobustParTAK4B_pass_T[njetmax];
   bool b_tag_RobustParTAK4B_pass_XT[njetmax];
   bool b_tag_RobustParTAK4B_pass_XXT[njetmax]; 

   for (int i = 0; i < njetmax; i++) {
	JetTree->Branch(("Weight_nom_" + std::to_string(i + 1)).c_str(), &Weight_nom[i]);
    JetTree->Branch(("jetAK4_btag_PNetB_WP_" + std::to_string(i + 1)).c_str(), &jet_btag_PNetB_WP[i]);
	JetTree->Branch(("jetAK4_btag_RobustParTAK4B_WP_" + std::to_string(i + 1)).c_str(), &jet_btag_RobustParTAK4B_WP[i]);

	JetTree->Branch(Form("b_tag_PNetB_pass_%d_L", i+1), &b_tag_PNetB_pass_L[i], Form("b_tag_PNetB_pass_%d_L/O", i+1));
    JetTree->Branch(Form("b_tag_PNetB_pass_%d_M", i+1), &b_tag_PNetB_pass_M[i], Form("b_tag_PNetB_pass_%d_M/O", i+1));
    JetTree->Branch(Form("b_tag_PNetB_pass_%d_T", i+1), &b_tag_PNetB_pass_T[i], Form("b_tag_PNetB_pass_%d_T/O", i+1));
    JetTree->Branch(Form("b_tag_PNetB_pass_%d_XT", i+1), &b_tag_PNetB_pass_XT[i], Form("b_tag_PNetB_pass_%d_XT/O", i+1));
    JetTree->Branch(Form("b_tag_PNetB_pass_%d_XXT", i+1), &b_tag_PNetB_pass_XXT[i], Form("b_tag_PNetB_pass_%d_XXT/O", i+1));

	JetTree->Branch(Form("b_tag_RobustParTAK4B_pass_%d_L", i+1), &b_tag_RobustParTAK4B_pass_L[i], Form("b_tag_RobustParTAK4B_pass_%d_L/O", i+1));
    JetTree->Branch(Form("b_tag_RobustParTAK4B_pass_%d_M", i+1), &b_tag_RobustParTAK4B_pass_M[i], Form("b_tag_RobustParTAK4B_pass_%d_M/O", i+1));
    JetTree->Branch(Form("b_tag_RobustParTAK4B_pass_%d_T", i+1), &b_tag_RobustParTAK4B_pass_T[i], Form("b_tag_RobustParTAK4B_pass_%d_T/O", i+1));
    JetTree->Branch(Form("b_tag_RobustParTAK4B_pass_%d_XT", i+1), &b_tag_RobustParTAK4B_pass_XT[i], Form("b_tag_RobustParTAK4B_pass_%d_XT/O", i+1));
    JetTree->Branch(Form("b_tag_RobustParTAK4B_pass_%d_XXT", i+1), &b_tag_RobustParTAK4B_pass_XXT[i], Form("b_tag_RobustParTAK4B_pass_%d_XXT/O", i+1));
   }

   
   //// Event loop ////
   std::cout <<"Entries: "<<tree->GetEntries()<< std::endl;  
   
   for(Long64_t jentry =0; jentry < tree->GetEntries() ; jentry++)
   {
	      
	tree->GetEntry(jentry);
	if( jentry % 10000 == 0) { std::cout <<jentry<<" events processed" << std::endl;}
  
	float weight_nom;
	
	if(isMC){
		
		//if (isSignal) { weight_nom = 1.0; }
		//else { weight_nom = Generator_weight; 	}
		weight_nom = Generator_weight; 
		
		weight_nom *= puWeight;
		//weight_nom *= prefiringweight;
		weight_nom *= btag_PNet_weight; // since using ParticleNet for offline event selection, need to be changed if offline selection is changed to ParT
		weight_nom *= triggersf_weight_L1HT;
		weight_nom *= triggersf_weight_pt;
		weight_nom *= triggersf_weight_btag;
	
		weight_nom *= xsec_weight;
	
	}
	else{
		weight_nom = 1.;
	}

   h_NPV->Fill(PV_npvsGood,weight_nom);
   
   std::vector<int> pt_indices(nJetAK4);
   for (int ix = 0; ix < pt_indices.size(); ++ix) {
        pt_indices[ix] = ix;
   }
   std::sort(pt_indices.begin(), pt_indices.end(), [&](int i1, int i2) {
        return JetAK4_pt[i1] > JetAK4_pt[i2]; // Descending order
   });

   for(int ijet=0; ijet<min(nJetAK4,njetmax); ijet++){
	   
	   int idx = pt_indices[ijet];

	   h_AK4jets[njetvars*ijet+0]->Fill(JetAK4_pt[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+1]->Fill(JetAK4_eta[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+2]->Fill(JetAK4_phi[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+3]->Fill(JetAK4_mass[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+4]->Fill(JetAK4_btag_DeepFlavB[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+5]->Fill(JetAK4_btag_DeepFlavB_WP[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+6]->Fill(JetAK4_btag_DeepFlavQG[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+7]->Fill(JetAK4_btag_PNetB[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+8]->Fill(JetAK4_btag_PNetB_WP[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+9]->Fill(JetAK4_btag_PNetQG[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+10]->Fill(JetAK4_btag_RobustParTAK4B[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+11]->Fill(JetAK4_btag_RobustParTAK4B_WP[idx], weight_nom);
	   h_AK4jets[njetvars*ijet+12]->Fill(JetAK4_btag_RobustParTAK4QG[idx], weight_nom);

       Weight_nom[ijet]  = weight_nom;

	   jet_btag_PNetB_WP[ijet] = JetAK4_btag_PNetB_WP[ijet];
	   
	   b_tag_PNetB_pass_L[ijet]   = (JetAK4_btag_PNetB_WP[ijet] >= 1);
	   b_tag_PNetB_pass_M[ijet]   = (JetAK4_btag_PNetB_WP[ijet] >= 2);
	   b_tag_PNetB_pass_T[ijet]   = (JetAK4_btag_PNetB_WP[ijet] >= 3);
	   b_tag_PNetB_pass_XT[ijet]  = (JetAK4_btag_PNetB_WP[ijet] >= 4);
	   b_tag_PNetB_pass_XXT[ijet] = (JetAK4_btag_PNetB_WP[ijet] >= 5);

	   jet_btag_RobustParTAK4B_WP[ijet] = JetAK4_btag_RobustParTAK4B_WP[ijet];

	   b_tag_RobustParTAK4B_pass_L[ijet]   = (JetAK4_btag_RobustParTAK4B_WP[ijet] >= 1);
	   b_tag_RobustParTAK4B_pass_M[ijet]   = (JetAK4_btag_RobustParTAK4B_WP[ijet] >= 2);
	   b_tag_RobustParTAK4B_pass_T[ijet]   = (JetAK4_btag_RobustParTAK4B_WP[ijet] >= 3);
	   b_tag_RobustParTAK4B_pass_XT[ijet]  = (JetAK4_btag_RobustParTAK4B_WP[ijet] >= 4);
	   b_tag_RobustParTAK4B_pass_XXT[ijet] = (JetAK4_btag_RobustParTAK4B_WP[ijet] >= 5);

   }

   JetTree->Fill();
   
  
   }//event loop
   
   final_file->Write();
   final_file->cd();
   final_file->Close();
 
}
