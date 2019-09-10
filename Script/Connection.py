from MessagePack import MessagePack
import struct
import sys


class Connection(object):

	def __init__(self, net_io_mgr, socket_fd):
		self._net_io_mgr = net_io_mgr
		self._socket_fd = socket_fd
		self._receive_data_buffer = bytes()
		self._send_data_buffer = bytes()
		self._add_read_need()

	def _add_read_need(self):
		self._net_io_mgr.add_read_need(self._socket_fd)

	def _remove_read_need(self):
		self._net_io_mgr.remove_read_need(self._socket_fd)

	def handle_read_event(self):
		data = self._socket_fd.recv(1024)
		if not data:
			self._remove_read_need()
			self._net_io_mgr.remove_connection(self._socket_fd)
			self._socket_fd.close()
		else:
			self._receive_data_buffer += data
			while True:
				if len(self._receive_data_buffer) < MessagePack.HeaderSize:
					break
				head_pack = struct.unpack('!I', self._receive_data_buffer[:MessagePack.HeaderSize])
				body_size = head_pack[0]
				if len(self._receive_data_buffer) < MessagePack.HeaderSize + body_size:
					break
				body = self._receive_data_buffer[MessagePack.HeaderSize: MessagePack.HeaderSize + body_size]
				self._receive_data_buffer = self._receive_data_buffer[MessagePack.HeaderSize + body_size:]
				self.handle_new_message(body)

	def handle_write_event(self):
		length = self._socket_fd.send(self._send_data_buffer)
		self._send_data_buffer = self._send_data_buffer[length:]
		if not len(self._send_data_buffer):
			self._net_io_mgr.remove_write_need(self._socket_fd)

	def handle_new_message(self, message_data):
		print message_data
		self.send_data("client ack")

	def send_data(self, data):
		data_size = sys.getsizeof(data)
		head_pack = struct.pack("!I", data_size)
		self._send_data_buffer += head_pack
		self._send_data_buffer += data
		self._net_io_mgr.add_write_need(self._socket_fd)

