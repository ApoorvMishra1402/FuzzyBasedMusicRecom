from kafka import KafkaProducer
import json

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Sample user music preferences data
user_preferences = {
    "user_id": 123,
    "preferences": {
        "Electronic": 0.7,
        "Rap": 0.3,
        "Anime": 0.5,
        "Hip-Hop": 0.8,
        "Jazz": 0.4,
        "Blues": 0.2,
        "Country": 0.6,
        "Alternative": 0.9,
        "Classical": 0.3,
        "Rock": 0.7
    }
}

# Send user music preferences data to Kafka topic
producer.send('user_music_preferences_topic',
              value=json.dumps(user_preferences))
