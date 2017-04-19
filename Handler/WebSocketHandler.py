import datetime
from json import dumps as json_dumps
from uuid import uuid4

import tornado.escape as tornado_escape
import tornado.websocket
from tornado.ioloop import PeriodicCallback

from Service.Game import transform_input, transform_output


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

        self.game, self.clients = kwargs['game'], kwargs['clients']
        self.user_id, self.notification = "", None

    def initialize(self, game, clients):
        pass

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def loop(self):
        """
        Periodic update the state based on current state
        State -> Next State
        
        """
        self.game.change(self.game.current())

        next_loop = self.game.current() \
            if self.game.started else {}

        self.write_message(p_json(time=str(self.game.time()),
                                  next_loop=str(next_loop)))

    def open(self):
        """
        Setup a periodic call on each connection
        Provide an uuid for each connection
        Add connection to connection list for further action
        
        """
        # self.notification = PeriodicCallback(self.loop, 1000)
        # self.notification.start()
        self.user_id = uuid4()

        if self.user_id not in self.clients.get_all_clients():
            self.clients.join((self.user_id, self))
            print(str(self.user_id) + '+')

    def on_message(self, message):
        """
        A mini dispatcher of behavior determine by incoming payload
        
        """
        payload = tornado_escape.json_decode(message)
        action, result = payload['action'], ''

        if action == 'query':
            self.write(p_json(result=self.game.current()))

        elif action == 'change':
            print(payload['cell'])
            self.game.start()
            self.game.change(transform_input(payload['cell']))
            self.write_message(p_json(result=list(transform_output(self.game.current()))))

        elif action == 'reset':
            self.game.stop()
            self.game.reset_time()

    def on_close(self):
        """
        When connection close
        Stop the periodic call
        Remove connection from connection list
         
        """
        # self.notification.stop()
        self.clients.remove((self.user_id, self))
        print(str(self.user_id) + '-')


def p_json(**kwargs):
    """
    Parse keyword arguments as json format
    
    """
    return '{}'.format(json_dumps(kwargs))


def current_time():
    """
    Return current time
    
    """
    return '{dt:%H}:{dt:%M}:{dt:%S}'.format(dt=datetime.datetime.now())
