class Clients:
    """
    Clients object is a map of [uuid => connection] pair
    """

    def __init__(self):
        self.clients = {}

    def join(self, client):
        """
        Store client as KV pair to achieve O(1) lookup

        """
        user_id, cli_obj = client
        self.clients[user_id] = cli_obj

    def remove(self, client):
        """
        Remove client by uuid
 
        """
        user_id, _ = client
        self.clients.pop(user_id)

    def get_client(self, user_id):
        """
        Get client connection by uuid (key)
        
        """
        return self.clients.get(user_id)

    def get_all_clients(self):
        """
        Return list of uuid represent each user

        """
        return list(self.clients.keys())
