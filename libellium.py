# ************************************** LIBELLIUM MODULE **************************************

import struct

class FrameType:
    """
    Defines a simple structure to identify the frame's type.
    """

    def __init__(self, encoding: str, type: str):
        """
        Constructor for FrameType class.

        Args:
            encoding (str): Encoding type, e.g., 'Binary' or 'ASCII'.
            type (str): Type of the frame, e.g., 'Information', 'TimeOut', 'Event', etc.
        """
        self.encoding = encoding
        self.type = type

    def __str__(self) -> str:
        """
        Returns a string representation of the FrameType object.
        """
        return f"<Type: {self.encoding} - {self.type}>"


FRAME_TYPES = {
    # Defines a dictionary mapping all possible types of frames and their encoding rules.
    # The keys are hexadecimal frame type IDs, and the values are FrameType objects.
    
    0x00: FrameType('Binary', 'Information'),
    0x01: FrameType('Binary', 'TimeOut'),
    0x02: FrameType('Binary', 'Event'),
    0x03: FrameType('Binary', 'Alarm'),
    0x04: FrameType('Binary', 'Service1'),
    0x05: FrameType('Binary', 'Service2'),
    0x06: FrameType('Binary', 'Information'),
    0x07: FrameType('Binary', 'Information'),
    0x08: FrameType('Binary', 'Information'),
    0x60: FrameType('Binary', 'AES_ECB_FRAME_v15'),
    0x61: FrameType('Binary', 'AES128_ECB_FRAME_v12'),
    0x62: FrameType('Binary', 'AES192_ECB_FRAME_v12'),
    0x63: FrameType('Binary', 'AES256_ECB_FRAME_v12'),
    0x64: FrameType('Binary', 'AES128_ECB_END_TO_END_v15'),
    0x65: FrameType('Binary', 'AES128_ECB_END_TO_END_v12'),
    0x80: FrameType('ASCII', 'Information'),
    0x81: FrameType('ASCII', 'TimeOut'),
    0x82: FrameType('ASCII', 'Event'),
    0x83: FrameType('ASCII', 'Alarm'),
    0x84: FrameType('ASCII', 'Service1'),
    0x85: FrameType('ASCII', 'Service2'),
    0x86: FrameType('ASCII', 'Information'),
    0x87: FrameType('ASCII', 'Information'),
    0x88: FrameType('ASCII', 'Information'),
    0x9B: FrameType('ASCII', 'Tyme Sync')

}


class FrameTypeNotExists(Exception):
    """
    Defines an exception for an invalid type, related to the FRAME_TYPES dictionary.
    """

    def __init__(self, frame_type_id):
        """
        Constructor for FrameTypeNotExists exception.

        Args:
            frame_type_id: The ID of the frame type that does not exist in the FRAME_TYPES dictionary.
        """
        self.frame_type_id = frame_type_id

    def __str__(self) -> str:
        """
        Returns a string representation of the FrameTypeNotExists exception.
        """
        return f"Frame type with ID {self.frame_type_id} does not exist in the FRAME_TYPES dictionary."



