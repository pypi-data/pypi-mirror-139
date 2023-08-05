from ..message import Message


def upload_file_client(args):
    file_name = args['upload']

    with open(file_name, 'r') as file:
        scripts = file.read()

    message = Message(title=file_name, content=scripts)
    return message


def upload_file_server(mess):
    file_name = mess.get_title()
    scripts = mess.get_content() 

    with open('server_' + file_name, 'w') as file:
        file.write(scripts)

    return ""
