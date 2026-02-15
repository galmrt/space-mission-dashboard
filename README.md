# Space Missions Dashboard 🚀

Interactive dashboard for analyzing historical space mission data from 1957 onwards.

## Tech Stack

- **Python 3.12**
- **Streamlit** - Dashboard framework
- **Pandas** - Data processing
- **Plotly** - Visualizations

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Dashboard

```bash
streamlit run run.py
```

## Project Structure

```
├── run.py                  # Main dashboard application
├── src/
│   ├── data_processing.py  # Data loading and required functions
│   ├── visualizations.py   # Chart generation
│   └── space_missions.csv  # Dataset
├── tests/
│   └── test_functions.py   # Unit tests
└── requirements.txt
```

## Required Functions

All 8 required functions are in `src/data_processing.py`:

| Function | Description |
|----------|-------------|
| `getMissionCountByCompany(companyName)` | Total missions for a company |
| `getSuccessRate(companyName)` | Success rate percentage |
| `getMissionsByDateRange(startDate, endDate)` | Missions in date range |
| `getTopCompaniesByMissionCount(n)` | Top N companies by missions |
| `getMissionStatusCount()` | Count by mission status |
| `getMissionsByYear(year)` | Missions in a specific year |
| `getMostUsedRocket()` | Most frequently used rocket |
| `getAverageMissionsPerYear(startYear, endYear)` | Average missions per year |

## Running Tests

```bash
pytest tests/test_functions.py -v
```

## Visualizations

1. **World Map** - Global launch distribution by country
2. **Activity Heatmap** - Company launch activity over time
3. **Interactive Histograms** - Customizable data exploration

