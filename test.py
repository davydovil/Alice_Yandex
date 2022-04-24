from smapi import Client
import datetime as dt

client = Client("r8eDzp0Vp645u89rzbjaiHOAd8eoMPSy")
future_date = dt.date.today() + dt.timedelta(days=1)
ans1 = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
answer_full = ""
for elem in ans1.values():
    answer_full += f'{(elem.split(":")[0])}\n'
print(answer_full)

# print(client.get_my_context()["groupIds"])
# print(client.get_group_timetable(group_id=1845266896493888494))
# print(client.get_person_marks_by_lesson_date(person_id=person_id, lesson_date="2022-04-18")[0]["lesson"])
# print(client.get_person_marks_by_lesson_date(person_id=person_id, lesson_date="2022-04-20"))
# client.get_group_weighted_average_marks_for_date_period()

