from astropy.table import Table, join
import os
from astropy.io import ascii

folder_path = '/Users/griffonknox/PycharmProjects/SNe.Ori.Analysis/Calc.Data2/18cow'

#find each file in directory
ew_list = []
import glob
for filename in glob.glob(os.path.join(folder_path, '*ew.txt')):
    ew_list.append(filename)
ew_list.sort()


cont_list = []
import glob
for filename in glob.glob(os.path.join(folder_path, '*cont.txt')):
    cont_list.append(filename)
cont_list.sort()

cont_tables = []
ew_tables = []
for j,k in zip(ew_list, cont_list):
    ew_tables.append(Table.read(j ,format = 'ascii'))
    cont_tables.append(Table.read(k , format='ascii'))

n = 4
ew_final = [ew_tables[i * n:(i + 1) * n] for i in range((len(ew_tables) + n - 1) // n )]
cont_final = [cont_tables[i * n:(i + 1) * n] for i in range((len(cont_tables) + n - 1) // n )]
ew_list = [ew_list[i * n:(i + 1) * n] for i in range((len(ew_list) + n - 1) // n )]

sne_names = []
for i in ew_list:
    sne_names.append(i[0].split('/')[-1].split('.')[1])


master_ew = []
master_cont = []
for j, k in zip(ew_final, cont_final):
    a = join(j[0], j[1], keys = 'date')
    b = join(j[2], j[3], keys='date')
    c = join(k[0], k[1], keys = 'date')
    d = join(k[2], k[3], keys='date')
    master_ew.append(join(a, b, keys='date'))
    master_cont.append(join(c, d, keys='date'))

for j, k, l  in zip(master_cont, master_ew, sne_names):
    mg = (j['mg cont'] * k['mg ew'] * -1).quantity
    Hb = (j['Hb cont'] * k['Hb ew'] * -1).quantity
    OIII = (j['OIII cont'] * k['OIII ew'] * -1).quantity
    HeII = (j['HeII cont'] * k['HeII ew'] * -1).quantity
    NII = (j['NII cont'] * k['NII ew'] * -1).quantity
    HeI1 = (j['HeI1 cont'] * k['HeI1 ew'] * -1).quantity
    FeII1 = (j['FeII1 cont'] * k['FeII1 ew'] * -1).quantity
    OI1 = (j['OI1 cont'] * k['OI1 ew'] * -1).quantity
    Ha = (j['Ha cont'] * k['Ha ew'] * -1).quantity
    HeI2 = (j['HeI2 cont'] * k['HeI2 ew'] * -1).quantity
    HeI3 = (j['HeI3 cont'] * k['HeI3 ew'] * -1).quantity
    FeII2 = (j['FeII2 cont'] * k['FeII2 ew'] * -1).quantity
    HeI4 = (j['HeI4 cont'] * k['HeI4 ew'] * -1).quantity
    CaII = (j['CaII cont'] * k['CaII ew'] * -1).quantity
    FeII3 = (j['FeII3 cont'] * k['FeII3 ew'] * -1).quantity
    OI2 = (j['OI2 cont'] * k['OI2 ew'] * -1).quantity
    CI = (j['CI'] * k['CI ew'] * -1).quantity
    exp_data = Table([j['date'].quantity, mg,Hb, OIII,HeII,NII,HeI1,FeII1,OI1,Ha,HeI2,HeI3,FeII2,HeI4,CaII,FeII3,OI2,CI],
                        names=['date', 'mg','Hb','OIII','HeII','NII','HeI1','FeII1','OI1','Ha','HeI2','HeI3','FeII2','HeI4','CaII','FeII3','OI2','CI'])
    ascii.write(exp_data, l +'.txt', overwrite=True)







