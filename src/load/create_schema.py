from sqlalchemy import text

from database import engine


def create_schema():

    statements = [

        """
        CREATE TABLE IF NOT EXISTS dim_country (
            country_id INT AUTO_INCREMENT PRIMARY KEY,
            country_code VARCHAR(10) NOT NULL UNIQUE,
            country_name VARCHAR(100) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS dim_indicator (
            indicator_id INT AUTO_INCREMENT PRIMARY KEY,
            indicator_code VARCHAR(50) NOT NULL UNIQUE,
            indicator_name VARCHAR(255) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS dim_year (
            year_id INT AUTO_INCREMENT PRIMARY KEY,
            year INT NOT NULL UNIQUE
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS fact_indicator_value (
            fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,

            country_id INT NOT NULL,
            indicator_id INT NOT NULL,
            year_id INT NOT NULL,

            value DOUBLE NULL,

            CONSTRAINT fk_fact_country
                FOREIGN KEY (country_id)
                REFERENCES dim_country(country_id),

            CONSTRAINT fk_fact_indicator
                FOREIGN KEY (indicator_id)
                REFERENCES dim_indicator(indicator_id),

            CONSTRAINT fk_fact_year
                FOREIGN KEY (year_id)
                REFERENCES dim_year(year_id),

            CONSTRAINT uq_indicator_observation
                UNIQUE (
                    country_id,
                    indicator_id,
                    year_id
                )
        );
        """
    ]

    with engine.begin() as connection:

        for statement in statements:

            connection.execute(
                text(statement)
            )

    print("-----------------------------")
    print("DATABASE SCHEMA")
    print("-----------------------------")
    print("Status: SUCCESS")
    print()
    print("Tables created:")
    print("- dim_country")
    print("- dim_indicator")
    print("- dim_year")
    print("- fact_indicator_value")


if __name__ == "__main__":
    create_schema()