from Connection import Connection
from select import select


class NetIOMgr(object):

	def __init__(self, server):
		self._server = server
		self._connections = {}
		self._need_read_sockets = []
		self._need_write_sockets = []

	def add_new_connection(self, socket_fd):
		conn = Connection(self, socket_fd)
		self._connections[socket_fd.fileno()] = conn

	def remove_connection(self, socket_fd):
		self._connections.pop(socket_fd)

	def add_read_need(self, socket):
		self._need_read_sockets.append(socket)

	def remove_read_need(self, socket):
		self._need_read_sockets.remove(socket)

	def add_write_need(self, socket):
		self._need_write_sockets.append(socket)

	def remove_write_need(self, socket):
		self._need_write_sockets.remove(socket)

	def update(self):
		in_fds, out_fds, _ = select(self._need_read_sockets, self._need_write_sockets, [], 0.1)

		for fd in in_fds:
			print "in fds(%s)" % (in_fds, )
			conn = self._connections.get(fd.fileno(), None)
			if conn:
				conn.handle_read_event()

		for fd in out_fds:
			print "out fds(%s)" % (out_fds,)
			conn = self._connections.get(fd.fileno(), None)
			if conn:
				conn.handle_write_event()

