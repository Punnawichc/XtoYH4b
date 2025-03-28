#include<stdio.h>
#include <bits/stdc++.h>
using namespace std;

void histjobmaker(bool isDATA=0, bool isSIGNAL=0, string year="2023")
{

string executable = "CutOptimizer";

string Filenames_MC[] = {
"TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
"TTto4Q_TuneCP5_13p6TeV_powheg-pythia8",
"TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8",
"TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
"TbarWplusto4Q_TuneCP5_13p6TeV_powheg-pythia8",
"TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8",
"TWminusto4Q_TuneCP5_13p6TeV_powheg-pythia8",
"TbarBQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8",
"TBbarQ_t-channel_4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8",
"Zto2Q-2Jets_PTQQ-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Zto2Q-2Jets_PTQQ-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-100to200_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-100to200_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-200to400_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-200to400_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-400to600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-400to600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-600_1J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"Wto2Q-2Jets_PTQQ-600_2J_TuneCP5_13p6TeV_amcatnloFXFX-pythia8",
"WWto4Q_TuneCP5_13p6TeV_powheg-pythia8",
"WZ_TuneCP5_13p6TeV_pythia8",
"ZZ_TuneCP5_13p6TeV_pythia8",
"ZZ_TuneCP5_13p6TeV_pythia8",
"QCD-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8",
"QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8"
};

// string Filenames_SIGNAL[] = {
// "NMSSM_XtoYHto4B_MX-300_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-300_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-300_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-400_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-400_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-400_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-400_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-650_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-650_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-650_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-650_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-650_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-900_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1200_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-1800_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-2500_MY-95_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-1000_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
// "NMSSM_XtoYHto4B_MX-4000_MY-95_TuneCP5_13p6TeV_madgraph-pythia8"
// };

string Filenames_SIGNAL[] = {
    "NMSSM_XtoYHto4B_MX-300_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-300_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-300_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-400_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-400_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-400_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-400_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-650_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-650_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-650_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-650_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-650_MY-80_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-500_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-900_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-300_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1200_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-300_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-1800_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-2500_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-1000_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-125_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-200_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-400_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-600_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-60_TuneCP5_13p6TeV_madgraph-pythia8",
    "NMSSM_XtoYHto4B_MX-4000_MY-90_TuneCP5_13p6TeV_madgraph-pythia8",
    };

vector<string> Filenames_Data;

if(year=="2022"){
Filenames_Data.push_back("Data_Run3_2022_C_JetHT");
Filenames_Data.push_back("Data_Run3_2022_C_JetMET");
Filenames_Data.push_back("Data_Run3_2022_D_JetMET");
}

string path = "/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/XtoYH4b/HistoMaker/";
string proxy = "/tmp/x509up_u81649";

fstream file_sub;
fstream file_local;
char name_submit[100], name_local[100];
if(isDATA){
sprintf(name_submit,"condor_submit_data.sh");
sprintf(name_local,"run_local_data.sh");
}
else{
sprintf(name_submit,"condor_submit.sh");
sprintf(name_local,"run_local.sh");
}
file_sub.open(name_submit,ios::out);
file_local.open(name_local,ios::out);

int nfile_data =  Filenames_Data.size();//  sizeof(Filenames_Data)/sizeof(Filenames_Data[0]);
int nfile_mc = sizeof(Filenames_MC)/sizeof(Filenames_MC[0]);
int nfile_sig = sizeof(Filenames_SIGNAL)/sizeof(Filenames_SIGNAL[0]);

vector<string> files;
if(isDATA){
for(int fg=0; fg<nfile_data; fg++){
files.push_back((Filenames_Data[fg]));
}
}
else{
if(isSIGNAL){
	for(int fg=0; fg<nfile_sig; fg++){
	files.push_back((Filenames_SIGNAL[fg]));
	}
}
else{
	for(int fg=0; fg<nfile_mc; fg++){
	files.push_back((Filenames_MC[fg]));
	}
}
}

int nfile = int(files.size());

for (int ii=0;ii<nfile;ii++)
{

fstream file;
char name_buffer[512];
sprintf(name_buffer,"execute_%s.csh",files[ii].c_str());
file.open(name_buffer,ios::out);
if(!file)
   {
       cout<<"Error in creating file!!!";
       //return 0;
   }

   file <<"#!/bin/bash\n";
   file << "source /cvmfs/cms.cern.ch/cmsset_default.sh\n";
   file <<"cd "<<path<<" \n";
   file<<"#export X509_USER_PROXY="<<proxy<<"\n";
   file<<"#cmssw-el7\n";
   file<<"eval `scram runtime -sh`\n";
   file<<"./"<<executable<<".exe  "<<isDATA<<" "<<isSIGNAL<<" "<<files[ii] << ".root "<<year<<'\n' ;

   cout<<"execute created successfully." << endl;
   file.close();

fstream file1;
char name_buffer1[512];
sprintf(name_buffer1,"submit_%s.sh",files[ii].c_str());
file1.open(name_buffer1,ios::out);
   if(!file1)
   {
       cout<<"Error in creating file!!!";
       //return 0;
   }
file1 << "universe = vanilla\n";
file1 << "executable = execute_"<< files[ii] << ".csh\n";
file1 << "getenv = TRUE\n";
file1 << "log = job_" << files[ii] << ".log\n";
file1 << "output = job_"<< files[ii] <<".out\n";
file1 << "error = job_"<< files[ii] <<".error\n";
file1 << "notification = never\n";
file1 << "should_transfer_files = YES\n";
file1 << "when_to_transfer_output = ON_EXIT\n";
file1 << "queue\n";
//file1 << "+JobFlavour = \"workday\"\n";
file1<< "+MaxRuntime = 100000\n";
cout<<"sub created successfully." << endl;
file1.close();

file_sub<<"condor_submit "<<name_buffer1<<"\n";
file_local<<"sh "<<name_buffer<<"\n";
}

file_sub.close();
  
//return 0;
}
