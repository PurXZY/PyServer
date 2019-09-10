from Acceptor import Acceptor
from NetIOMgr import NetIOMgr


class TcpServer(object):

	def __init__(self, config):
		self._host = config.get("host", None)
		self._port = config.get("port", None)
		self._acceptor = Acceptor(self)
		self._net_io_mgr = NetIOMgr(self)

	def run(self):
		self._acceptor.start(self._host, self._port)
		print "Server Start"
		while True:
			self._acceptor.update()
			self._net_io_mgr.update()

	def new_client(self, socket_fd):
		self._net_io_mgr.add_new_connection(socket_fd)
		print "new client %s fd(%s)" % (socket_fd.getpeername(), socket_fd.fileno())
