import os
import uproot
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd

input_path = "/data/dust/user/chokepra/XtoYH4b/HistoMaker/output_adding_dnn_score/2022"
output_path = "/data/dust/user/chokepra/XtoYH4b/HistoMaker/output_adding_dnn_score/2022"

for file in os.listdir(input_path):
    if file.startswith("Histogram_"):
        file_path = os.path.join(input_path, file)
        f = uproot.open(file_path)

        tree = f["DNNFeatureTree"]
        
        branches = ["jetAK4_pt_1", "jetAK4_pt_2", "jetAK4_pt_3", "jetAK4_pt_4",
                    "jetAK4_eta_1", "jetAK4_eta_2", "jetAK4_eta_3", "jetAK4_eta_4",
                    "jetAK4_phi_1", "jetAK4_phi_2", "jetAK4_phi_3", "jetAK4_phi_4",
                    "jetAK4_mass_1", "jetAK4_mass_2", "jetAK4_mass_3", "jetAK4_mass_4",]

        df = tree.arrays(branches, library="pd")

        scaler_mean = np.array([
            113.5630, 112.0937, 106.3473, 110.2283,
            0.0041, 0.0057, 0.0195, 0.0009,
            0.0078, 0.0039, -0.0165, 0.0057,
            13.6675, 14.2124, 14.4676, 14.2592
        ])

        scaler_std = np.array([
            65.3103, 67.5320, 75.5511, 77.3119,
            1.0533, 1.1009, 1.3459, 1.2973,
            1.8219, 1.8181, 1.8219, 1.8116,
            7.8249, 8.2738, 8.9954, 8.5319
        ])

        features = df.to_numpy()

        features = (features - scaler_mean) / scaler_std

        model = load_model("/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/XtoYH4b/DNN/model_v2.h5")

        # scores from Python framework
        dnn_scores = model.predict(features)

        out_file = os.path.join(output_path, file_path.replace("Histogram_", "DNNScore_"))
        with uproot.recreate(out_file) as fout:
            fout["DNNScoreTree"] = {"DNN_score": dnn_scores}

        # obtains the scores from C++ framework
        score_tree = f["JetTree"]

        df_scores = score_tree.arrays(["DNN_score"], library="pd")

        # scores from C++ framework
        arr_scores = df_scores.to_numpy()

        # comparison
        diff = np.abs(arr_scores - dnn_scores)
        print("Max diff:", np.max(diff))

