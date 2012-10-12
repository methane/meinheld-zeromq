import zmq
from threading import Thread
from time import sleep

ctx = zmq.Context()

sock = ctx.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:10000")
while True:
    msg = sock.recv()
    print msg
    sleep(1)
    sock.send(msg + msg)
