from .resource_record import ResourceRecord
from typing import List
from .items import *
from dns_messages.utilities.bit_and_byte_manipulators import extract_int_from_raw_bits
from dns_messages.utilities.name_encoder_and_decoder import parse_name, convert_name_to_bytes


class SOA(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, mname: str, rname: str, serial: int, refresh: int, retry: int, expire: int, minimum: int):
        super().__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.mname = mname
        self.rname = rname
        self.serial = serial
        self.refresh = refresh
        self.retry = retry
        self.expire = expire
        self.minimum = minimum

    def __str__(self) -> str:
        return 'SOA[mname={},rname={},serial={}]'.format(self.mname, self.rname, self.serial)

    def get_RR_type(self) -> RRType:
        return RRType.SOA

    @staticmethod
    def from_bytes(raw_bytes: bytes, raw_bits: List[int], byte_offset: int, rr_data_length: int, name: str, rr_class: RRClass, ttl: int) -> 'SOA':
        byte_offset, mname = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=byte_offset)
        byte_offset, rname = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=byte_offset)
        serial: int = extract_int_from_raw_bits(raw_bits=raw_bits,  byte_offset=byte_offset + 1 * 4, bit_offset=0, number_of_bits=32)
        refresh: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset + 2 * 4, bit_offset=0, number_of_bits=32)
        retry: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset + 3 * 4, bit_offset=0, number_of_bits=32)
        expire: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset + 4 * 4, bit_offset=0, number_of_bits=32)
        minimum: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset + 5 * 4, bit_offset=0, number_of_bits=32)
        return SOA(name=name, rr_class=rr_class, ttl=ttl, mname=mname, rname=rname, serial=serial, refresh=refresh, retry=retry, expire=expire, minimum=minimum)

    def _data_to_bytes(self) -> bytes:
        return convert_name_to_bytes(name=self.mname) + \
               convert_name_to_bytes(name=self.rname) + \
               self.serial.to_bytes(length=4, byteorder='big', signed=False) + \
               self.refresh.to_bytes(length=4, byteorder='big', signed=False) + \
               self.retry.to_bytes(length=4, byteorder='big', signed=False) + \
               self.expire.to_bytes(length=4, byteorder='big', signed=False) + \
               self.minimum.to_bytes(length=4, byteorder='big', signed=False)
