# ************************************** LIBELLIUM MODULE **************************************

import libellium.sensor as sensor
import libellium.frametype as ft


SENSORS = sensor.read_sensors("libellium/sensor.json")


class Libellium:
    """
    Represents a Libellium frame and provides methods for parsing it.

    Attributes:
        frame (str): The input Libellium frame in hexadecimal format.
        type (FrameType): The type of the Libellium frame.
        number_of_bytes (int): The number of bytes in the frame.
        serial_id (str): The serial ID of the frame.
        waspmote_id (str): The Waspmote ID associated with the frame.
        frame_sequence (int): The frame sequence number.
        measurements (list): A list of tuples containing (Sensor, measurement) pairs.
    """


    def __init__(self, frame: str):
        """
        Constructor for Libellium class.

        Args:
            frame (str): The input Libellium frame in hexadecimal format.
        """
        self.frame = frame
        self.type = -1
        self.number_of_bytes = 0
        self.serial_id = ''
        self.waspmote_id = ''
        self.frame_sequence = 0
        self.measurements = []



    def __str__(self) -> str:

        """
        String representation of decoded frame.
        """

        string = f"------------------------------------------------------------------------------------------------------------------------\
        \nFrame:\
        \n\t{self.type}\
        \n\t<Number of bytes: {self.number_of_bytes}>\
        \n\t<Serial ID: {self.serial_id}>\
        \n\t<Waspmote ID: {self.waspmote_id}>\
        \n\t<Frame sequence: {self.frame_sequence}>\
        \n\n"

        for measure in self.measurements:
            s = measure[0]
            m = measure[1]
            string += f"\t<SENSOR>\t{s.string_measure(m)}\n"

        string += "\n------------------------------------------------------------------------------------------------------------------------"
        return string



    def hex_to_binary(self, hex_string: str) -> str:
        """
        Converts a hexadecimal string into a binary string.

        Args:
            hex_string (str): The hexadecimal string to be converted.

        Returns:
            str: The binary representation of the input hexadecimal string.
        """
        integer_value = int(hex_string, 16)
        binary_string = bin(integer_value)[2:]  # Remove the prefix "0b"
        return binary_string



    def binary_to_char(self, binary_string: str) -> str:
        """
        Converts a binary string into a character.

        Args:
            binary_string (str): The binary string to be converted.

        Returns:
            str: The character representation of the input binary string.
        """
        ascii_value = int(binary_string, 2)
        char = chr(ascii_value)
        return char



    def tokenize(self, hex_string: str) -> list:
        """
        Tokenizes a hexadecimal string into a list of binary strings.

        Args:
            hex_string (str): The hexadecimal string to be tokenized.

        Returns:
            list: A list of binary strings representing tokens from the input hexadecimal string.
        """
        tokens = []
        for i in range(0, len(hex_string), 2):
            byte = self.hex_to_binary(hex_string[i:i + 2])
            tokens.append('0' * (8 - len(byte)) + byte)
        return tokens
    


    def parse_header(self) -> int:

        """
        Parses the Libellium frame header and populates the relevant attributes.

        Returns:
            int: The index of the first token in the payload after parsing the header.
        """

        tokens = self.tokenize(self.frame)

        starter = chr(int(tokens[0], 2)) + chr(int(tokens[1], 2)) + chr(int(tokens[2], 2))

        if starter != "<=>":
            raise sensor.UnexpectedTokenException("0-2", starter, "<=>")

        try:
            self.type = ft.FRAME_TYPES[int(tokens[3], 2)]
        except ft.FrameTypeNotExists:
            print("[LIBELLIUM] Frame type not found.")

        self.number_of_bytes = int(tokens[4], 2)

        for token in tokens[5:13]:
            self.serial_id += token
        self.serial_id = int(self.serial_id, 2)

        self.waspmote_id = ''
        index = 13
        for token in tokens[13:]:
            if token == '00100011':  # '00100011' = 0x23 = 35 = '#'
                break
            else:
                self.waspmote_id += chr(int(token, 2))
                index += 1

        separator = chr(int(tokens[index], 2))

        if separator != "#":
            raise sensor.UnexpectedTokenException(index - 1, separator, "#")

        index += 1
        self.frame_sequence = int(tokens[index], 2)
        index += 1

        return index



    def parse_payload(self, index : int):

        """
        Parses the Libellium frame payload and populates the measurements list.

        Args:
            index (int): The index of the first token in the payload.
        """

        tokens = self.tokenize(self.frame)

        end_of_frame = False
        while not end_of_frame:
            try:
                sensor_id = int(tokens[index], 2)
                index += 1
                sensor_obj = SENSORS[sensor_id]

                # Read strings of variable length until '\0'
                if sensor_obj.fields_type == "string":
                    measure = sensor_obj.string_convert(tokens[index:])
                    index += len(measure)
                    self.measurements.append((sensor_obj, measure))

                else:
                    measure = []

                    try:
                        for token in tokens[index:index + sensor_obj.size_per_field]:
                            measure.append(token)
                            index += 1
                    except IndexError:
                        print("Unexpected error: sensor measurement's length mismatch.")

                    # Little endian conversions
                    measure_decoded = sensor_obj.little_endian_conversion(measure, sensor_obj.fields_type)

                    self.measurements.append((sensor_obj, measure_decoded))

            except sensor.SensorIdNotExists(sensor_id):
                print("[LIBELLIUM] Sensor ID not valid.")

            try:
                tokens[index]
            except IndexError:
                end_of_frame = True



    def parse(self):
        """
        Parses the Libellium frame and populates the class attributes accordingly.
        It works by calling two distinct functions to decode header and then payload,
        by resuming from the same index in the tokens' list.
        """
        
        index_payload = self.parse_header()
        self.parse_payload(index_payload)



if __name__ == '__main__':
    frame = "3C3D3E06451B20B4BD3C195E206E6F64655F3031231434641500000000006185EB3F0100000000046179913E4A7B14C4414C005462424DBFD0C647460000000047000000004800000000"

    measure = Libellium(frame)
    measure.parse()

    print(measure)
