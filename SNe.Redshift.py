import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import os
from specutils import Spectrum1D
from astropy.visualization import quantity_support
quantity_support()

#input command for directory of files to open
folder_path = input('Input path to directory of SNe Data:')

#find each file in directory for application
file_list = []
date_list = []
import glob
for filename in glob.glob(os.path.join(folder_path, '*.txt')): #<-- change extension to open up desired documents
    file_list.append(filename)
    date_list.append(filename.split('_')[1])
file_list.sort()
date_list.sort()

#input command for redshift
redshift = float(input('Input Redshift of SNe:'))
z = 1 + redshift

#turn each file name into array
#apply obs to rest wavelength and flux conversion
#create list of spectrum files
data = []
for epoch in file_list:
    file = np.genfromtxt(fname= epoch)
    lamb = (file[:, 0] / z) * u.AA
    flux = file[:, 1] * 10 ** -15 * u.Unit('erg cm-2 s-1 AA-1')
    data.append(Spectrum1D(spectral_axis=lamb, flux=flux))

#plot specifics
desig = int(input('1 for entire list, or 2 for single observation.'))
if desig == 1:
    fig, ax1 = plt.subplots(figsize=(10, 8))
    for plot, num in zip(data, range(len(data))):
        ax1.step(plot.spectral_axis, plot.flux, label = date_list[num])

if desig == 2:
    print(date_list)
    index = int(input('Input index of desired observation:'))
    spec = data[index]
    fig, ax1 = plt.subplots(figsize=(10, 8))
    ax1.step(spec.spectral_axis, spec.flux, label=date_list[index])

#grid limits, legend, and vertical line identifiers
ax1.legend(loc = 'best', ncol = 2)
wave = [6562.8, 5876, 6678, 7065]
for line in wave:
    plt.axvline(x = line)
plt.xlim(4400*u.AA,9000*u.AA)
plt.grid(True)
plt.show()





