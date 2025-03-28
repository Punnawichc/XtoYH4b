#######################################################

# This script extracts data from a ROOT file and converts it into a DataFrame format. 
# It applies signal and background selection cuts, as well as standard scaling using StandardScaler. 
# The data is then split into various sets, particularly training and testing datasets.

# command to run this scripts:
# python3 prepare_data.py

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################


import uproot
import awkward as ak
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


input_path = "/data/dust/user/chatterj/XToYHTo4b/SmallNtuples/Analysis_NTuples/2022/Data_Run3_2022_C_JetMET.root"

f = uproot.open(input_path)

tree = f["Tout"]

columns_jetAK4 = ["JetAK4_btag_PNetB_WP", "JetAK4_pt", "JetAK4_eta", "JetAK4_phi", "JetAK4_mass"]

ak_array = tree.arrays(columns_jetAK4, library="ak")

# df = df[columns_jetAK4]

njets = 4
df_dict = {f"{col}_{i+1}": ak.to_list(ak_array[col][:, i]) for col in columns_jetAK4 for i in range(njets)}

# data = {col: [[row[ijet] for row in df[col]] for ijet in range(njets)] for col in columns_jetAK4}

# columns_data = [["JetAK4_btag_PNetB_WP_1", "JetAK4_btag_PNetB_WP_2", "JetAK4_btag_PNetB_WP_3", "JetAK4_btag_PNetB_WP_4"],
#                 ["JetAK4_pt_1", "JetAK4_pt_2", "JetAK4_pt_3", "JetAK4_pt_4"],
#                 ["JetAK4_eta_1", "JetAK4_eta_2", "JetAK4_eta_3", "JetAK4_eta_4"],
#                 ["JetAK4_phi_1", "JetAK4_phi_2", "JetAK4_phi_3", "JetAK4_phi_4"],
#                 ["JetAK4_mass_1", "JetAK4_mass_2", "JetAK4_mass_3", "JetAK4_mass_4"]]

# df_data = pd.DataFrame()
# i = 0
# for idx_obj, obj in enumerate(data.values()):
#     for idx_col, col in enumerate(obj):
#         df_data.insert(i, columns_data[idx_obj][idx_col], col)
#         i += 1

df_data = pd.DataFrame(df_dict)

df_signal = df_data[(df_data["JetAK4_btag_PNetB_WP_1"] >= 3) &
                    (df_data["JetAK4_btag_PNetB_WP_2"] >= 3) &
                    (df_data["JetAK4_btag_PNetB_WP_3"] >= 2) &
                    (df_data["JetAK4_btag_PNetB_WP_4"] < 2)]

df_background = df_data[(df_data["JetAK4_btag_PNetB_WP_1"] >= 3) &
                        (df_data["JetAK4_btag_PNetB_WP_2"] >= 3) &
                        (df_data["JetAK4_btag_PNetB_WP_3"] < 2) &
                        (df_data["JetAK4_btag_PNetB_WP_4"] < 2)]

# df_background = df_data[~df_data.index.isin(df_signal.index)]

df_signal = df_signal.drop(columns=["JetAK4_btag_PNetB_WP_1", 
                                    "JetAK4_btag_PNetB_WP_2", 
                                    "JetAK4_btag_PNetB_WP_3", 
                                    "JetAK4_btag_PNetB_WP_4"])

df_background = df_background.drop(columns=["JetAK4_btag_PNetB_WP_1", 
                                            "JetAK4_btag_PNetB_WP_2", 
                                            "JetAK4_btag_PNetB_WP_3", 
                                            "JetAK4_btag_PNetB_WP_4"])

# df_background = df_background.iloc[:len(df_signal), :]

df_signal.insert(0, "signal", 1)
df_background.insert(0, "signal", 0)

print(f"signal: {len(df_signal)}")
print(f"background: {len(df_background)}")

df_signal_background = pd.concat([df_signal, df_background], axis=0, ignore_index=True)

df_signal_background.to_csv("data.csv", index=False)

features = df_signal_background.iloc[:, 1:].to_numpy()

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

df_features_scaled = pd.DataFrame(features_scaled)
df_signal_background_scaled = pd.concat([df_signal_background.iloc[:, 0], df_features_scaled], axis=1, ignore_index=True)
print(df_signal_background_scaled)

df_signal_background_scaled.to_csv("scaled_data.csv", index=False)

df_signal_ = df_signal_background_scaled[df_signal_background_scaled.iloc[:, 0] == 1]
df_background_ = df_signal_background_scaled[df_signal_background_scaled.iloc[:, 0] == 0]
df_background_ = df_background_.iloc[:len(df_signal_), :]
df_signal_background_scaled_ = pd.concat([df_signal_, df_background_], axis=0, ignore_index=True)

df_train, df_test = train_test_split(df_signal_background_scaled_, test_size=0.2, random_state=1234)
df_train.to_csv("train_data.csv", index=False)
df_test.to_csv("test_data.csv", index=False)
