import requests
import pandas as pd
import json
import numpy as np
from datetime import datetime
api_token = 'jFwqjbvAfnuMrlNwENGxuAhvpPskYhsA'

# TO RUN:
# DIR: Documents/Barefoot_Files/Bayer_Crop_Science/MMM/Weather_Data/weather_api
# conda activate MMM
# python weather_script.py
# Current Inputs: GHCND:USW00023129,GHCND:US1CALA0064


# HELPER
def get_average_temp(station_code):
    # Creates Arrays and Dataframe for data to be placed
    dates = []
    temps = []

    # Go through each stations and pull data for years 2015 to 2020 (inclusive)
    for year in range(2015, 2020):
        year = str(year)
        print('WORKING ON YEAR ' + year + ' FOR CODE ' + station_code + '...')

        # Make the API call for each year
        r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid=' +
                         station_code+'&startdate=' + year+'-01-01&enddate='+year+'-12-31', headers={'token': api_token})

        # Make sure the result set is not empty
        if len(r.json().keys()) == 0:
            continue
        else:
            # Load the API response as a json
            data = r.json()['results']
        # Get all items in the response which are average temperature readings
        avg_temps = filter(lambda temp: temp['datatype'] == 'TAVG', data)

        for avg_temp in avg_temps:
            # Add the average temperature date to the dates list
            # Format date as year, month, day (e.g., 2019-12-05)
            date = avg_temp['date']
            dates.append(date)
            # Add the average temperature value to the temps list
            # Format temperature in Fahrenheit
            temp = float(avg_temp['value'])/10.0*1.8 + 32
            temps.append(temp)

    datesAndTemps = dict({'dates': dates, 'temps': temps})
    
    return datesAndTemps

# MAIN
if __name__ == "__main__":
    # Creates Arrays and Dataframe for data to be placed
    finalDates = []
    finalTemps = []

    # Receives string input such as "abc, def"
    # Splits input into array with a new element at each comma ["abc", "def"]
    codes = input("Enter station codes (seperated by commas): ").split(',')

    if codes[0] == "":
        codes = ["GHCND:USW00023129", "GHCND:USW00023129"]

    # Loop through each code and get the average temperature data
    for code in codes:
        # average_temps_df.append(get_average_temp(code.strip()))
        current = get_average_temp(code.strip())

        if current is not None:
            print('ADDING DATA FROM STATION ' + code)
            finalDates.extend(current.get('dates', ''))
            finalTemps.extend(current.get('temps', ''))

    # Define avg_temp
    final = dict({'dates': finalDates, 'temps': finalTemps})
    average_temps_df = pd.DataFrame(final)

    average_temps_df.to_csv(r'Temp_Data.csv')
    print(average_temps_df)

