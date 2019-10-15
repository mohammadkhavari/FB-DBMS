from Models.book import Book
from Models.publisher import Publisher

while(True):

    command = input("\n-->")

    if len(command) == 0:
        continue

    command_parsed = command.split()
    if len(command_parsed) < 3:
        print('Invalid Command')
        continue

    model = command_parsed[1]
    query_type = command_parsed[0]
    body = ' '.join(command_parsed[2:])

    if model == 'book':
        Book.query(query_type, body)
    elif model == 'publisher':
        Publisher.query(query_type, body)
    else:
        print('Invalid Command')
