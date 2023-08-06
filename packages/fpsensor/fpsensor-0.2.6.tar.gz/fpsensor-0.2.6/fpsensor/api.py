#!/usr/bin/python
# -*- coding: ascii -*-
"""
Fingerprint API definitions.

:date:      2021
:author:    Christian Wiche
:contact:   cwichel@gmail.com
:license:   The MIT License (MIT)
"""

import math
import typing as tp

import attr
import PIL.Image as PilI
import embutils.utils as embu

# -->> Definitions <<------------------
ADDRESS         = 0xFFFFFFFF        # Default address
PASSWORD        = 0x00000000        # Default password
NOTEPAD_SIZE    = 32                # Notepad size : 32 bytes per page
NOTEPAD_COUNT   = 16                # Notepad count: 16 pages


class FpPID(embu.IntEnum):
    """
    Fingerprint packet IDs.
    """
    COMMAND     = 0x01          # Command
    DATA        = 0x02          # Data
    ACK         = 0x07          # Acknowledge
    END_OF_DATA = 0x08          # End of data


class FpCommand(embu.IntEnum):
    """
    Fingerprint command IDs.
    """
    # System
    ADDRESS_SET             = 0x15
    PASSWORD_SET            = 0x12
    PASSWORD_VERIFY         = 0x13
    PARAMETERS_SET          = 0x0E
    PARAMETERS_GET          = 0x0F
    HANDSHAKE               = 0x53

    # Image
    IMAGE_CAPTURE           = 0x01
    IMAGE_CAPTURE_FREE      = 0x52
    IMAGE_CONVERT           = 0x02
    IMAGE_UPLOAD            = 0x0B
    IMAGE_DOWNLOAD          = 0x0A

    # Template
    TEMPLATE_MATCH          = 0x03
    TEMPLATE_SEARCH         = 0x04
    TEMPLATE_SEARCH_FAST    = 0x1B
    TEMPLATE_CREATE         = 0x05
    TEMPLATE_SAVE           = 0x06
    TEMPLATE_LOAD           = 0x07
    TEMPLATE_UPLOAD         = 0x09
    TEMPLATE_DOWNLOAD       = 0x08
    TEMPLATE_DELETE         = 0x0C
    TEMPLATE_EMPTY          = 0x0D
    TEMPLATE_COUNT          = 0x1D
    TEMPLATE_INDEX          = 0x1F

    # Extras
    NOTEPAD_SET             = 0x18
    NOTEPAD_GET             = 0x19
    GENERATE_RANDOM         = 0x14
    BACKLIGHT_ON            = 0x50
    BACKLIGHT_OFF           = 0x51


class FpError(embu.IntEnum):
    """
    Fingerprint error IDs.
    """
    SUCCESS                             = 0x00
    HANDSHAKE_SUCCESS                   = 0x55

    ERROR_INVALID_REGISTER              = 0x1A
    ERROR_INVALID_CONFIGURATION         = 0x1B

    ERROR_NOTEPAD_INVALID_PAGE          = 0x1C

    ERROR_PACKET_TRANSMISSION           = 0x01
    ERROR_PACKET_RECEPTION              = 0x0E

    ERROR_FINGER_NOT_IN_SENSOR          = 0x02
    ERROR_FINGER_ENROLL_FAILED          = 0x03
    ERROR_FINGER_MISMATCH               = 0x08
    ERROR_FINGER_NOT_FOUND              = 0x09

    ERROR_IMAGE_MESSY                   = 0x06
    ERROR_IMAGE_INVALID                 = 0x15
    ERROR_IMAGE_FEW_FEATURE_POINTS      = 0x07
    ERROR_IMAGE_DOWNLOAD                = 0x0F

    ERROR_CHARACTERISTICS_MISMATCH      = 0x0A

    ERROR_TEMPLATE_INVALID_INDEX        = 0x0B
    ERROR_TEMPLATE_LOAD                 = 0x0C
    ERROR_TEMPLATE_UPLOAD               = 0xFD
    ERROR_TEMPLATE_DOWNLOAD             = 0x0D
    ERROR_TEMPLATE_DELETE               = 0x10
    ERROR_TEMPLATE_EMPTY                = 0x11

    ERROR_FLASH                         = 0x18
    ERROR_UNDEFINED                     = 0x19
    ERROR_COMMUNICATION_PORT            = 0x1D

    ERROR_ADDRESS                       = 0x20
    ERROR_PASSWORD                      = 0x13
    ERROR_PASSWORD_VERIFY               = 0x21

    # Custom error codes
    ERROR_PACKET_FAULTY                 = 0xFD
    ERROR_DATABASE_FULL                 = 0xFE
    ERROR_TIMEOUT                       = 0xFF


