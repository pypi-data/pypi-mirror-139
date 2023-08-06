from typing import List


def _grouped(iterable, n):
    """s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."""
    return zip(*[iter(iterable)] * n)


def convert_bytes_to_bit_list(message: bytes) -> List[int]:
    bit_list = list()
    for byte in message:
        bits_from_byte = _convert_byte_to_bit_list(byte=byte)
        bit_list.extend(bits_from_byte)
    return bit_list


def _convert_byte_to_bit_list(byte: int) -> List[int]:
    bit_list = list()
    for x in range(8):
        bit_list.append((byte >> x) & 1)
    bit_list.reverse()
    return bit_list


def extract_int_from_raw_bits(raw_bits: List[int], bit_offset: int, number_of_bits: int, byte_offset: int = 0) -> int:
    start = bit_offset + byte_offset * 8
    bits = raw_bits[start: start + number_of_bits]
    value = 0
    for bit in bits:
        value = value << 1
        value = value | bit
    return value


def int_to_bit_list(value, number_of_bits) -> List[int]:
    in_bytes = value.to_bytes(2, byteorder='big')
    in_bites = convert_bytes_to_bit_list(in_bytes)
    return in_bites[len(in_bites) - number_of_bits:]


def bit_list_to_bytes(bit_list: List[int]) -> bytes:
    assert (len(bit_list) % 8 == 0), 'the number of elements in bit list has to be a multiple of 8'
    list_of_bytes = bytes()
    for index in range(0, len(bit_list), 8):
        byte = convert_bits_into_byte(bit_list=bit_list[index: (index + 8)])
        list_of_bytes += byte.to_bytes(length=1, signed=False, byteorder='big')
    return list_of_bytes


def convert_bits_into_byte(bit_list) -> int:
    assert (len(bit_list) % 8 == 0), 'the number of elements in bit list has to be a multiple of 8'
    return bit_list[0] * 128 + bit_list[1] * 64 + bit_list[2] * 32 + bit_list[3] * 16 + bit_list[4] * 8 + bit_list[5] * 4 + bit_list[6] * 2 + bit_list[7]



