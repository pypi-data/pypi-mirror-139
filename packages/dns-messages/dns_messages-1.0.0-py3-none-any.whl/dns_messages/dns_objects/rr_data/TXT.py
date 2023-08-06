from dns_messages.utilities import decode_character_string
from typing import List
from .items import *
from .resource_record import ResourceRecord
from ...utilities.character_string_encoder_and_decoder import encode_character_string


class TXT(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, text_lines: List[bytes]):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.text_lines = text_lines

    def __str__(self) -> str:
        return 'TXT[name={},data={}]'.format(self.name, self.text_lines)

    def get_RR_type(self) -> RRType:
        return RRType.TXT

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'TXT':
        stop_index = byte_offset + rr_data_length
        string_list = list()
        while True:
            if byte_offset == stop_index:
                break
            number_of_bytes_parsed, txt = decode_character_string(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_offset=byte_offset)
            byte_offset += byte_offset
            string_list.append(txt)
        return TXT(name=name, rr_class=rr_class, ttl=ttl, text_lines=string_list)

    def _data_to_bytes(self) -> bytes:
        return_bytes = bytes()
        for text_line in self.text_lines:
            return_bytes += encode_character_string(text_line)
        return return_bytes
