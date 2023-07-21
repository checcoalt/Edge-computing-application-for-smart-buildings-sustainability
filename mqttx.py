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



"""
    Exception classes for MQTT protocol
"""

class MqttConnectionError(Exception):
    def __init__(self, message="MQTT connection error"):
        self.message = message
        super().__init__(self.message)

class MqttSubscriptionError(Exception):
    def __init__(self, message="MQTT subscription error"):
        self.message = message
        super().__init__(self.message)

class MqttPublishError(Exception):
    def __init__(self, message="MQTT message publish error"):
        self.message = message
        super().__init__(self.message)

class MqttTopicNotSpecified(Exception):
    def __init__(self, message="MQTT topic not specified"):
        self.message = message
        super().__init__(self.message)


"""
    Class for a MQTT client.
    Defines methods for start and stop the client, publishing and subscribing.
    It also defines two event handlers (connection, message).
"""

class Client():

    def __init__(self, broker : str, topic : str = '') -> None:

        """
            Constructor: initializes client configuration and utility attributes.
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
            Callback when client connects to the broker.
        """        

        try:
            print("[MQTTX MODULE] Connection outcome: " + RETURN_CODES[rc])

            if rc == 0 and self.topic != '':
                # Subscription to a topic after connection
                client.subscribe(self.topic)
                self.subscriptions.append(self.topic)

        except KeyError:
            print("[MQTTX MODULE] Connection outcome: " + "FAILURE - unknown reason") 
        

    def on_message(client, userdata, msg):

        """
            Callback when a new message on a topic in which client is subscribed is received.
        """

        print("[MQTTX MODULE] TOPIC: " + msg.topic + " - PAYLOAD: " + str(msg.payload))


    def start(self):

        """
            Starts connection to the broker.
        """

        # MQTT broker connectioon
        self.client.connect(self.broker, 1883, 60)

        # Starts MQTT connection manager loop
        self.client.loop_start()


    def publish(self, message : str, topic : str = ''):

        """
            Publishes specified message on the specified topic.
        """

        # Publishes a message on a topic.
        if self.topic != '':
            message_id = self.client.publish(self.topic, message)
        elif topic != '':
            message_id = self.client.publish(topic, message)
        else:
            raise MqttTopicNotSpecified

        # Raise an error if message has no id (publish failed).
        if message_id is None:
            raise MqttPublishError
        
    def subscribe (self, topic : str):

        """
            Subscription to a new topic.
        """
        
        self.client.subscribe(topic)
        self.subscriptions.append(topic)

    def stop(self):

        """
            Connection shut down.
        """
        
        self.client.loop_stop()
        self.client.disconnect()




if __name__ == '__main__':

    print("[MQTTX MODULE]: Test main.")

    BROKER = "broker.emqx.io"
    TOPIC = "DTLab/measurements"
    MESSAGE = "Test message: " + str(randint(1, 10))

    test = Client(BROKER, TOPIC)

    try:
        test.start()
        result = test.publish(MESSAGE)
        test.stop()
        print("[MQTTX MODULE]: Tested successfully.")
    
    except MqttConnectionError:
        print("[MQTTX MODULE]: connection error.")
    except MqttSubscriptionError:
        print("[MQTTX MODULE]: subscription error.")
    except MqttTopicNotSpecified:
        print("[MQTTX MODULE]: topic not specified.")
    except MqttPublishError:
        print("[MQTTX MODULE]: publish error.")