import socket
from select import select


class Acceptor(object):

	def __init__(self, server):
		self._server = server
		self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._listen_socket.setblocking(False)

	def start(self, host, port):
		self._listen_socket.bind((host, port))
		self._listen_socket.listen(100)

	def update(self):
		in_fd, _, _ = select([self._listen_socket], [], [])
		if len(in_fd):
			self.accept_new_client()

	def accept_new_client(self):
		client_socket, client_addr = self._listen_socket.accept()
		client_socket.setblocking(False)
		self._server.new_client(client_socket)

