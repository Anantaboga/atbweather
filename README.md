# atbweather

A tiny terminal weather app using [wttr.in](https://wttr.in) (no API key required).

## Install (local dev)

```bash
  git clone https://github.com/your-username/atbweather.git
  cd atbweather
  pip install .
  # or (recommended for CLIs)
  pipx install .
```

# Usage
## Auto-detected location (by IP)
atbweather

## Specific city
atbweather -l "Denpasar"
atbweather --location Tokyo

# Requirements
python 3.9 +
requests (installed automatically)

`.gitignore` (Python typical):

```gitignore
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
venv/
.venv/
