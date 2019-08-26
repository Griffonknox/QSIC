# Sne_Spectra
This Read Me is an attempt to help the user walk through the process that was implmented for Spectral SNe Analysis in Summer 2019.  STSci Summer internship

Contents:
1. Red Shift Calibration
2. Emission Calculations
3. Intensity Computation

Before completeing steps, organize by putting all observations of SNe into one directory and one directory per SNe.

1. This step is used to plot the spectra and confirm the accurate redshift and rest wavelength obtained.  This can be skipped if confidently known.
  -Using code; SNe.Redshift.py
  -Execute Code - > directory input. (ex. /Users/Documents/SNe.Analysis/Data) Note* Can change file extesion type on line 16
    -> designate one or all observations -> plot generated.
   
 **Here you can use the vertical lines which are identifying Helium and H-alpha lines to confirm accurate rest wavelength.
 
 2. This step is the process of using Q-SIC and is accompanied by 4 different codes that distribute 17 emission lines of interest.  Repeat Steps for each code.
  -Using codes; SNe.QSIC.1.py - SNe.QSIC.4.py
  -Execute Code - > Directory input. (ex. /Users/Documents/SNe.Analysis/Data)
    -> code will generate plot with vertical lines identifying the 4-3 emisson lines of interest.  Use this to identify the start and end wavelengths to run the calculator.
    -> Next Code will designate and ask for the input of identified start/end wavelengths.  Note* Input needs to be with a space between the two wavelengths and in Angstroms. (ex. 6563 7410)
    -> code will automatically output the calcuation of Equivalent Width and Continuum in two seperate .txt files.
    
  **It is important to know that there must be data in the identified wavelengths or the code will throw a warning.
    
  3. This final step takes the out put files from step 2, runs the computation to calculate the Intesity.
  
