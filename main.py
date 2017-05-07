from tornado import web, ioloop

from Handler.WebSocketHandler import WebSocketHandler


def router():
    return [
        (r'/ws/game', WebSocketHandler),
    ]


def main():
    app = web.Application(
        router(), autoreload=True
    )
    app.listen(8001)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
