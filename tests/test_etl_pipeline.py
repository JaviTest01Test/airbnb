import sys
import os

# Add the 'src' folder to the Python path before importing
sys.path.append(os.path.join(os.getcwd(), '..', 'src'))


import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType
from etl_pipeline import process_landing_zone


@pytest.fixture(scope="session")
def spark():
    """Creates a SparkSession for the tests."""
    return SparkSession.builder \
        .appName("Test process_landing_zone") \
        .master("local[*]") \
        .getOrCreate()


@pytest.fixture
def listings_data(spark):
    """Creates a mock DataFrame for listings_details."""
    data = [
        (73282, "https://www.airbnb.com/rooms/73282", "377532", "Sihlfeld", "Sihlfeld", 23.0, 4.78, "2019-04-27"),
        (143821, "https://www.airbnb.com/rooms/143821", "697307", "Alt-Wiedikon", "Alt-Wiedikon", 25.0, 4.89, "2024-06-29"),
        (178448, "https://www.airbnb.com/rooms/178448", "854016", "Zurich", "Enge", 0.0, None, None),
    ]
    schema = StructType([
        StructField("id", LongType(), True),
        StructField("listing_url", StringType(), True),
        StructField("host_id", StringType(), True),
        StructField("neighbourhood", StringType(), True),
        StructField("neighbourhood_cleansed", StringType(), True),
        StructField("number_of_reviews", DoubleType(), True),
        StructField("review_scores_rating", DoubleType(), True),
        StructField("last_review", StringType(), True),
    ])
    return spark.createDataFrame(data, schema)


@pytest.fixture
def neighbourhoods_data(spark):
    """Creates a mock DataFrame for neighbourhoods."""
    data = [
        ("Kreis 1", "City"),
        ("Kreis 1", "Hochschulen"),
    ]
    schema = StructType([
        StructField("neighbourhood_group", StringType(), True),
        StructField("neighbourhood", StringType(), True),
    ])
    return spark.createDataFrame(data, schema)


def test_process_landing_zone(spark, listings_data, neighbourhoods_data, tmp_path):
    """Tests the process_landing_zone function."""
    # Create temporary paths to simulate CSV files
    listings_path = str(tmp_path / "listings_details.csv")
    neighbourhoods_path = str(tmp_path / "neighbourhoods.csv")

    # Save the mock data as CSV files
    listings_data.write.option("header", True).csv(listings_path)
    neighbourhoods_data.write.option("header", True).csv(neighbourhoods_path)

    # Call the function
    listings_result, neighbourhoods_result = process_landing_zone(spark, listings_path, neighbourhoods_path)

    # Verify results for listings_details
    assert listings_result.count() == 3  # Should process all rows
    assert set(listings_result.columns) == {
        "id", "listing_url", "host_id", "neighbourhood",
        "neighbourhood_cleansed", "number_of_reviews",
        "review_scores_rating", "last_review"
    }

    # Verify that the data types are correct
    assert dict(listings_result.dtypes) == {
        "id": "bigint",
        "listing_url": "string",
        "host_id": "string",
        "neighbourhood": "string",
        "neighbourhood_cleansed": "string",
        "number_of_reviews": "double",
        "review_scores_rating": "double",
        "last_review": "string",
    }

    # Verify results for neighbourhoods
    assert neighbourhoods_result.count() == 2  # Should process all rows
    assert set(neighbourhoods_result.columns) == {"neighbourhood_group", "neighbourhood"}
