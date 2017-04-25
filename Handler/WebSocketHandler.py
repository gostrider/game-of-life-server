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

    def open(self):
        self.user_id = uuid4()
        if self.user_id not in self.clients.get_all_clients():
            self.clients.join((self.user_id, self, []))
            print(str(self.user_id) + '+')

    def on_message(self, message):
        payload = tornado_escape.json_decode(message)
        action = payload['action']

        if action == 'query':
            self.query()
        elif action == 'change':
            self.change(color=payload['color'], cells=payload['cells'])
        elif action == 'reset':
            self.reset(color=payload['color'])
        elif action == 'activity':
            self.activity(color=payload['color'], cells=payload['cells'])

    def on_close(self):
        self.clients.remove(self.user_id)
        print(str(self.user_id) + '-')

    def query(self):
        resp_json = p_json(action='query', result=self.game.current())
        self.write_message(resp_json)

    def change(self, **kwargs):
        self.game.change(transform_input(kwargs['cells']))
        result_response = transform_output(kwargs['color'], self.game.current())
        resp_json = p_json(color=kwargs['color'], action='result', cells=list(result_response))
        self.clients.fan_out(resp_json)

    def activity(self, **kwargs):
        resp_json = p_json(color=kwargs['color'], action='activity', cells=kwargs['cells'])
        self.clients.broadcast(self.user_id, resp_json)

    def reset(self, **kwargs):
        self.game.stop()
        self.game.reset_time()
        resp_json = p_json(color=kwargs['color'], action='reset')
        self.clients.broadcast(self.user_id, resp_json)


def p_json(**kwargs):
    return '{}'.format(json_dumps(kwargs))


def current_time():
    return '{dt:%H}:{dt:%M}:{dt:%S}'.format(dt=datetime.datetime.now())
