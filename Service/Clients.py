from Service.User import User

class Clients:
    def __init__(self):
        self.clients = {}

    def join(self, client):
        user_id, cli_obj, pending = client
        self.clients[user_id] = User(pending=pending, connection=cli_obj)

    def remove(self, user_id):
        self.clients.pop(user_id)

    def get_client(self, user_id):
        return self.clients.get(user_id)

    def get_all_clients(self):
        return list(self.clients.keys())

    def fan_out(self, message):
        for u in self.get_all_clients():
            conn = self.get_client(u)
            conn.write_message(message)

    def broadcast(self, send_from, message):
        for u in self.get_all_clients():
            if u != send_from:
                self.get_client(u).write_message(message)
