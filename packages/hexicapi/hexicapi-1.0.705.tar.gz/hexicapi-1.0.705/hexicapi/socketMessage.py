import socket, time
from hexicapi.verinfo import __version__, __title__, __author__, __license__, __copyright__

def recv_all(the_socket:socket.socket, packet_size=1024):
    data_length = int(the_socket.recv(16).decode('utf-8'))
    the_socket.send('ok')
    data = b''
    while len(data) < data_length:
        data += the_socket.recv(packet_size)
    return data
def send_all(the_socket:socket.socket, data):
    length = str(len(data)).encode('utf-8')
    if len(length) < 16:
        length = '0' + length
    the_socket.send(length.encode('utf-8'))
    the_socket.send(data)