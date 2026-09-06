import io
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "worldbank_analytics.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "docs"
    / "figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)


# --------------------------------------------------
# Safe figure saving
# --------------------------------------------------

def save_figure(output_file):
    """
    Save a Matplotlib figure through memory first.

    This avoids some Windows/Pillow path issues.
    """

    buffer = io.BytesIO()

    plt.savefig(
        buffer,
        format="png",
        dpi=200,
        bbox_inches="tight"
    )

    buffer.seek(0)

    output_file.write_bytes(
        buffer.getvalue()
    )

    buffer.close()


# --------------------------------------------------
# Generic chart function
# --------------------------------------------------

def plot_indicator(
    column,
    title,
    ylabel,
    filename
):
    plt.figure(figsize=(10, 6))

    countries = sorted(
        df["country"].unique()
    )

    for country in countries:

        country_data = (
            df[df["country"] == country]
            .sort_values("year")
        )

        plt.plot(
            country_data["year"],
            country_data[column],
            marker="o",
            markersize=2,
            label=country
        )

    plt.title(
        title,
        fontsize=14
    )

    plt.xlabel("Year")

    plt.ylabel(ylabel)

    plt.legend()

    plt.grid(
        alpha=0.3
    )

    plt.tight_layout()

    output_file = (
        OUTPUT_DIR
        / filename
    )

    save_figure(output_file)

    plt.close()

    print(
        f"Saved: {output_file}"
    )


# --------------------------------------------------
# 1. GDP
# --------------------------------------------------

plot_indicator(
    column="gdp_usd",
    title="GDP Evolution in Selected West African Countries",
    ylabel="GDP (current US$)",
    filename="gdp_evolution.png"
)


# --------------------------------------------------
# 2. GDP per capita
# --------------------------------------------------

plot_indicator(
    column="gdp_per_capita_usd",
    title="GDP per Capita Evolution",
    ylabel="GDP per capita (current US$)",
    filename="gdp_pc.png"
)


# --------------------------------------------------
# 3. Inflation
# --------------------------------------------------

plot_indicator(
    column="inflation_pct",
    title="Inflation Evolution",
    ylabel="Inflation (%)",
    filename="inflation.png"
)


# --------------------------------------------------
# 4. Agriculture
# --------------------------------------------------

plot_indicator(
    column="agriculture_pct_gdp",
    title="Agriculture Value Added",
    ylabel="Agriculture value added (% of GDP)",
    filename="agriculture.png"
)


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("\n-----------------------------")
print("ANALYSIS COMPLETE")
print("-----------------------------")

print("Charts generated: 4")

print(
    f"Output directory: {OUTPUT_DIR}"
)