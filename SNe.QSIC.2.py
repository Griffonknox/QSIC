import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
import os
from astropy.visualization import quantity_support
quantity_support()
from specutils.fitting import fit_generic_continuum
from specutils import SpectralRegion, Spectrum1D
from specutils.analysis import equivalent_width
from specutils.manipulation import extract_region
from astropy.table import Table
from astropy.io import ascii

#input command for directory of files to open
folder_path = input('Input path to directory of SNe Data:')

#find each file in directory
file_list = []
date_list = []
import glob
for filename in glob.glob(os.path.join(folder_path, '*.flm')):
    file_list.append(filename)
    date_list.append(filename.split('-')[1])
file_list.sort()
date_list.sort()
sne_name = folder_path.split('/')[-1]

#input command for redshift
redshift = float(input('Input Redshift of SNe:'))
z = 1 + redshift

#turn each file name into array
#apply obs to rest wavelength and flux conversion
#create list of spectrum files, and continuum files
cont_list = []
data = []
for epoch in file_list:
    file = np.genfromtxt(fname= epoch)
    lamb = (file[:, 0] / z) * u.AA
    flux = file[:, 1] * 10 ** -15 * u.Unit('erg cm-2 s-1 AA-1')
    spec = Spectrum1D(spectral_axis=lamb, flux=flux)
    data.append(spec)
    cont_list.append((spec /spec) * fit_generic_continuum(spec)(spec.spectral_axis))


#plot to find the lines to calculate EW
spcplt = data[0]
cntplt = cont_list[0]
f, ax = plt.subplots()
ax.step(spcplt.wavelength, spcplt.flux)
ax.step(cntplt.wavelength, cntplt.flux)
ax.set_xlim(5650*u.AA, 6500*u.AA)
ax.grid(True)
wave = [5755, 5876, 6248, 6300]
for line in wave:
    plt.axvline(x = line)
plt.show()

#Identify the Region for flux extraction
region_list = [[5752,5758],[5873,5879],[6245,6251],[6297,6303]]

###input values to integrate EW through
input_list = []
input_list.append(input('NII wavelengths:'))
input_list.append(input('HeI1 wavelengths:'))
input_list.append(input('FeII1 wavelengths:'))
input_list.append(input('OI1 wavelengths:'))


ew_list = []
cont_lst = []
##iterate through each observation to calculate Intensity.
for cont,spec in zip(cont_list,data):
    ew_iter = []
    cont_iter = []
    for inp ,region in zip(input_list,region_list):
        cont_iter.append(extract_region(cont, SpectralRegion(region[0] * u.AA, region[1] * u.AA)).flux)
        ew_iter.append(equivalent_width(spec, regions=SpectralRegion(int(inp.split(' ')[0]) * u.AA, int(inp.split(' ')[1]) * u.AA), continuum=extract_region(cont, SpectralRegion(region[0] * u.AA, region[1] * u.AA)).flux))
    ew_list.append(ew_iter)
    cont_lst.append(cont_iter)


ew1 = []
ew2 = []
ew3 = []
ew4 = []
for i in ew_list:
    ew1.append(np.mean(np.array(i[0])))
    ew2.append(np.mean(np.array(i[1])))
    ew3.append(np.mean(np.array(i[2])))
    ew4.append(np.mean(np.array(i[3])))

cont1 = []
cont2 = []
cont3 = []
cont4 = []
for i in cont_lst:
    cont1.append(np.mean(np.array(i[0])))
    cont2.append(np.mean(np.array(i[1])))
    cont3.append(np.mean(np.array(i[2])))
    cont4.append(np.mean(np.array(i[3])))


exp_data_ew = Table([date_list, ew1, ew2, ew3, ew4], names=['date', 'NII ew', 'HeI1 ew', 'FeII1 ew', 'OI1 ew'])
ascii.write(exp_data_ew, sne_name +'.2.ew.txt', overwrite=True)

exp_data_cont = Table([date_list, cont1, cont2, cont3, cont4], names=['date', 'NII cont', 'HeI1 cont', 'FeII1 cont', 'OI1 cont'])
ascii.write(exp_data_cont, sne_name +'.2.cont.txt', overwrite=True)


