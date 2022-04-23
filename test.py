from smapi import Client
import datetime
import datetime as dt


future_date = dt.date.today() + dt.timedelta(days=-5)
today = dt.date.today()
print(future_date)
token = 'KnPluy1laXn42n6QNh8FjqcObzFIlRAB'
client = Client(token)
person_id = client.get_me()
ans1 = dict(sorted(client.my_homeworks(future_date).items(), key=lambda f: int(f[0])))
s = ' '.join(list(ans1.values()))

sub = ["Математика (алгебра)", "Русский язык", "Химия", "Биология", "Литература", "География", "ОБЖ",
       "Математика (геом.)", "Физика", "Обществознание", "Право", "Физическая культура", "Иностр. язык (англ.)",
       "Информатика", "История", "Родня литература", "Родной язык", "Инд.проект"]

hui = []

for i in range(len(sub)):
    if sub[i] in s:
        hui.append(sub[i])
        print(sub[i])

# for i in range(len(hui)):
    # if hui[i] in s:
        # print(hui[i])
















print(" ")
print(s)


# print(client.get_my_context()["groupIds"])
# print(client.get_group_timetable(group_id=1845266896493888494))
# print(client.get_person_marks_by_lesson_date(person_id=person_id, lesson_date="2022-04-18")[0]["lesson"])
# print(client.get_person_marks_by_lesson_date(person_id=person_id, lesson_date="2022-04-20"))
# client.get_group_weighted_average_marks_for_date_period()

