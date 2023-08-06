from ..message import Message


def download_file_client(args, client, socket):
    client.send(Message(title="waiting", content=args['download']), socket)
    msg = client.receive(socket)
    data = msg.get_content()

    with open("client_"+args['download'], 'w') as file:
        file.write(data)
    return 


def download_file_server(server, socket):
    mess = server.receive(socket)
    with open(mess.get_content(), 'r') as file:
        data = file.read()

    done_msg = Message(title='done', content=data)
    server.send(done_msg, socket)
    return 
