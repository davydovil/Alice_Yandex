from smapi import Client
import datetime
import datetime as dt


future_date = dt.date.today() + dt.timedelta(days=1)
today = dt.date.today()
print(future_date)
token = 'OfN4nuja4zabUX3S0v5Hv3i2f28TnqQn'
client = Client(token)
person_id = client.get_me()["id"]
print(client.get_person_marks_by_lesson_date(person_id=person_id, lesson_date="2022-04-21"))





