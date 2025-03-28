import uproot
import awkward as ak
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import mplhep as hep
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import StandardScaler
from hist.intervals import ratio_uncertainty
from tensorflow.keras.models import load_model

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

df_background = df_background.iloc[:len(df_signal), :]

df_signal.insert(0, "signal", 1)
df_background.insert(0, "signal", 0)

print(f"signal: {len(df_signal)}")
print(f"background: {len(df_background)}")

df_signal_background = pd.concat([df_signal, df_background], axis=0)

df_train, df_test = train_test_split(df_signal_background, test_size=0.2, random_state=1234)
x_train, y_train  = df_train.iloc[:, 1:], df_train.iloc[:, 0]
x_test, y_test    = df_test.iloc[:, 1:], df_test.iloc[:, 0]

x_train, y_train = x_train.to_numpy(), y_train.to_numpy()
x_test, y_test   = x_test.to_numpy(), y_test.to_numpy()

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

## Model

# model = tf.keras.models.Sequential([
# tf.keras.layers.Flatten(input_shape=(len(x_train[0]),)),
# tf.keras.layers.Dense(128, activation='relu'),
# # tf.keras.layers.Dropout(0.2),
# tf.keras.layers.Dense(64, activation='relu'),
# tf.keras.layers.Dense(1, activation='sigmoid')
# ])

# model.compile(optimizer=Adam(learning_rate=0.0001),
#             loss='binary_crossentropy',
#             metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=10)
# model.evaluate(x_test, y_test)

# model.save("model.h5")

model = load_model("model.h5")

dnn_score = model.predict(x_test)

# dnn_signal = dnn_score[:, 0]
# dnn_background = 1 - dnn_signal

dnn_signal = dnn_score[y_test == 1]
dnn_background = dnn_score[y_test == 0]

# use for output layer dense 2
# dnn_signal = dnn_score[:, 1]
# dnn_background = dnn_score[:, 0]

y_true = y_test
# y_scores = np.argmax(dnn_score, axis=1)
y_score = dnn_score[:, 0]

fpr, tpr, _ = metrics.roc_curve(y_true, y_score)
auc_score = metrics.auc(fpr, tpr)

hep.style.use("CMS")
fig, (ax, rax) = plt.subplots(2, 1, gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
hep.cms.label("Preliminary", data=True, loc=0, ax=ax) # com= , lumi=
ax.set_ylabel("Entries")
rax.set_xlabel("DNN Score")

bins = np.linspace(0, 1, 51)

hist_dnn_signal = np.histogram(dnn_signal, bins=bins)[0]
hist_dnn_background = np.histogram(dnn_background, bins=bins)[0]

hep.histplot(
    [hist_dnn_background, hist_dnn_signal],
    bins=bins,
    ax=ax,
    stack=False,
    histtype='fill',
    label=["Background", "Signal"]
)

errps = {'hatch':'////', 'facecolor':'none', 'lw': 0, 'edgecolor': 'k', 'alpha': 0.5}
hep.histplot(sum([hist_dnn_background, hist_dnn_signal]), histtype='band', ax=ax, **errps)

ratio = hist_dnn_signal / np.where(hist_dnn_background > 0, hist_dnn_background, 1)
yerr_ratio = np.sqrt(hist_dnn_signal) / np.where(hist_dnn_background > 0, hist_dnn_background, 1) # need to correct

hep.histplot(ratio, bins=bins, yerr=yerr_ratio, ax=rax, 
             histtype='errorbar', color='k', capsize=2, label="Signal / Background")

yerr_ratio_band = ratio_uncertainty(hist_dnn_signal, hist_dnn_background, 'poisson-ratio') # need to correct
rax.stairs(1+yerr_ratio_band[1], baseline=1-yerr_ratio_band[0], **errps)

rax.axhline(1, ls='--', color='k')
rax.set_ylim(-1, 3)
ax.set_xlabel("")
ax.set_xlim(0, 1)
ax.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
plt.savefig("DNN_score.png", dpi=300, bbox_inches="tight")
plt.savefig("DNN_score.pdf", bbox_inches="tight")
plt.close()


# hep.style.use("CMS")
# hep.cms.text("Preliminary", loc=0)

# plt.figure()
# plt.hist(dnn_signal, bins=50, range=(0,1), histtype='step', color='red', label="Signal", density=False)
# plt.hist(dnn_background, bins=50, range=(0,1), histtype='step', color='blue', label="Background", density=False)
# plt.xlabel("DNN Score")
# plt.ylabel("Entries")
# plt.legend()
# plt.savefig("DNN_score.png")
# plt.savefig("DNN_score.pdf")
# plt.close()

# plt.figure()
# plt.plot(fpr, tpr, color="blue", lw=2, label=f"ROC Curve (AUC = {auc_score:.3f})")
# plt.plot([0, 1], [0, 1], color="gray", linestyle="--", lw=1)
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel("Background Efficiency")
# plt.ylabel("Signal Efficiency")
# plt.legend(loc="lower right")
# plt.savefig("ROC_curve.png")
# plt.savefig("ROC_curve.pdf")
# plt.close()
