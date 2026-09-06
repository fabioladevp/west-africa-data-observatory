import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/raw/worldbank_indicators.csv")
OUTPUT_DIRECTORY = Path("data/processed")


def transform_world_bank_data():
    df = pd.read_csv(INPUT_FILE)

    # -----------------------------
    # 1. Standardiser les pays
    # -----------------------------

    country_names = {
        "TGO": "Togo",
        "GHA": "Ghana",
        "BEN": "Benin",
        "CIV": "Cote d'Ivoire"
    }

    df["country"] = df["country_code"].map(country_names)

    # -----------------------------
    # 2. Trier les données
    # -----------------------------

    df = df.sort_values(
        by=["country", "indicator", "year"]
    )

    # -----------------------------
    # 3. Supprimer les doublons éventuels
    # -----------------------------

    df = df.drop_duplicates(
        subset=[
            "country_code",
            "indicator_code",
            "year"
        ]
    )

    # -----------------------------
    # 4. Créer une version LARGE
    #    1 ligne = 1 pays / 1 année
    # -----------------------------

    wide_df = df.pivot_table(
        index=[
            "country",
            "country_code",
            "year"
        ],
        columns="indicator",
        values="value"
    ).reset_index()

    # Supprimer le nom technique de l'index de colonnes
    wide_df.columns.name = None

    # -----------------------------
    # 5. Renommer les colonnes
    # -----------------------------

    wide_df = wide_df.rename(
        columns={
            "GDP": "gdp_usd",
            "GDP per capita": "gdp_per_capita_usd",
            "Population": "population",
            "Agriculture value added (% GDP)": "agriculture_pct_gdp",
            "Inflation": "inflation_pct"
        }
    )

    # -----------------------------
    # 6. Trier
    # -----------------------------

    wide_df = wide_df.sort_values(
        by=["country", "year"]
    )

    # -----------------------------
    # 7. Sauvegarder
    # -----------------------------

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    clean_file = (
        OUTPUT_DIRECTORY /
        "worldbank_clean.csv"
    )

    analytics_file = (
        OUTPUT_DIRECTORY /
        "worldbank_analytics.csv"
    )

    # Version longue propre
    df.to_csv(
        clean_file,
        index=False
    )

    # Version large pour analyse/dashboard
    wide_df.to_csv(
        analytics_file,
        index=False
    )

    return df, wide_df


if __name__ == "__main__":

    clean_df, analytics_df = (
        transform_world_bank_data()
    )

    print("\n-----------------------------")
    print("DATA TRANSFORMATION COMPLETE")
    print("-----------------------------")

    print(
        f"Clean dataset: {len(clean_df)} rows"
    )

    print(
        f"Analytics dataset: {len(analytics_df)} rows"
    )

    print("\nAnalytics columns:")

    for column in analytics_df.columns:
        print(f"- {column}")

    print("\nPreview:")
    print(analytics_df.head(10))