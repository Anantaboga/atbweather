import argparse
import sys
from typing import Optional
import threading
import time
import itertools

import requests
from colorama import init as colorama_init, Fore, Style

colorama_init(autoreset=True)

BASE_URL = "https://wttr.in"


class WeatherError(Exception):
    """Custom error for weather fetching problems."""
    pass


# ASCII Banner
BANNER = r"""
            █████    █████                                         █████    █████                        
           ░░███    ░░███                                         ░░███    ░░███                         
  ██████   ███████   ░███████  █████ ███ █████  ██████   ██████   ███████   ░███████    ██████  ████████ 
 ░░░░░███ ░░░███░    ░███░░███░░███ ░███░░███  ███░░███ ░░░░░███ ░░░███░    ░███░░███  ███░░███░░███░░███
  ███████   ░███     ░███ ░███ ░███ ░███ ░███ ░███████   ███████   ░███     ░███ ░███ ░███████  ░███ ░░░ 
 ███░░███   ░███ ███ ░███ ░███ ░░███████████  ░███░░░   ███░░███   ░███ ███ ░███ ░███ ░███░░░   ░███     
░░████████  ░░█████  ████████   ░░████░████   ░░██████ ░░████████  ░░█████  ████ █████░░██████  █████    
 ░░░░░░░░    ░░░░░  ░░░░░░░░     ░░░░ ░░░░     ░░░░░░   ░░░░░░░░    ░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░                                                                                                      
"""


def print_banner() -> None:
    print(Fore.GREEN + BANNER)
    print(
        Fore.GREEN + Style.BRIGHT +
        "      Simple CLI Weather • Productivity\n"
    )


# Spinner class for loading animation
class Spinner:
    def __init__(self, message: str = "Fetching weather"):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        frames = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while not self._stop_event.is_set():
            symbol = next(frames)
            print(f"\r{symbol} {self.message}...", end="", flush=True)
            time.sleep(0.1)
        print("\r", end="", flush=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()


def fetch_weather(location: Optional[str] = None) -> dict:
    path = "" if not location else f"/{location}"
    url = f"{BASE_URL}{path}"
    params = {"format": "j1"}

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        raise WeatherError(f"Network error: {e}") from e
    except ValueError as e:
        raise WeatherError("Failed to parse JSON from wttr.in") from e

    if "current_condition" not in data or not data["current_condition"]:
        raise WeatherError("Unexpected API response format")

    return data


def format_weather(data: dict, location: Optional[str]) -> str:
    curr = data["current_condition"][0]

    temp_c = curr.get("temp_C", "?")
    temp_f = curr.get("temp_F", "?")
    feels_c = curr.get("FeelsLikeC", "?")
    feels_f = curr.get("FeelsLikeF", "?")
    desc = curr.get("weatherDesc", [{"value": "Unknown"}])[0]["value"]
    humidity = curr.get("humidity", "?")
    wind_kmph = curr.get("windspeedKmph", "?")
    wind_dir = curr.get("winddir16Point", "?")
    pressure = curr.get("pressure", "?")
    visibility = curr.get("visibility", "?")
    obs_time = curr.get("observation_time", "?")

    loc_display = location or "Your Location"

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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atbweather",
        description="atbweather - tiny CLI weather app using wttr.in (no API key required).",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  atbweather\n"
            "  atbweather -l Tokyo\n"
            "  atbweather --location \"Atlantico\"\n"
        ),
    )
    parser.add_argument(
        "-l", "--location",
        metavar="LOCATION",
        help="City/region (if omitted, auto-detect by IP)",
    )
    return parser


def main(argv=None) -> int:
    print_banner()

    parser = build_parser()
    args = parser.parse_args(argv)

    spinner = Spinner("Fetching weather")
    try:
        spinner.start()
        data = fetch_weather(args.location)
        spinner.stop()

        print()  # newline after spinner
        print(format_weather(data, args.location))
        return 0

    except WeatherError as e:
        spinner.stop()
        print(f"\nError: {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        spinner.stop()
        print("\nAborted by user.", file=sys.stderr)
        return 130
