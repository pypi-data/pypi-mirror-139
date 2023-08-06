import enum
from typing import List, Tuple

from dns_messages.exceptions.parser_exception import DnsPacketParsingException
from dns_messages.utilities.bit_and_byte_manipulators import extract_int_from_raw_bits


class RRType(enum.Enum):
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6
    PTR = 12
    HINFO = 13
    MX = 15
    TXT = 16
    RP = 17
    AFSDB = 18
    SIG = 24
    KEY = 25
    AAAA = 28
    LOC = 29
    SRV = 33
    NAPTR = 35
    KK = 36
    CERT = 37
    DNAME = 39
    APL = 42
    DS = 43
    SSHFP = 44
    IPSECKEY = 45
    RRSIG = 46
    NSEC = 47
    DNSKEY = 48
    DHCID = 49
    NSEC3 = 50
    NSEC3PARAM = 51
    TLSA = 52
    SMIMEA = 53
    HIP = 55
    CDS = 59
    CDNSKEY = 60
    OPENPGPKEY = 61
    CSYNC = 62
    ZONEMD = 63
    SVCB = 64
    HTTPS = 65
    EUI48 = 108
    EUI64 = 109
    TKEY = 249
    TSIG = 250
    URI = 256
    CAA = 257
    TA = 32768
    DLV = 32769

    IXFR = 251
    AXFR = 252
    MAILB = 253
    MAILA = 254
    ALL_RECORDS = 255

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(2, byteorder='big', signed=False)

    @staticmethod
    def from_bytes(raw_bits: List[int], byte_offset: int) -> Tuple[int, 'RRType']:
        rr_type_int = extract_int_from_raw_bits(raw_bits=raw_bits, byte_offset=byte_offset, bit_offset=0, number_of_bits=16)
        try:
            return byte_offset + 2, RRType(rr_type_int)
        except ValueError:
            raise DnsPacketParsingException('TYPE is not valid: {}'.format(rr_type_int))
