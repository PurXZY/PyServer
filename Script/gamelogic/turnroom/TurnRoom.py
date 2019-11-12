from usercmd import base_pb2
from BattleEntity import BattleEntity
import logging


class TurnRoom:

	def __init__(self, room_owner):
		self.logger = logging.getLogger("TurnRoom")
		self.logger.setLevel(logging.DEBUG)
		self._room_owner = room_owner
		self._sync_avatar_into_room()
		self._cur_big_turn = 0
		self._cur_small_turn = 0
		self._cur_move_entity = None
		self._entities = {}
		self._sorted_entity_ids = []
		self._start_logic()

	def broadcast_msg(self, msg_id, msg):
		self._room_owner.send_data(msg_id, msg)

	def _start_logic(self):
		self._create_all_battle_entities()
		self._sync_all_battle_entities()
		self._cur_big_turn = 1
		self._cur_small_turn = 0
		self._sort_entity_speed()
		self._cur_move_entity_id = self._sorted_entity_ids[self._cur_small_turn]
		self._sync_turn_info()

	def _create_all_battle_entities(self):
		enemy_data = {
			base_pb2.PosELeft: 1,
			base_pb2.PosECenter: 1,
			base_pb2.PosERight: 2,
		}
		for entity_id, entity_type in enemy_data.iteritems():
			self._create_battle_entity(entity_id, entity_type)
		my_data = {
			base_pb2.PosBCenter: 3,
		}
		for entity_id, entity_type in my_data.iteritems():
			self._create_battle_entity(entity_id, entity_type)

	def _create_battle_entity(self, entity_id, entity_type):
		self._entities[entity_id] = BattleEntity(entity_id, entity_type)

	def get_entity(self, entity_id):
		return self._entities.get(entity_id, None)

	def _sort_entity_speed(self):
		ret = sorted(self._entities.iteritems(), key=lambda _x: _x[1].MoveSpeed, reverse=True)
		self._sorted_entity_ids = [x[0] for x in ret]
		self.logger.debug("sort ret:%s", self._sorted_entity_ids)

	def _sync_avatar_into_room(self):
		msg = base_pb2.IntoRoomS2CMsg()
		msg.RoomId = 8888
		self.broadcast_msg(base_pb2.IntoRoomRes, msg)

	def _sync_turn_info(self):
		msg = base_pb2.TurnInfoS2CMsg()
		msg.BigTurnIndex = self._cur_big_turn
		msg.SmallTurnIndex = self._cur_small_turn
		msg.CurEntityPosIndex = self._cur_move_entity_id
		for s in self.get_entity(self._cur_move_entity_id).SkillSet:
			msg.SkillSet.append(s)
		self.broadcast_msg(base_pb2.TurnInfo, msg)

	def _sync_all_battle_entities(self):
		msg = base_pb2.SyncAllBattleEntitiesS2CMsg()
		for entity_id, entity in self._entities.iteritems():
			be = msg.entities.add()
			be.PosIndex = entity_id
			be.EntityType = entity.entity_type
			be.Health = entity.Health
			be.PhysicalAttack = entity.PhysicalAttack
			be.MagicAttack = entity.MagicAttack
			be.PhysicalDefend = entity.PhysicalDefend
			be.MagicDefend = entity.MagicDefend
			be.MoveSpeed = entity.MoveSpeed
		self.broadcast_msg(base_pb2.SyncAllBattleEntities, msg)
