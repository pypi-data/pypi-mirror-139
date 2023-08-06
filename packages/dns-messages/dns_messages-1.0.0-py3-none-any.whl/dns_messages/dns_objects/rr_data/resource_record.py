from abc import ABCMeta, abstractmethod
from .items import RRClass, RRType
from ...utilities.bit_and_byte_manipulators import extract_int_from_raw_bits
from ...utilities.name_encoder_and_decoder import convert_name_to_bytes, parse_name
from typing import Tuple, List


class ResourceRecord(metaclass=ABCMeta):
    def __init__(self, name: str, rr_class: RRClass, ttl: int):
        super().__init__()
        self.name = name
        self.rr_class = rr_class
        self.ttl = ttl

    def __str__(self) -> str:
        return 'ResourceRecord[name={},class={},ttl={}]'.format(self.name, self.rr_class.name, self.ttl)

    @abstractmethod
    def get_RR_type(self) -> RRType:
        pass

    def to_bytes(self) -> bytes:
        value = convert_name_to_bytes(name=self.name)
        value += self.get_RR_type().to_bytes()
        value += self.rr_class.to_bytes()
        value += self.ttl.to_bytes(length=4, byteorder='big', signed=False)

        encoded_data = self._data_to_bytes()
        value += len(encoded_data).to_bytes(length=2, byteorder='big', signed=False)
        value += encoded_data
        return value

    @abstractmethod
    def _data_to_bytes(self) -> bytes:
        pass


class UnparsedResourceRecord(ResourceRecord):
    def __init__(self, name: str, rr_class: RRClass, ttl: int, rr_type: RRType, raw_data: bytes):
        super(UnparsedResourceRecord, self).__init__(name=name, rr_class=rr_class, ttl=ttl)
        self.rr_type = rr_type
        self.raw_data = raw_data

    def get_RR_type(self) -> RRType:
        return self.rr_type

    def __str__(self) -> str:
        return 'UnparsedResourceRecord[name={},type={}]'.format(self.name, self.rr_type.name)

    @abstractmethod
    def _data_to_bytes(self) -> bytes:
        return self.raw_data
