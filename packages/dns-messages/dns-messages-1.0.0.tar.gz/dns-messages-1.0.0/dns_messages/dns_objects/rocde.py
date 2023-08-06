import enum
from typing import List

from dns_messages.exceptions import DnsPacketParsingException
from dns_messages.utilities import int_to_bit_list, extract_int_from_raw_bits


class RCODE(enum.Enum):
    no_error = 0
    format_error = 1
    server_error = 2
    non_existing_domain = 3
    not_implemented = 4
    refused = 5
    yx_domain = 6
    yx_rr_set = 7
    nx_rr_set = 8
    not_auth = 9
    not_zone = 10
    dso_type_not_implemented = 11
    bad_opt_version_or_tsig_signature_fail = 16
    key_not_recognized = 17
    signature_out_of_time_window = 18
    bad_tkey_mode = 19
    duplicate_key_name = 20
    algorithm_not_supported = 21
    bad_truncation = 22
    bad_missing_server_cookie = 23

    def to_bits(self) -> List[int]:
        return int_to_bit_list(value=self.value, number_of_bits=4)

    @staticmethod
    def from_bits(raw_bits: List[int], byte_offset: int, bit_offset: int) -> 'RCODE':
        value_int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=bit_offset, number_of_bits=4)
        try:
            return RCODE(value_int)
        except ValueError:
            raise DnsPacketParsingException('RCODE is not valid: {}'.format(value_int))
