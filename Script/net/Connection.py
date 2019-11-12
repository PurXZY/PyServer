import struct
import logging

MsgLenSize = 4
MsgIdSize = 2


class Connection(object):

	def __init__(self, server, socket):
		self.logger = logging.getLogger("Connection")
		self.logger.setLevel(logging.DEBUG)
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
		data = self._socket.recv(10 * 1024)
		if not data:
			self.close_connection()
		else:
			self._receive_data_buffer += data
			while True:
				if len(self._receive_data_buffer) < MsgLenSize:
					break
				head_pack = struct.unpack('!I', self._receive_data_buffer[:MsgLenSize])
				body_size = head_pack[0]
				if len(self._receive_data_buffer) < body_size:
					break
				body = self._receive_data_buffer[MsgLenSize:body_size]
				self._receive_data_buffer = self._receive_data_buffer[body_size:]
				msg_pack = struct.unpack('!H', body[:MsgIdSize])
				msg_id = msg_pack[0]
				body = body[MsgIdSize:]
				self.handle_new_message(msg_id, body)

	def handle_write_event(self):
		length = self._socket.send(self._send_data_buffer)
		self._send_data_buffer = self._send_data_buffer[length:]
		if not len(self._send_data_buffer):
			self._server.remove_write_need(self._socket)

	def handle_new_message(self, message_id, message_data):
		self.logger.debug("new message id(%s)", message_id)

	def send_data(self, msg_id, msg):
		msg_data = msg.SerializeToString()
		data_size = len(msg_data)
		head_pack = struct.pack("!I", int(data_size+MsgLenSize+MsgIdSize))
		msg_id = struct.pack("!H", int(msg_id))
		self._send_data_buffer += head_pack
		self._send_data_buffer += msg_id
		self._send_data_buffer += msg_data
		self._server.add_write_need(self._socket)

	def close_connection(self):
		self.logger.debug("Close Connection fd(%s)", self._socket_fd)
		self._remove_read_need()
		self._server.remove_connection(self._socket)
		self._socket.close()

