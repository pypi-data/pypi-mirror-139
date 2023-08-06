from dns_messages.utilities import decode_character_string
from typing import List
from .items import *
from .resource_record import ResourceRecord
from ...utilities.character_string_encoder_and_decoder import encode_character_string


class HINFO(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, cpu: bytes, os: bytes):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.cpu = cpu
        self.os = os

    def __str__(self) -> str:
        return 'HINFO[name={}, cpu={}, os={}]'.format(self.name, self.cpu, self.os)

    def get_RR_type(self) -> RRType:
        return RRType.HINFO

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'HINFO':
        byte_offset, cpu = decode_character_string(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_offset=byte_offset)
        _, os = decode_character_string(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_offset=byte_offset)
        return HINFO(name=name, rr_class=rr_class, ttl=ttl, cpu=cpu, os=os)

    def _data_to_bytes(self) -> bytes:
        return encode_character_string(character_string=self.cpu) + encode_character_string(character_string=self.os)
