from threading import Thread
import socket
from dns_messages.dns_objects import DnsMessage
from dns_messages.exceptions import DnsPacketParsingException
from abc import abstractmethod


class DnsServerNotRunningException(Exception):
    pass


class DnsServer(Thread):
    def __init__(self, ip_address: str, port: int = 53):
        super().__init__(daemon=True)
        self._server_socket_ip_address = ip_address
        self._server_socket_port = port

        self._running = False

        self._server_socket = None

    def start(self) -> None:
        """ starts the DNS server. The DNS server is running in a new thread """
        if self._running:
            return  # server is already running
        else:
            self._running = True
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._server_socket.bind((self._server_socket_ip_address, self._server_socket_port))
            super(DnsServer, self).start()

    def run(self) -> None:
        while self._running:
            try:
                raw_bytes, (remote_ip, remote_port) = self._server_socket.recvfrom(1024)
            except Exception as exception:
                if self._running:
                    raise exception
                else:
                    return

            try:
                parsed_message = DnsMessage.from_bytes(raw_bytes=raw_bytes)
            except DnsPacketParsingException as exception:
                self._handle_broken_message(exception=exception, remote_ip=remote_ip, remote_port=remote_port)
            else:
                self._handle_received_message(message=parsed_message, remote_ip=remote_ip, remote_port=remote_port)

    def send_message(self, message: DnsMessage, remote_ip: str, remote_port: int) -> None:
        """ sends the given DNS message to the given recipient """
        if not self._running:
            raise DnsServerNotRunningException('dns server must be running to send a message')
        message_in_bytes = message.to_bytes()
        self._server_socket.sendto(message_in_bytes, (remote_ip, remote_port))

    def stop(self) -> None:
        """ stops the a DNS server """
        self._running = False
        self._server_socket.close()

    def is_running(self):
        """ returns """
        return self._running

    def _handle_broken_message(self, exception: DnsPacketParsingException, remote_ip: str, remote_port: int) -> None:
        """ methods will be called if an message could not be parsed properly. This method is designed be overwritten in sub-classes """
        print('[!] received package from {}:{} which could not be parsed: {}'.format(remote_ip, remote_port, exception))

    @abstractmethod
    def _handle_received_message(self, message: DnsMessage, remote_ip: str, remote_port: int) -> None:
        """ methods will be called if a new incoming DNS message was received. This method should be overwritten in sub-classes """
        pass
