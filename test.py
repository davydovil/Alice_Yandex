from smapi import Client
token = 'JzfJSkiCl8kuNuUifZvZqIBEFYVcNp9v'
client = Client(token)
print(client.my_homeworks("2022-04-18"))
print(client.my_timetable("2022-04-18"))
