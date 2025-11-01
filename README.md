# Program Impact Dashboard MVP

A Streamlit-based dashboard for visualizing key initiatives' performance against Ambition 2045 target sheets, focusing on Pillar 2 (BMGF Impact).

## Features

- **Expectations vs. Performance**: View baseline, actual, and target values with progress percentages
- **Status Classification**: Automatic classification as On Track / At Risk / Off Track
- **Evidence Linking**: Associate metrics with evidence summaries and confidence scores
- **Future Projections**: Visualize current trajectory vs. desired 2030 targets
- **Narrative Insights**: Add qualitative notes and learnings

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare your data files:
   - `Expectations.csv`: Baseline and target expectations
   - `Performance.csv`: Current or periodic actuals
   - `Evidence.csv`: Supporting studies or evaluations

3. Run the dashboard:
```bash
streamlit run dashboard.py
```

## Data Format

### Expectations.csv
Columns: `Initiative ID`, `Metric`, `Baseline`, `Target 2030`, `Target 2045`, `Expectation Type`

- **Initiative ID**: Unique identifier for each initiative (e.g., "INIT-001")
- **Metric**: Name of the metric being tracked
- **Baseline**: Starting value (typically current or historical baseline)
- **Target 2030**: Target value for 2030
- **Target 2045**: Target value for 2045 (long-term goal)
- **Expectation Type**: Either "topline" or "intermediate"

### Performance.csv
Columns: `Initiative ID`, `Metric`, `Year`, `Actual Value`, `Data Source`, `Quality`

- **Initiative ID**: Must match an ID from Expectations.csv
- **Metric**: Must match a metric from Expectations.csv
- **Year**: Year of the measurement (numeric, e.g., 2024)
- **Actual Value**: The measured value for that year
- **Data Source**: Where the data came from
- **Quality**: Data quality indicator (e.g., "High", "Medium", "Low")

### Evidence.csv
Columns: `Initiative ID`, `Evidence Type`, `Confidence Score`, `Link / Summary`

- **Initiative ID**: Must match an ID from Expectations.csv
- **Evidence Type**: Type of evidence (e.g., "RCT", "QED", "Descriptive")
- **Confidence Score**: Numeric score from 1-3 (1=Weak, 2=Moderate, 3=Strong)
- **Link / Summary**: URL or text description of the evidence

## Status Classification

The dashboard automatically calculates progress and classifies each metric:

- **On Track** (Green): ≥80% progress toward target
- **At Risk** (Orange): 50-79% progress toward target
- **Off Track** (Red): <50% progress toward target

Progress is calculated as: `(Actual - Baseline) / (Target - Baseline) * 100`

For "lower is better" metrics (e.g., equity gaps, costs), the calculation is inverted automatically.

## Usage

1. **Upload Data**: Use the sidebar to upload your three CSV files, or use the sample data if files exist in the directory.

2. **Filter by Initiative**: Select a specific initiative from the sidebar dropdown to focus on a single program, or select "All" to see all initiatives.

3. **View KPIs**: The main dashboard shows KPI cards for each metric with:
   - Baseline, Actual, and Target values
   - Progress percentage and status
   - Delta from target

4. **Detailed Analysis**: When viewing a specific initiative, you can:
   - Select any metric for detailed analysis
   - View trend charts with projections
   - Review evidence summaries and grades
   - Add narrative insights

5. **Summary Statistics**: The bottom section provides an overview of all metrics and their status classifications.

## Deployment

See `DEPLOYMENT.md` for instructions on deploying this dashboard to Streamlit Cloud or other platforms.
