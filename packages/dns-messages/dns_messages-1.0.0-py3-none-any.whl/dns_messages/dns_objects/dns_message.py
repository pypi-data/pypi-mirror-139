from typing import List

from .question import Question
from .rocde import RCODE
from .opcode import OPCODE
from .rr_data import ResourceRecord
from ..exceptions import DnsPacketParsingException
from ..utilities import int_to_bit_list, bit_list_to_bytes


class DnsMessage:
    def __init__(self, message_id: int, qr: int, op_code: OPCODE = OPCODE.QUERY, aa: int = 0, tc: int = 0, rd: int = 0, ra: int = 0, z: int = 0, rcode: RCODE = RCODE.no_error):
        self.message_id = message_id
        self.qr = qr
        self.op_code = op_code
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.rcode = rcode
        self.questions: List[Question] = list()
        self.answers_RRs: List[ResourceRecord] = list()
        self.authority_RRs: List[ResourceRecord] = list()
        self.additional_RRs: List[ResourceRecord] = list()

    def __str__(self) -> str:
        return 'DnsMessage[id={},qr={}]'.format(self.message_id, self.qr)

    @staticmethod
    def from_bytes(raw_bytes) -> 'DnsMessage':
        """ parses raw bytes to a DnsMessage """
        from .dns_message_parser import DnsMessageParser
        try:
            return DnsMessageParser(message=raw_bytes).parse_message()
        except DnsPacketParsingException as exception:
            raise exception
        except Exception as exception:
            raise DnsPacketParsingException(exception.__str__())

    def to_bytes(self) -> bytes:
        """ generates from a DNS message a DNS packet in raw bytes which can be used to be sent over the network """
        message_in_bytes = self._generate_message_header()
        for question in self.questions:
            message_in_bytes += question.to_bytes()
        for rr in self.answers_RRs:
            message_in_bytes += rr.to_bytes()
        for rr in self.authority_RRs:
            message_in_bytes += rr.to_bytes()
        for rr in self.additional_RRs:
            message_in_bytes += rr.to_bytes()
        return message_in_bytes

    def _generate_message_header(self) -> bytes:
        header = list()
        message_id = int_to_bit_list(value=self.message_id, number_of_bits=16)
        header.extend(message_id)
        header.extend(int_to_bit_list(value=self.qr, number_of_bits=1))
        header.extend(self.op_code.to_bits())
        header.extend(int_to_bit_list(value=self.aa, number_of_bits=1))
        header.extend(int_to_bit_list(value=self.tc, number_of_bits=1))
        header.extend(int_to_bit_list(value=self.rd, number_of_bits=1))
        header.extend(int_to_bit_list(value=self.ra, number_of_bits=1))
        header.extend(int_to_bit_list(value=self.z, number_of_bits=3))
        header.extend(self.rcode.to_bits())
        header.extend(int_to_bit_list(value=len(self.questions), number_of_bits=16))
        header.extend(int_to_bit_list(value=len(self.answers_RRs), number_of_bits=16))
        header.extend(int_to_bit_list(value=len(self.authority_RRs), number_of_bits=16))
        header.extend(int_to_bit_list(value=len(self.additional_RRs), number_of_bits=16))
        return bit_list_to_bytes(bit_list=header)

    def is_query(self) -> bool:
        """ returns True if the message is a dns query """
        return self.qr == 0

    def number_of_questions(self) -> int:
        return len(self.questions)

    def number_of_answer_records(self) -> int:
        return len(self.answers_RRs)

    def number_of_authority_records(self) -> int:
        return len(self.authority_RRs)

    def number_of_additional_records(self) -> int:
        return len(self.additional_RRs)