class Sensor:
    """
    Represents a sensor with its properties.

    Attributes:
        name (str): Name of the sensor.
        reference (str): Reference code of the sensor.
        tag (str): Tag associated with the sensor.
        binary_id (int): Binary identifier of the sensor.
        ascii_id (str): ASCII identifier of the sensor.
        number_of_fields (int): Number of fields in the sensor data.
        fields_type (str): Type of the sensor's fields, e.g., 'float', 'int', 'string'.
        size_per_field (int): Size per field in bytes.
        default_decimal_precision (int): Default decimal precision for floating-point fields.
        unit (str): Measurement unit of the sensor data.
    """


    def __init__(
        self,
        name: str = '',
        reference: str = '',
        tag: str = '',
        binary_id: int = 0,
        ascii_id: str = '',
        number_of_fields: int = 0,
        fields_type: str = '',
        size_per_field: int = 0,
        default_decimal_precision: int = 0,
        unit: str = ''
    ):
        """
        Constructor for Sensor class.

        Args:
            name (str, optional): Name of the sensor. Default is an empty string.
            reference (str, optional): Reference code of the sensor. Default is an empty string.
            tag (str, optional): Tag associated with the sensor. Default is an empty string.
            binary_id (int, optional): Binary identifier of the sensor. Default is 0.
            ascii_id (str, optional): ASCII identifier of the sensor. Default is an empty string.
            number_of_fields (int, optional): Number of fields in the sensor data. Default is 0.
            fields_type (str, optional): Type of the sensor's fields, e.g., 'float', 'int', 'string'. Default is an empty string.
            size_per_field (int, optional): Size per field in bytes. Default is 0.
            default_decimal_precision (int, optional): Default decimal precision for floating-point fields. Default is 0.
            unit (str, optional): Measurement unit of the sensor data. Default is an empty string.
        """
        self.name = name
        self.reference = reference
        self.tag = tag
        self.binary_id = binary_id
        self.ascii_id = ascii_id
        self.number_of_fields = number_of_fields
        self.fields_type = fields_type
        self.size_per_field = size_per_field
        self.default_decimal_precision = default_decimal_precision
        self.unit = unit



    def string_convert(self, tokens : list) -> str:

        """
        Converts a list of binary tokens to a string.

        Args:
            tokens (list): The list of binary tokens.

        Returns:
            str: The converted string representation of the binary tokens.
        """

        measure = ''
        for token in tokens:
            measure += chr(int(token, 2))

            if chr(int(token, 2)) == '\0':
                break
        return measure



    def little_endian_conversion(self, byte_list : list, data_type : str):

        """
        Converts a little-endian byte list to its corresponding integer or floating-point value.

        Args:
            byte_list (list): The list of binary tokens representing the little-endian byte sequence.
            data_type (str): The data type to be converted. Supported types: 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', 'float'.

        Returns:
            Union[int, float]: The converted integer or floating-point value.
        
        Raises:
            ValueError: If the data type is not supported (use 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t', or 'float').
            ValueError: If the byte_list length does not match the expected size for the given data type.
        """

        if data_type == 'uint8_t':
            return int("".join(byte_list), 2)

        elif data_type == 'uint16_t':
            if len(byte_list) != 2:
                raise ValueError("La lista di byte per 'uint16_t' deve contenere esattamente 2 elementi.")
            return int("".join(byte_list[::-1]), 2)

        elif data_type == 'uint32_t':
            if len(byte_list) != 4:
                raise ValueError("La lista di byte per 'uint32_t' deve contenere esattamente 4 elementi.")
            return int("".join(byte_list[::-1]), 2)

        elif data_type == 'uint64_t':
            if len(byte_list) != 8:
                raise ValueError("La lista di byte per 'uint64_t' deve contenere esattamente 8 elementi.")
            return int("".join(byte_list[::-1]), 2)

        elif data_type == 'float':
            if len(byte_list) != 4:
                raise ValueError("La lista di byte per 'float' deve contenere esattamente 8 elementi.")
            else:
                binary_str = "".join(byte_list[::-1])

                sign_bit = int(binary_str[0])
                exponent_bits = binary_str[1:9]
                fraction_bits = binary_str[9:]

                sign = -1 if sign_bit else 1
                exponent = int(exponent_bits,2) - 127

                fraction = 1.0
                for i, bit in enumerate(fraction_bits):
                    fraction += int(bit) * 2 ** -(i + 1)

                result = sign * fraction * 2 ** exponent
                return result

        else:
            raise ValueError("Tipo di dato non supportato. Usare 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t' o 'float'.")
            


    def string_measure(self, measure) -> str:

        """
        Returns a formatted string representation of the sensor's measurement.

        Args:
            measure: Measurement value of the sensor.

        Returns:
            str: Formatted string representation of the sensor measurement.
        """
        return f"{self.name} [{self.tag}]: {measure} {self.unit}"


class SensorIdNotExists(Exception):
    """
    Defines an exception for an invalid sensor ID, related to the SENSORS dictionary.
    """

    def __init__(self, sensor_id):
        """
        Constructor for SensorIdNotExists exception.

        Args:
            sensor_id: The ID of the sensor that does not exist in the SENSORS dictionary.
        """
        self.sensor_id = sensor_id

    def __str__(self) -> str:
        """
        Returns a string representation of the SensorIdNotExists exception.
        """
        return f"Sensor with ID {self.sensor_id} does not exist in the SENSORS dictionary."


