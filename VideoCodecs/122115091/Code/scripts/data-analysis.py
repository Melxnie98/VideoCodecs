import pandas as pd
import numpy as np

def create_dataframe(psnr_file, ssim_file, probe_file):
    psnr_raw = pd.read_csv(psnr_file, sep="\s+|;|:", header=None, engine="python")
    psnr_filtered = psnr_raw.iloc[:, [1,3,11]]
    psnr_filtered.columns = ["Number", "MSE", "PSNR"]

    ssim_raw = pd.read_csv(ssim_file, sep="\s+|;|:", header=None, engine="python")
    ssim_filtered = ssim_raw.iloc[:, [1,9]]
    ssim_filtered.columns = ["Number", "SSIM"]

    metrics = pd.merge(left=psnr_filtered, right=ssim_filtered, left_on='Number', right_on='Number')

    probe_raw = pd.read_csv(probe_file, sep=",", header=None, engine="python")
    probe_filtered = probe_raw[probe_raw[0]=='frame'].iloc[:,[13,18,19,20]]
    probe_filtered.columns = ["size","type","coding", "Number"]
    probe_filtered["Number"] = probe_filtered.index + 1

    return pd.merge(left=metrics, right=probe_filtered, left_on='Number', right_on='Number')
    
    
def create_GOP_dataframe(dataframe, fps):
    gop_lengths = np.diff(dataframe[dataframe['type'] == 'I']['Number'])
    gop_lengths = np.append(gop_lengths, dataframe.iloc[-1]['Number'] - dataframe[dataframe['type'] == 'I'].iloc[-1]['Number'] + 1)
    # + 1 to count the last picture in the shortened GOP
    
    gop_sizes = []
    start = 0
    
    for gop_l in gop_lengths:
        gop_sizes.append(sum(dataframe[start:start+gop_l]['size']))
        start += gop_l
    
    columns = ['Number', 'Length', 'Duration', 'Size', 'Bitrate']
    data = []
    
    for i, gop_size in enumerate(gop_sizes):
        record = [(i+1), gop_lengths[i], gop_lengths[i] / fps, gop_size, gop_size * 8 / (gop_lengths[i] / fps) / 1e6]
        data.append(record)
 
    return pd.DataFrame(data, columns=columns)
        