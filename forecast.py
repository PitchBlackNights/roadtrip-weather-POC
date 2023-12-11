import requests, pytz
from datetime import datetime

user_agent = {"user-agent": "roadtrip-weather"}


#### date = ["-0600", "10/02/2000", "10:28:56"]
#### date = ["%z", "%m/%d/%Y", "%H:%M:%S"]
#### date = ["-+HHMM", "mm/dd/yyyy", "HH:MM:SS"]
def get_forecast(location: tuple, date: list):
    """
    Get forecast data for `location` on `date`\n
    date = ["%z", "%m/%d/%Y", "%H:%M:%S"]\n
    date = ["-+HHMM", "mm/dd/yyyy", "HH:MM:SS"]\n
    date = ["-0600", "10/02/2000", "10:28:56"]
    """

    # Send API request
    point_info_request = requests.get(
        f"https://api.weather.gov/points/{location[0]},{location[1]}",
        headers=user_agent,
    )
    if point_info_request.status_code != 200:
        raise Exception(
            f"get_forecast(): Web Request Status Code {point_info_request.status_code}\nWEB REQUEST URL: https://api.weather.gov/points/{location[0]},{location[1]}"
        )
    # print(point_info_request.json())
    # Grab point timezone, and convert user-provided date to point timezone
    point_info = point_info_request.json()["properties"]
    try:
        forecast_local_date = datetime.strptime(
            f"{date[0]} {date[1]} {date[2]}", "%z %m/%d/%Y %H:%M:%S"
        )
    except ValueError:
        raise Exception(
            "Please check the formatting of your date and time.\nFORMAT: '%z %m/%d/%Y %H:%M:%S'"
        )
    forecast_date = forecast_local_date.astimezone(
        pytz.timezone(point_info["timeZone"])
    )
    local_date = datetime.now(datetime.now().astimezone().tzinfo)
    time_difference = (forecast_date - local_date).total_seconds()

    # If, user-defined date is more than 7 days in the future, raise Exception()
    if time_difference > 604800.0 or time_difference < 0.0:
        raise Exception(
            f'User Provided Date is too far in the {"future" if time_difference > 0 else "past"} ({time_difference})'
        )
    # Else, request hourly forecast
    forecast = _get_forecast_hour(point_info["forecastHourly"], forecast_date)
    return (point_info["forecastHourly"],forecast)


def _get_forecast_hour(api_url: str, forecast_date: datetime):
    # Send API Request
    forecast_request = requests.get(api_url, headers=user_agent)
    if forecast_request.status_code != 200:
        raise Exception(
            f"get_forecast_hour(): Web Request Status Code = {forecast_request.status_code}\nWEB REQUEST URL: {api_url}"
        )
    forecast_full = forecast_request.json()["properties"]["periods"]

    # Convert user-provided date to floored ISO format
    forecast_date = (
        pytz.timezone(str(forecast_date.tzinfo))
        .localize(
            datetime.strptime(
                f"{forecast_date.month} {forecast_date.day} {forecast_date.year} {forecast_date.hour} 00 00",
                "%m %d %Y %H %M %S",
            )
        )
        .isoformat()
    )

    # Look for the forecast entry that corresponds to the user-provided date
    for forecast_index in forecast_full:
        if forecast_index["startTime"] == str(forecast_date):
            return forecast_index
    raise Exception(
        f"The corresponding forecast date was never found!\nHINT: This might mean that your date is just a little bit too far in the future\nWEB REQUEST URL: {api_url}"
    )


# def get_forecast_day(api_url: str, forecast_date: datetime):
#     print("Forecast Day:", api_url)
#     forecast_request = requests.get(api_url, headers=user_agent)
#     if forecast_request.status_code != 200:
#         raise Exception(
#             f"get_forecast_day(): Web Request Status Code = {forecast_request.status_code}"
#         )
#     forecast_full = forecast_request.json()["properties"]["periods"]
#     return forecast_full[0]
