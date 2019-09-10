import struct
import sys

MsgLenSize = 4
MsgIdSize = 4


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
				if len(self._receive_data_buffer) < MsgLenSize:
					break
				head_pack = struct.unpack('!I', self._receive_data_buffer[:MsgLenSize])
				body_size = head_pack[0]
				if len(self._receive_data_buffer) < MsgLenSize + body_size:
					break
				body = self._receive_data_buffer[MsgLenSize:MsgLenSize + body_size]
				self._receive_data_buffer = self._receive_data_buffer[MsgLenSize + body_size:]
				msg_pack = struct.unpack('!I', body[:MsgIdSize])
				msg_id = msg_pack[0]
				body = body[MsgIdSize:]
				self.handle_new_message(msg_id, body)

	def handle_write_event(self):
		length = self._socket_fd.send(self._send_data_buffer)
		self._send_data_buffer = self._send_data_buffer[length:]
		if not len(self._send_data_buffer):
			self._net_io_mgr.remove_write_need(self._socket_fd)

	def handle_new_message(self, message_id, message_data):
		print "new message id(%s) data(%s)" % (message_id, message_data)
		self.send_data(122, "client ack")

	def send_data(self, msg_id, msg_data):
		data_size = sys.getsizeof(msg_data)
		head_pack = struct.pack("!I", data_size)
		msg_id = struct.pack("!I", msg_id)
		self._send_data_buffer += head_pack
		self._send_data_buffer += msg_id
		self._send_data_buffer += msg_data
		self._net_io_mgr.add_write_need(self._socket_fd)

