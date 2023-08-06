from .bit_and_byte_manipulators import extract_int_from_raw_bits, _convert_byte_to_bit_list
from typing import Tuple, List

from ..exceptions.parser_exception import DnsPacketParsingException


def parse_name(raw_bytes: bytes, raw_bits: List[int], byte_index: int) -> Tuple[int, str]:
    extracted_label = list()
    while True:
        pointer_or_label: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_index, bit_offset=0, number_of_bits=2)

        if pointer_or_label == 0:
            length_of_label: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_index, bit_offset=2, number_of_bits=6)
            byte_index += 1

            if length_of_label == 0:    # a length of 0 indicates that the end of the label was reached
                break

            # extract the label from the package, decode it and append it to the label list
            label_in_bytes = raw_bytes[byte_index: byte_index + length_of_label]
            byte_index += length_of_label
            label = label_in_bytes.decode('ascii')
            extracted_label.append(label)

        elif pointer_or_label == 3:
            pointer_to_label: int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_index, bit_offset=2, number_of_bits=14)
            _, label = parse_name(raw_bytes=raw_bytes, raw_bits=raw_bits, byte_index=pointer_to_label)
            extracted_label.append(label)
            byte_index += 2
            break
        else:
            raise DnsPacketParsingException('label start must be 0 or 3 but was: {}'.format(pointer_or_label))

    return byte_index, '.'.join(extracted_label)


def convert_name_to_bytes(name: str) -> bytes:
    value = bytes()
    for label in name.split('.'):
        value += _convert_label_to_bytes(label=label)
    value += (0).to_bytes(length=1, signed=False, byteorder='big')
    return value


def _convert_label_to_bytes(label: str) -> bytes:
    value = bytes()
    value += len(label).to_bytes(length=1, byteorder='big', signed=False)
    value += label.encode('ascii')
    return value
