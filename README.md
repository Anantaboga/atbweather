# 🌦 atbweather – Terminal Weather App
```
            █████    █████                                         █████    █████                        
           ░░███    ░░███                                         ░░███    ░░███                         
  ██████   ███████   ░███████  █████ ███ █████  ██████   ██████   ███████   ░███████    ██████  ████████ 
 ░░░░░███ ░░░███░    ░███░░███░░███ ░███░░███  ███░░███ ░░░░░███ ░░░███░    ░███░░███  ███░░███░░███░░███
  ███████   ░███     ░███ ░███ ░███ ░███ ░███ ░███████   ███████   ░███     ░███ ░███ ░███████  ░███ ░░░ 
 ███░░███   ░███ ███ ░███ ░███ ░░███████████  ░███░░░   ███░░███   ░███ ███ ░███ ░███ ░███░░░   ░███     
░░████████  ░░█████  ████████   ░░████░████   ░░██████ ░░████████  ░░█████  ████ █████░░██████  █████    
 ░░░░░░░░    ░░░░░  ░░░░░░░░     ░░░░ ░░░░     ░░░░░░   ░░░░░░░░    ░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░     
                                                                                                         
```
atbweather is a simple yet stylish CLI weather tool that fetches real-time weather data from **wttr.in** — no API key required!  
Easy to use anywhere.

---

## ✨ Features

✔ No API keys needed  
✔ Supports **custom locations**  
✔ Detects **location automatically**  
✔ Works on **Windows, Linux, macOS**  
✔ Colorful banner intro 😎  

---

## 🛠 Installation

### Install from GitHub (recommended while in development)

```bash
pip install git+https://github.com/Anantaboga/atbweather.git
```

### Or with pipx (best for CLI apps):
```
pip install --user pipx
pipx ensurepath
pipx install git+https://github.com/Anantaboga/atbweather.git
```

## 🚀 Usage
### Auto-detected location (via IP)
```
atbweather
```
### Specific location
```
atbweather -l Atlantico
atbweather --location "Atlantico"
```
### Help
```
atbweather -h
```

## 🧩 Requirements
- Python 3.9+
- Internet connection

## 🐧 Installation on Linux (Recommended Methods)

Starting with modern Debian/Ubuntu systems, Python packages should not be installed system-wide using `pip`.
Below are the safest ways to install **ATBWEATHER** on Linux.

---

### ✔ Best Option (Recommended): Install with `pipx`

`pipx` isolates CLI tools into their own environments — clean and safe.

Install pipx:
```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```
Reload your terminal session:
```
source ~/.profile
```
Install ATBWEATHER using `pipx`:
```
pipx install git+https://github.com/Anantaboga/atbweather.git
```
Run:
```
atbweather -l Tokyo
```
### 🧪 Option B — Virtual Environment (Development Use)
Create venv:
```
python3 -m venv venv
source venv/bin/activate
```
Install ATBWEATHER in editable mode:
```
pip install git+https://github.com/Anantaboga/atbweather.git
```
Run:
```
atbweather -l Tokyo
```
Deactivate when done:
```
deactivate
```
