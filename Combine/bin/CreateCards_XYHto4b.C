#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"

using namespace std;

int main(int argc, char **argv) {
	
   string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/CombineHarvester/CombineTools/bin/";

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  // Here we will just define two categories for an 8TeV analysis. Each entry in
  // the vector below specifies a bin name and corresponding bin_id.
  ch::Categories cats = {};
 
  //! [part1]
   
  // v1 (old histograms) and v2 (new histograms)
  // cats.push_back({1, "h_MX_Comb_5_5_4_4_Inclusive"});
  // cats.push_back({2, "h_MX_Comb_5_5_4_4"});
  // cats.push_back({3, "h_MX_Comb_5_5_5_4"});
  // cats.push_back({4, "h_MX_Comb_5_5_5_5"}); # 5 is a combination of 2,3,4 in datacard level
  // cats.push_back({6, "h_MX_Comb_3_3_3_2_Inclusive"});

  // v3
  cats.push_back({1, "h_MX_Comb_5_5_4_4_Inclusive_mHcut"});
  cats.push_back({2, "h_MX_Comb_5_5_4_4_mHcut"});
  cats.push_back({3, "h_MX_Comb_5_5_5_4_mHcut"});
  cats.push_back({4, "h_MX_Comb_5_5_5_5_mHcut"});
  cats.push_back({6, "h_MX_Comb_3_3_3_2_Inclusive_mHcut"});

  // v4
  // cats.push_back({1, "h_MX_MY_Comb_5_5_4_4_Inclusive"});
  // cats.push_back({2, "h_MX_MY_Comb_5_5_4_4"});
  // cats.push_back({3, "h_MX_MY_Comb_5_5_5_4"});
  // cats.push_back({4, "h_MX_MY_Comb_5_5_5_5"});
  // cats.push_back({6, "h_MX_MY_Comb_3_3_3_2_Inclusive"});

  // v5
  // cats.push_back({1, "h_MX_MY_Comb_5_5_4_4_Inclusive_mHcut"});
  // cats.push_back({2, "h_MX_MY_Comb_5_5_4_4_mHcut"});
  // cats.push_back({3, "h_MX_MY_Comb_5_5_5_4_mHcut"});
  // cats.push_back({4, "h_MX_MY_Comb_5_5_5_5_mHcut"});
  // cats.push_back({6, "h_MX_MY_Comb_3_3_3_2_Inclusive_mHcut"});

  // v6
  // cats.push_back({7, "h_MX_Comb_3_3_3_2_Inclusive_mHcut"});
  // cats.push_back({8, "h_MX_MY_Comb_3_3_3_2_Inclusive"});
  // cats.push_back({9, "h_MX_MY_Comb_3_3_3_2_Inclusive_mHcut"});


  //! [part2]
   vector<string> signals;
  signals.push_back("XtoYHto4B_MX-300_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-300_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-300_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-400_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-400_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-400_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-400_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-650_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-650_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-650_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-650_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-650_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-600_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-900_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-600_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1200_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-600_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-1800_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-600_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-2500_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-1000_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-125_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-200_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-400_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-600_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-60_TuneCP5_13p6TeV_madgraph-pythia8");
  signals.push_back("XtoYHto4B_MX-4000_MY-95_TuneCP5_13p6TeV_madgraph-pythia8");
   
     
  cout<<"# of signal points "<<signals.size()<<endl;
  
  //! [part2]

  //! [part3]
  //backgrounds
  vector<string> bkg_procs;
  bkg_procs.push_back("TT");
  bkg_procs.push_back("ST");
  bkg_procs.push_back("QCD");
  //signal
  vector<string> sig_procs = {"NMSSM_"};
  cb.AddObservations({"*"}, {"XYH"}, {"13p6TeV_2022"}, {"4b"}, cats);
  cb.AddProcesses({"*"}, {"XYH"}, {"13p6TeV_2022"},  {"4b"}, bkg_procs, cats, false); 
  cb.AddProcesses(signals, {"XYH"}, {"13p6TeV_2022"}, {"4b"}, sig_procs, cats, true);
  
  //! [part4]

  //Some of the code for this is in a nested namespace, so
  // we'll make some using declarations first to simplify things a bit.
  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;

  //! [part5]
//  cb.cp().signals()

    cb.cp()
      .AddSyst(cb, "lumi_13TeV_Uncorrelated_2022", "lnN", SystMap<era>::init
      ({"13TeV_2022"}, 1.015));
      

  //! [part5]

  //! [part7]
  string input_filename; 
  input_filename = "combine_input_XYH4b_v3.root";

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + input_filename,
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + input_filename,
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  //! [part8]
 
  auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(1.e-3)
    .SetFixNorm(true);
  bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  
  //! [part8]
  //
  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  // Finally we iterate through each bin,mass combination and write a datacard.
  char filename[100];
  for (auto m : signals) {
	sprintf(filename,"NMSSM_XYHto4b_2022_%s.input.root",m.c_str()); 
	TFile output(filename, "RECREATE");

	for (auto b : bins) {
		cout << ">> Writing datacard for bin: " << b << " and mass: " << m<< "\n";
		cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(b + "_" + m + ".txt", output);
	}
  }
  //! [part9]

}
