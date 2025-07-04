#!/usr/bin/env bash
set -e

# 1) Create a virtual environment
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment…"
  python3 -m venv .venv
fi

# 2) Activate venv for this script
#    (Note: To use it in your shell after this script runs, you'll still need to `source .venv/bin/activate`)
source .venv/bin/activate

# 3) Ensure pip is up-to-date
echo "Upgrading pip…"
pip install --upgrade pip

# 4) Install system dependency: OpenMP runtime
#    Required by XGBoost on macOS
echo "Installing libomp via Homebrew…"
brew list libomp &>/dev/null || brew install libomp

# 5) Install Python packages
echo "Installing Python requirements…"
pip install -r requirements.txt

echo
echo "✅ Setup complete!"
echo "   • Activate your venv with:   source .venv/bin/activate"
echo "   • Run Jupyter notebooks under this venv."