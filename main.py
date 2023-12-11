from forecast import get_forecast

if True:  # SKIP
    lattitude = 65.62
    longitude = -168.09
    time_tz = "-0600"
    time_date = "12/11/2023"
    time_time = "15:59:59"
else:
    print('Values: (44.47, -73.15), ["-06:00", "12/11/2023", "12:28:56"]')
    lattitude = float(input("Lattitude: "))
    longitude = float(input("Longitute: "))
    time_tz = input("UTC Offset (+-HHMM): ")
    time_date = input("Date (MM/DD/YYYY): ")
    time_time = input("Time (HH:MM:SS): ")

forecast_url,forecast = get_forecast((lattitude, longitude), [time_tz, time_date, time_time])
print(
    f'On {time_date} at {time_time} (Local Time),\n\
The weather at {lattitude}°N, {longitude}°E will be:\n\
======================================================\n\
Temperature: {forecast["temperature"]}°{forecast["temperatureUnit"]}\n\
Probability of Precipitation: {forecast["probabilityOfPrecipitation"]["value"]}%\n\
Dew Point: {round(float(forecast["dewpoint"]["value"]), 2)}°C\n\
Humidity: {forecast["relativeHumidity"]["value"]}%\n\
Wind: {forecast["windSpeed"]} {forecast["windDirection"]}\n\
Short Forecast: {forecast["shortForecast"]}\n\
URL: {forecast_url}'
)
