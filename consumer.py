from kafka import KafkaConsumer

# Create a Kafka consumer
consumer = KafkaConsumer('user_music_recommendations_topic',
                         bootstrap_servers='localhost:9092')

# Consume and print music recommendations
for message in consumer:
    print(f"Received recommendation: {message.value.decode('utf-8')}")
