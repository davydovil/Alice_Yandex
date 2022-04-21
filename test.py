from smapi import Client
token = 'JzfJSkiCl8kuNuUifZvZqIBEFYVcNp9v'
client = Client(token)
print(client.my_homeworks("2022-04-18"))
###res['response']['text'] = client.my_homeworks(date="2022-04-21")['1']
