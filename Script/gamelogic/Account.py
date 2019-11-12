from net import Connection
from usercmd import base_pb2
import logging
from gamelogic.turnroom.TurnRoom import TurnRoom


class Account(Connection.Connection):

	def __init__(self, server, socket):
		super(Account, self).__init__(server, socket)
		self.logger = logging.getLogger("Account")

	def handle_new_message(self, message_id, message_data):
		super(Account, self).handle_new_message(message_id, message_data)
		if message_id == base_pb2.LoginReq:
			msg = base_pb2.LoginC2SMsg()
			msg.ParseFromString(message_data)
			self.logger.debug("name: %s", msg.name)
			self._on_login()
		elif message_id == base_pb2.IntoRoomReq:
			self._on_into_room()
		elif message_id == base_pb2.CastSkillReq:
			msg = base_pb2.CastSkillC2SMsg
			msg.ParseFromString(message_data)
			self._on_cast_skill(msg.SkillId, msg.TargetIds)

	def _on_login(self):
		msg = base_pb2.LoginS2CMsg()
		msg.PlayerId = 7777
		self.send_data(base_pb2.LoginRes, msg)

	def _on_into_room(self):
		TurnRoom(self)

	def _on_cast_skill(self, skill_id, target_ids):
		self.logger.debug("cast skill id($i) target_ids(%s)", skill_id, target_ids)