class FpBufferID(embu.IntEnum):
    """
    Fingerprint buffer IDs.
    """
    BUFFER_1    = 0x01
    BUFFER_2    = 0x02


class FpSecurity(embu.IntEnum):
    """
    Fingerprint security levels.
    """
    SECURITY_LVL1   = 0x01
    SECURITY_LVL2   = 0x02
    SECURITY_LVL3   = 0x03
    SECURITY_LVL4   = 0x04
    SECURITY_LVL5   = 0x05


class FpBaudrate(embu.IntEnum):
    """
    Fingerprint compatible baudrate.
    """
    BAUDRATE_9600   = 0x01
    BAUDRATE_19200  = 0x02
    BAUDRATE_28800  = 0x03
    BAUDRATE_34800  = 0x04
    BAUDRATE_48000  = 0x05
    BAUDRATE_57600  = 0x06
    BAUDRATE_67200  = 0x07
    BAUDRATE_76800  = 0x08
    BAUDRATE_86400  = 0x09
    BAUDRATE_96000  = 0x0A
    BAUDRATE_105600 = 0x0B
    BAUDRATE_115200 = 0x0C

    def to_int(self) -> int:
        """
        Converts the fingerprint baudrate definitions into integers.

        :return: Baudrate value.
        :rtype: int
        """
        return self * 9600

    @classmethod
    def from_int(cls, value: int) -> 'FpBaudrate':
        """
        Tries to convert an integer into a suitable fingerprint baudrate definition.

        :param int value: Baudrate value.

        :return: Fingerprint baudrate code.
        :rtype: FpBaudrate
        """
        if cls.has_value(value=value):
            return FpBaudrate(value)
        val = (value // 9600)
        if cls.has_value(value=val):
            return FpBaudrate(val)
        raise ValueError(f"Value {value} is not supported by the sensor.")


class FpPacketSize(embu.IntEnum):
    """
    Fingerprint packet sizes.
    """
    PACKET_SIZE_32  = 0x00
    PACKET_SIZE_64  = 0x01
    PACKET_SIZE_128 = 0x02
    PACKET_SIZE_256 = 0x03

    def to_int(self) -> int:
        """
        Converts the fingerprint packet size to integer.

        :return: Packet size.
        :rtype: int
        """
        return 32 * (2 ** self)

    @classmethod
    def from_int(cls, value: int) -> 'FpPacketSize':
        """
        Tries to convert an integer into a suitable fingerprint packet size definition.

        :param int value: Packet size.

        :return: Fingerprint packet size code.
        :rtype: FpBaudrate
        """
        if cls.has_value(value=value):
            return FpPacketSize(value)
        val = int(math.log2(value >> 5))
        if cls.has_value(value=val):
            return FpPacketSize(val)
        raise ValueError(f"Value {value} is not a compatible packet size.")


class FpParameterID(embu.IntEnum):
    """
    Fingerprint editable parameters.
    """
    BAUDRATE        = 0x04
    SECURITY        = 0x05
    PACKET_SIZE     = 0x06

    def get_type(self) -> tp.Type[tp.Union[FpBaudrate, FpSecurity, FpPacketSize]]:
        """
        Returns the datatype for the given parameter configuration.

        :return: Parameter data type.
        :rtype: Type[FpBaudrate, FpSecurity, FpPacketSize]
        """
        if self == self.BAUDRATE:
            return FpBaudrate
        if self == self.SECURITY:
            return FpSecurity
        if self == self.PACKET_SIZE:
            return FpPacketSize
        raise ValueError('Parameter type not implemented')


# -->> API <<--------------------------
@attr.s
class FpSystemParameters(embu.AbstractSerialized):
    """
    Fingerprint system parameters structure definition.

    Structure:

    .. code-block::

        0: Status       : 2 byte MSB    : 0 - 1
        1: ID           : 2 byte MSB    : 2 - 3
        2: Lib. Size    : 2 byte MSB    : 4 - 5
        3: Security Lvl.: 2 byte MSB    : 6 - 7
        4: Address      : 4 byte MSB    : 8 - 11
        5: Pack. Size   : 2 byte MSB    : 12 - 13
        6: Baudrate     : 2 byte MSB    : 14 - 15

    .. note::
        * Size: `16`

    """
    #: Minimum packet size
    SIZE_MIN = 16

    #: Device Status
    status:     int = attr.ib(repr=lambda v: f"0x{v:04X}")
    #: Device ID
    id:         int = attr.ib(repr=lambda v: f"0x{v:04X}")
    #: Device address
    address:    int = attr.ib(repr=lambda v: f"0x{v:08X}")
    #: Database capacity
    capacity:   int = attr.ib()
    #: Packet size
    packet:     FpPacketSize = attr.ib(repr=lambda v: str(v))
    #: Security level
    security:   FpSecurity   = attr.ib(repr=lambda v: str(v))
    #: System baudrate
    baudrate:   FpBaudrate   = attr.ib(repr=lambda v: str(v))

    def serialize(self) -> bytearray:
        """
        Convert the packet into a byte array.
        """
        return bytearray(
            to_bytes(value=self.status, size=2) +
            to_bytes(value=self.id, size=2) +
            to_bytes(value=self.capacity, size=2) +
            to_bytes(value=self.security, size=2) +
            to_bytes(value=self.address, size=2) +
            to_bytes(value=self.packet, size=2) +
            to_bytes(value=self.baudrate, size=2)
            )

    @classmethod
    def deserialize(cls, data: bytearray) -> tp.Optional['FpSystemParameters']:
        """
        Parses the parameters from a byte array.

        :param bytearray data: Bytes to be parsed.

        :return: None if deserialization fail, deserialized object otherwise.
        :rtype: FpSystemParameters
        """
        # Check data size
        if len(data) < cls.SIZE_MIN:
            return None

        # Parse data
        _stat   = from_bytes(data=data[0:2])
        _id     = from_bytes(data=data[2:4])
        _cap    = from_bytes(data=data[4:6])
        _sec    = from_bytes(data=data[6:8])
        _addr   = from_bytes(data=data[8:12])
        _pack   = from_bytes(data=data[12:14])
        _baud   = from_bytes(data=data[14:16])

        # Check security
        if not FpSecurity.has_value(value=_sec):
            return None

        # Check packet size
        if not FpPacketSize.has_value(value=_pack):
            return None

        # Check baudrate
        if not FpBaudrate.has_value(value=_baud):
            return None

        # Parse
        return FpSystemParameters(
            status=(0x0F & _stat),
            id=_id,
            capacity=_cap,
            security=FpSecurity(_sec),
            address=_addr,
            packet=FpPacketSize(_pack),
            baudrate=FpBaudrate(_baud)
            )


@attr.s
class FpResponseSet:
    """
    Set command response.

    :attr bool succ:    True if the command succeed, false otherwise.
    :attr FpError code: Command response code.
    """
    succ:   bool    = attr.ib()
    code:   FpError = attr.ib()


@attr.s
class FpResponseGet(FpResponseSet):
    """
    Get command response.

    :attr bytearray pack: Response packet data without the response code byte.
    :attr bytearray data: Response data.
    """
    pack:   bytearray = attr.ib()
    data:   bytearray = attr.ib()


@attr.s
class FpResponseMatch(FpResponseSet):
    """
    Fingerprint match response.

    :attr int index: Index of the matching fingerprint on database. -1 if no available.
    :attr int score: Matching fingerprint accuracy score.
    """
    index:  int = attr.ib()
    score:  int = attr.ib()


@attr.s
class FpResponseValue(FpResponseSet):
    """
    Command value response.

    :attr Union[None, int, bytearray, Image.Image, FpSystemParameters] value: Response value (depends on command).
    """
    value:  tp.Union[None, int, bytearray, PilI.Image, FpSystemParameters] = attr.ib()


def to_bytes(value: int, size: int) -> bytearray:
    """
    Converts an integer value into a bytearray.

    :param int value:   Input value.
    :param int size:    Number of bytes.

    :return: Value bytes.
    :rtype: bytearray
    """
    return bytearray(value.to_bytes(length=size, byteorder='big', signed=False))


def from_bytes(data: bytearray) -> int:
    """
    Retrieves an integer value from a bytearray.

    :param bytearray data: Input bytes.

    :return: Value.
    :rtype: int
    """
    return int.from_bytes(bytes=data, byteorder='big', signed=False)
