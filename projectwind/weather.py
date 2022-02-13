import numpy as np
import requests
import datetime
import pandas as pd



def get_weather(lon=19.696598,lat=-71.219500, start_date="01/05/19", end_date ="30/09/21"):

    date_1 = datetime.datetime.strptime(start_date, "%d/%m/%y")
    date_2 = date_1 + datetime.timedelta(days=29, hours=23)
    break_date = datetime.datetime.strptime(end_date, "%d/%m/%y")+datetime.timedelta(hours=23)

    col = ['tempC', 'precipMM', 'windspeedKmph', 'winddirDegree']
    weather = pd.DataFrame(columns=col)
    print (weather)

#Loop over all the dates to then do the GET request
    while date_2<=break_date:
        date_2= min(date_2, break_date)
        print(date_1, date_2)
        url = f"https://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=32c9c3f028054024b1c160353220402&q={lon},{lat}&date={date_1.strftime('%d/%m/%Y')}&enddate={date_2.strftime('%d/%m/%Y')}&tp=1&format=json"

        #Get the json for a specific range of dates and for specific zone
        resp = requests.get(url).json()
        #Create a dataframe
        df=pd.json_normalize(resp["data"]["weather"],['hourly'], errors='ignore', meta="date")
        #fill with 0 the hour and create the Fecha column
        df["Fecha"] = pd.to_datetime(df["date"]+" "+df["time"].str.zfill(4))
        #Set Fecha as index
        df.set_index("Fecha", inplace=True)
        #add the minutes to the DF
        df = df.reindex(pd.date_range(start=date_1, end=date_2, freq="10min"),method='ffill')
                    #Append the data to a new dataframe
        print(df)
        weather = weather.append(df[['tempC', 'precipMM', 'windspeedKmph', 'winddirDegree']])
        date_1 = date_1 + datetime.timedelta(days=30)
        date_2 = date_2 + datetime.timedelta(days=30)
    weather.index= weather.index- pd.DateOffset(hours=12)
    weather[['tempC', 'precipMM', 'windspeedKmph', 'winddirDegree']] = weather[['tempC', 'precipMM', 'windspeedKmph', 'winddirDegree']].apply(pd.to_numeric, downcast="float", errors='ignore')
    print(weather)
    print(weather.info())
    return feature_engineering(weather)

def feature_engineering(df):

    # Find wind direction (by correcting nacelle orientation with windspeedKmph)
    df['winddirDegree'] = df['winddirDegree']* np.pi / 180 # Transform into radians


    # Build vectors from wind direction and wind speed
    df['Wind_API_X'] = df['windspeedKmph'] * np.cos(df['winddirDegree'])
    df['Wind_API_Y'] = df['windspeedKmph'] * np.sin(df['winddirDegree'])

    # Remove superseeded columns, except wind speed
    df.drop(columns=['windspeedKmph','winddirDegree'], inplace=True)

    return df

if __name__=="__main__":
    df = get_weather()
    print(df)