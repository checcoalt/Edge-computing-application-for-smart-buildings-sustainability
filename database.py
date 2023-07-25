from pymongo import MongoClient
from json import loads
import mqttx
import config

class DatabaseClient(mqttx.Client):
    """
    MQTT client to store incoming messages in a MongoDB database.
    """

    def __init__(self, broker: str, topic: str, db_name: str, collection: str):
        super().__init__(broker, topic)

        # Connection details for MongoDB
        # Replace "mongodb://localhost:27017" with your MongoDB server connection URL
        self.connection_string = "mongodb://localhost:27017"
        self.database_name = db_name
        self.collection_name = collection

        self.document = ''

    def start(self):
        """
        Connects to the MongoDB server, accesses the specified database and collection,
        and starts the MQTT client to listen for incoming messages.
        """
        # Connect to the MongoDB server
        self.mongo_client = MongoClient(self.connection_string)

        # Access the specified database
        self.db = self.mongo_client[self.database_name]

        # Access the specified collection
        self.collection = self.db[self.collection_name]

        # Start the MQTT client
        super().start()

    def on_message(self, client, userdata, msg):
        """
        Callback when a new message on the subscribed topic is received.
        Stores the received message in the 'document' variable.

        Args:
            client: The MQTT client instance.
            userdata: User-defined data.
            msg (mqtt.MQTTMessage): The received message.
        """
        self.document = msg.payload.decode()


if __name__ == "__main__":
    try:
        # Create an MQTT client and set the on_message callback
        client = DatabaseClient(config.BROKER, config.TOPIC_MEASUREMENTS, "DTLab", "measurements")

        # Connect to the MQTT broker and start listening for messages
        client.start()

        while True:
            # Enter a loop to wait for a message
            print("[DATABASE MODULE] Waiting for message ...")
            while client.document == '':
                pass

            # Process the received message (in this case, just printing it)
            print("\n[DATABASE MODULE] Received message:\n", client.document)

            # Insert the document into the collection
            json_result = loads(client.document)
            insert_result = client.collection.insert_one(json_result)

            # Clean document to avoid loop
            client.document = ''

            # Check if the document was inserted successfully
            if insert_result.acknowledged:
                print("[DATABASE MODULE] Document inserted successfully.")
                print("[DATABASE MODULE] Inserted document ID:", insert_result.inserted_id)
            else:
                print("[DATABASE MODULE] Failed to insert document.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Stop the MQTT client
        client.stop()
