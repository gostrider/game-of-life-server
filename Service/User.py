class User(object):
    def __init__(self, **kwargs):
        self.pending = kwargs['pending']
        self.connection = kwargs['connection']

    def write_message(self, message):
        self.connection.write_message(message)
