from smapi import Client
import datetime
import datetime as dt


future_date = dt.date.today() + dt.timedelta(days=1)
print(future_date)
token = 'JzfJSkiCl8kuNuUifZvZqIBEFYVcNp9v'
client = Client(token)

answer = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
print(answer.values())

