import enum
from typing import List, Tuple

from dns_messages.exceptions.parser_exception import DnsPacketParsingException
from dns_messages.utilities.bit_and_byte_manipulators import extract_int_from_raw_bits


class RRClass(enum.Enum):
    IN = 1
    CS = 2
    CH = 3
    HS = 4

    ANY_CLASS = 255

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(2, byteorder='big', signed=False)

    @staticmethod
    def from_bytes(raw_bits: List[int], byte_offset: int) -> Tuple[int, 'RRClass']:
        rr_type_int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=0, number_of_bits=16)
        try:
            return byte_offset + 2, RRClass(rr_type_int)
        except ValueError:
            raise DnsPacketParsingException('CLASS is not valid: {}'.format(rr_type_int))