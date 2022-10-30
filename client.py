import socket, sys

interactive_flag = True


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def decide_move(state, play):
    # YOUR CODE GOES HEREE.....
    return None


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect((sys.argv[1], int(sys.argv[2])))  # connecting client to server

hello_msg = '%s_%s' % (sys.argv[4], sys.argv[3])
client.send(hello_msg.encode('ascii'))

client.send(sys.argv[3].encode('ascii'))

player = int(sys.argv[4])

while True:  # making valid connection
    while True:
        message = client.recv(1024).decode('ascii')
        if len(message) > 0:
            break

    if interactive_flag:
        row_from = int(input('Row from > '))
        col_from = int(input('Col from > '))
        row_to = int(input('Row to > '))
        col_to = int(input('Col to > '))

        p_from = pos2_to_pos1([row_from, col_from])
        p_to = pos2_to_pos1([row_to, col_to])

        if (0 <= p_from <= 63) and (0 <= p_to <= 63):
            message = list(message)
            aux = message[p_from]
            message[p_from] = 'z'
            message[p_to] = aux
            message = ''.join(message)
    else:
        message = decide_move(message, player)

    client.send(message.encode('ascii'))
