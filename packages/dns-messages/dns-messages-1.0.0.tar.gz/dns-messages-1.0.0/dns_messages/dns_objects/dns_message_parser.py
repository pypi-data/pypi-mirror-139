from dns_messages.dns_objects import *
from ..dns_objects.dns_message import DnsMessage, OPCODE, RCODE
from ..utilities import convert_bytes_to_bit_list, extract_int_from_raw_bits, parse_name


RR_TYPE_TO_CLASS_MAPPING = {
    RRType.A: A,
    RRType.NS: None,
    RRType.CNAME: CNAME,
    RRType.SOA: SOA,
    RRType.PTR: PTR,
    RRType.HINFO: HINFO,
    RRType.MX: MX,
    RRType.TXT: TXT,
    RRType.RP: None,
    RRType.AFSDB: None,
    RRType.SIG: None,
    RRType.KEY: None,
    RRType.AAAA: AAAA,
    RRType.LOC: None,
    RRType.SRV: None,
    RRType.NAPTR: None,
    RRType.KK: None,
    RRType.CERT: None,
    RRType.DNAME: None,
    RRType.APL: None,
    RRType.DS: None,
    RRType.SSHFP: None,
    RRType.IPSECKEY: None,
    RRType.RRSIG: None,
    RRType.NSEC: None,
    RRType.DNSKEY: None,
    RRType.DHCID: None,
    RRType.NSEC3: None,
    RRType.NSEC3PARAM: None,
    RRType.TLSA: None,
    RRType.SMIMEA: None,
    RRType.HIP: None,
    RRType.CDS: None,
    RRType.CDNSKEY: None,
    RRType.OPENPGPKEY: None,
    RRType.CSYNC: None,
    RRType.ZONEMD: None,
    RRType.SVCB: None,
    RRType.HTTPS: None,
    RRType.EUI48: None,
    RRType.EUI64: None,
    RRType.TKEY: None,
    RRType.TSIG: None,
    RRType.URI: None,
    RRType.CAA: None,
    RRType.TA: None,
    RRType.DLV: None,
}


class DnsMessageParser:
    def __init__(self, message: bytes):
        self._message_in_bytes = message
        self._message_in_bits = convert_bytes_to_bit_list(message=message)

        self._qd_count = 0
        self._an_count = 0
        self._ns_count = 0
        self._ar_count = 0

        self._byte_index = 12

        self._parsed_message: DnsMessage = None

    def parse_message(self) -> DnsMessage:
        self._parsed_message: DnsMessage = self._parse_message_header()
        self._parse_question_section()
        self._parse_answer_section()
        self._parse_authority_section()
        self._parse_additional_section()
        return self._parsed_message

    def _parse_message_header(self) -> DnsMessage:
        message_id: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, bit_offset=0, number_of_bits=16)
        qr: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=0, number_of_bits=1)
        op_code: OPCODE = OPCODE.from_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=1)
        aa: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=5, number_of_bits=1)
        tc: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=6, number_of_bits=1)
        rd: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=7, number_of_bits=1)
        ra: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=8, number_of_bits=1)
        z: int = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=2, bit_offset=9, number_of_bits=3)
        rcode: RCODE = RCODE.from_bits(raw_bits=self._message_in_bits, byte_offset=3, bit_offset=2)

        self._qd_count = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=4, bit_offset=0, number_of_bits=16)
        self._an_count = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=6, bit_offset=0, number_of_bits=16)
        self._ns_count = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=8, bit_offset=0, number_of_bits=16)
        self._ar_count = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=10, bit_offset=0, number_of_bits=16)

        return DnsMessage(message_id=message_id, qr=qr, op_code=op_code, aa=aa, tc=tc, rd=rd, ra=ra, z=z, rcode=rcode)

    def _parse_question_section(self) -> None:
        for _ in range(self._qd_count):
            self._byte_index, parsed_question = Question.from_bytes(raw_bytes=self._message_in_bytes, raw_bits=self._message_in_bits, byte_offset=self._byte_index)
            self._parsed_message.questions.append(parsed_question)

    def _parse_answer_section(self) -> None:
        for _ in range(self._an_count):
            parsed_rr = self._parse_resource_record()
            self._parsed_message.answers_RRs.append(parsed_rr)

    def _parse_authority_section(self) -> None:
        for _ in range(self._ns_count):
            parsed_rr = self._parse_resource_record()
            self._parsed_message.authority_RRs.append(parsed_rr)

    def _parse_additional_section(self) -> None:
        for _ in range(self._ar_count):
            parsed_rr = self._parse_resource_record()
            self._parsed_message.additional_RRs.append(parsed_rr)

    def _parse_resource_record(self) -> ResourceRecord:
        # parse name of the resource record
        self._byte_index, rr_name = parse_name(raw_bytes=self._message_in_bytes, raw_bits=self._message_in_bits, byte_index=self._byte_index)
        self._byte_index, rr_type = RRType.from_bytes(raw_bits=self._message_in_bits, byte_offset=self._byte_index)

        self._byte_index, rr_class = RRClass.from_bytes(raw_bits=self._message_in_bits, byte_offset=self._byte_index)

        # parse the time to live of the resource record
        rr_ttl = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=self._byte_index, bit_offset=0, number_of_bits=32)
        self._byte_index += 4

        # parse the data of the resource record
        rr_data_length = extract_int_from_raw_bits(raw_bits=self._message_in_bits, byte_offset=self._byte_index, bit_offset=0, number_of_bits=16)
        self._byte_index += 2

        record_class = RR_TYPE_TO_CLASS_MAPPING.get(rr_type, None)
        if record_class is None:
            raw_data = self._message_in_bytes[self._byte_index: self._byte_index + rr_data_length]
            record = UnparsedResourceRecord(name=rr_name, rr_class=rr_class, ttl=rr_ttl, rr_type=rr_type, raw_data=raw_data)
        else:
            record = record_class.from_bytes(raw_bytes=self._message_in_bytes, raw_bits=self._message_in_bits, byte_offset=self._byte_index,
                                             rr_data_length=rr_data_length, name=rr_name, rr_class=rr_class, ttl=rr_ttl)

        self._byte_index += rr_data_length
        return record
