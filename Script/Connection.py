import struct
import sys

MsgLenSize = 4
MsgIdSize = 4


class Connection(object):

	def __init__(self, server, socket):
		self._server = server
		self._socket = socket
		self._socket_fd = socket.fileno()
		self._receive_data_buffer = bytes()
		self._send_data_buffer = bytes()
		self._add_read_need()

	def _add_read_need(self):
		self._server.add_read_need(self._socket)

	def _remove_read_need(self):
		self._server.remove_read_need(self._socket)

	def handle_read_event(self):
		data = self._socket.recv(1024)
		print "data:%s" % (data, )
		if not data:
			self.close_connection()
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
		length = self._socket.send(self._send_data_buffer)
		self._send_data_buffer = self._send_data_buffer[length:]
		if not len(self._send_data_buffer):
			self._server.remove_write_need(self._socket)

	def handle_new_message(self, message_id, message_data):
		print "new message id(%s) data(%s) fd(%s)" % (message_id, message_data, self._socket_fd)
		self.send_data(122, bytearray("client ack", encoding='utf-8'))

	def send_data(self, msg_id, msg_data):
		data_size = sys.getsizeof(msg_data)
		head_pack = struct.pack("!I", data_size)
		msg_id = struct.pack("!I", msg_id)
		self._send_data_buffer += head_pack
		self._send_data_buffer += msg_id
		self._send_data_buffer += msg_data
		self._server.add_write_need(self._socket)

	def close_connection(self):
		print "Close Connection fd(%s)" % (self._socket_fd, )
		self._remove_read_need()
		self._server.remove_connection(self._socket)
		self._socket.close()

