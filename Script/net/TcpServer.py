import socket
import select
from gamelogic import Account
import logging


class TcpServer(object):

	def __init__(self, config):
		self.logger = logging.getLogger("TcpServer")
		self.logger.setLevel(logging.DEBUG)
		self._host = config.get("host", None)
		self._port = config.get("port", None)
		self._listen_socket = None
		self._connections = {}
		self._need_read_sockets = []
		self._need_write_sockets = []

	def start(self):
		self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._listen_socket.setblocking(False)
		self._listen_socket.bind((self._host, self._port))
		self._listen_socket.listen(100)
		self._need_read_sockets.append(self._listen_socket)

	def run(self):
		self.logger.info("Server Start")
		while True:
			in_sockets, out_sockets, _ = select.select(self._need_read_sockets, self._need_write_sockets, [], 0.1)
			for obj in in_sockets:
				if obj == self._listen_socket:
					self.new_client()
				conn = self._connections.get(obj, None)
				if conn:
					conn.handle_read_event()
			for obj in out_sockets:
				conn = self._connections.get(obj, None)
				if conn:
					conn.handle_write_event()

	def new_client(self):
		client_socket, client_addr = self._listen_socket.accept()
		client_socket.setblocking(False)
		conn = Account.Account(self, client_socket)
		self._connections[client_socket] = conn
		self.logger.info("new client %s fd(%s)", client_socket.getpeername(), client_socket.fileno())

	def remove_connection(self, socket_obj):
		self._connections.pop(socket_obj)

	def add_read_need(self, socket_obj):
		self._need_read_sockets.append(socket_obj)

	def remove_read_need(self, socket_obj):
		self._need_read_sockets.remove(socket_obj)

	def add_write_need(self, socket_obj):
		self._need_write_sockets.append(socket_obj)

	def remove_write_need(self, socket_obj):
		self._need_write_sockets.remove(socket_obj)
