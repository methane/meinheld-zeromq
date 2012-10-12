import zmq

ctx = zmq.Context()
sock = ctx.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:10000")

while True:
    msg = sock.recv()
    print msg
    sock.send(msg + msg)
