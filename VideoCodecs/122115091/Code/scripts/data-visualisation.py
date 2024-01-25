from matplotlib import pyplot as plt
import numpy as np

def visualise_pictures(dataframe, range, property, units='bytes'):
    plt.rcParams["figure.figsize"] = (14, 6)
    plt.rcParams["axes.grid"] = True
    COLOURS = { 'I': 'red', 'P':'green', 'B':'blue'}
    
    (start, end) = range
    plot_data = dataframe[start:end]
    
    plot_data.plot(x ='Number', y=property, kind='bar', color=plot_data['type'].replace(COLOURS), legend=False)
    plt.xlabel('Picture Number (display)')
    plt.ylabel(f'{property} ({units})')
    
    
    
def visualise_GOPs(dataframe, expected_gop_length, fps):
    plt.rcParams["figure.figsize"] = (14, 6)
    plt.rcParams["axes.grid"] = True
        
    gop_lengths = dataframe['Length']
    gop_sizes = dataframe['Size']
    gop_bitrates = dataframe['Bitrate']
    
    bars = plt.bar(x=range(0, len(gop_sizes)), height=gop_sizes)
    
    for i, bar in enumerate(bars):
        if gop_lengths[i] != expected_gop_length:
            bar.set_color('r')
    
    for i, v in enumerate(gop_sizes):
        tag_text = "GOP (" + str(gop_lengths[i]) + ")\n"  + str(round(gop_bitrates[i], 2)) + " Mbps"
        plt.text(i - 0.4, v, tag_text, color='black')
        
    plt.xlabel('GOP Number')
    plt.ylabel('Size (bytes)')
    
def visualise_GOP_bitrates(dataframe, maximum_bitrate, expected_gop_length, fps):
    plt.rcParams["figure.figsize"] = (14, 6)
    plt.rcParams["axes.grid"] = True
        
    gop_lengths = dataframe['Length']
    gop_sizes = dataframe['Size']
    gop_bitrates = dataframe['Bitrate']
    
    average_bitrate = np.mean(gop_bitrates)

    above_threshold = np.maximum(gop_bitrates - maximum_bitrate, 0)
    below_threshold = np.minimum(gop_bitrates, maximum_bitrate)

    fig, ax = plt.subplots()
    ax.bar(range(0, len(gop_sizes)), below_threshold, 0.35, color="g")
    ax.bar(range(0, len(gop_sizes)), above_threshold, 0.35, color="r", bottom=below_threshold)
    
    ax.plot([0, len(gop_sizes)], [maximum_bitrate, maximum_bitrate], "-", color='black')
    ax.plot([0, len(gop_sizes)], [average_bitrate, average_bitrate], "k--")
    
    ax.text(len(gop_sizes), maximum_bitrate, str(round(maximum_bitrate, 2)) + "Mbps")
    ax.text(len(gop_sizes), average_bitrate, str(round(average_bitrate, 2)) + "Mbps")
        
    plt.xlabel('GOP Number')
    plt.ylabel('Bitrate (Mbps)')
    plt.xticks(range(0, len(gop_sizes)))

