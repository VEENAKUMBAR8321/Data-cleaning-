# Data Cleaning & Reporting Automation

A beginner-friendly Python internship mini-project that cleans a CSV file and automatically creates reports and charts.

## What it does

- Standardizes column names.
- Removes duplicate rows.
- Trims extra spaces from text.
- Attempts to convert date and common numeric columns.
- Fills missing numeric values with the median and missing text values with `Unknown`.
- Exports cleaned data, column-quality details, numeric summary statistics, a text report, and charts.

> Note: Missing-value handling is a simple demo strategy. For real projects, choose a method that fits the meaning of each column.

## Project structure

```text
data_cleaning_reporting_automation/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_data.csv
└── output/                 # created when the program runs
```

## Requirements

- Python 3.10 or later
- Internet connection for installing libraries

## Setup on Windows (VS Code)

1. Extract the ZIP file.
2. Open the extracted project folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Check Python:

   ```powershell
   python --version
   ```

5. Install the required libraries:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Run the project:

   ```powershell
   python main.py
   ```

If `python` is not recognized, install Python from the official Python website and select **Add Python to PATH** during installation. Restart VS Code after installation.

## Output files

The program creates an `output` folder containing:

- `cleaned_data.csv` — cleaned dataset
- `column_quality_report.csv` — data type, missing count, and unique count for each column
- `numeric_summary.csv` — summary statistics for numeric columns (when available)
- `report.txt` — readable project summary
- `missing_values.png` — missing-value chart
- `numeric_distributions.png` — histograms for numeric columns (when available)

## Use your own CSV

```powershell
python main.py --input "data/your_file.csv" --output "output"
```

Use a CSV file with a header row. Keep a backup of original data before cleaning.

## How it works

1. Load CSV with pandas.
2. Standardize column names.
3. Trim text and replace blank text with missing values.
4. Remove duplicate rows.
5. Convert date-like and common numeric columns where possible.
6. Fill missing numeric/text values using the demonstration rules.
7. Save cleaned data and generate reports/charts.

## Learning goals

After completing this project, you should understand CSV processing with pandas, data-quality checks, missing-value handling, duplicate removal, summary statistics, and basic report automation.
