# %%
import h5py
import numpy as np
import pandas as pd
from pathlib import Path
from skimage import io,util,measure
from organelle_measure.tools import batch_apply

def postprocess_mito(path_in,path_out):
    with h5py.File(str(path_in),'r') as f_in:
        img_in = f_in["exported_data"][:]
    img_in = (img_in[1]>img_in[0])
    img_out = measure.label(img_in)
    io.imsave(
        str(path_out),
        util.img_as_uint(img_out)
    )
    return None

# %%
folders = [
    "EYrainbow_glucose",
    "EYrainbow_glucose_largerBF",
    "EYrainbow_rapamycin_1stTry",
    "EYrainbow_rapamycin_CheckBistability",
    "EYrainbow_1nmpp1_1st",
    "EYrainbowWhi5Up_betaEstrodiol",
    "EYrainbow_leucine_large",
    "EYrainbow_leucine"
]
folder_i = "./images/preprocessed/"
fodler_o = "./images/labelled/"

# %%
list_i = []
list_o = []

for path_binary in Path("images/preprocessed/paperRebuttal").glob("probability_mito*.h5"):
    path_output = Path("images/labelled/paperRebuttal")/f"label-{path_binary.stem.partition('_')[2]}.tiff"
    list_i.append(path_binary)
    list_o.append(path_output)
args = pd.DataFrame({
    "path_in":  list_i,
    "path_out": list_o
})
# %%
batch_apply(postprocess_mito,args)
# %%
