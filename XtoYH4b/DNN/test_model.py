#######################################################

# This script evaluates the model and shows the results 
# using an ROC curve and DNN score distribution.
# The tranfer factor (First method) are also created here.

# command to run this scripts:
# python3 test_model.py
# please check input and output file names before running

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import pandas as pd
import numpy as np
import mplhep as hep
import matplotlib.pyplot as plt
import ROOT
import sklearn.metrics as metrics
from hist.intervals import ratio_uncertainty
from tensorflow.keras.models import load_model


df_test = pd.read_csv("scaled_data.csv")
x_test = df_test.iloc[:, 1:].to_numpy()
y_test = df_test.iloc[:, 0].to_numpy()

model = load_model("model_v2.h5")

dnn_score = model.predict(x_test)

df_data = pd.read_csv("data.csv")
df_data["DNN_Score"] = dnn_score
df_data.to_csv("data_add_dnn_score_v2.csv", index=False)

dnn_signal = dnn_score[y_test == 1]
dnn_background = dnn_score[y_test == 0]

y_true = y_test
y_score = dnn_score[:, 0]

fpr, tpr, _ = metrics.roc_curve(y_true, y_score)
auc_score = metrics.auc(fpr, tpr)

hep.style.use("CMS")
fig, (ax, rax) = plt.subplots(2, 1, gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
hep.cms.label("Preliminary", data=True, loc=0, ax=ax) # com= , lumi=
ax.set_ylabel("Entries")
rax.set_xlabel("DNN Score")

bins = np.linspace(0, 1, 51)

hist_dnn_signal, _ = np.histogram(dnn_signal, bins=bins)
hist_dnn_background, _ = np.histogram(dnn_background, bins=bins)

hep.histplot([hist_dnn_background, hist_dnn_signal], bins=bins, ax=ax,
            stack=False, histtype='step', label=["Background", "Signal"])

# errps = {'hatch':'////', 'facecolor':'none', 'lw': 0, 'edgecolor': 'k', 'alpha': 0.5}
# hep.histplot(sum([hist_dnn_background, hist_dnn_signal]), histtype='band', ax=ax, **errps)
# hep.histplot(sum([hist_dnn_background, hist_dnn_signal]), histtype='band', ax=ax)

ratio = hist_dnn_signal / np.where(hist_dnn_background > 0, hist_dnn_background, 1)
# yerr_ratio = np.sqrt(hist_dnn_signal) / np.where(hist_dnn_background > 0, hist_dnn_background, 1) # need to correct

hep.histplot(ratio, bins=bins, ax=rax, 
            histtype='errorbar', color='k', capsize=2, label="Signal / Background")

# yerr_ratio_band = ratio_uncertainty(hist_dnn_signal, hist_dnn_background, 'poisson-ratio') # need to correct
# rax.stairs(1+yerr_ratio_band[1], baseline=1-yerr_ratio_band[0], **errps)

rax.axhline(1, ls='--', color='k')
rax.set_ylim(-1, 3)
ax.set_xlabel("")
ax.set_xlim(0, 1)
# ax.set_ylim(0, 6000)
ax.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
plt.savefig("DNN_score_v2.png", dpi=300, bbox_inches="tight")
plt.savefig("DNN_score_v2.pdf", bbox_inches="tight")
plt.close()

# plt.figure()
# hep.style.use("CMS")
# hep.cms.label("Preliminary", data=True, loc=0) # com= , lumi=
# plt.hist(dnn_background, bins=50, range=(0,1), histtype='step', color='blue', label="Background", density=False)
# plt.hist(dnn_signal, bins=50, range=(0,1), histtype='step', color='red', label="Signal", density=False)
# plt.xlabel("DNN Score")
# plt.ylabel("Entries")
# plt.legend()
# plt.savefig("DNN_score_test.png")
# plt.savefig("DNN_score_test.pdf")
# plt.close()

plt.figure()
hep.style.use("CMS")
hep.cms.label("Preliminary", data=True, loc=0) # com= , lumi=
plt.plot(fpr, tpr, color="blue", lw=2, label=f"ROC Curve (AUC = {auc_score:.3f})")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--", lw=1)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("Background Efficiency")
plt.ylabel("Signal Efficiency")
plt.legend(loc="lower right")
plt.savefig("ROC_curve_v2.png")
plt.savefig("ROC_curve_v2.pdf")
plt.close()

tf_file = ROOT.TFile("transfer_factor_v2.root", "RECREATE")
ratio_hist = ROOT.TH1D("ratio", "DNN Signal/Background Ratio", len(hist_dnn_signal), 0, 1)

for i in range(len(hist_dnn_signal)):
    ratio_hist.SetBinContent(i + 1, ratio[i])

ratio_hist.Write()
tf_file.Close()
