import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os
%pylab
# This is for inline plotting

project_path = os.path.realpath('.')

project_path
database_path = project_path + os.sep + 'Database' + os.sep
graph_path = project_path + os.sep + 'Analyse' + os.sep + 'Graph' + os.sep

df = pd.read_hdf(database_path + 'selected_df.h5','table')


#%%
# Create dictonary translation from original to new! (not the other way around)
headers = pd.read_excel(project_path + os.sep + 'General' + os.sep + 'headers_dict.xlsx')
# Load the data from the Excel-file with headers. Please not the project_path
# Create a list of each column, then a dictonary which is acting as the translotor.
old = headers['ORIGINAL_HEADER']
new = headers['NEW_HEADER']
d = {}
for n in range(len(old)):
    d[old[n]] = new[n]
    d[new[n]] = old[n] # To make it bi-directional

#%%

# creating histograms for all Datapoints and saving them

nr_bin=60

for i in list(df):
    series1 = df[i]
    plt.hist(series1,bins=nr_bin)
    plt.title((d[i]))
    plt.xlabel('Datapoints: ' + str(len(series1)) + ', bins: ' + str(nr_bin))
    plt.figtext(0.13,0.66,series1.describe(),alpha=0.8,fontsize=8)
    plt.savefig(graph_path + d[i])
    fig = matplotlib.pyplot.gcf() # higher res
    fig.set_size_inches(10,5) #higher res
    plt.clf()


#%%

# full year time series plotting for ship speed. resampling to one hour.

i1='SHIP_SPEED_KNOT_'
series1=df[d[i1]]
series1 = series1.resample('H').mean()
series1.plot(linewidth=0,marker='o')
plt.title(i1)
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()

#%%

# ships speed time series for each day average and both max and mean

i1='SHIP_SPEED_KNOT_'
series1=df[d[i1]]
speed_av = series1.resample('M').mean()
speed_max = series1.resample('M').max()
speed_av.plot(linewidth=0,marker='o')
speed_max.plot(linewidth=0,marker='*')
plt.title(i1 + ' average and maximum, Month')
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()

#%%
# Resample the speed for hour and make histogram over a year

nr_bin=linspace(0,21,22)
i1='SHIP_SPEED_KNOT_'
series1=df[d[i1]]
speed_av = series1.resample('H').mean()
plt.hist(speed_av,bins=nr_bin)
plt.title(i1)
plt.figtext(0.13,0.66,speed_av.describe(),alpha=0.8,fontsize=8)
plt.show()

#%%

# the total elecrical power in percentage of maximum capacity

nr_bin=50
i1='AE1_POWER_Wdot_OUT'
i2='AE2_POWER_Wdot_OUT'
i3='AE3_POWER_Wdot_OUT'
i4='AE4_POWER_Wdot_OUT'
series1=df[d[i1]]
series2=df[d[i2]]
series3=df[d[i3]]
series4=df[d[i4]]

tot_aux_power = (series1 + series2 + series3 + series4) / (2760 * 4)

plt.hist(tot_aux_power,bins=nr_bin)
#tot_aux_power = tot_aux_power.resample('H').mean()
#plt.hist(tot_aux_power,bins=nr_bin)

plt.title('total aux power percentage')
plt.figtext(0.13,0.66,tot_aux_power.describe(),alpha=0.8,fontsize=8)
plt.show()


#%%
# Time series plotting of total aux power

i1='AE1_POWER_Wdot_OUT'
i2='AE2_POWER_Wdot_OUT'
i3='AE3_POWER_Wdot_OUT'
i4='AE4_POWER_Wdot_OUT'
series1=df[d[i1]]
series2=df[d[i2]]
series3=df[d[i3]]
series4=df[d[i4]]

tot_aux_power = (series1 + series2 + series3 + series4) / (2760 * 4)
tot_aux_power_av = tot_aux_power.resample('D').mean()
tot_aux_power_max = tot_aux_power.resample('D').max()
tot_aux_power_av.plot(linewidth=0,marker='x')
tot_aux_power_max.plot(linewidth=0,marker='_')
plt.title('total aux power average and max/day')
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()

#%%

month='2014-04'

i1='AE1_POWER_Wdot_OUT'
i2='AE2_POWER_Wdot_OUT'
i3='AE3_POWER_Wdot_OUT'
i4='AE4_POWER_Wdot_OUT'
series1_mean=df[d[i1]].resample('D').mean()/2760
series2_mean=df[d[i2]].resample('D').mean()/2760
series3_mean=df[d[i3]].resample('D').mean()/2760
series4_mean=df[d[i4]].resample('D').mean()/2760

series1_max=df[d[i1]].resample('D').max()/2760
series2_max=df[d[i2]].resample('D').max()/2760
series3_max=df[d[i3]].resample('D').max()/2760
series4_max=df[d[i4]].resample('D').max()/2760

