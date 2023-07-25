import json
import mqttx
import config

class LoggerClient(mqttx.Client):
    """
    MQTT client to log incoming messages to a JSON file.
    """

    def __init__(self, broker: str, topic: str, filename: str):
        """
        Initialize the LoggerClient.

        Args:
            broker (str): The MQTT broker address.
            topic (str): The MQTT topic to subscribe to.
            filename (str): The name of the JSON log file.
        """
        super().__init__(broker, topic)
        self.filename = filename
        self.document = ''

    def start(self):
        """
        Start the MQTT client and connect to the broker.
        """
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
        client = LoggerClient(config.BROKER, config.TOPIC_MEASUREMENTS, "log.json")

        # Connect to the MQTT broker and start listening for messages
        client.start()

        while True:
            # Enter a loop to wait for a message
            print("[LOGGER MODULE] Waiting for message ...")
            while client.document == '':
                pass

            # Process the received message (in this case, just printing it)
            print("\n[LOGGER MODULE] Received message:\n", client.document)

            # Decode the received message as JSON
            json_result = json.loads(client.document)

            # Read the content of the existing JSON file into a list
            with open(client.filename, 'r') as file:
                list_json = json.load(file)
                list_json.append(json_result)

            # Write the updated list to the JSON file without overwriting existing data
            with open(client.filename, 'w') as file:
                json.dump(list_json, file, indent=4)

            # Clean document to avoid loop
            client.document = ''

            print("\n[LOGGER MODULE]: Log file updated.\n")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Stop the MQTT client
        client.stop()
