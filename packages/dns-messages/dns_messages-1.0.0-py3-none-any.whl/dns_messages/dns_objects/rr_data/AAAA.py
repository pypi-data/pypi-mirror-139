import ipaddress
from .resource_record import ResourceRecord
from typing import List
from .items import *


class AAAA(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, ip_address: ipaddress.IPv6Address):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.ip_address = ip_address

    def __str__(self) -> str:
        return 'AAAA[name={},ip_address={}]'.format(self.name, self.ip_address)

    def get_RR_type(self) -> RRType:
        return RRType.AAAA

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'AAAA':
        ip_address = ipaddress.IPv6Address(raw_bytes[byte_offset: byte_offset + 16])
        return AAAA(name=name, rr_class=rr_class, ttl=ttl, ip_address=ip_address)

    def _data_to_bytes(self) -> bytes:
        return int(self.ip_address).to_bytes(length=16, byteorder='big', signed=False)
