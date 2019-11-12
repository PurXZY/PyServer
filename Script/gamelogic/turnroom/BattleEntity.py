from data.entity_data import data


class BattleEntity:

	def __init__(self, entity_id, entity_type):
		self.entity_id = entity_id
		self.entity_type = entity_type

		entity_data = data.get(entity_type, {})
		for attr_name, value in entity_data.iteritems():
			setattr(self, attr_name, value)
