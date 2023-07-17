# TCP MODULE
# Collects informations from remote sensors.

import socket
import libellium_parser, mqttx_publisher

class TCP_module():


    def __init__(self,
                 ip_address = 'localhost',
                 port_number = 0,
                 buffer_size = 1024) -> None:
        
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

        # Socket creation
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind
        s.bind((self.ip_address, self.port_number))

        # Listen
        s.listen(1)

        # Message at start
        print("server on: ", self.ip_address, "port: ", self.port_number)

        # Accept: returns a tuple (socket, (ip, port)) of the client
        connection, client_address = s.accept()
        print("Client: " + str(client_address))

        # Receive: writes the established number of bytes into the buffer
        self.buffer = connection.recv(self.buffer_size)



    def decode(self) -> dict:

        """
            Decodes frame into strcutured data.
            Parser's logic is implemented into 'libellium_parser' module.

            Returns a dictionary of type <measure_type, measure_value>.
        """

        parser = libellium_parser.Parser()
        measurement = parser.parse()
        return measurement

    

    def to_mqtt_broker(self) -> bool:

        """
            Publishes on the broker for the selected topic.
            Publisher's logic is implemented into 'mqttx_publisher' module.

            Returns True if publish is successful, False otherwise.
        """

        publisher = mqttx_publisher.Pubisher()
        result = publisher.publish()
        return result




if __name__ == '__main__':

    print("[TCP MODULE]: Test main.")

    test = TCP_module()

    result = False

    try:
        test.start()
        measurement = test.decode()
        result = test.to_mqtt_broker(measurement)

        print("[TCP MODULE]: Tested successfully.")
    except:
        pass
    # except socketError, decoderError, publisherError