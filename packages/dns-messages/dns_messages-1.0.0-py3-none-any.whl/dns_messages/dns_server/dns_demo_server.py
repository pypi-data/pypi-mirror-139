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
