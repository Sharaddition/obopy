import logging
from websocket_server import WebsocketServer

def new_client(client, server):
	print(f"This client joimed us {client}")
	server.send_message_to_all("Hey all, a new client has joined us")

def new_msg(client, server, msg):
    print(f"Message {msg}")
    server.send_message_to_all(msg)

server = WebsocketServer(host='127.0.0.1', port=6969, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(new_msg)
server.run_forever()