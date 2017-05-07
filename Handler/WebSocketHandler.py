from uuid import uuid4

import tornado.escape as tornado_escape
import tornado.websocket

from Service.Clients import Clients
from Service.Game import Game, transform_input, transform_output
from Service.User import User
from Utils.Format import p_json
from Utils.Logger import debug, get_iso_time


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.game, self.clients = Game(), Clients()
        self.user_id = ""
        super().__init__(application, request, **kwargs)

    def initialize(self):
        pass

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def open(self):
        user = User(user_id=uuid4(), pending=[], connection=self)
        self.user_id = user.user_id
        if self.user_id not in self.clients.get_all_clients():
            self.clients.join(user)
            log(self.user_id, 'Connected')

    def on_message(self, message):
        payload = tornado_escape.json_decode(message)
        self.dispatch(parse_payload('action', payload), payload)

    def on_close(self):
        self.clients.remove(self.user_id)
        log(self.user_id, 'Disconnected')

    """ Internal methods """

    def dispatch(self, action, payload):
        """
        Map input action to behavior.
        
        :param action: [String] Name of the action 
        :param payload: [Dict] Require parameters for behavior
        :return: None
        """
        self.apply_behavior(action)(gen_params(payload))

    def apply_behavior(self, event):
        """
        Return behavior according input action.
        
        :param event: [String] Name of the action 
        :return: [Func] Method of behavior
        """
        return self.behaviors().get(event)

    def behaviors(self):
        """
        Return action behavior mappings.
        
        :return: [Dict] { action :: key => behavior :: function } 
        """
        return {
            'query': self.query,
            'change': self.change,
            'activity': self.activity,
            'reset': self.reset
        }

    def query(self, *args):
        """
        Handle player check game status.
        
        :param args: [Optional] 
        :return: None
        """
        resp_json = p_json(action='query', result=self.game.current())
        log(self.user_id, resp_json)
        self.write_message(resp_json)

    def change(self, params):
        """
        Handle action for changing game state.
        
        :param params: [Dict] Require keys { color, cells } 
        :return: None
        """
        self.game.change(transform_input(params['cells']))
        result_response = transform_output(params['color'], self.game.current())
        resp_json = p_json(color=params['color'], action='result', cells=list(result_response))
        log(self.user_id, resp_json)
        self.clients.fan_out(resp_json)

    def activity(self, params):
        """
        Handle player action affects the game.
        
        :param params: [Dict] Require keys { color, cells }
        :return: None 
        """
        resp_json = p_json(color=params['color'], action='activity', cells=params['cells'])
        log(self.user_id, resp_json)
        self.clients.broadcast(self.user_id, resp_json)

    def reset(self, params):
        """
        Handle player reset the game state.
        
        :param params: Require keys { color }
        :return: None
        """
        resp_json = p_json(color=params['color'], action='reset')
        log(self.user_id, resp_json)
        self.clients.broadcast(self.user_id, resp_json)


def gen_params(payload):
    """
    Return fields available from payload.
    
    :param payload: [Dict] JSON body 
    :return: [Dict] { key :: String => Optional[value] }
    """
    return {
        'color': parse_payload('color', payload),
        'cells': parse_payload('cells', payload)
    }


def parse_payload(field, payload):
    """
    Getter for handling input payload with default value.
    
    :param field: [String] JSON field name
    :param payload: [JSON] JSON body
    :return: [String] Value of JSON field
    """
    return payload.get(field, False)


def log(user_id, message):
    """
    Log message with user_id using predefined fields.
    
    :param user_id: [UUID] UUID of user 
    :param message: [String] JSON format of log message
    :return: None
    """
    debug(timestamp=get_iso_time(), user=str(user_id), message=message)
