import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.REQ)
sock.connect('tcp://127.0.0.1:10000')

while True:
    sock.send(b'hello')
    print sock.recv()
    time.sleep(1)
