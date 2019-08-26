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
ax.set_xlim(7000*u.AA, 9000*u.AA)
ax.grid(True)
wave = [7281, 7324, 7720, 8466, 8727]
for line in wave:
    plt.axvline(x = line)
plt.show()

#Identify the Region for flux extraction
region_list = [[7278, 7284],[7321, 7327],[7717, 7723],[8463, 8469], [8724, 8730]]

###input values to integrate EW through
input_list = []
input_list.append(input('HeI4 wavelengths:'))
input_list.append(input('CaII wavelengths:'))
input_list.append(input('FeII3 wavelengths:'))
input_list.append(input('OI2 wavelengths:'))
input_list.append(input('CI wavelengths:'))


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
ew5= []
for i in ew_list:
    ew1.append(np.mean(np.array(i[0])))
    ew2.append(np.mean(np.array(i[1])))
    ew3.append(np.mean(np.array(i[2])))
    ew4.append(np.mean(np.array(i[3])))
    ew5.append(np.mean(np.array(i[4])))

cont1 = []
cont2 = []
cont3 = []
cont4 = []
cont5 = []
for i in cont_lst:
    cont1.append(np.mean(np.array(i[0])))
    cont2.append(np.mean(np.array(i[1])))
    cont3.append(np.mean(np.array(i[2])))
    cont4.append(np.mean(np.array(i[3])))
    cont5.append(np.mean(np.array(i[4])))


exp_data_ew = Table([date_list, ew1, ew2, ew3, ew4, ew5], names=['date', 'HeI4 ew', 'CaII ew', 'FeII3 ew', 'OI2 ew', 'CI ew'])
ascii.write(exp_data_ew, sne_name +'.4.ew.txt', overwrite=True)

exp_data_cont = Table([date_list, cont1, cont2, cont3, cont4, cont5], names=['date', 'HeI4 cont', 'CaII cont', 'FeII3 cont', 'OI2 cont', 'CI'])
ascii.write(exp_data_cont, sne_name +'.4.cont.txt', overwrite=True)


