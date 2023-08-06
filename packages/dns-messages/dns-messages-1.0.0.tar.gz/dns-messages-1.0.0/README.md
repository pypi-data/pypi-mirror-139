# DNS-Messages

A Python3 library for parsing and generating DNS messages.
Additionally, it provides a dns server which enables receiving and sending dns messages.

Currently, it only supports some types of resource records (A, AAAA, CNAME, PTR, TXT, SOA, MX, HINFO) but can be easily extended - feel free to create a pull request :wink: 
If a message contains an unsupported RR, the parser will ignore the data of this RR but will not break  :smiley:

The logic to encode a message is very simple - no compression etc. is done.

## Installation

Install the package with pip

    pip3 install dns-messages

## Parsing DNS Messages
Use the function ``from_bytes`` of the ``DnsMessage`` class to parse dns messages in raw bytes. 
```python3
from dns_messages import DnsMessage

raw_bytes: bytes
parsed_message: DnsMessage = DnsMessage.from_bytes(raw_bytes)
```

## Generating DNS Messages
Build a message using the provided classes ``DnsMessage``, ``OPCODE``, ``Question``, ``A``, ``RRType`` etc.: 
```python3
from dns_messages import DnsMessage, OPCODE, RRType, RRClass, Question

# build a simple query for the A record of "example.com"
message = DnsMessage(message_id=1, qr=1, op_code=OPCODE.QUERY)

question = Question(qname="example.com", qtype=RRType.A, qclass=RRClass.IN)
message.questions.append(question)

message_in_bytes: bytes = message.to_bytes()
```

## DNS server
The package also provides a dns server ``DnsServer`` which can easily be extended with your own logic by overwriting the functions ``_handle_broken_message`` and ``_handle_received_message``.  
```python3
from dns_messages import DnsServer, DnsPacketParsingException, DnsMessage

class TestServer(DnsServer):
    def __init__(self, ip_address: str, port: int = 53):
        super().__init__(ip_address=ip_address, port=port)
        
    def _handle_broken_message(self, exception: DnsPacketParsingException, remote_ip: str, remote_port: int) -> None:
        print('received package from {}:{} which could not be parsed: {}'.format(remote_ip, remote_port, exception))

    def _handle_received_message(self, message: DnsMessage, remote_ip: str, remote_port: int) -> None:
        # print out names of questions
        for question in message.questions:
            print(question.name)
```

## Simple demo server
The package includes a simple demo for using the built-in dns server. 
You can start the dns demo server with the following three lines of code. 
The server prints out information about incoming dns packages.
```python3
from dns_messages.dns_server import DnsDemoServer
demo = DnsDemoServer(ip_address='127.0.0.1')
demo.start()
```

Here is the complete code of the demo server:
```python3
from .dns_server import DnsServer
from .. import DnsMessage, Question, ResourceRecord, A, AAAA


class DnsDemoServer(DnsServer):
    def __init__(self, ip_address: str):
        super().__init__(ip_address)

    def _handle_received_message(self, message: DnsMessage, remote_ip: str, remote_port: int) -> None:
        print(30*'-')
        print('a new dns message was parsed')
        print('message id: ', message.message_id)
        print('is a query: ', message.is_query())
        print('number of questions: ', message.number_of_questions())
        print('number of questions: ', message.number_of_answer_records())

        print('Questions:')
        question: Question
        for i, question in enumerate(message.questions):
            print('\tquestion {}'.format(i+1))
            print('\t- name: {}'.format(question.name))
            print('\t- type: {}'.format(question.rr_type.name))
            print('\t- class: {}'.format(question.rr_class.name))

        print('Answers:')
        answer: ResourceRecord
        for i, answer in enumerate(message.answers_RRs):
            print('\tanswer {}'.format(i + 1))
            print('\t- name: {}'.format(answer.name))
            print('\t- type: {}'.format(answer.get_RR_type()))
            print('\t- class: {}'.format(answer.rr_class.name))
            print('\t- ttl: {}'.format(answer.rr_class.name))
            if isinstance(answer, A) or isinstance(answer, AAAA):
                print('\t- IP: {}'.format(answer.ip_address))
```