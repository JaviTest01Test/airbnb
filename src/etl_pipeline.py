from pyspark.sql import SparkSession
from pyspark.sql.types import LongType, DoubleType
from pyspark.sql import functions as F

def process_landing_zone(spark: SparkSession, listings_path: str, neighbourhoods_path: str):
    """
    Processes data in the Landing Zone:
    - Filters the necessary columns.
    - Applies the appropriate schema.

    Args:
        spark (SparkSession)
        listings_path (str): Ruta al archivo listings_details.csv.
        neighbourhoods_path (str): Ruta al archivo neighbourhoods.csv.

    Returns:
        tuple: DataFrames (listings_details, neighbourhoods)
    """
    # Define the necessary columns
    columns_needed = [
        "id", "listing_url", "host_id", "neighbourhood",
        "neighbourhood_cleansed", "number_of_reviews",
        "review_scores_rating", "last_review"
    ]

    # Read listings_details.csv
    listings_details = spark.read.option("header", True).csv(listings_path)

    # Select the necessary columns
    listings_details = listings_details.select(*columns_needed)

    # Apply the schema
    listings_details = listings_details \
        .withColumn("id", F.col("id").cast(LongType())) \
        .withColumn("number_of_reviews", F.col("number_of_reviews").cast(DoubleType())) \
        .withColumn("review_scores_rating", F.col("review_scores_rating").cast(DoubleType()))

    # Read neighbourhoods.csv (if you need to merge data later)
    neighbourhoods = spark.read.option("header", True).csv(neighbourhoods_path)
    
    return listings_details, neighbourhoods