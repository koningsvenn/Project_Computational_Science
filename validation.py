import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

#load data
rain = pd.read_csv('validation_data_final/rainfall_climate_knowledge_portal.csv', delimiter=';')
humidity = pd.read_csv('validation_data_final/humidity.csv', delimiter=';')

#plot humidity vs rainfall per season
seasons = ['Summer', 'Fall', 'Winter', 'Spring']

#start subpolots
fig, axs = plt.subplots(2, 2, figsize=(22, 12))
fig.suptitle(f'Rainfall for different humidities per season', y =0.95)

#plot all seasons together
for season, ax in zip(seasons, axs.ravel()):
    ax.scatter(humidity[season], rain[season], label=season)
    ax.set_xlabel('relative humidity')
    ax.set_ylabel('rainfall [mm]')
    ax.set_title(season)
    
    #plot linear fit
    a, b = np.polyfit(humidity[season], rain[season], 1)
    ax.plot(humidity[season], a*humidity[season]+b, linestyle='--', linewidth=2)

plt.savefig(f'figures/validation')

#plot only one season
for season in seasons:
    plt.figure()
    plt.scatter(humidity[season], rain[season], label=season)
    plt.xlabel('relative humidity')
    plt.ylabel('rainfall [mm]')

    #plot linear fit
    a, b = np.polyfit(humidity[season], rain[season], 1)
    plt.plot(humidity[season], a*humidity[season]+b, linestyle='--', linewidth=2)

    plt.savefig(f'figures/validation_{season}')

