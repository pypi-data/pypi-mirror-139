import ipaddress
from typing import List
from .items import *
from .resource_record import ResourceRecord
from ...utilities.bit_and_byte_manipulators import extract_int_from_raw_bits, bit_list_to_bytes


class A(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, ip_address: ipaddress.IPv4Address):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.ip_address = ip_address

    def __str__(self) -> str:
        return 'A[name={},ip_address={}]'.format(self.name, self.ip_address)

    def get_RR_type(self) -> RRType:
        return RRType.A

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'A':
        ip_address = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=0, number_of_bits=32)
        ip_address = ipaddress.IPv4Address(ip_address)
        return A(name=name, rr_class=rr_class, ttl=ttl, ip_address=ip_address)

    def _data_to_bytes(self) -> bytes:
        return int(self.ip_address).to_bytes(length=4, byteorder='big', signed=False)
