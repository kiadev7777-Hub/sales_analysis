from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no window, just save the files
import matplotlib.pyplot as plt
import pandas as pd

# Paths are built relative to this file, so it works from anywhere
ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "raw" / "sales_analysis.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "clean_sales.csv"
IMAGES_DIR = ROOT / "images"


def load_and_clean() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"File not found: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)
    print(f"Loaded {len(df)} rows")

    df = df.drop_duplicates(subset="Invoice ID")
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    df["Month"] = df["Date"].dt.month_name()
    df["Weekday"] = df["Date"].dt.day_name()

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Saved clean data to {PROCESSED_PATH}")
    return df


def save_fig(name: str) -> None:
    IMAGES_DIR.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / name, dpi=150)
    plt.close()
    print(f"Saved {name}")


def make_charts(df: pd.DataFrame) -> None:
    # 1. Revenue by branch
    df.groupby("Branch")["Total"].sum().plot(kind="bar", color="steelblue", figsize=(7, 5))
    plt.title("Revenue by Branch")
    plt.ylabel("Revenue")
    plt.xticks(rotation=0)
    save_fig("revenue_by_branch.png")

    # 2. Revenue by product line
    df.groupby("Product line")["Total"].sum().sort_values().plot(
        kind="barh", color="seagreen", figsize=(8, 5)
    )
    plt.title("Revenue by Product Line")
    plt.xlabel("Revenue")
    save_fig("product_line_revenue.png")

    # 3. Sales by hour
    df.groupby("Hour")["Total"].sum().plot(kind="line", marker="o", figsize=(8, 5))
    plt.title("Revenue by Hour of Day")
    plt.xlabel("Hour")
    plt.ylabel("Revenue")
    save_fig("sales_by_hour.png")

    # 4. Monthly trend
    months = ["January", "February", "March"]
    df.groupby("Month")["Total"].sum().reindex(months).plot(
        kind="bar", color="darkorange", figsize=(7, 5)
    )
    plt.title("Monthly Revenue")
    plt.ylabel("Revenue")
    plt.xticks(rotation=0)
    save_fig("monthly_trend.png")

    # 5. Payment methods
    df["Payment"].value_counts().plot(
        kind="pie", autopct="%1.1f%%", figsize=(6, 6), ylabel=""
    )
    plt.title("Payment Methods")
    save_fig("payment_methods.png")

    # 6. Rating distribution
    df["Rating"].plot(kind="hist", bins=12, color="mediumpurple", edgecolor="white", figsize=(7, 5))
    plt.title("Customer Rating Distribution")
    plt.xlabel("Rating")
    save_fig("rating_distribution.png")


def main() -> None:
    df = load_and_clean()
    make_charts(df)
    print("Done!")


if __name__ == "__main__":
    main()
