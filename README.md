# Space Missions Dashboard

Interactive dashboard for analyzing historical space mission data from 1957 onwards.

Dashboard is available at: https://space-mission-dashboard-hcw8it9wsyqlmxpuq39t4y.streamlit.app

## Dashboard Features

- **Date Range Filter** - Filter all data by selecting start and end dates
- **Summary Statistics** - Key metrics including total missions, success rate, and most used rocket
- **Interactive Charts** - Hover for details, zoom, and pan on all visualizations

## How to Use

1. **Filter by Date** - Use the sidebar date pickers to narrow down the time range. Click "Reset" to restore the full dataset.
2. **Explore the Map** - Hover over countries to see launch counts. Darker colors = more launches.
3. **Read the Heatmap** - Each row is a company, each column is a year. Brighter cells = more activity.
4. **Create Histograms** - Click "Add histogram" and select a column to visualize its distribution.

## Visualization Choices:  
- **World Map** - Shows global distribution of space launches by country. I chose this to provide immediate geographic context and highlight which regions have been most active in space exploration
- **Company Activity Heatmap** - Displays company launch activity over time. This visualization reveals patterns like when companies were most active and allows comparison across the space industry's history
- **Interactive Histograms** - Customizable distribution charts for various attributes. This gives users flexibility to explore the data.
- 
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
