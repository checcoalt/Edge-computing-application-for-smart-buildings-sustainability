
class FrameType ():
    
    def __init__(self, encoding: str, type : str) -> None:
        self.encoding = encoding
        self.type = type

    def __str__(self) -> str:
        return f"<Type: {self.encoding} - {self.type}>"

FRAME_TYPES = {
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


class Libellium():

    def __init__(self, frame : str = '') -> None:

        """
        """
        
        self.frame = frame

        self.type = -1
        self.number_of_bytes = 0
        self.serial_id = ''
        self.waspmote_id = ''
        self.frame_sequence = ''

        # completare con self.co2_measure, ...

    # Overriding "to string" method to display informations in a proper way
    def __str__(self) -> str:
        return f"----------------------------------------\nFrame:\n\t{self.type}\n\t<Number of bytes: {self.number_of_bytes}>\n\t<Serial ID: {self.serial_id}>\n----------------------------------------"

    def hex_to_binary(self, hex_string: str) -> str:

        """
            Converts a hexadecimal string into a binary string.
        """

        integer_value = int(hex_string, 16)
        binary_string = bin(integer_value)[2:]  # Rimuovi il prefisso "0b"
        return binary_string

    def binary_to_char(self, binary_string : str) -> str:

        """
        """

        ascii_value = int(binary_string, 2)
        char = chr(ascii_value)

        return char
    
    def tokenize(self, hex_string: str) -> list:

        """
        """

        tokens = []

        for i in range(0, len(hex_string), 2):

            byte = self.hex_to_binary(hex_string[i:i+2])
            tokens.append('0' * (8 - len(byte)) + byte)

        return tokens


    def parse(self):

        """
        """

        tokens = self.tokenize(self.frame)

        # starter must be '<=>'
        starter = chr(int(tokens[0], 2)) + \
                  chr(int(tokens[1], 2)) + \
                  chr(int(tokens[2], 2))

        if starter != "<=>":
            raise Exception

        # read type (1 byte)
        self.type = FRAME_TYPES[int(tokens[3], 2)]

        # read number of bytes (1 byte)
        self.number_of_bytes = int(tokens[4], 2)

        # separator must be '#'
        separator = chr(int(tokens[5], 2))

        """if separator != "#":     LA STRINGA DI PROVA RISULTA ESSERE 1B = 27 = ESC
            raise Exception"""

        # read serial id (8 bytes)
        for i in range(6, 14):
            self.serial_id += tokens[i]

        self.serial_id = int(self.serial_id, 2)

        # qui dipende dalla configurazione .....


if __name__ == '__main__':

    frame = "3C3D3E06451B20B4BD3C195E206E6F64655F3031231434641500000000006185EB3F0100000000046179913E4A7B14C4414C005462424DBFD0C647460000000047000000004800000000"

    measure = Libellium(frame)
    measure.parse()

    print(measure)