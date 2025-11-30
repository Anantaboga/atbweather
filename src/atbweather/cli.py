import argparse
import sys
from typing import Optional

import requests

BASE_URL = "https://wttr.in"


class WeatherError(Exception):
    """Custom error for weather fetching problems."""
    pass


def fetch_weather(location: Optional[str] = None) -> dict:
    """
    Fetch weather data from wttr.in in JSON format.

    If location is None or empty, wttr.in will detect by IP.
    """
    path = "" if not location else f"/{location}"
    url = f"{BASE_URL}{path}"
    params = {"format": "j1"}  # JSON format

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"Network error: {e}") from e
    except ValueError as e:
        raise WeatherError("Failed to parse JSON from wttr.in") from e

    if "current_condition" not in data or not data["current_condition"]:
        raise WeatherError("Unexpected API response: no current_condition field")

    return data


def format_weather(data: dict, location: Optional[str]) -> str:
    curr = data["current_condition"][0]

    temp_c = curr.get("temp_C", "?")
    temp_f = curr.get("temp_F", "?")
    feels_c = curr.get("FeelsLikeC", "?")
    feels_f = curr.get("FeelsLikeF", "?")
    desc_list = curr.get("weatherDesc", [])
    desc = desc_list[0].get("value") if desc_list else "Unknown"

    humidity = curr.get("humidity", "?")
    wind_kmph = curr.get("windspeedKmph", "?")
    wind_dir = curr.get("winddir16Point", "?")
    pressure = curr.get("pressure", "?")
    visibility = curr.get("visibility", "?")
    obs_time = curr.get("observation_time", "?")

    area_name = None
    country = None
    try:
        nearest_area = data.get("nearest_area", [])[0]
        names = nearest_area.get("areaName", [])
        countries = nearest_area.get("country", [])
        if names:
            area_name = names[0].get("value")
        if countries:
            country = countries[0].get("value")
    except (IndexError, AttributeError, TypeError):
        pass

    loc_display = location or area_name or "Your Location"
    if country and loc_display != country:
        loc_display = f"{loc_display}, {country}"

    lines = []
    lines.append(f"Weather for: {loc_display}")
    lines.append("-" * len(lines[0]))

    lines.append(f"Now:           {desc}")
    lines.append(f"Temperature:   {temp_c}°C  ({temp_f}°F)")
    lines.append(f"Feels like:    {feels_c}°C  ({feels_f}°F)")
    lines.append("")

    lines.append(f"Humidity:      {humidity}%")
    lines.append(f"Wind:          {wind_kmph} km/h {wind_dir}")
    lines.append(f"Pressure:      {pressure} hPa")
    lines.append(f"Visibility:    {visibility} km")
    lines.append(f"Observation:   {obs_time} (UTC, from API)")

    return "\n".join(lines)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="atbweather - tiny CLI weather app using wttr.in (no API key required)."
    )
    parser.add_argument(
        "-l",
        "--location",
        metavar="LOCATION",
        help="City/region, e.g. 'Tokyo', 'Denpasar', 'New York'. "
             "If omitted, use IP-based location.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    try:
        data = fetch_weather(args.location)
        output = format_weather(data, args.location)
        print(output)
        return 0
    except WeatherError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nAborted by user.", file=sys.stderr)
        return 130

