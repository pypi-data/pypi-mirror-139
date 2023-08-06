from dns_messages.utilities.bit_and_byte_manipulators import extract_int_from_raw_bits
from dns_messages.utilities.name_encoder_and_decoder import parse_name, convert_name_to_bytes
from typing import List
from .items import *
from .resource_record import ResourceRecord
from ...utilities.character_string_encoder_and_decoder import encode_character_string


class MX(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, preference: int, exchange: str):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.preference = preference
        self.exchange = exchange

    def __str__(self) -> str:
        return 'MX[name={}, exchange={}]'.format(self.name, self.exchange)

    def get_RR_type(self) -> RRType:
        return RRType.MX

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'MX':
        preference: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=0, number_of_bits=16)
        _, exchange = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=byte_offset + 2)
        return MX(name=name, rr_class=rr_class, ttl=ttl, preference=preference, exchange=exchange)

    def _data_to_bytes(self) -> bytes:
        return self.preference.to_bytes(length=2, byteorder='big', signed=False) + convert_name_to_bytes(name=self.exchange)