class UnexpectedTokenException(Exception):
    """
    Defines an exception for unexpected tokens in parsing the Libellium frame.
    """

    def __init__(self, position, token, expected_token):
        """
        Constructor for UnexpectedTokenException.

        Args:
            position (int): The position of the unexpected token.
            token (str): The unexpected token.
            expected_token (str): The token expected at the given position.
        """
        self.position = position
        self.token = token
        self.expected_token = expected_token

    def __str__(self):
        """
        Returns a string representation of the UnexpectedTokenException.
        """
        return f"Unexpected token in position {self.position}: '{self.token}', expected '{self.expected_token}'"


SENSORS = {
    0: Sensor('Carbon Monoxide - CO', '9229', 'SENSOR_GASES_CO', 0, 'CO', 1, 'float', 4, 3, 'ppm'),
    1: Sensor('Carbon Dioxide - CO2', '9230', 'SENSOR_GASES_CO2', 1, 'CO2', 1, 'float', 4, 3, 'ppm'),
    2: Sensor('Oxygen - O2', '9231', 'SENSOR_GASES_O2', 2, 'O2', 1, 'float', 4, 3, 'ppm'),
    3: Sensor('Methane - CH4', '9232', 'SENSOR_GASES_CH4', 3, 'CH4', 1, 'float', 4, 3, 'ppm'),
    4: Sensor('Ozone - O3', '9258', 'SENSOR_GASES_O3', 4, 'O3', 1, 'float', 4, 3, 'ppm'),
    5: Sensor('Ammonia - NH3', '9233', 'SENSOR_GASES_NH3', 5, 'NH3', 1, 'float', 4, 3, 'ppm'),
    6: Sensor('Nitrogen Dioxide - NO2', '9238', 'SENSOR_GASES_NO2', 6, 'NO2', 1, 'float', 4, 3, 'ppm'),
    7: Sensor('Liquefied Petroleum Gases', '9234', 'SENSOR_GASES_LPG', 7, 'LPG', 1, 'float', 4, 3, 'ppm'),
    8: Sensor('Air Pollutants 1', '9235', 'SENSOR_GASES_AP1', 8, 'AP1', 1, 'float', 4, 3, 'ppm'),
    9: Sensor('Air Pollutants 2', '9236', 'SENSOR_GASES_AP2', 9, 'AP2', 1, 'float', 4, 3, 'ppm'),
    10: Sensor('Solvent Vapors', '9237', 'SENSOR_GASES_SV', 10, 'SV', 1, 'float', 4, 3, 'ppm'),
    11: Sensor('Hydrocarbons - VOC', '9201', 'SENSOR_GASES_VOC', 11, 'VOC', 1, 'float', 4, 3, 'ppm'),
    12: Sensor('Nitrogen Monoxide - NO', '9375-P', 'SENSOR_GASES_PRO_NO', 12, 'NO', 1, 'float', 4, 3, 'ppm'),
    13: Sensor('Chlorine - CL2', '9386-P', 'SENSOR_GASES_PRO_CL2', 13, 'CL2', 1, 'float', 4, 3, 'ppm'),
    14: Sensor('Ethylene Oxide', '9385-P', 'SENSOR_GASES_PRO_ETO', 14, 'ETO', 1, 'float', 4, 3, 'ppm'),
    15: Sensor('Hydrogen - H2', '9380-P', 'SENSOR_GASES_PRO_H2', 15, 'H2', 1, 'float', 4, 3, 'ppm'),
    16: Sensor('Hydrogen Sulphide - H2S', '9381-P', 'SENSOR_GASES_PRO_H2S', 16, 'H2S', 1, 'float', 4, 3, 'ppm'),
    17: Sensor('Hydrogen Chloride - HCL', '9382-P', 'SENSOR_GASES_PRO_HCL', 17, 'HCL', 1, 'float', 4, 3, 'ppm'),
    18: Sensor('Hydrogen Cyanide - HCN', '9383-P', 'SENSOR_GASES_PRO_HCN', 18, 'HCN', 1, 'float', 4, 3, 'ppm'),
    19: Sensor('Phosphine - PH3', '9384-P', 'SENSOR_GASES_PRO_PH3', 19, 'PH3', 1, 'float', 4, 3, 'ppm'),
    20: Sensor('Sulfur Dioxide - SO2', '9377-P', 'SENSOR_GASES_PRO_SO2', 20, 'SO2', 1, 'float', 4, 3, 'ppm'),
    21: Sensor('Noise Level', 'TBD', 'SENSOR_CITIES_PRO_NOISE', 21, 'NOISE', 1, 'float', 4, 2, 'dBA'),
    30: Sensor('P&S! SOCKET A (gas sensor)', 'N/A', 'SENSOR_GASES_PRO_SOCKET_A', 30, 'GP_A', 1, 'float', 4, 3, 'ppm'),
    31: Sensor('P&S! SOCKET B (gas sensor)', 'N/A', 'SENSOR_GASES_PRO_SOCKET_B', 31, 'GP_B', 1, 'float', 4, 3, 'ppm'),
    32: Sensor('P&S! SOCKET C (gas sensor)', 'N/A', 'SENSOR_GASES_PRO_SOCKET_C', 32, 'GP_C', 1, 'float', 4, 3, 'ppm'),
    35: Sensor('P&S! SOCKET F (gas sensor)', 'N/A', 'SENSOR_GASES_PRO_SOCKET_F', 35, 'GP_F', 1, 'float', 4, 3, 'ppm'),
    40: Sensor('Water flow', '9296 / 9297 / 9298', 'SENSOR_EVENTS_WF', 40, 'WF', 1, 'float', 4, 3, 'l/min'),
    41: Sensor('PIR', '9212', 'SENSOR_EVENTS_PIR', 41, 'PIR', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    42: Sensor('Liquid presence', '9243', 'SENSOR_EVENTS_LP', 42, 'LP', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    43: Sensor('Liquid level', '9239 / 9240 / 9242', 'SENSOR_EVENTS_LL', 43, 'LL', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    44: Sensor('Hall effect', '9207', 'SENSOR_EVENTS_HALL', 44, 'HALL', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    45: Sensor('Relay input', 'N/A', 'SENSOR_EVENTS_RELAY_IN', 45, 'RIN', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    46: Sensor('Relay output', 'N/A', 'SENSOR_EVENTS_RELAY_OUT', 46, 'ROUT', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    47: Sensor('P&S! SOCKET A (binary)', 'N/A', 'SENSOR_EVENTS_SOCKET_A', 47, 'EV_A', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    48: Sensor('P&S! SOCKET C (binary)', 'N/A', 'SENSOR_EVENTS_SOCKET_C', 48, 'EV_C', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    49: Sensor('P&S! SOCKET D (binary)', 'N/A', 'SENSOR_EVENTS_SOCKET_D', 49, 'EV_D', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    50: Sensor('P&S! SOCKET E (binary)', 'N/A', 'SENSOR_EVENTS_SOCKET_E', 50, 'EV_E', 1, 'uint8_t', 1, 0, 'Open / Closed'),
    52: Sensor('Battery level', 'N/A', 'SENSOR_BAT', 52, 'BAT', 1, 'uint8_t', 1, 0, '%'),
    53: Sensor('Global Positioning System', 'N/A', 'SENSOR_GPS', 53, 'GPS', 2, 'float', 4, 6, 'degrees'),
    54: Sensor('RSSI', 'N/A', 'SENSOR_RSSI', 54, 'RSSI', 1, 'int', 2, 0, 'N/A'),
    55: Sensor('MAC Address', 'N/A', 'SENSOR_MAC', 55, 'MAC', 1, 'string', 'variable', 'N/A', 'N/A'),
    56: Sensor('Network Address (XBee)', 'N/A', 'SENSOR_NA', 56, 'NA', 1, 'string', 'variable', 'N/A', 'N/A'),
    57: Sensor('Network ID origin (XBee)', 'N/A', 'SENSOR_NID', 57, 'NID', 1, 'string', 'variable', 'N/A', 'N/A'),
    58: Sensor('Date', 'N/A', 'SENSOR_DATE', 58, 'DATE', 3, 'uint8_t', 1, 'N/A', 'N/A'),
    59: Sensor('Time', 'N/A', 'SENSOR_TIME', 59, 'TIME', 3, 'uint8_t', 1, 'N/A', 'N/A'),
    60: Sensor('GMT', 'N/A', 'SENSOR_GMT', 60, 'GMT', 1, 'int', 1, 'N/A', 'N/A'),
    61: Sensor('Free_RAM', 'N/A', 'SENSOR_RAM', 61, 'RAM', 1, 'int', 2, 0, 'bytes'),
    62: Sensor('Internal_temperature', 'N/A', 'SENSOR_IN_TEMP', 62, 'IN_TEMP', 1, 'float', 4, 2, 'ºC'),
    63: Sensor('Accelerometer', 'N/A', 'SENSOR_ACC', 63, 'ACC', 3, 'int', 2, 0, 'mg'),
    64: Sensor('Millis', 'N/A', 'SENSOR_MILLIS', 64, 'MILLIS', 1, 'uint32_t', 4, 0, 'ms'),
    65: Sensor('String', 'N/A', 'SENSOR_STR', 65, 'STR', 1, 'string', 'variable', 'N/A', 'N/A'),
    68: Sensor('Unique Identifier', 'N/A', 'SENSOR_UID', 68, 'UID', 1, 'string', 'variable', 'N/A', 'N/A'),
    70: Sensor('Particle Matter - PM1', '9387-P', 'SENSOR_GASES_PRO_PM1', 70, 'PM1', 1, 'float', 4, 4, 'μg/m3'),
    71: Sensor('Particle Matter - PM2.5', '9387-P', 'SENSOR_GASES_PRO_PM2_5', 71, 'PM2_5', 1, 'float', 4, 4, 'μg/m3'),
    72: Sensor('Particle Matter - PM10', '9387-P', 'SENSOR_GASES_PRO_PM10', 72, 'PM10', 1, 'float', 4, 4, 'μg/m3'),
    74: Sensor('BME - Temperature Celsius', '9370-P', 'SENSOR_GASES_TC', 74, 'TC', 1, 'float', 4, 2, 'ºC'),
    75: Sensor('BME - Temperature Farhenheit', '9370-P', 'SENSOR_GASES_TF', 75, 'TF', 1, 'float', 4, 2, 'ºF'),
    76: Sensor('BME - Humidity', '9370-P', 'SENSOR_GASES_HUM', 76, 'HUM', 1, 'float', 4, 1, '%RH'),
    77: Sensor('BME - Pressure', '9370-P', 'SENSOR_GASES_PRES', 77, 'PRES', 1, 'float', 4, 2, 'Pascales'),
    78: Sensor('Luxes', '9325', 'SENSOR_GASES_LUXES', 78, 'LUX', 1, 'uint32_t', 4, 0, 'luxes'),
    79: Sensor('Ultrasound', '9246-P', 'SENSOR_GASES_US', 79, 'US', 1, 'uint16_t', 2, 0, 'cm')
}




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
            raise UnexpectedTokenException("0-2", starter, "<=>")

        try:
            self.type = FRAME_TYPES[int(tokens[3], 2)]
        except FrameTypeNotExists:
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
            raise UnexpectedTokenException(index - 1, separator, "#")

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
                sensor = SENSORS[sensor_id]

                # Read strings of variable length until '\0'
                if sensor.fields_type == "string":
                    measure = sensor.string_convert(tokens[index:])
                    index += len(measure)
                    self.measurements.append((sensor, measure))

                else:
                    measure = []

                    try:
                        for token in tokens[index:index + sensor.size_per_field]:
                            measure.append(token)
                            index += 1
                    except IndexError:
                        print("Unexpected error: sensor measurement's length mismatch.")

                    # Little endian conversions
                    measure_decoded = sensor.little_endian_conversion(measure, sensor.fields_type)

                    self.measurements.append((sensor, measure_decoded))

            except SensorIdNotExists(sensor_id):
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
