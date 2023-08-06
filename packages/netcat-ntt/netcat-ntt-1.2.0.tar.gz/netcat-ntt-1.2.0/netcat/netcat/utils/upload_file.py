from ..message import Message


def upload_file_client(args, client, socket):
    file_name = args['upload']

    with open(file_name, 'r') as file:
        scripts = file.read()

    message = Message(title=file_name, content=scripts)
    client.send(message, socket)
    msg = client.receive(socket)
    return 


def upload_file_server(server, socket):
    mess = server.receive(socket)
    file_name = mess.get_title()
    scripts = mess.get_content() 

    with open('server_' + file_name, 'w') as file:
        file.write(scripts)

    msg = Message(title='done')
    server.send(msg, socket)
    return 
