from pathlib import Path
from datetime import datetime

from src.extract.worldbank import fetch_all_data
from src.transform.validate_data import validate_data
from src.transform.transform_data import transform_world_bank_data
from src.load.load_worldbank import load_database


PROJECT_ROOT = Path(__file__).resolve().parent

RAW_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "raw"
)

RAW_FILE = (
    RAW_DIRECTORY
    / "worldbank_indicators.csv"
)


def print_step(number, title):

    print()
    print("=" * 60)
    print(f"STEP {number} — {title}")
    print("=" * 60)


def run_pipeline():

    started_at = datetime.now()

    print()
    print("=" * 60)
    print("WEST AFRICA DATA OBSERVATORY")
    print("DATA PIPELINE")
    print("=" * 60)

    print(
        "Started:",
        started_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )


    # ==================================================
    # STEP 1 — EXTRACTION
    # ==================================================

    print_step(
        1,
        "WORLD BANK EXTRACTION"
    )

    dataframe = fetch_all_data()

    RAW_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    dataframe.to_csv(
        RAW_FILE,
        index=False
    )

    print(
        f"Rows extracted: {len(dataframe)}"
    )

    print(
        f"Raw dataset saved: {RAW_FILE}"
    )


    # ==================================================
    # STEP 2 — DATA QUALITY
    # ==================================================

    print_step(
        2,
        "DATA QUALITY"
    )

    errors = validate_data(
        dataframe
    )

    if errors:

        print(
            "DATA QUALITY FAILED"
        )

        for error in errors:

            print(
                f"- {error}"
            )

        raise RuntimeError(
            "Pipeline stopped because "
            "data validation failed."
        )


    print(
        "All quality checks passed."
    )


    # ==================================================
    # STEP 3 — TRANSFORMATION
    # ==================================================

    print_step(
        3,
        "DATA TRANSFORMATION"
    )

    clean_df, analytics_df = (
        transform_world_bank_data()
    )

    print(
        f"Clean rows: {len(clean_df)}"
    )

    print(
        f"Analytics rows: "
        f"{len(analytics_df)}"
    )


    # ==================================================
    # STEP 4 — DATABASE LOAD
    # ==================================================

    print_step(
        4,
        "DATABASE LOAD"
    )

    load_database()


    # ==================================================
    # COMPLETE
    # ==================================================

    finished_at = datetime.now()

    duration = (
        finished_at
        - started_at
    )

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print(
        "Finished:",
        finished_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print(
        f"Duration: {duration}"
    )

    print(
        f"Countries: "
        f"{dataframe['country_code'].nunique()}"
    )

    print(
        f"Indicators: "
        f"{dataframe['indicator_code'].nunique()}"
    )

    print(
        f"Observations: "
        f"{len(dataframe)}"
    )


if __name__ == "__main__":

    run_pipeline()