from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import json

# Create a Spark session
spark = SparkSession.builder.appName("FuzzyMusicRecommender").getOrCreate()

# Create a StreamingContext with a batch interval of x seconds
ssc = StreamingContext(spark.sparkContext, batchDuration=5)

# Read data from Kafka topic for music preferences
stream = ssc \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user_music_preferences_topic") \
    .load()

# Assume the stream has columns: key, value, timestamp, ...
# We'll use the "value" column containing user preferences JSON
stream = stream.selectExpr("CAST(value AS STRING)")

# Define trapezoidal membership functions for music genres


def trapezoidal_membership(x, lower_left, lower_peak, upper_peak, upper_right):
    if x <= lower_left or x >= upper_right:
        return 0
    elif lower_left <= x <= lower_peak:
        return (x - lower_left) / (lower_peak - lower_left)
    elif lower_peak <= x <= upper_peak:
        return 1
    else:
        return (upper_right - x) / (upper_right - upper_peak)

# Define advanced fuzzy rules and inference for music genres


def fuzzy_inference(preferences_json):
    preferences = json.loads(preferences_json)

    # Define membership function parameters for multiple music genres
    membership_params = {
        "Electronic": {"lower_left": 0.2, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Rap": {"lower_left": 0.1, "lower_peak": 0.3, "upper_peak": 0.7, "upper_right": 0.9},
        "Anime": {"lower_left": 0.0, "lower_peak": 0.2, "upper_peak": 0.5, "upper_right": 0.7},
        "Hip-Hop": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Jazz": {"lower_left": 0.2, "lower_peak": 0.5, "upper_peak": 0.7, "upper_right": 0.9},
        "Blues": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Country": {"lower_left": 0.0, "lower_peak": 0.2, "upper_peak": 0.5, "upper_right": 0.7},
        "Alternative": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8},
        "Classical": {"lower_left": 0.2, "lower_peak": 0.5, "upper_peak": 0.7, "upper_right": 0.9},
        "Rock": {"lower_left": 0.1, "lower_peak": 0.4, "upper_peak": 0.6, "upper_right": 0.8}
        # Add more genres and parameters as needed
    }

    recommendation_strengths = {}

    for genre, params in membership_params.items():
        membership_value = preferences.get(genre, 0)
        membership_function = trapezoidal_membership(
            membership_value, params["lower_left"], params["lower_peak"], params["upper_peak"], params["upper_right"]
        )

        # Define advanced fuzzy rules and recommendation strengths based on membership values
        if membership_function > 0:
            recommendation_strengths[genre] = membership_function * 0.8
            # Add more rules and genres as needed

    # Combine recommendation strengths based on fuzzy rules
    recommendation = max(recommendation_strengths,
                         key=recommendation_strengths.get)

    return recommendation


fuzzy_inference_udf = udf(fuzzy_inference, StringType())

# Apply the advanced fuzzy inference UDF to create a new column "recommendation"
stream_with_recommendation = stream.withColumn(
    "recommendation", fuzzy_inference_udf(stream["value"]))

# Save processed music genre recommendations to another storage system (e.g., Parquet files)
query = stream_with_recommendation \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "processed_music_data/") \
    .option("checkpointLocation", "music_checkpoint/") \
    .start()

# Start the streaming context
ssc.start()
ssc.awaitTermination()
