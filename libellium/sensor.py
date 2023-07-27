import json
from sys import argv

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
    
    def __str__(self):
        return f"{self.binary_id} - {self.ascii_id}: {self.name} [{self.tag}]"


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



def read_sensors(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        sensors = data.get('sensors', [])

        sensor_dict = {}
        for sensor_data in sensors:
            binary_id = sensor_data.get('binary_id')
            sensor = Sensor(**sensor_data)
            sensor_dict[binary_id] = sensor

            print(sensor + " read.")

        return sensor_dict
    
SENSORS = {}

if __name__ == "__main__":
    # Get sensor file loading mode from CLI
    try:
        mode = argv[1]
        sensor_dict = {}

        if mode == "latest":
            # Bind a URL from where latest sensor.json will be downloaded
            print("Available in future")

        elif mode == "local":
            # Leggi i dati dei sensori dal file JSON e popola il dizionario di oggetti
            SENSORS = read_sensors("sensor.json")

        else:
            raise ValueError
        
    except IndexError | ValueError:
        print("Usage: python -m sensor [local | latest]")
