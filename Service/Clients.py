class Clients:
    def __init__(self):
        self.clients = {}

    def join(self, client):
        user_id, cli_obj = client
        self.clients[user_id] = cli_obj

    def remove(self, client):
        user_id, _ = client
        self.clients.pop(user_id)

    def get_client(self, user_id):
        return self.clients.get(user_id)

    def get_all_clients(self):
        return list(self.clients.keys())
