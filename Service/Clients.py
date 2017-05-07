class Clients:
    def __init__(self):
        self.clients = {}

    def join(self, client):
        self.clients[client.user_id] = client

    def remove(self, user_id):
        self.clients.pop(user_id)

    def get_client(self, user_id):
        return self.clients.get(user_id)

    def get_all_clients(self):
        return self.clients.keys()

    def fan_out(self, message):
        for u in self.get_all_clients():
            self.get_client(u).send(message)

    def broadcast(self, send_from, message):
        for u in self.get_all_clients():
            if u != send_from:
                self.get_client(u).send(message)
