from typing import List
from dns_messages.utilities.name_encoder_and_decoder import parse_name, convert_name_to_bytes
from .items import *
from .resource_record import ResourceRecord


class CNAME(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, domain_name: str):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.domain_name = domain_name

    def __str__(self) -> str:
        return 'CNAME[name={}, cname={}]'.format(self.name, self.domain_name)

    def get_RR_type(self) -> RRType:
        return RRType.CNAME

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'CNAME':
        _, domain_name = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=byte_offset)
        return CNAME(name=name, rr_class=rr_class, ttl=ttl, domain_name=domain_name)

    def _data_to_bytes(self) -> bytes:
        return convert_name_to_bytes(name=self.domain_name)
