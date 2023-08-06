import enum
from typing import List

from dns_messages.exceptions import DnsPacketParsingException
from dns_messages.utilities import int_to_bit_list, extract_int_from_raw_bits


class OPCODE(enum.Enum):
    QUERY = 0
    IQUERY = 1
    STATUS = 2
    op_code_3 = 3
    NOTIFY = 4
    UPDATE = 5
    DNS_STATEFUL_OPERATIONS = 6
    op_code_7 = 7
    op_code_8 = 8
    op_code_9 = 9
    op_code_10 = 10
    op_code_11 = 11
    op_code_12 = 12
    op_code_13 = 13
    op_code_14 = 14
    op_code_15 = 15

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(2, byteorder='big', signed=False)

    def to_bits(self) -> List[int]:
        return int_to_bit_list(value=self.value, number_of_bits=4)

    @staticmethod
    def from_bits(raw_bits: List[int], byte_offset: int, bit_offset: int) -> 'OPCODE':
        value_int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=bit_offset, number_of_bits=4)
        try:
            return OPCODE(value_int)
        except ValueError:
            raise DnsPacketParsingException('OPCODE is not valid: {}'.format(value_int))
