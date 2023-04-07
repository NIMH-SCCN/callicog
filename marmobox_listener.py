import argparse
import socket
import signal
import pickle
import json
import sys
from marmobox_interface import MarmoboxInterface
from threading import Thread, Event

MAX_LENGTH = 4096
PORT = 10000
HOST = '0.0.0.0'

class ServiceExit(Exception):
    pass

def service_shutdown(signum, frame):
    print(': Caught signal %d' % signum)
    raise ServiceExit

class ClientJob(Thread):
    def __init__(self, client_socket, client_address, arduino_port, window_size, is_dummy, is_fullscreen):
        Thread.__init__(self)
        self.shutdown_flag = Event()
        self.mbox_interface = MarmoboxInterface(arduino_port, window_size, is_dummy, is_fullscreen)
        self.client_socket = client_socket
        self.client_address = client_address

    def pack_response(self, response_object):
        response = { 'success': 0 }
        if response_object:
            response['success'] = 1
            response['body'] = {
                'data': response_object
            }
        return response

    def parse_msg(self, msg):
        if msg['action'] == 'run_trial':
            trial_data = self.mbox_interface.run_trial(msg['trial_params'])
            response = self.pack_response(trial_data)
        self.client_socket.send(bytes(json.dumps(response), 'utf8'))

    def run(self):
        print('Client thread #%s started from %s' % (self.ident, self.client_address))
        try:
            self.mbox_interface.initialize()
            print('Marmobox interface initialized') # status report
            self.client_socket.send(bytes(json.dumps(self.pack_response({'status': 'init success'})), 'utf8'))
            while not self.shutdown_flag.is_set():
                buf = self.client_socket.recv(MAX_LENGTH)
                if buf is None:
                    break
                try:
                    msg = json.loads(buf.decode())
                except:
                    print('Cannot decode data as JSON. Trying with pickle...')
                    pass
                try:
                    msg = pickle.loads(buf)
                except:
                    break
                self.parse_msg(msg)
            self.mbox_interface.close()
        except Exception as exc: # status report
            self.client_socket.send(bytes(json.dumps(self.pack_response({'status': str(exc)})), 'utf8'))
        print('Client thread #%s stopped' % self.ident)

def main():
    parser = argparse.ArgumentParser(description='Marmobox server. \
        Waits for client then opens psychopy window and Arduino USB interface.')
    parser.add_argument('port', help='Arduino port (e.g. "ttyACM0")', type=str)
    parser.add_argument('--width', help='Width of the Psychopy window', type=int, default=1280)
    parser.add_argument('--height', help='Height of the Psychopy window', type=int, default=720)
    parser.add_argument('--dummy', help='Dummy box (no actuators)', dest='dummy', action='store_true')
    parser.add_argument('--fullscreen', help='Psychopy window is fullscreen', dest='fullscreen', action='store_true')
    parser.set_defaults(dummy=False, fullscreen=False)
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print(f'Listening for incoming connections')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.settimeout(None)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1) # up to 1 connection(s)

    ct = None
    while True:
        try:
            (client_socket, address) = server_socket.accept()
            ct = ClientJob(client_socket, address, args.port, [args.width, args.height], args.dummy, args.fullscreen)
            ct.start()
        except ServiceExit:
            if ct:
                ct.shutdown_flag.set()
                ct.join()
            break
    print('Exiting main thread')

if __name__ == '__main__':
    main()
