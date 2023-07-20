# TCP MODULE
# Collects informations from remote sensors.

import socket, threading
import libellium, mqttx
import config


class TcpModule():


    def __init__(self,
                 ip_address : str = 'localhost',
                 port_number : int = 0,
                 buffer_size : int = 1024) -> None:
        
        """
            Constructor: defines a configurable method to init TCP server.
                @param ip_address: str     Host's ip address
                @param port_number: int    Host's port number where it is listening
                @param buffer_size: int    Max dimension in bytes readble from messages
        """
        
        self.ip_address = ip_address    # localhost if not specified
        self.port_number = port_number  # gets the first port available if not specified
        self.buffer_size = buffer_size  # 1024 (1 KB) if not specified

        self.buffer = ''                # inits an empty buffer where raw data will be written


    def start(self) -> None:

        """
            Starts a TCP connection.
        """

        try:
            # Socket creation
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind
            s.bind((self.ip_address, self.port_number))

            # Listen (max 5 connections)
            s.listen(5)

            # Message at start
            print(f"[TCP MODULE] Server on: <{self.ip_address}, {self.port_number}>")

            # Always listening for new connections
            while True:

                # Accept: returns a tuple (socket, (ip, port)) of the client
                connection, client_address = s.accept()
                print("[TCP MODULE] Client: " + str(client_address))

                # start a new thread
                t = threading.Thread(target = self.thread_function, args=(connection,))
                t.start()

        except socket.error as e:
            print("[TCP MODULE] TCP connection error: " + str(e))


    def decode(self) -> str:   # str deve diventare dict

        """
            Decodes frame into strcutured data.
            Parser's logic is implemented into 'libellium' module.

            Returns a dictionary with collected informations: <measure_type, measure_value>.
        """

        try:
            measurement = libellium.Libellium(self.buffer)
            measurement.parse()
            print(measurement)

            # Measurement -> dict

            return str(measurement)
        except:
            pass


    def to_mqtt_broker(self, measures : str) -> None:       # str deve diventare dict

        """
            Publishes on the broker for the selected topic.
            Publisher's logic is implemented into 'mqttx' module.

            @param measures : dict  A dictionary of couples of kind <measure_type, measure_value>
        """

        try:
            # Starts a MQTTX client
            publisher = mqttx.Client(config.BROKER, config.TOPIC_MEASUREMENTS)
            publisher.start()

            ################# Qui il dict va trasformato in JSON

            # Publish on the given topic
            publisher.publish(measures)

            # Kills the client
            publisher.stop()
        
        except mqttx.MqttConnectionError:
            print("[MQTTX MODULE]: connection error.")
        except mqttx.MqttSubscriptionError:
            print("[MQTTX MODULE]: subscription error.")
        except mqttx.MqttPublishError:
            print("[MQTTX MODULE]: publish error.")


    def thread_function(self, connection):

        """
            When a connection is established, this function represents a thread
            whose waits for new messages on the given connection, and completes
            expected tasks of this module for the received data.
        """

        while True:
            # Receive: writes the established number of bytes into the buffer
            self.buffer = connection.recv(self.buffer_size).decode("utf-8")

            # Do stuffs
            measurement = self.decode()
            self.to_mqtt_broker(measurement)


if __name__ == '__main__':

    print("[TCP MODULE]: Test main.")

    test = TcpModule('localhost', 8000, 1024)

    test.start()