![Banner](assets/banner.png)

## Features
- Rule-based strategies (moving averages, RSI, etc.)
- Machine Learning predictions using XGBoost
- Backtesting with performance metrics
- Simple UI for daily trade suggestions

## Project Structure
- `notebooks/`: Analysis and prototyping
- `src/`: Modular and reusable code
- `data/`: Historical stock data (downloaded with `Polygon`)
- `models/`: Saved ML models    
- `interface/`: Front-end for displaying suggestions

## Setup

1. **Clone the repo:**
```bash
git clone https://github.com/1amt0ny/AlphaVestra.git
cd AlphaVestra
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file:**
I use Polygon.io to acquire the data. Store the API key in the `.env` file:
```bash
POLYGON_API_KEY=your_actual_api_key_here
```

5. **Get started!**

Run the Jupyter notebook:
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```