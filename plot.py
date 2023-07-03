import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
import pandas as pd 
import matplotlib.ticker as ticker
import sys 
import argparse

def band_structure_gen(file_path):
    """ reads in """
    with open(file_path, "r") as f:
        lines = f.readlines()
    data = [[[],[]]]
    counter = 0 
    for index, line in enumerate(lines):
        row_data = line.strip() 
        if row_data == "":
            counter += 1 
            data.append([[],[]])
            continue 
        row_data = row_data.split()
        if row_data[0] == '#k-distance':
            continue 
        data[counter][0].append(float(row_data[0]))
        data[counter][1].append(float(row_data[1]))
    
    return data 

def remove_bands_energy_range(data, E_min, E_max):
    """ removes bands with energies outside of this range """
    data_new = [[[], []]]
    counter = 0 
    for deets in data:
        if deets[1] == []:
            continue 
        max_value = max(deets[1])
        min_value = min(deets[1])
        
        if max_value > E_max + 5 or min_value < E_min - 5:
            continue 
        else: 
            data_new[counter][0] = deets[0]
            data_new[counter][1] = deets[1]
            counter += 1 
            data_new.append([[],[]])
    return data_new

def plot_bands_new(data, fermi_energy, E_min, E_max, kspacing = 30, struct = 'full', colormap = "viridis", kpath = 'MGM', filename = 'eucd2as2'):
    
    plt.clf()
    # generate colors 
    n_bands = len(data)
    colors = plt.get_cmap(colormap, n_bands)
    if colormap == "YlGnBu":
        colors = colors.reversed()
    custom_palette = [mpl.colors.rgb2hex(colors(i)) for i in range(colors.N)]
    
    for index, deets in enumerate(data):
        y_axis = [x - fermi_energy for x in deets[1]]
        plt.plot(deets[0], y_axis, color = custom_palette[index], linewidth = 1.5)
    
    plt.ylabel("E - E$_F$ (eV)")
    plt.ylim(E_min - fermi_energy, E_max - fermi_energy)
    plt.xlim(0.0, data[0][0][-1])
                             
    # plotting horizontal line fermi 
    data_length = len(data[0][0])
    y_zeros = np.zeros(data_length)
    plt.plot(data[0][0], y_zeros, linestyle = '--', color = 'black', linewidth = 1)
    
    # plotting vertical lines 
    midpoint = (data[0][0][-1] - data[0][0][0])/2
    
    #x_zeros = np.zeros(data_length)
    x_mids = np.full(data_length, midpoint)
    #x_last = np.full(data_length, data[0][0][-1])
    
    y_vals = np.linspace(E_min - fermi_energy, E_max - fermi_energy, data_length)
    

    width = data[0][0][-1] - data[0][0][0]
    height = E_max - E_min
    if struct == 'Full':
        plt.gca().set_aspect(width/height * 1.25)
    else:
        plt.gca().set_aspect(width/height/2)
        
    if kpath == 'NAN':
        pass 
    else: 
        labels = [] 
        xticks_location = [] 
        for index, point in enumerate([*kpath]):
            if index == 0:
                x_vals = np.full(data_length, data[0][0][0])
                plt.plot(x_vals, y_vals, color = 'black', linewidth = 1)
                if point == 'G':
                    labels.append("$\Gamma$")
                else:
                    labels.append(point)
                xticks_location.append(data[0][0][0])
            else:
                x_vals = np.full(data_length, data[0][0][index * kspacing -1])
                plt.plot(x_vals, y_vals, color = 'black', linewidth = 1)
                if point == 'G':
                    labels.append("$\Gamma$")
                else:
                    labels.append(point)
                xticks_location.append(data[0][0][index * kspacing - 1])                
        plt.gca().set_xticks(xticks_location)
        plt.gca().set_xticklabels(labels)
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(1))
    
    plt.savefig(filename + '_' + kpath + '.pdf', bbox_inches = 'tight')
    #plt.show()
    
def plot_bandstructure(file_path, fermi_energy, E_min, E_max, kspacing, struct, kpath = 'MGM', filename = 'eucd2as2', colormap = 'viridis'):
    data = band_structure_gen(file_path)
    data = remove_bands_energy_range(data, E_min, E_max)
    plot_bands_new(data, fermi_energy, E_min, E_max, kspacing, struct, colormap, kpath, filename)



def _get_parser():
    """ parser function """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--filepath"
    )

    parser.add_argument(
        "--fermi_energy",
        default = 0.0,
    )

    parser.add_argument(
        "--E_min",
        default = -3
    )

    parser.add_argument(
        "--E_max", 
        default = 1
    )

    parser.add_argument(
        "--kspacing",
        default = 45 
    )

    parser.add_argument(
        "--struct", 
        default = "full"
    )

    parser.add_argument(
        "--colormap",
        default = 'viridis'
    )

    parser.add_argument(
        "--kpath",
        default = 'GMKGALHA'
    )

    parser.add_argument(
        "--filename"
    )
    return parser 

def main():
    args = _get_parser().parse_args()
    plot_bandstructure(
        file_path=args.filepath,
        fermi_energy=args.fermi_energy, 
        E_min=args.E_min,
        E_max=args.E_max, 
        struct=args.struct, 
        kpath=args.kpath, 
        kspacing = args.kspacing,
        filename=args.filename,
        colormap=args.colormap
    )



if __name__ == "__main__":
    main()




