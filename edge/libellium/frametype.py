
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

