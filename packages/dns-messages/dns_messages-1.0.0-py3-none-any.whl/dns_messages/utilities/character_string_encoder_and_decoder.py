from dns_messages.utilities.bit_and_byte_manipulators import extract_int_from_raw_bits
from typing import List, Tuple


def decode_character_string(raw_bytes: bytes, raw_bits: List[int], byte_offset: int) -> Tuple[int, bytes]:
    length: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=0, number_of_bits=8)
    byte_offset += 1
    data = raw_bytes[byte_offset: byte_offset + length]
    byte_offset += length
    return byte_offset, data


def encode_character_string(character_string: bytes) -> bytes:
    length = len(character_string)
    length_in_bytes = length.to_bytes(length=1, byteorder='big', signed=False)
    return length_in_bytes + character_string
