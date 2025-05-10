import random
from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def get_schoolkid_by_name(full_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__icontains=full_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        raise ValueError("Ученик с таким именем не найден!")
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError("Найдено несколько учеников с таким именем.")


def fix_marks(schoolkid):
    bad_points = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for point in bad_points:
        point.points = random.choice([4, 5])
        point.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_random_commendation(schoolkid, subject_title):
    commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]

    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__icontains=subject_title
    ).order_by('date').last()

    if not lesson:
        print(f"Ошибка: Урок по предмету '{subject_title}' не найден.")
        return

    commendation_text = random.choice(commendations)
    Commendation.objects.create(
        text=commendation_text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    print(f'Добавлена похвала по предмету "{subject_title}": "{commendation_text}"')


def main():
    schoolkid_name = input("Введите имя ученика: ")
    subject_title = input("Введите название предмета: ")

    try:
        schoolkid = get_schoolkid_by_name(schoolkid_name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_random_commendation(schoolkid, subject_title)
    except ValueError as e:
        print(f"Ошибка: {e}")


main()






# import random
# from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Lesson
# from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


# def get_schoolkid_by_name(full_name):

#     try:
#         schoolkid = Schoolkid.objects.get(full_name__icontains=full_name)
#         return schoolkid
#     except Schoolkid.DoesNotExist:
#         raise ValueError("Ученик с таким именем не найден!")
#     except Schoolkid.MultipleObjectsReturned:
#         raise ValueError("Найдено несколько учеников с таким именем.")


# def fix_marks(schoolkid):

#     bad_points = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
#     for point in bad_points:
#         point.points = random.choice([4, 5])
#         point.save()


# def remove_chastisements(schoolkid):

#     chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
#     chastisements.delete()


# def create_random_commendation(schoolkid_name):

#     commendations = [
#         'Молодец!',
#         'Отлично!',
#         'Хорошо!',
#         'Гораздо лучше, чем я ожидал!',
#         'Ты меня приятно удивил!',
#         'Великолепно!',
#         'Прекрасно!',
#         'Ты меня очень обрадовал!',
#         'Именно этого я давно ждал от тебя!',
#         'Сказано здорово – просто и ясно!',
#         'Ты, как всегда, точен!',
#         'Очень хороший ответ!',
#         'Талантливо!',
#         'Ты сегодня прыгнул выше головы!',
#         'Я поражен!',
#         'Уже существенно лучше!',
#         'Потрясающе!',
#         'Замечательно!',
#         'Прекрасное начало!',
#         'Так держать!',
#         'Ты на верном пути!',
#         'Здорово!',
#         'Это как раз то, что нужно!',
#         'Я тобой горжусь!',
#         'С каждым разом у тебя получается всё лучше!',
#         'Мы с тобой не зря поработали!',
#         'Я вижу, как ты стараешься!',
#         'Ты растешь над собой!',
#         'Ты многое сделал, я это вижу!',
#         'Теперь у тебя точно все получится!',
#     ]

#     schoolkid = get_schoolkid_by_name(schoolkid_name)

#     marks = Mark.objects.filter(schoolkid=schoolkid)
#     if not marks:
#         raise ValueError(f"У ученика {schoolkid_name} нет оценок!")
#     random_mark = random.choice(marks)

#     random_subject = random_mark.subject

#     lessons = Lesson.objects.filter(
#         year_of_study=schoolkid.year_of_study,
#         group_letter=schoolkid.group_letter,
#         subject=random_subject
#     ).order_by('date')

#     if not lessons:
#         print(f'Уроки по предмету "{random_subject}" не найдены.')
#         return

#     last_lesson = lessons.last()

#     commendation_text = random.choice(commendations)

#     Commendation.objects.create(
#         text=commendation_text,
#         created=last_lesson.date,
#         schoolkid=schoolkid,
#         subject=last_lesson.subject,
#         teacher=last_lesson.teacher
#     )

#     print(f'Добавлена похвала по предмету "{random_subject}": "{commendation_text}"')


# def main():

#     schoolkid_name = input("Введите имя ученика: ")
#     try:
#         schoolkid = get_schoolkid_by_name(schoolkid_name)
#         fix_marks(schoolkid)
#         remove_chastisements(schoolkid)
#         create_random_commendation(schoolkid_name)
#     except ValueError as e:
#         print(f"Ошибка: {e}")


# main()



# if __name__ == "__main__":
#     main()

    # commendations = [
    #     'Молодец!', 'Отлично!', 'Хорошо!', 'Так держать!',
    #     'Прекрасно!', 'Замечательно!', 'Очень хорошо!',
    #     'Ты меня приятно удивил!', 'Великолепно!', 'Гораздо лучше, чем я ожидал!',
    #     'Ты меня радуешь!', 'Я тобой горжусь!', 'Ты растешь над собой!',
    #     'С каждым разом у тебя получается всё лучше!', 'Я вижу твой прогресс!'
    # ]

