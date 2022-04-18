from smapi import Client
import datetime as dt




token = 'bnXpnw48AaqXawOW3OdZso40Q1kVYivv'
client = Client(token)
client_1 = Client('DDC1OZOKkl8Ic9E8RHodtfeL7r0FIhAT')
me = client.get_me()
school_id = client.get_my_context()['schools'][0]['id']
my_id = me['id']

client = Client(token)
client.my_homeworks("2022-04-18 00:00:00", "2022-04-18 23:59:00", school_id)
