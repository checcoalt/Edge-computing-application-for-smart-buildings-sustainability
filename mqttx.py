from random import randint
import paho.mqtt.client as mqtt


RETURN_CODES = {
    0: "SUCCESS",
    1: "FAILURE - unacceptable protocol version",
    2: "FAILURE - identifier rejected",
    3: "FAILURE - server unavailable",
    4: "FAILURE - bad username or password",
    5: "FAILURE - not authorized",
}


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


class Client():

    def __init__(self, broker : str, topic : str) -> None:
        # Configurazione del client MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.broker = broker
        self.topic = topic

    # Callback quando il client MQTT è connesso al broker
    def on_connect(self, client, userdata, flags, rc):

        try:
            print("[MQTTX MODULE] Connection outcome: " + RETURN_CODES[rc])

            if rc == 0:
                # Sottoscrizione a un topic dopo la connessione
                client.subscribe(self.topic)

        except KeyError:
            print("[MQTTX MODULE] Connection outcome: " + "FAILURE - unknown reason") 
        

    # Callback quando un messaggio viene ricevuto da un topic a cui si è sottoscritti
    def on_message(client, userdata, msg):
        print("[MQTTX MODULE] Ricevuto messaggio su topic: " + msg.topic + " - Contenuto: " + str(msg.payload))

    def start(self):

        # Connessione al broker MQTT
        self.client.connect(self.broker, 1883, 60)

        # Avvio del loop di gestione delle comunicazioni MQTT
        self.client.loop_start()


    def publish(self, message : str):

        # Pubblicazione di un messaggio su un topic
        message_id = self.client.publish(self.topic, message)

        # Returns True if message has been successfully published, False otherwise.
        if message_id is None:
            raise MqttPublishError

    def stop(self):

        # Disconnessione dal broker MQTT
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
    except MqttPublishError:
        print("[MQTTX MODULE]: publish error.")