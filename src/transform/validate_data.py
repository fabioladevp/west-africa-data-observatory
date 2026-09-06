import pandas as pd


df = pd.read_csv("data/raw/worldbank_indicators.csv")


def validate_data(dataframe):
    errors = []

    # 1. Vérifier le nombre de pays
    expected_countries = 4
    actual_countries = dataframe["country"].nunique()

    if actual_countries != expected_countries:
        errors.append(
            f"Expected {expected_countries} countries, found {actual_countries}"
        )

    # 2. Vérifier le nombre d'indicateurs
    expected_indicators = 5
    actual_indicators = dataframe["indicator"].nunique()

    if actual_indicators != expected_indicators:
        errors.append(
            f"Expected {expected_indicators} indicators, found {actual_indicators}"
        )

    # 3. Vérifier les valeurs manquantes
    missing_values = dataframe.isnull().sum().sum()

    if missing_values > 0:
        errors.append(
            f"Found {missing_values} missing values"
        )

    # 4. Vérifier les doublons
    duplicates = dataframe.duplicated(
        subset=["country_code", "indicator_code", "year"]
    ).sum()

    if duplicates > 0:
        errors.append(
            f"Found {duplicates} duplicate rows"
        )

    # 5. Vérifier les années
    invalid_years = dataframe[
        (dataframe["year"] < 2000)
        | (dataframe["year"] > 2025)
    ]

    if len(invalid_years) > 0:
        errors.append(
            f"Found {len(invalid_years)} invalid years"
        )

    return errors


errors = validate_data(df)


print("\n-----------------------------")
print("DATA QUALITY CHECK")
print("-----------------------------")

if len(errors) == 0:
    print("PASS - All quality checks passed")

else:
    print("FAIL")

    for error in errors:
        print(f"- {error}")