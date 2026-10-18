"""
Data Cleaning & Reporting Automation
Beginner-friendly project:
1. Loads a CSV file
2. Cleans column names, duplicate rows, missing values, and text spacing
3. Converts common date and numeric columns when possible
4. Creates summary statistics and a text report
5. Saves cleaned data, a data-quality report, and charts
"""

from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names lowercase and replace spaces/symbols with underscores."""
    df = df.copy()
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def clean_dataframe(df: pd.DataFrame):
    """Clean a DataFrame and return it with a quality summary."""
    original_rows, original_cols = df.shape
    df = clean_column_names(df)

    # Trim leading/trailing spaces in text cells.
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)

    missing_before = int(df.isna().sum().sum())
    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Attempt to convert columns that look like dates or numbers.
    for col in df.columns:
        name = col.lower()
        if any(word in name for word in ["date", "time", "timestamp"]):
            converted = pd.to_datetime(df[col], errors="coerce")
            # Convert only if at least one value was parsed.
            if converted.notna().any():
                df[col] = converted

    for col in df.select_dtypes(include=["object", "string"]).columns:
        name = col.lower()
        if any(word in name for word in ["amount", "price", "sales", "revenue", "quantity",
                                          "qty", "age", "score", "cost", "total", "profit"]):
            cleaned = df[col].str.replace(",", "", regex=False).str.replace("₹", "", regex=False)
            converted = pd.to_numeric(cleaned, errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted

    # Fill missing numeric values with the median and text values with "Unknown".
    # This is a simple demonstration strategy; choose a domain-appropriate method for real data.
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            if df[col].isna().any():
                median = df[col].median()
                df[col] = df[col].fillna(median if pd.notna(median) else 0)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            # Keep unknown dates as missing instead of inventing dates.
            pass
        else:
            if df[col].isna().any():
                df[col] = df[col].fillna("Unknown")

    missing_after = int(df.isna().sum().sum())
    quality = {
        "original_rows": original_rows,
        "cleaned_rows": int(len(df)),
        "original_columns": original_cols,
        "cleaned_columns": int(len(df.columns)),
        "duplicate_rows_removed": duplicates_removed,
        "missing_cells_before": missing_before,
        "missing_cells_after": missing_after,
    }
    return df, quality


def create_outputs(df: pd.DataFrame, quality: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    cleaned_path = output_dir / "cleaned_data.csv"
    df.to_csv(cleaned_path, index=False)

    # Column-level data quality report.
    quality_rows = []
    for col in df.columns:
        quality_rows.append({
            "column": col,
            "data_type": str(df[col].dtype),
            "missing_values": int(df[col].isna().sum()),
            "unique_values": int(df[col].nunique(dropna=True)),
        })
    pd.DataFrame(quality_rows).to_csv(output_dir / "column_quality_report.csv", index=False)

    # Summary statistics for numeric columns.
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        numeric.describe().T.to_csv(output_dir / "numeric_summary.csv")

    # A readable text report.
    report_path = output_dir / "report.txt"
    with report_path.open("w", encoding="utf-8") as f:
        f.write("DATA CLEANING & REPORTING AUTOMATION\n")
        f.write("=" * 40 + "\n\n")
        f.write("OVERVIEW\n")
        for key, value in quality.items():
            f.write(f"{key.replace('_', ' ').title()}: {value}\n")
        f.write("\nCOLUMN DETAILS\n")
        f.write(f"Columns: {', '.join(map(str, df.columns))}\n")
        f.write(f"Rows in cleaned dataset: {len(df)}\n")
        f.write(f"Missing cells remaining: {int(df.isna().sum().sum())}\n")
        if not numeric.empty:
            f.write("\nNUMERIC SUMMARY\n")
            f.write(numeric.describe().to_string())
            f.write("\n")
        f.write("\nFiles generated:\n")
        f.write("- cleaned_data.csv\n- column_quality_report.csv\n")
        if not numeric.empty:
            f.write("- numeric_summary.csv\n")
        f.write("- report.txt\n- missing_values.png\n")
        if not numeric.empty:
            f.write("- numeric_distributions.png\n")

    # Missing-values chart (based on cleaned data).
    missing_counts = df.isna().sum()
    plt.figure(figsize=(max(7, len(df.columns) * 0.65), 4))
    missing_counts.plot(kind="bar")
    plt.title("Missing Values by Column (After Cleaning)")
    plt.xlabel("Column")
    plt.ylabel("Missing values")
    plt.tight_layout()
    plt.savefig(output_dir / "missing_values.png", dpi=150)
    plt.close()

    # Histograms for numeric columns.
    if not numeric.empty:
        numeric.hist(figsize=(10, 6), bins=12)
        plt.suptitle("Numeric Column Distributions")
        plt.tight_layout()
        plt.savefig(output_dir / "numeric_distributions.png", dpi=150)
        plt.close()

    return cleaned_path, report_path


def main():
    parser = argparse.ArgumentParser(description="Clean a CSV and generate reports.")
    parser.add_argument("--input", default="data/sample_data.csv", help="Path to input CSV file")
    parser.add_argument("--output", default="output", help="Directory for generated files")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise SystemExit(
            f"Input file not found: {input_path}\n"
            "Run with --input data/sample_data.csv or provide your own CSV path."
        )

    try:
        raw_df = pd.read_csv(input_path)
    except Exception as exc:
        raise SystemExit(f"Could not read CSV file: {exc}")

    cleaned_df, quality = clean_dataframe(raw_df)
    cleaned_path, report_path = create_outputs(cleaned_df, quality, output_dir)

    print("\nProject completed successfully!")
    print(f"Cleaned data: {cleaned_path}")
    print(f"Text report:  {report_path}")
    print(f"Output folder: {output_dir.resolve()}")
    print("\nCleaning summary:")
    for key, value in quality.items():
        print(f"- {key.replace('_', ' ').title()}: {value}")


if __name__ == "__main__":
    main()
