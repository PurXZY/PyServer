from data.entity_data import data


class BattleEntity:

	def __init__(self, entity_id, entity_type):
		self.entity_id = entity_id
		self.entity_type = entity_type

		entity_data = data.get(entity_type, {})
		for attr_name, value in entity_data.iteritems():
			setattr(self, attr_name, value)
		# self.Health = entity_data["Health"]
		# self.PhysicalAttack = entity_data["PhysicalAttack"]
		# self.MagicAttack = entity_data["MagicAttack"]
		# self.PhysicalDefend = entity_data["PhysicalDefend"]
		# self.MagicDefend = entity_data["MagicDefend"]
		# self.MoveSpeed = entity_data["MoveSpeed"]

		self.SkillSet = [1, 2, 3]
