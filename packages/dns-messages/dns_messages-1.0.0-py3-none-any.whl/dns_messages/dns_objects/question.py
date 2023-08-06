from dns_messages.utilities import convert_name_to_bytes

from dns_messages.dns_objects.rr_data.items.rr_type import RRType
from dns_messages.dns_objects.rr_data.items.rr_class import RRClass
from typing import Tuple, List
from dns_messages.utilities import parse_name


class Question:
    def __init__(self, name: str, rr_type: RRType, rr_class: RRClass):
        self.name = name
        self.rr_type = rr_type
        self.rr_class = rr_class

    def __str__(self) -> str:
        return 'Question[name={},type={},class={}]'.format(self.name, self.rr_type.name, self.rr_class.name)

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int) -> Tuple[int, 'Question']:
        byte_offset, name = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=byte_offset)
        byte_offset, rr_type = RRType.from_bytes(raw_bits=raw_bits, byte_offset=byte_offset)
        byte_offset, rr_class = RRClass.from_bytes(raw_bits=raw_bits, byte_offset=byte_offset)
        parsed_question = Question(name=name, rr_type=rr_type, rr_class=rr_class)
        return byte_offset, parsed_question

    def to_bytes(self) -> bytes:
        raw_bytes = convert_name_to_bytes(name=self.name)
        raw_bytes += self.rr_type.to_bytes()
        raw_bytes += self.rr_class.to_bytes()
        return raw_bytes
