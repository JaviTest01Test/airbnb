# src/data_validation.py
from pyspark.sql import SparkSession
from great_expectations.dataset import SparkDFDataset

def validate_data(df):
    """Validate the data using Great Expectations."""
    spark_df = SparkDFDataset(df)

    # Define expectations
    result1 = spark_df.expect_column_values_to_not_be_null("neighbourhood_group")
    result2 = spark_df.expect_column_values_to_be_between("review_scores_rating", 0, 5)

    # Return results
    return result1, result2