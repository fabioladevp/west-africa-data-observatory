from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "worldbank_indicators.csv"
)


def validate_data(dataframe):

    errors = []

    # --------------------------------------------------
    # Countries
    # --------------------------------------------------

    expected_country_codes = {
        "TGO",
        "GHA",
        "BEN",
        "CIV"
    }

    actual_country_codes = set(
        dataframe["country_code"].unique()
    )

    if actual_country_codes != expected_country_codes:

        errors.append(
            "Unexpected country coverage: "
            f"{actual_country_codes}"
        )


    # --------------------------------------------------
    # Indicators
    # --------------------------------------------------

    expected_indicators = 5

    actual_indicators = (
        dataframe["indicator_code"].nunique()
    )

    if actual_indicators != expected_indicators:

        errors.append(
            f"Expected {expected_indicators} indicators, "
            f"found {actual_indicators}"
        )


    # --------------------------------------------------
    # Required columns
    # --------------------------------------------------

    required_columns = {
        "country",
        "country_code",
        "indicator",
        "indicator_code",
        "year",
        "value"
    }

    missing_columns = (
        required_columns
        - set(dataframe.columns)
    )

    if missing_columns:

        errors.append(
            f"Missing columns: {missing_columns}"
        )


    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    missing_values = (
        dataframe[
            [
                "country",
                "country_code",
                "indicator",
                "indicator_code",
                "year"
            ]
        ]
        .isnull()
        .sum()
        .sum()
    )

    if missing_values > 0:

        errors.append(
            f"Found {missing_values} missing "
            "values in required fields"
        )


    # --------------------------------------------------
    # Duplicates
    # --------------------------------------------------

    duplicates = dataframe.duplicated(
        subset=[
            "country_code",
            "indicator_code",
            "year"
        ]
    ).sum()

    if duplicates > 0:

        errors.append(
            f"Found {duplicates} duplicate rows"
        )


    # --------------------------------------------------
    # Years
    # --------------------------------------------------

    invalid_years = dataframe[
        (dataframe["year"] < 2000)
        |
        (dataframe["year"] > 2025)
    ]

    if not invalid_years.empty:

        errors.append(
            f"Found {len(invalid_years)} invalid years"
        )


    return errors


def validate_file():

    dataframe = pd.read_csv(
        DATA_FILE
    )

    errors = validate_data(
        dataframe
    )

    return errors


if __name__ == "__main__":

    errors = validate_file()

    print("\n-----------------------------")
    print("DATA QUALITY CHECK")
    print("-----------------------------")

    if not errors:

        print(
            "PASS - All quality checks passed"
        )

    else:

        print("FAIL")

        for error in errors:
            print(f"- {error}")