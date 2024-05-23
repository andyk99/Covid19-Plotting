import tarfile
import urllib.request
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import numpy as np
import sys

# Retrieve the COVID-19 death data for the US
urllib.request.urlretrieve("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/4360e50239b4eb6b22f3a1759323748f36752177/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv", 
                           "time_series_covid19_deaths_US.csv")

# Read the CSV file into a DataFrame
df_FileRead = pd.read_csv("time_series_covid19_deaths_US.csv")
df_FileRead = df_FileRead[df_FileRead["Province_State"] == "California"]
df_FileRead = df_FileRead.reset_index(drop=True)

# Extract date columns and calculate total cases per county
date_columns = df_FileRead.columns[12:]
total_cases_per_county = df_FileRead[date_columns].sum(axis=1)

# Initialize dot sizes for plotting
dot_size = [0] * len(df_FileRead)

# Define geographical bounds for California and filter dataframe to include entries within bounds
lon_min, lon_max, lat_min, lat_max = -124.55, -113.80, 32.45, 42.05
in_bounds = (df_FileRead["Long_"] > lon_min) & (df_FileRead["Long_"] < lon_max) & \
            (df_FileRead["Lat"] > lat_min) & (df_FileRead["Lat"] < lat_max)
filtered_df = df_FileRead[in_bounds]
filtered_dot_size = [(np.sqrt(total_cases)/40)**2 if in_bounds[i] else 0 for i, total_cases in enumerate(total_cases_per_county)]

# Plot the map of California with COVID-19 deaths per county
plt.figure(figsize=(26, 8))
plt.subplot(1, 2, 1)
plt.scatter(df_FileRead["Long_"], df_FileRead["Lat"], s=filtered_dot_size, c="royalblue", alpha=0.4)
california = mpimg.imread('california.png')
plt.imshow(california, extent=[lon_min, lon_max, lat_min, lat_max])
plt.ylabel("Latitude", fontsize=8, labelpad=8)
plt.xlabel("Longitude", fontsize=8, labelpad=8)
plt.title("Covid Deaths Per County in California", fontsize=18, pad=10)


# Plot COVID-19 daily deaths for a specific county and California
#if len(sys.argv) != 2: #1st arg is auto
#    print(f"Usage: {sys.argv[0]} <County Name>")
#    exit()
county_in = 'Los Angeles'
# county_in = sys.argv[1]
if county_in in df_FileRead['Admin2'].values:
    county_data = df_FileRead[(df_FileRead['Admin2'] == county_in) & (df_FileRead['Province_State'] == 'California')]
    county_daily_deaths = county_data.iloc[:, 12:].diff(axis=1).fillna(0).iloc[0].clip(lower=0)
    county_rolling_avg = county_daily_deaths.rolling(window=7).mean()

    california_data = df_FileRead[df_FileRead['Province_State'] == 'California']
    california_daily_deaths = california_data.iloc[:, 12:].diff(axis=1).sum(axis=0).fillna(0).clip(lower=0)
    california_rolling_avg = california_daily_deaths.rolling(window=7).mean()
else:
    raise ValueError(f"County '{county_in}' not in the dataset")
plt.subplot(1, 2, 2)
plt.fill_between(california_rolling_avg.index, california_rolling_avg, color='royalblue', alpha=0.3, label='California 7-Day Average')
plt.bar(county_daily_deaths.index, county_daily_deaths, color='red', alpha=0.8, label=f'{county_in} Daily Deaths')
plt.plot(county_rolling_avg.index, county_rolling_avg, color='red', label=f'{county_in} 7-Day Average')
plt.title(f"Covid Daily Deaths in {county_in} and CA", fontsize=18, pad=10)
plt.ylabel("Number of Deaths", fontsize=8, labelpad=8)
plt.xlabel("Date", fontsize=8, labelpad=8)
date_columns_str = df_FileRead.columns[12:].tolist() #List of date strings for incrementing the x axis ticks (prevent date blob)
selected_dates_str = date_columns_str[::75]
plt.xticks(selected_dates_str, rotation=45)
plt.text(-10, 900, f'California Total: {california_daily_deaths.sum()}', fontsize=8, color='black', verticalalignment='bottom', backgroundcolor='cornflowerblue')
plt.text(-10, 850, f'Los Angeles Total: {county_daily_deaths.sum()}', fontsize=8, color='black', verticalalignment='bottom', backgroundcolor='lightcoral')
plt.legend(loc='upper right')
plt.ylim(bottom=0)
plt.tight_layout(pad=9.0)
plt.show()
