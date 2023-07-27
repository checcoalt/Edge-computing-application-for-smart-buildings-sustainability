# ************************************** MQTTX MODULE **************************************

from random import randint
import paho.mqtt.client as mqtt


"""
    Defines a dictionary containing all the return codes
    that could be found inside a connection response message.
"""

RETURN_CODES = {
    0: "SUCCESS",
    1: "FAILURE - unacceptable protocol version",
    2: "FAILURE - identifier rejected",
    3: "FAILURE - server unavailable",
    4: "FAILURE - bad username or password",
    5: "FAILURE - not authorized",
}



class MqttConnectionError(Exception):
    """
    Exception class for MQTT connection errors.
    """

    def __init__(self, message="MQTT connection error"):
        """
        Constructor for MqttConnectionError exception.

        Args:
            message (str, optional): Custom error message. Defaults to "MQTT connection error".
        """
        self.message = message
        super().__init__(self.message)


class MqttSubscriptionError(Exception):
    """
    Exception class for MQTT subscription errors.
    """

    def __init__(self, message="MQTT subscription error"):
        """
        Constructor for MqttSubscriptionError exception.

        Args:
            message (str, optional): Custom error message. Defaults to "MQTT subscription error".
        """
        self.message = message
        super().__init__(self.message)


class MqttPublishError(Exception):
    """
    Exception class for MQTT message publish errors.
    """

    def __init__(self, message="MQTT message publish error"):
        """
        Constructor for MqttPublishError exception.

        Args:
            message (str, optional): Custom error message. Defaults to "MQTT message publish error".
        """
        self.message = message
        super().__init__(self.message)


class MqttTopicNotSpecified(Exception):
    """
    Exception class for MQTT topic not specified errors.
    """

    def __init__(self, message="MQTT topic not specified"):
        """
        Constructor for MqttTopicNotSpecified exception.

        Args:
            message (str, optional): Custom error message. Defaults to "MQTT topic not specified".
        """
        self.message = message
        super().__init__(self.message)


class Client:
    """
    Class for an MQTT client.

    This class defines methods for starting and stopping the client, publishing messages, and subscribing to topics.
    It also defines two event handlers: on_connect and on_message.

    Attributes:
        broker (str): The MQTT broker's address to connect to.
        topic (str): The topic to subscribe or publish to.
        subscriptions (list): A list to store subscribed topics.
        client (mqtt.Client): The MQTT client instance.
    """

    def __init__(self, broker: str, topic: str = ''):
        """
        Constructor for Client class.

        Args:
            broker (str): The MQTT broker's address to connect to.
            topic (str, optional): The topic to subscribe or publish to. Defaults to an empty string.
        """
        # MQTT client configuration
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Initializing attributes
        self.broker = broker
        self.topic = topic
        self.subscriptions = []

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback when the client connects to the broker.

        Args:
            client: The MQTT client instance.
            userdata: User-defined data.
            flags: Response flags from the broker.
            rc (int): The connection result code.
        """
        try:
            print("[MQTTX MODULE] Connection outcome: " + RETURN_CODES[rc])

            if rc == 0 and self.topic != '':
                client.subscribe(self.topic)
                self.subscriptions.append(self.topic)

        except KeyError:
            print("[MQTTX MODULE] Connection outcome: " + "FAILURE - unknown reason")

    def on_message(self, client, userdata, msg):
        """
        Callback when a new message on a subscribed topic is received.

        Args:
            client: The MQTT client instance.
            userdata: User-defined data.
            msg (mqtt.MQTTMessage): The received message.
        """
        print("[MQTTX MODULE] TOPIC: " + msg.topic + " - PAYLOAD: " + str(msg.payload))

    def start(self):
        """
        Starts the connection to the MQTT broker.
        """
        self.client.connect(self.broker, 1883, 60)
        self.client.loop_start()

    def publish(self, message: str, topic: str = ''):
        """
        Publishes a specified message on the specified topic.

        Args:
            message (str): The message to be published.
            topic (str, optional): The topic to publish the message to. Defaults to an empty string.

        Raises:
            MqttTopicNotSpecified: If neither the default topic nor a custom topic is specified.
            MqttPublishError: If the message publish fails.
        """
        if self.topic != '':
            message_id = self.client.publish(self.topic, message)
        elif topic != '':
            message_id = self.client.publish(topic, message)
        else:
            raise MqttTopicNotSpecified

        if message_id is None:
            raise MqttPublishError

    def subscribe(self, topic: str):
        """
        Subscribes to a new topic.

        Args:
            topic (str): The topic to subscribe to.

        Raises:
            MqttSubscriptionError: If the subscription fails.
        """
        self.client.subscribe(topic)
        self.subscriptions.append(topic)

    def stop(self):
        """
        Stops the MQTT connection.
        """
        self.client.loop_stop()
        self.client.disconnect()
