import meinheld_zeromq as zmq
import meinheld.server
import greenlet

ctx = zmq.Context()
main_greenlet = greenlet.getcurrent()

def sleep(secs):
    meinheld.schedule_call(secs, greenlet.getcurrent().switch)
    main_greenlet.switch()

def pingpong():
    def run():
        sock = ctx.socket(zmq.REQ)
        sock.connect('tcp://127.0.0.1:10000')
        while True:
            sleep(1)
            sock.send(b'hello')
            print sock.recv()
    meinheld.spawn(run)

def dummy_app(env, start):
    sock = ctx.socket(zmq.REQ)
    sock.connect('tcp://127.0.0.1:10000')
    sock.send(env['PATH_INFO'])
    msg = sock.recv()
    start("200 OK", [('Content-Type', 'text/plain'), ('Content-Length', str(len(msg)))])
    return [msg]

meinheld.spawn(pingpong)
meinheld.listen(("127.0.0.1", 10001))
meinheld.run(dummy_app)
