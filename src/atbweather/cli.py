import argparse
import sys
from typing import Optional
import threading
import time
import itertools

import requests
from colorama import init as colorama_init, Fore, Style

# Initialize colorama for Windows terminals
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


class Spinner:
    """Spinner that disables automatically if not in a real terminal."""
    def __init__(self, message: str = "Fetching weather"):
        self.message = message
        self.enabled = sys.stdout.isatty()  # auto disable when output is piped
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self):
        frames = itertools.cycle(["⠋", "⠙", "⠹", "⠸",
                                  "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
        while not self._stop_event.is_set():
            if self.enabled:
                print(
                    f"\r{next(frames)} {self.message}...",
                    end="", flush=True
                )
            time.sleep(0.1)

    def start(self):
        if self.enabled:
            self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self.enabled:
            self._thread.join()
            # Clear spinner line completely
            clear_len = len(self.message) + 5
            print("\r" + " " * clear_len, end="\r", flush=True)


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
    except ValueError:
        raise WeatherError("Invalid response from wttr.in")

    if "current_condition" not in data:
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
    try:
        nearest_area = data.get("nearest_area", [])[0]

        city = nearest_area.get("areaName", [{}])[0].get("value", "")
        region = nearest_area.get("region", [{}])[0].get("value", "")
        country = nearest_area.get("country", [{}])[0].get("value", "")

        parts = [p for p in [city, region, country] if p]
        loc_display = ", ".join(parts) if parts else loc_display
    except Exception:
        pass

    return (
        f"Weather for: {loc_display}\n"
        + "-" * (15 + len(loc_display)) + "\n"
        f"Now:           {desc}\n"
        f"Temperature:   {temp_c}°C  ({temp_f}°F)\n"
        f"Feels like:    {feels_c}°C  ({feels_f}°F)\n\n"
        f"Humidity:      {humidity}%\n"
        f"Wind:          {wind_kmph} km/h {wind_dir}\n"
        f"Pressure:      {pressure} hPa\n"
        f"Visibility:    {visibility} km\n"
        f"Observation:   {obs_time} (UTC, from API)"
    )


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
        help="City/region (if omitted, auto-detect by IP)"
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
