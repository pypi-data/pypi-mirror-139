from ..message import Message
import subprocess


def send_command_client(args, client, socket):
    command = args['send'] 
    if args['result']:
        title = "result"
    else:
        title = None

    message = Message(title=title, content=command)
    print(message.get_content())
    client.send(message, socket)
    msg = client.receive(socket)
    if args['result']:
        print(msg.get_content())
    return


def send_command_server(server, socket):
    mess = server.receive(socket)
    command = ' '.join(mess.get_content()) 
    print("Command: ", command)
    result = subprocess.run(command, shell=True, 
            stdout=subprocess.PIPE)

    if mess.get_title() == "result": 
        print(result.stdout.decode('utf-8'))
        msg = Message(title='done', content=result.stdout.decode('utf-8')) 
    else:
        msg = Message(title='done')

    server.send(msg, socket)
    return

