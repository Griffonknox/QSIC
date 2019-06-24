def spectra_plot(name):
    import json
    import pandas as pd
    import matplotlib.pyplot as plt


    file_name = name + '.json'

    with open(file_name, "r") as read_file:
        sne_data = json.load(read_file)

    # select specific data
    sne_data2 = sne_data[name]
    sne_spectra = sne_data2['spectra']

    #Create empty df to append to
    sne_df = pd.DataFrame(columns=['wave', 'flux', 'error', 'time'])

    #iterate through each epoch
    for epoch in sne_spectra:
        sne_epoch = epoch['data']
        if len(sne_epoch[0]) == 3:
            dfObj = pd.DataFrame(sne_epoch, columns=['wave', 'flux', 'error'])
            dfObj3 = dfObj.astype(float)
            dfObj3['time'] = epoch['time']
            sne_df = sne_df.append(dfObj3)

        if len(sne_epoch[0]) == 2:
            dfObj = pd.DataFrame(sne_epoch, columns=['wave', 'flux'])
            dfObj3 = dfObj.astype(float)
            dfObj3['error'] = ''
            dfObj3['time'] = epoch['time']
            sne_df = sne_df.append(dfObj3)

    fig, ax = plt.subplots(figsize=(12, 8))

    sne_df.groupby('time').plot(kind='line', x="wave", y="flux", ax=ax, legend=False)
    plt.title(name)
    plt.ylabel('Flux (ergs/s/cm^2)')
    plt.xlabel('Wavelength (Angstroms)')


    return plt.show()


#print(spectra_plot('SN2005gj'))