series1_mean[month].plot(marker='x',label=i1)
series2_mean[month].plot(marker='x',label=i2)
series3_mean[month].plot(marker='x',label=i3)
series4_mean[month].plot(marker='x',label=i4)

series1_max[month].plot(linewidth=0,marker='o',label=i1+' max')
series2_max[month].plot(linewidth=0,marker='o',label=i2+' max')
series3_max[month].plot(linewidth=0,marker='o',label=i3+' max')
series4_max[month].plot(linewidth=0,marker='o',label=i4+' max')

plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0.)

plt.title('aux engine average and max/day')
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()


#%%
nr_bin=50
i='AE1-TC_EG_T_OUT'

series2=df[d[i]]
series2 = series2[series2 > 0]
plt.hist(series2,bins=nr_bin)
plt.title((d[i]))
plt.xlabel('Datapoints: ' + str(len(series2)) + ', bins: ' + str(nr_bin))
plt.figtext(0.13,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.savefig(graph_path + d[i])
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()


#%%



i1='AE1-HT_FW_T_IN'
i2='AE1_POWER_Wdot_OUT'

series1=df[d[i1]]
series2=df[d[i2]]
series2= series2[series1 > 60]
series1= series1[series1 > 60]

plt.plot(series2,series1,linewidth=0,marker='x')
plt.title((d[i1]))
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()


#%%


i1='AE1-LOC_OIL_P_IN'
i2='AE1-LOC_OIL_T_OUT'

series1=df[d[i1]]
series2=df[d[i2]]
series2= series2[series1 > 0]
series1= series1[series1 > 0]
plt.plot(series2,series1,linewidth=0,marker='x')
plt.title((d[i1]))
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()


#%%



i='AE2-LT-CAC_FW_T_IN'

series2=df[d[i]]
series2 = series2[series2 > 0]
plt.hist(series2,bins=nr_bin)
plt.title((d[i]))
plt.xlabel('Datapoints: ' + str(len(series2)) + ', bins: ' + str(nr_bin))
plt.figtext(0.13,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.savefig(graph_path + d[i])
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()


#%%



i1='AE2-LT-CAC_FW_T_IN'
i2='AE1-LT-CAC_FW_T_IN'

series1=df[d[i1]]
series2=df[d[i2]]
series2= series2[series2 > 40]
series1= series1[series1 > 40]

plt.hist(series1,bins=nr_bin,alpha=0.5,color='r')
plt.hist(series2,bins=nr_bin,alpha=0.5)

plt.title((d[i]))
plt.xlabel('Datapoints: ' + str(len(series2)) + ', bins: ' + str(nr_bin))
plt.figtext(0.13,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.figtext(0,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.savefig(graph_path + d[i])
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()




#%%

#%%


i1='ER13-HT_FW_T_1'
i2='AE2-HT_FW_T_IN'

series1=df[d[i1]]
series2=df[d[i2]]
series2= series2[series2 > 40]
series1= series1[series1 > 40]

plt.hist(series1,bins=nr_bin,alpha=0.5,color='r')
plt.hist(series2,bins=nr_bin,alpha=0.5)

plt.title(i1 +' and ' + i2)
plt.xlabel('Datapoints: ' + str(len(series2)) + ', bins: ' + str(nr_bin))
plt.figtext(0.13,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.figtext(0.13,0.42,series2.describe(),alpha=0.8,fontsize=8)
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()

#%%






i1='AE1-LT-CAC_FW_T_IN'
i2='AE1-CAC_AIR_T_OUT'

series1=df[d[i1]]
series2=df[d[i2]]
series2= series2[series1 > 0]
series1= series1[series1 > 0]
plt.plot(series2,series1,linewidth=0,marker='x')
plt.plot(series1,series1)
plt.title((d[i1]))
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()




#%%


i1='AE2-LT-CAC_FW_T_IN'
i2='AE1-LT-CAC_FW_T_IN'
i1='AE2-LT-CAC_FW_T_IN'
i2='AE1-LT-CAC_FW_T_IN'

series1=df[d[i1]]
series2=df[d[i2]]
series1=df[d[i1]]
series2=df[d[i2]]


series2= series2[series2 > 40]
series1= series1[series1 > 40]
series2= series2[series2 > 40]
series1= series1[series1 > 40]



plt.hist(series1,bins=nr_bin,alpha=0.5,color='r')
plt.hist(series2,bins=nr_bin,alpha=0.5)

plt.title((d[i]))
plt.xlabel('Datapoints: ' + str(len(series2)) + ', bins: ' + str(nr_bin))
plt.figtext(0.13,0.66,series2.describe(),alpha=0.8,fontsize=8)
plt.figtext(0,0.66,series2.describe(),alpha=0.8,fontsize=8)
#plt.savefig(graph_path + d[i])
fig = matplotlib.pyplot.gcf() # higher res
fig.set_size_inches(10,5) #higher res
plt.show()
