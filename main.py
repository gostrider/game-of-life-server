from tornado import web, ioloop

from Handler.WebSocketHandler import WebSocketHandler
from Service.Clients import Clients
from Service.Game import Game


def router(game, clients):
    return [
        (r'/ws/test', WebSocketHandler, {'game': game, 'clients': clients}),
    ]


def main():
    app = web.Application(
        router(Game(), Clients()), autoreload=True
    )
    app.listen(8001)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
