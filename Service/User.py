from Utils.Format import p_json


class User(object):
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.pending = kwargs['pending']
        self.connection = kwargs['connection']

    def send(self, message):
        self.connection.write_message(message)

    def __str__(self):
        return p_json(user_id=self.user_id,
                      pending=self.pending,
                      conn=self.connection)
