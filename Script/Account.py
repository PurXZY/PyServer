import Connection


class Account(Connection.Connection):

	def __init__(self, server, socket):
		super(Account, self).__init__(server, socket)
		pass

	def handle_new_message(self, message_id, message_data):
		super(Account, self).handle_new_message(message_id, message_data)
		print "dispatch msg"
